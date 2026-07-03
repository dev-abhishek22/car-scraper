from __future__ import annotations

import asyncio
import re
from collections.abc import Mapping
from typing import Any

from pymongo.errors import PyMongoError

from src.clients.client import (
    ExternalClientError,
    ExternalResponseError,
)
from src.databases.mongodb import mongo_connection
from src.external.constants.cardekho import (
    CARDEKHO_CITIES_BUNDLE_URL,
)
from src.external.executors.cardekho.async_client_factory import (
    create_cardekho_async_client,
)
from src.external.executors.cardekho.cities import (
    CarDekhoCitiesExecutor,
)
from src.logger.logger import logger_service
from src.models.scraper_job import ScraperJob
from src.models.scraper_run import ScraperRun
from src.repositories.cardekho_city_repository import (
    cardekho_city_repository,
)
from src.repositories.scraper_job_repository import (
    JobStatusCounts,
    scraper_job_repository,
)
from src.repositories.scraper_run_repository import (
    scraper_run_repository,
)

COMMAND_NAME = "cardekho-cities"
SOURCE_NAME = "cardekho"
RESOURCE_NAME = "cities"
JOB_TYPE = "fetch-cities-bundle"

TARGET_COLLECTION = "cardekho_cities"

HTTP_STATUS_PATTERN = re.compile(
    r"(?:status|status_code|http_status)" r"\s*[=:]\s*(\d{3})",
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


def _validate_requests_per_second(
    requests_per_second: float,
) -> float:
    if (
        isinstance(requests_per_second, bool)
        or not isinstance(
            requests_per_second,
            (
                int,
                float,
            ),
        )
        or requests_per_second <= 0
    ):
        raise ValueError("requests_per_second must be greater " "than zero")

    return float(requests_per_second)


def _validate_pause_configuration(
    *,
    pause_every_requests: int,
    pause_seconds: float,
) -> tuple[int, float]:
    if (
        isinstance(pause_every_requests, bool)
        or not isinstance(
            pause_every_requests,
            int,
        )
        or pause_every_requests < 0
    ):
        raise ValueError("pause_every_requests must be a " "non-negative integer")

    if (
        isinstance(pause_seconds, bool)
        or not isinstance(
            pause_seconds,
            (
                int,
                float,
            ),
        )
        or pause_seconds < 0
    ):
        raise ValueError("pause_seconds must be a non-negative " "number")

    normalized_pause_seconds = float(pause_seconds)

    if (pause_every_requests > 0) != (normalized_pause_seconds > 0):
        raise ValueError(
            "pause_every_requests and pause_seconds "
            "must both be greater than zero or both "
            "be zero"
        )

    return (
        pause_every_requests,
        normalized_pause_seconds,
    )


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
            and not isinstance(
                status_value,
                bool,
            )
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

    if isinstance(
        error,
        ExternalResponseError,
    ):
        return False

    return isinstance(
        error,
        (
            ExternalClientError,
            PyMongoError,
        ),
    )


def _build_job(
    *,
    run_id: str,
) -> ScraperJob:
    return ScraperJob.create(
        run_id=run_id,
        job_id="cities-bundle",
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        job_type=JOB_TYPE,
        item_key="cities-bundle",
        payload={
            "sourceUrl": (CARDEKHO_CITIES_BUNDLE_URL),
        },
        metadata={
            "targetCollection": (TARGET_COLLECTION),
            "sourceType": ("webpack-javascript-bundle"),
        },
        priority=100,
        max_attempts=3,
    )


def _build_progress(
    *,
    job_counts: JobStatusCounts,
    aggregate: Mapping[str, int],
) -> dict[str, int]:
    return {
        "produced": job_counts.total,
        "skipped": job_counts.skipped,
        "successful": job_counts.completed,
        "failed": job_counts.failed,
        "written": aggregate["totalCities"],
        "inserted": aggregate["inserted"],
        "matched": aggregate["matched"],
        "modified": aggregate["modified"],
        "failureRecordsWritten": (job_counts.failed),
        "totalJobs": job_counts.total,
        "pendingJobs": job_counts.pending,
        "runningJobs": job_counts.running,
        "completedJobs": (job_counts.completed),
        "failedJobs": job_counts.failed,
        "skippedJobs": (job_counts.skipped),
        "cancelledJobs": (job_counts.cancelled),
    }


def _build_totals_metadata(
    aggregate: Mapping[str, int],
) -> dict[str, Any]:
    return {
        "cityTotals": {
            "rawCityCount": (aggregate["rawCityCount"]),
            "uniqueCityCount": (aggregate["totalCities"]),
            "duplicateCityRows": (aggregate["duplicateCityRows"]),
            "popularCities": (aggregate["popularCities"]),
            "primeCities": (aggregate["primeCities"]),
            "citiesWithRegions": (aggregate["citiesWithRegions"]),
            "totalAliases": (aggregate["totalAliases"]),
            "totalRegions": (aggregate["totalRegions"]),
            "matched": (aggregate["matched"]),
            "modified": (aggregate["modified"]),
            "inserted": (aggregate["inserted"]),
        }
    }


async def _mark_job_failed_safely(
    *,
    run_id: str,
    job_id: str,
    worker_id: str,
    error: BaseException,
    retryable: bool,
    http_status: int | None,
) -> bool:
    current_job = await scraper_job_repository.get(
        run_id=run_id,
        job_id=job_id,
    )

    if current_job is None or current_job.status not in {
        "pending",
        "running",
    }:
        return False

    await scraper_job_repository.mark_failed(
        run_id=run_id,
        job_id=job_id,
        error=error,
        retryable=retryable,
        http_status=http_status,
        worker_id=worker_id,
    )

    return True


async def _cancel_job_safely(
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
                "Unable to cancel CarDekho cities "
                "job: "
                f"run_id={run_id}, "
                f"job_id={job_id}, "
                "error="
                f"{type(tracking_error).__name__}: "
                f"{tracking_error}"
            ),
            context="CarDekhoCitiesCommand",
        )


