from __future__ import annotations

import asyncio
import json
import os
import re
from datetime import datetime, timezone
from typing import Any

from pymongo.errors import PyMongoError

from src.clients.client import (
    ExternalClientError,
    ExternalResponseError,
)
from src.databases.mongodb import (
    mongo_connection,
)
from src.external.constants.goodreturns import (
    GOODRETURNS_FUEL_TYPES,
    GOODRETURNS_TIMEFRAMES,
)
from src.external.executors.goodreturns.fuel_graph import (
    GoodReturnsFuelGraphExecutor,
)
from src.logger.logger import logger_service
from src.models.goodreturns_fuel_graph_price import (
    GoodReturnsFuelGraphPoint,
    GoodReturnsFuelGraphPrice,
)
from src.models.scraper_job import (
    ScraperJob,
)
from src.models.scraper_run import (
    ScraperRun,
)
from src.repositories.goodreturns_fuel_graph_repository import (
    goodreturns_fuel_graph_repository,
)
from src.repositories.scraper_job_repository import (
    JobStatusCounts,
    scraper_job_repository,
)
from src.repositories.scraper_run_repository import (
    scraper_run_repository,
)

COMMAND_NAME = "goodreturns-fuel-graph-prices"
SOURCE_NAME = "goodreturns"
RESOURCE_NAME = "fuel-graph-prices"
JOB_TYPE = "fetch-fuel-graph"

DEFAULT_CITIES_JSON_PATH = "data/raw/goodreturns_fuel_cities.json"

HTTP_STATUS_PATTERN = re.compile(
    r"(?:status|status_code|http_status)\s*[=:]\s*(\d{3})",
    re.IGNORECASE,
)

RETRYABLE_HTTP_STATUSES = {
    401,
    403,
    408,
    425,
    429,
    500,
    502,
    503,
    504,
}


class GoodReturnsBlockedError(RuntimeError):
    pass


def _validate_positive_integer(
    value: int,
    *,
    field_name: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")

    return value


def _validate_non_negative_integer(
    value: int,
    *,
    field_name: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")

    return value


def _validate_workers(
    workers: int,
) -> int:
    normalized_workers = _validate_positive_integer(
        workers,
        field_name="workers",
    )

    if normalized_workers > 1000:
        raise ValueError("workers cannot exceed 1000")

    return normalized_workers


def _validate_requests_per_second(
    requests_per_second: float,
) -> float:
    if (
        isinstance(requests_per_second, bool)
        or not isinstance(requests_per_second, (int, float))
        or requests_per_second <= 0
    ):
        raise ValueError("requests_per_second must be greater than zero")

    return float(requests_per_second)


def _validate_batch_size(
    batch_size: int,
) -> int:
    return _validate_positive_integer(
        batch_size,
        field_name="batch_size",
    )


def _validate_retries(
    retries: int,
) -> int:
    normalized_retries = _validate_non_negative_integer(
        retries,
        field_name="retries",
    )

    if normalized_retries > 20:
        raise ValueError("retries cannot exceed 20")

    return normalized_retries


def _normalize_optional_slug(
    value: str | None,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")

    normalized_value = value.strip().lower()

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    return normalized_value


def _normalize_required_token(
    value: str | None,
) -> str:
    token = value or os.getenv("GOODRETURNS_TOKEN")

    if not isinstance(token, str):
        raise ValueError(
            "GOODRETURNS_TOKEN is required. Pass --token or set GOODRETURNS_TOKEN env."
        )

    normalized_token = token.strip()

    if not normalized_token:
        raise ValueError(
            "GOODRETURNS_TOKEN is required. Pass --token or set GOODRETURNS_TOKEN env."
        )

    return normalized_token


def _normalize_fuel_types(
    fuel_types: tuple[str, ...],
) -> tuple[str, ...]:
    normalized_fuel_types = tuple(
        fuel_type.strip().lower()
        for fuel_type in fuel_types
        if isinstance(fuel_type, str) and fuel_type.strip()
    )

    if not normalized_fuel_types:
        raise ValueError("fuel_types cannot be empty")

    invalid_fuel_types = sorted(set(normalized_fuel_types) - GOODRETURNS_FUEL_TYPES)

    if invalid_fuel_types:
        raise ValueError(f"Invalid fuel types: {', '.join(invalid_fuel_types)}")

    return normalized_fuel_types


def _normalize_timeframe(
    timeframe: str,
) -> str:
    if not isinstance(timeframe, str):
        raise ValueError("timeframe must be a string")

    normalized_timeframe = timeframe.strip()

    if normalized_timeframe not in GOODRETURNS_TIMEFRAMES:
        raise ValueError(
            f"Invalid timeframe: {normalized_timeframe}. "
            f"Allowed: {', '.join(sorted(GOODRETURNS_TIMEFRAMES))}"
        )

    return normalized_timeframe


def _normalize_cities_json_path(
    cities_json_path: str | None,
) -> str:
    path = cities_json_path or DEFAULT_CITIES_JSON_PATH

    if not isinstance(path, str):
        raise ValueError("cities_json_path must be a string")

    normalized_path = path.strip()

    if not normalized_path:
        raise ValueError("cities_json_path cannot be empty")

    return normalized_path


def slugify_city_name(
    value: str,
) -> str:
    value = str(value or "").strip().lower()
    value = re.sub(r"\s+", "-", value)
    return value


def normalize_number(
    value: Any,
) -> float | None:
    if value is None:
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)

    value = str(value)
    value = value.replace("₹", "")
    value = value.replace(",", "")
    value = value.replace("/Ltr", "")
    value = value.replace("/Kg", "")
    value = value.strip()

    match = re.search(r"-?\d+(?:\.\d+)?", value)

    if not match:
        return None

    return float(match.group(0))


def normalize_timestamp_ms(
    value: Any,
) -> int | None:
    if value is None:
        return None

    try:
        number = int(float(value))
    except Exception:
        return None

    if number <= 0:
        return None

    if number < 10_000_000_000:
        number = number * 1000

    return number


def normalize_date_value(
    value: Any,
) -> tuple[str | None, int | None]:
    timestamp_ms = normalize_timestamp_ms(value)

    if timestamp_ms:
        date_value = (
            datetime.fromtimestamp(
                timestamp_ms / 1000,
                tz=timezone.utc,
            )
            .date()
            .isoformat()
        )

        return date_value, timestamp_ms

    if value is None:
        return None, None

    return str(value), None


def find_points(
    value: Any,
) -> list[Any]:
    if isinstance(value, list):
        if not value:
            return []

        if all(isinstance(item, dict) for item in value):
            sample = value[0]
            keys = {str(key).lower() for key in sample.keys()}

            if keys & {"date", "month", "x", "label", "name"} and keys & {
                "price",
                "value",
                "y",
                "rate",
            }:
                return value

        if all(isinstance(item, list) for item in value):
            return value

    if isinstance(value, dict):
        direct_keys = [
            "data",
            "graphData",
            "graph_data",
            "prices",
            "priceData",
            "price_data",
            "history",
            "fuel_prices",
            "fuelPrices",
            "result",
            "records",
        ]

        for key in direct_keys:
            if key in value:
                result = find_points(value[key])

                if result:
                    return result

        if "categories" in value and "series" in value:
            categories = value.get("categories") or []
            series = value.get("series") or []

            if categories and series and isinstance(series, list):
                first_series = series[0] if series else {}
                data = (
                    first_series.get("data") if isinstance(first_series, dict) else None
                )

                if isinstance(data, list):
                    return [
                        {
                            "x": categories[index],
                            "y": data[index],
                        }
                        for index in range(min(len(categories), len(data)))
                    ]

        for child in value.values():
            result = find_points(child)

            if result:
                return result

    return []


def normalize_points(
    raw_points: list[Any],
) -> list[GoodReturnsFuelGraphPoint]:
    points: list[GoodReturnsFuelGraphPoint] = []

    for item in raw_points:
        if isinstance(item, dict):
            x_value = (
                item.get("x")
                or item.get("date")
                or item.get("month")
                or item.get("label")
                or item.get("name")
            )

            y_value = (
                item.get("y")
                or item.get("price")
                or item.get("value")
                or item.get("rate")
            )

            date_value, timestamp_ms = normalize_date_value(x_value)

            points.append(
                GoodReturnsFuelGraphPoint(
                    date=date_value,
                    timestamp_ms=timestamp_ms,
                    price=normalize_number(y_value),
                    raw=item,
                )
            )

        elif isinstance(item, list) and len(item) >= 2:
            date_value, timestamp_ms = normalize_date_value(item[0])

            points.append(
                GoodReturnsFuelGraphPoint(
                    date=date_value,
                    timestamp_ms=timestamp_ms,
                    price=normalize_number(item[1]),
                    raw=item,
                )
            )

    return points


def _extract_http_status(
    error: BaseException,
) -> int | None:
    for attribute_name in (
        "status_code",
        "http_status",
        "status",
    ):
        status_value = getattr(
            error,
            attribute_name,
            None,
        )

        if (
            isinstance(status_value, int)
            and not isinstance(status_value, bool)
            and 100 <= status_value <= 599
        ):
            return status_value

    match = HTTP_STATUS_PATTERN.search(str(error))

    if match is None:
        return None

    try:
        status_code = int(match.group(1))
    except ValueError:
        return None

    if not 100 <= status_code <= 599:
        return None

    return status_code


def _is_retryable_error(
    error: BaseException,
) -> bool:
    http_status = _extract_http_status(error)

    if http_status is not None:
        return http_status in RETRYABLE_HTTP_STATUSES

    if isinstance(error, ExternalResponseError):
        return False

    return isinstance(
        error,
        (
            GoodReturnsBlockedError,
            ExternalClientError,
            PyMongoError,
        ),
    )


def _read_city_rows(
    *,
    cities_json_path: str,
    fuel_types: tuple[str, ...],
    timeframe: str,
) -> list[dict[str, Any]]:
    with open(cities_json_path, "r", encoding="utf-8") as file:
        payload = json.load(file)

    if isinstance(payload, list):
        cities = payload

    elif isinstance(payload, dict) and isinstance(payload.get("cities"), list):
        cities = payload["cities"]

    else:
        raise ValueError(
            "Goodreturns cities JSON must be an array or an object with cities array"
        )

    rows: list[dict[str, Any]] = []

    for city in cities:
        if not isinstance(city, dict):
            continue

        city_id = city.get("city_id") or city.get("cityId")
        city_name = city.get("city_name") or city.get("cityName")
        city_slug = city.get("city_slug") or city.get("citySlug")

        if city_id is None or city_name is None:
            continue

        try:
            normalized_city_id = int(city_id)
        except Exception:
            continue

        if normalized_city_id <= 0:
            continue

        normalized_city_name = str(city_name).strip()

        if not normalized_city_name:
            continue

        normalized_city_slug = (
            str(city_slug).strip().lower()
            if city_slug is not None and str(city_slug).strip()
            else slugify_city_name(normalized_city_name)
        )

        if not normalized_city_slug:
            continue

        for fuel_type in fuel_types:
            rows.append(
                {
                    "_id": (
                        f"{SOURCE_NAME}:{fuel_type}:{normalized_city_slug}:{timeframe}"
                    ),
                    "cityId": normalized_city_id,
                    "cityName": normalized_city_name,
                    "citySlug": normalized_city_slug,
                    "fuelType": fuel_type,
                    "timeframe": timeframe,
                }
            )

    unique_rows: dict[str, dict[str, Any]] = {}

    for row in rows:
        unique_rows[row["_id"]] = row

    return list(unique_rows.values())


def _build_job(
    *,
    run_id: str,
    row: dict[str, Any],
    max_attempts: int,
) -> ScraperJob:
    fuel_type = row["fuelType"]
    city_slug = row["citySlug"]
    timeframe = row["timeframe"]

    job_id = f"fuel:{fuel_type}:{city_slug}:{timeframe}"
    item_key = f"{fuel_type}:{city_slug}:{timeframe}"

    return ScraperJob.create(
        run_id=run_id,
        job_id=job_id,
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        job_type=JOB_TYPE,
        item_key=item_key,
        payload={
            "documentId": row["_id"],
            "cityId": row["cityId"],
            "cityName": row["cityName"],
            "citySlug": city_slug,
            "fuelType": fuel_type,
            "timeframe": timeframe,
        },
        metadata={
            "targetCollection": "goodreturns_fuel_graph_prices",
        },
        priority=100,
        max_attempts=max_attempts,
        retryable=True,
    )


def _build_progress(
    *,
    job_counts: JobStatusCounts,
    written: int,
    matched: int,
    modified: int,
    inserted: int,
) -> dict[str, int]:
    return {
        "produced": job_counts.total,
        "skipped": job_counts.skipped,
        "successful": job_counts.completed,
        "failed": job_counts.failed,
        "written": written,
        "inserted": inserted,
        "matched": matched,
        "modified": modified,
        "failureRecordsWritten": job_counts.failed,
        "totalJobs": job_counts.total,
        "pendingJobs": job_counts.pending,
        "runningJobs": job_counts.running,
        "completedJobs": job_counts.completed,
        "failedJobs": job_counts.failed,
        "skippedJobs": job_counts.skipped,
        "cancelledJobs": job_counts.cancelled,
    }


async def _cancel_claimed_job_safely(
    *,
    run_id: str,
    job_id: str,
    reason: str,
) -> None:
    try:
        current_job = await scraper_job_repository.get(
            run_id=run_id,
            job_id=job_id,
        )

        if current_job is not None and current_job.status in {
            "pending",
            "running",
        }:
            await scraper_job_repository.mark_cancelled(
                run_id=run_id,
                job_id=job_id,
                reason=reason,
            )

    except Exception as tracking_error:
        logger_service.error(
            (
                "Unable to cancel Goodreturns fuel graph job: "
                f"run_id={run_id}, "
                f"job_id={job_id}, "
                f"error={type(tracking_error).__name__}: {tracking_error}"
            ),
            context="GoodReturnsFuelGraphCommand",
        )


async def run_goodreturns_fuel_graph_prices(
    *,
    cities_json_path: str | None = None,
    fuel_types: tuple[str, ...] = ("petrol", "diesel", "cng"),
    timeframe: str = "1M",
    token: str | None = None,
    workers: int = 3,
    requests_per_second: float = 2.0,
    batch_size: int = 50,
    retries: int = 2,
    city: str | None = None,
    limit: int | None = None,
    refresh_existing: bool = False,
) -> dict[str, Any]:
    normalized_cities_json_path = _normalize_cities_json_path(cities_json_path)
    normalized_fuel_types = _normalize_fuel_types(fuel_types)
    normalized_timeframe = _normalize_timeframe(timeframe)
    normalized_token = _normalize_required_token(token)
    normalized_workers = _validate_workers(workers)
    normalized_requests_per_second = _validate_requests_per_second(
        requests_per_second,
    )
    normalized_batch_size = _validate_batch_size(batch_size)
    normalized_retries = _validate_retries(retries)
    normalized_city = _normalize_optional_slug(
        city,
        field_name="city",
    )

    if limit is not None:
        normalized_limit = _validate_positive_integer(
            limit,
            field_name="limit",
        )
    else:
        normalized_limit = None

    mode = "single-city" if normalized_city is not None else "full"

    rows = _read_city_rows(
        cities_json_path=normalized_cities_json_path,
        fuel_types=normalized_fuel_types,
        timeframe=normalized_timeframe,
    )

    if normalized_city is not None:
        rows = [
            row
            for row in rows
            if row["citySlug"] == normalized_city
            or slugify_city_name(row["cityName"]) == normalized_city
        ]

    if normalized_limit is not None:
        rows = rows[:normalized_limit]

    total_before_resume_filter = len(rows)

    run = ScraperRun.create(
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        command=COMMAND_NAME,
        mode=mode,
        filters={
            "city": normalized_city,
            "fuelTypes": list(normalized_fuel_types),
            "timeframe": normalized_timeframe,
        },
        settings={
            "workers": normalized_workers,
            "requestsPerSecond": normalized_requests_per_second,
            "batchSize": normalized_batch_size,
            "retries": normalized_retries,
            "refreshExisting": refresh_existing,
            "citiesJsonPath": normalized_cities_json_path,
        },
        metadata={
            "storage": "mongodb",
            "targetCollection": "goodreturns_fuel_graph_prices",
        },
    )

    run_id = run.run_id
    run_created = False

    aggregate_lock = asyncio.Lock()

    aggregate: dict[str, int] = {
        "written": 0,
        "matched": 0,
        "modified": 0,
        "inserted": 0,
    }

    async def get_aggregate_snapshot() -> dict[str, int]:
        async with aggregate_lock:
            return dict(aggregate)

    async def refresh_run_progress() -> None:
        job_counts = await scraper_job_repository.count_by_status(
            run_id=run_id,
        )

        aggregate_snapshot = await get_aggregate_snapshot()

        progress = _build_progress(
            job_counts=job_counts,
            written=aggregate_snapshot["written"],
            matched=aggregate_snapshot["matched"],
            modified=aggregate_snapshot["modified"],
            inserted=aggregate_snapshot["inserted"],
        )

        await scraper_run_repository.update_progress(
            run_id,
            progress=progress,
        )

    try:
        await mongo_connection.connect()

        await goodreturns_fuel_graph_repository.ensure_indexes()

        if refresh_existing:
            queued_rows = rows
            skipped_existing = 0
        else:
            existing_ids = (
                await goodreturns_fuel_graph_repository.get_existing_price_ids(
                    [row["_id"] for row in rows]
                )
            )

            queued_rows = [row for row in rows if row["_id"] not in existing_ids]

            skipped_existing = len(rows) - len(queued_rows)

        await scraper_run_repository.create(run)

        run_created = True

        jobs = [
            _build_job(
                run_id=run_id,
                row=row,
                max_attempts=normalized_retries + 1,
            )
            for row in queued_rows
        ]

        create_result = await scraper_job_repository.create_many(jobs)

        await scraper_run_repository.mark_started(run_id)

        if skipped_existing > 0:
            await scraper_run_repository.update_progress(
                run_id,
                progress={
                    "skipped": skipped_existing,
                },
            )

        active_workers = min(
            normalized_workers,
            max(len(queued_rows), 1),
        )

        logger_service.info(
            (
                "Starting Goodreturns fuel graph scraping: "
                f"run_id={run_id}, "
                f"mode={mode}, "
                f"total={total_before_resume_filter}, "
                f"queued={len(queued_rows)}, "
                f"skipped_existing={skipped_existing}, "
                f"fuel_types={','.join(normalized_fuel_types)}, "
                f"timeframe={normalized_timeframe}, "
                f"workers={active_workers}, "
                f"requests_per_second={normalized_requests_per_second}, "
                f"refresh_existing={refresh_existing}"
            ),
            context="GoodReturnsFuelGraphCommand",
        )

        executor = GoodReturnsFuelGraphExecutor(
            requests_per_second=normalized_requests_per_second,
        )

        async with executor.create_client(
            concurrency=active_workers,
        ) as client:

            async def worker(
                worker_number: int,
            ) -> None:
                worker_id = f"goodreturns-fuel-graph-worker-{worker_number}"

                while True:
                    claimed_job = await scraper_job_repository.claim_next(
                        run_id=run_id,
                        worker_id=worker_id,
                        resource=RESOURCE_NAME,
                        job_type=JOB_TYPE,
                    )

                    if claimed_job is None:
                        return

                    job_id = claimed_job.job_id
                    payload = claimed_job.payload

                    city_slug: Any = None
                    city_name: Any = None
                    fuel_type: Any = None
                    job_timeframe: Any = None

                    try:
                        if not isinstance(payload, dict):
                            raise ValueError(
                                "Goodreturns job payload must be an object"
                            )

                        city_id = payload.get("cityId")
                        city_name = payload.get("cityName")
                        city_slug = payload.get("citySlug")
                        fuel_type = payload.get("fuelType")
                        job_timeframe = payload.get("timeframe")

                        if not isinstance(city_id, int) or isinstance(city_id, bool):
                            raise ValueError("payload.cityId must be an integer")

                        if not isinstance(city_name, str) or not city_name.strip():
                            raise ValueError(
                                "payload.cityName must be a non-empty string"
                            )

                        if not isinstance(city_slug, str) or not city_slug.strip():
                            raise ValueError(
                                "payload.citySlug must be a non-empty string"
                            )

                        if fuel_type not in GOODRETURNS_FUEL_TYPES:
                            raise ValueError(f"Invalid payload fuelType: {fuel_type!r}")

                        if job_timeframe not in GOODRETURNS_TIMEFRAMES:
                            raise ValueError(
                                f"Invalid payload timeframe: {job_timeframe!r}"
                            )

                        status_code, raw_response = await executor.fetch_graph_data(
                            client=client,
                            token=normalized_token,
                            city_slug=city_slug,
                            fuel_type=fuel_type,
                            timeframe=job_timeframe,
                        )

                        if status_code in RETRYABLE_HTTP_STATUSES:
                            raise GoodReturnsBlockedError(
                                "Goodreturns blocked/unauthorized/rate-limited/server "
                                f"response HTTP {status_code}: "
                                f"{json.dumps(raw_response, ensure_ascii=False)[:500]}"
                            )

                        if status_code >= 400:
                            raise ExternalResponseError(
                                "Goodreturns fuel graph API failed "
                                f"HTTP {status_code}: "
                                f"{json.dumps(raw_response, ensure_ascii=False)[:500]}"
                            )

                        raw_points = find_points(raw_response)
                        points = normalize_points(raw_points)

                        price = GoodReturnsFuelGraphPrice.create(
                            city_id=city_id,
                            city_name=city_name,
                            city_slug=city_slug,
                            fuel_type=fuel_type,
                            timeframe=job_timeframe,
                            page_url=executor.build_referer_url(
                                fuel_type=fuel_type,
                                city_slug=city_slug,
                            ),
                            points=points,
                            raw_response=raw_response,
                            last_run_id=run_id,
                            last_http_status=status_code,
                        )

                        upsert_result = (
                            await goodreturns_fuel_graph_repository.bulk_upsert_prices(
                                [price]
                            )
                        )

                        await scraper_job_repository.mark_completed(
                            run_id=run_id,
                            job_id=job_id,
                            worker_id=worker_id,
                            result={
                                "documentId": price.id,
                                "cityId": city_id,
                                "cityName": city_name,
                                "citySlug": city_slug,
                                "fuelType": fuel_type,
                                "timeframe": job_timeframe,
                                "pointsCount": len(points),
                                "matched": upsert_result.matched,
                                "modified": upsert_result.modified,
                                "inserted": upsert_result.inserted,
                            },
                        )

                        async with aggregate_lock:
                            aggregate["written"] += 1
                            aggregate["matched"] += upsert_result.matched
                            aggregate["modified"] += upsert_result.modified
                            aggregate["inserted"] += upsert_result.inserted

                        await refresh_run_progress()

                        logger_service.info(
                            (
                                "Goodreturns fuel graph completed: "
                                f"run_id={run_id}, "
                                f"city={city_slug}, "
                                f"fuel_type={fuel_type}, "
                                f"timeframe={job_timeframe}, "
                                f"points={len(points)}, "
                                f"inserted={upsert_result.inserted}, "
                                f"modified={upsert_result.modified}"
                            ),
                            context="GoodReturnsFuelGraphCommand",
                        )

                    except asyncio.CancelledError:
                        await _cancel_claimed_job_safely(
                            run_id=run_id,
                            job_id=job_id,
                            reason="Goodreturns fuel graph command interrupted",
                        )

                        raise

                    except Exception as error:
                        retryable_error = _is_retryable_error(error)
                        http_status = _extract_http_status(error)

                        await scraper_job_repository.mark_failed(
                            run_id=run_id,
                            job_id=job_id,
                            error=error,
                            retryable=retryable_error,
                            http_status=http_status,
                            worker_id=worker_id,
                        )

                        requeued_jobs = 0

                        if retryable_error:
                            requeued_jobs = await scraper_job_repository.requeue_failed(
                                run_id=run_id,
                            )

                        await refresh_run_progress()

                        if requeued_jobs > 0:
                            logger_service.info(
                                (
                                    "Goodreturns fuel graph retry scheduled: "
                                    f"run_id={run_id}, "
                                    f"city={city_slug}, "
                                    f"fuel_type={fuel_type}, "
                                    f"timeframe={job_timeframe}, "
                                    f"error={type(error).__name__}: {error}"
                                ),
                                context="GoodReturnsFuelGraphCommand",
                            )

                            continue

                        logger_service.error(
                            (
                                "Goodreturns fuel graph failed: "
                                f"run_id={run_id}, "
                                f"city={city_slug}, "
                                f"fuel_type={fuel_type}, "
                                f"timeframe={job_timeframe}, "
                                f"error={type(error).__name__}: {error}"
                            ),
                            context="GoodReturnsFuelGraphCommand",
                        )

            if queued_rows:
                worker_tasks = [
                    asyncio.create_task(
                        worker(worker_number),
                        name=f"goodreturns-fuel-graph-worker-{worker_number}",
                    )
                    for worker_number in range(
                        1,
                        active_workers + 1,
                    )
                ]

                await asyncio.gather(*worker_tasks)

        job_counts = await scraper_job_repository.count_by_status(
            run_id=run_id,
        )

        aggregate_snapshot = await get_aggregate_snapshot()

        progress = _build_progress(
            job_counts=job_counts,
            written=aggregate_snapshot["written"],
            matched=aggregate_snapshot["matched"],
            modified=aggregate_snapshot["modified"],
            inserted=aggregate_snapshot["inserted"],
        )

        if skipped_existing > 0:
            progress["skipped"] += skipped_existing

        finished_run = await scraper_run_repository.mark_completed(
            run_id,
            progress=progress,
        )

        logger_service.info(
            (
                "Goodreturns fuel graph scraping completed: "
                f"run_id={run_id}, "
                f"status={finished_run.status}, "
                f"total={total_before_resume_filter}, "
                f"queued={len(queued_rows)}, "
                f"skipped_existing={skipped_existing}, "
                f"successful={job_counts.completed}, "
                f"failed={job_counts.failed}"
            ),
            context="GoodReturnsFuelGraphCommand",
        )

        return {
            "command": COMMAND_NAME,
            "runId": run_id,
            "status": finished_run.status,
            "mode": mode,
            "city": normalized_city,
            "fuelTypes": list(normalized_fuel_types),
            "timeframe": normalized_timeframe,
            "total": total_before_resume_filter,
            "queued": len(queued_rows),
            "skippedExisting": skipped_existing,
            "workers": active_workers,
            "requestsPerSecond": normalized_requests_per_second,
            "batchSize": normalized_batch_size,
            "retries": normalized_retries,
            "refreshExisting": refresh_existing,
            "jobsCreated": create_result.inserted,
            "jobsExisting": create_result.existing,
            "successfulPrices": job_counts.completed,
            "failedPrices": job_counts.failed,
            "skippedPrices": job_counts.skipped + skipped_existing,
            "cancelledPrices": job_counts.cancelled,
            "written": aggregate_snapshot["written"],
            "matched": aggregate_snapshot["matched"],
            "modified": aggregate_snapshot["modified"],
            "inserted": aggregate_snapshot["inserted"],
            "sourceCollection": normalized_cities_json_path,
            "collection": "goodreturns_fuel_graph_prices",
            "jobs": job_counts.to_dict(),
        }

    except (
        KeyboardInterrupt,
        asyncio.CancelledError,
    ) as error:
        if run_created:
            try:
                job_counts = await scraper_job_repository.count_by_status(
                    run_id=run_id,
                )

                aggregate_snapshot = await get_aggregate_snapshot()

                progress = _build_progress(
                    job_counts=job_counts,
                    written=aggregate_snapshot["written"],
                    matched=aggregate_snapshot["matched"],
                    modified=aggregate_snapshot["modified"],
                    inserted=aggregate_snapshot["inserted"],
                )

                await scraper_run_repository.mark_interrupted(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason="Goodreturns fuel graph command interrupted",
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark Goodreturns fuel graph run as interrupted: "
                        f"{type(tracking_error).__name__}: {tracking_error}"
                    ),
                    context="GoodReturnsFuelGraphCommand",
                )

        raise

    except Exception as error:
        if run_created:
            try:
                job_counts = await scraper_job_repository.count_by_status(
                    run_id=run_id,
                )

                aggregate_snapshot = await get_aggregate_snapshot()

                progress = _build_progress(
                    job_counts=job_counts,
                    written=aggregate_snapshot["written"],
                    matched=aggregate_snapshot["matched"],
                    modified=aggregate_snapshot["modified"],
                    inserted=aggregate_snapshot["inserted"],
                )

                await scraper_run_repository.mark_failed(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason="Goodreturns fuel graph scraping failed",
                    stop_http_status=_extract_http_status(error),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark Goodreturns fuel graph run as failed: "
                        f"{type(tracking_error).__name__}: {tracking_error}"
                    ),
                    context="GoodReturnsFuelGraphCommand",
                )

        logger_service.error(
            (
                "Goodreturns fuel graph scraping failed: "
                f"{type(error).__name__}: {error}"
            ),
            context="GoodReturnsFuelGraphCommand",
        )

        raise

    finally:
        await mongo_connection.close()