async def run_cardekho_cities(
    *,
    requests_per_second: float = 1.0,
    pause_every_requests: int = 0,
    pause_seconds: float = 0.0,
) -> dict[str, Any]:
    normalized_requests_per_second = _validate_requests_per_second(requests_per_second)

    (
        normalized_pause_every_requests,
        normalized_pause_seconds,
    ) = _validate_pause_configuration(
        pause_every_requests=(pause_every_requests),
        pause_seconds=pause_seconds,
    )

    run = ScraperRun.create(
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        command=COMMAND_NAME,
        mode="full",
        filters={},
        settings={
            "workers": 1,
            "requestsPerSecond": (normalized_requests_per_second),
            "pauseEveryRequests": (normalized_pause_every_requests),
            "pauseSeconds": (normalized_pause_seconds),
        },
        metadata={
            "storage": "mongodb",
            "sourceType": ("webpack-javascript-bundle"),
            "sourceUrl": (CARDEKHO_CITIES_BUNDLE_URL),
            "targetCollection": (TARGET_COLLECTION),
        },
    )

    run_id = run.run_id
    run_created = False

    aggregate: dict[str, int] = {
        "rawCityCount": 0,
        "totalCities": 0,
        "duplicateCityRows": 0,
        "popularCities": 0,
        "primeCities": 0,
        "citiesWithRegions": 0,
        "totalAliases": 0,
        "totalRegions": 0,
        "matched": 0,
        "modified": 0,
        "inserted": 0,
    }

    client_metrics: dict[
        str,
        Any,
    ] = {}

    try:
        await mongo_connection.connect()

        await scraper_run_repository.create(run)

        run_created = True

        job = _build_job(run_id=run_id)

        create_result = await scraper_job_repository.create_many([job])

        await scraper_run_repository.mark_started(run_id)

        logger_service.info(
            (
                "Starting CarDekho cities scraping: "
                f"run_id={run_id}, "
                "source_type="
                "webpack-javascript-bundle, "
                "requests_per_second="
                f"{normalized_requests_per_second}"
            ),
            context="CarDekhoCitiesCommand",
        )

        async with create_cardekho_async_client(
            concurrency=1,
            requests_per_second=(normalized_requests_per_second),
            pause_every_requests=(normalized_pause_every_requests),
            pause_seconds=(normalized_pause_seconds),
        ) as client:
            executor = CarDekhoCitiesExecutor(client=client)

            worker_id = "cardekho-cities-worker-1"

            while True:
                claimed_job = await scraper_job_repository.claim_next(
                    run_id=run_id,
                    worker_id=worker_id,
                    resource=RESOURCE_NAME,
                    job_type=JOB_TYPE,
                )

                if claimed_job is None:
                    break

                job_id = claimed_job.job_id

                try:
                    city_result = await executor.execute()

                    cities = city_result.get("cities")

                    if not isinstance(
                        cities,
                        list,
                    ):
                        raise ExternalResponseError(
                            "CarDekho cities executor "
                            "did not return a cities "
                            "array"
                        )

                    upsert_result = await cardekho_city_repository.bulk_upsert(
                        cities=cities,
                        run_id=run_id,
                    )

                    popular_cities = sum(
                        1
                        for city in cities
                        if isinstance(
                            city,
                            Mapping,
                        )
                        and city.get("isPopular") is True
                    )

                    prime_cities = sum(
                        1
                        for city in cities
                        if isinstance(
                            city,
                            Mapping,
                        )
                        and city.get("isPrime") is True
                    )

                    cities_with_regions = sum(
                        1
                        for city in cities
                        if isinstance(
                            city,
                            Mapping,
                        )
                        and isinstance(
                            city.get("regions"),
                            list,
                        )
                        and bool(city.get("regions"))
                    )

                    aggregate.update(
                        {
                            "rawCityCount": int(city_result["rawCityCount"]),
                            "totalCities": (upsert_result.processed),
                            "duplicateCityRows": int(city_result["duplicateCityRows"]),
                            "popularCities": (popular_cities),
                            "primeCities": (prime_cities),
                            "citiesWithRegions": (cities_with_regions),
                            "totalAliases": (upsert_result.total_aliases),
                            "totalRegions": (upsert_result.total_regions),
                            "matched": (upsert_result.matched),
                            "modified": (upsert_result.modified),
                            "inserted": (upsert_result.inserted),
                        }
                    )

                    await scraper_job_repository.mark_completed(
                        run_id=run_id,
                        job_id=job_id,
                        worker_id=worker_id,
                        result={
                            "sourceUrl": (city_result["sourceUrl"]),
                            "rawCityCount": (aggregate["rawCityCount"]),
                            "uniqueCityCount": (aggregate["totalCities"]),
                            "duplicateCityRows": (aggregate["duplicateCityRows"]),
                            "popularCities": (aggregate["popularCities"]),
                            "primeCities": (aggregate["primeCities"]),
                            "citiesWithRegions": (aggregate["citiesWithRegions"]),
                            "totalAliases": (aggregate["totalAliases"]),
                            "totalRegions": (aggregate["totalRegions"]),
                            "matched": (aggregate["matched"]),
                            "modified": (aggregate["modified"]),
                            "inserted": (aggregate["inserted"]),
                        },
                    )

                    logger_service.info(
                        (
                            "CarDekho cities bundle "
                            "completed: "
                            f"run_id={run_id}, "
                            "raw_cities="
                            f"{aggregate['rawCityCount']}, "
                            "unique_cities="
                            f"{aggregate['totalCities']}, "
                            "duplicates="
                            f"{aggregate['duplicateCityRows']}, "
                            "inserted="
                            f"{aggregate['inserted']}, "
                            "modified="
                            f"{aggregate['modified']}"
                        ),
                        context=("CarDekhoCitiesCommand"),
                    )

                except asyncio.CancelledError:
                    await _cancel_job_safely(
                        run_id=run_id,
                        job_id=job_id,
                        reason=("CarDekho cities command " "interrupted"),
                    )

                    raise

                except Exception as error:
                    retryable_error = _is_retryable_error(error)

                    http_status = _extract_http_status(error)

                    failure_recorded = await _mark_job_failed_safely(
                        run_id=run_id,
                        job_id=job_id,
                        worker_id=worker_id,
                        error=error,
                        retryable=(retryable_error),
                        http_status=http_status,
                    )

                    requeued_jobs = 0

                    if failure_recorded and retryable_error:
                        requeued_jobs = await scraper_job_repository.requeue_failed(
                            run_id=run_id
                        )

                    if requeued_jobs > 0:
                        logger_service.info(
                            (
                                "CarDekho cities bundle "
                                "retry scheduled: "
                                f"run_id={run_id}, "
                                "error="
                                f"{type(error).__name__}: "
                                f"{error}"
                            ),
                            context=("CarDekhoCitiesCommand"),
                        )

                        continue

                    logger_service.error(
                        (
                            "CarDekho cities bundle "
                            "failed: "
                            f"run_id={run_id}, "
                            "error="
                            f"{type(error).__name__}: "
                            f"{error}"
                        ),
                        context=("CarDekhoCitiesCommand"),
                    )

                    break

            client_metrics = client.metrics_snapshot()

        job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

        progress = _build_progress(
            job_counts=job_counts,
            aggregate=aggregate,
        )

        finished_run = await scraper_run_repository.mark_completed(
            run_id,
            progress=progress,
            metadata=(_build_totals_metadata(aggregate)),
        )

        logger_service.info(
            (
                "CarDekho cities scraping completed: "
                f"run_id={run_id}, "
                f"status={finished_run.status}, "
                "unique_cities="
                f"{aggregate['totalCities']}, "
                f"failed_jobs={job_counts.failed}"
            ),
            context="CarDekhoCitiesCommand",
        )

        return {
            "command": COMMAND_NAME,
            "runId": run_id,
            "status": finished_run.status,
            "mode": "full",
            "sourceUrl": (CARDEKHO_CITIES_BUNDLE_URL),
            "requestsPerSecond": (normalized_requests_per_second),
            "pauseEveryRequests": (normalized_pause_every_requests),
            "pauseSeconds": (normalized_pause_seconds),
            "jobsCreated": (create_result.inserted),
            "jobsExisting": (create_result.existing),
            "successfulJobs": (job_counts.completed),
            "failedJobs": (job_counts.failed),
            "skippedJobs": (job_counts.skipped),
            "cancelledJobs": (job_counts.cancelled),
            "rawCityCount": (aggregate["rawCityCount"]),
            "uniqueCityCount": (aggregate["totalCities"]),
            "duplicateCityRows": (aggregate["duplicateCityRows"]),
            "popularCities": (aggregate["popularCities"]),
            "primeCities": (aggregate["primeCities"]),
            "citiesWithRegions": (aggregate["citiesWithRegions"]),
            "totalAliases": (aggregate["totalAliases"]),
            "totalRegions": (aggregate["totalRegions"]),
            "matched": (aggregate["matched"]),
            "modified": (aggregate["modified"]),
            "inserted": (aggregate["inserted"]),
            "collection": (TARGET_COLLECTION),
            "httpMetrics": (client_metrics),
            "jobs": (job_counts.to_dict()),
        }

    except (
        KeyboardInterrupt,
        asyncio.CancelledError,
    ) as error:
        if run_created:
            try:
                job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

                progress = _build_progress(
                    job_counts=job_counts,
                    aggregate=aggregate,
                )

                await scraper_run_repository.mark_interrupted(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("CarDekho cities command " "interrupted"),
                    metadata=(_build_totals_metadata(aggregate)),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarDekho cities "
                        "run as interrupted: "
                        f"{type(tracking_error).__name__}: "
                        f"{tracking_error}"
                    ),
                    context=("CarDekhoCitiesCommand"),
                )

        raise

    except Exception as error:
        if run_created:
            try:
                job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

                progress = _build_progress(
                    job_counts=job_counts,
                    aggregate=aggregate,
                )

                await scraper_run_repository.mark_failed(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("CarDekho cities scraping " "failed"),
                    stop_http_status=(_extract_http_status(error)),
                    metadata=(_build_totals_metadata(aggregate)),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarDekho cities "
                        "run as failed: "
                        f"{type(tracking_error).__name__}: "
                        f"{tracking_error}"
                    ),
                    context=("CarDekhoCitiesCommand"),
                )

        logger_service.error(
            (
                "CarDekho cities scraping failed: "
                f"{type(error).__name__}: "
                f"{error}"
            ),
            context="CarDekhoCitiesCommand",
        )

        raise

    finally:
        await mongo_connection.close()
