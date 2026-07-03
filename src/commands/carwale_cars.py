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
from src.databases.mongodb import (
    mongo_connection,
)
from src.external.executors.carwale.async_client_factory import (
    create_carwale_async_client,
)
from src.external.executors.carwale.cars import (
    CarWaleCarsExecutor,
)
from src.logger.logger import logger_service
from src.models.carwale_model import (
    CarWaleModel,
)
from src.models.scraper_job import (
    ScraperJob,
)
from src.models.scraper_run import (
    ScraperRun,
)
from src.repositories.carwale_brand_repository import (
    carwale_brand_repository,
)
from src.repositories.carwale_car_repository import (
    carwale_car_repository,
)
from src.repositories.carwale_model_repository import (
    carwale_model_repository,
)
from src.repositories.scraper_job_repository import (
    JobStatusCounts,
    scraper_job_repository,
)
from src.repositories.scraper_run_repository import (
    scraper_run_repository,
)

COMMAND_NAME = "carwale-cars"
SOURCE_NAME = "carwale"
RESOURCE_NAME = "cars"
JOB_TYPE = "fetch-car"

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
        or not isinstance(
            requests_per_second,
            (int, float),
        )
        or requests_per_second <= 0
    ):
        raise ValueError("requests_per_second must be greater than zero")

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
        raise ValueError("pause_every_requests must be a non-negative integer")

    if (
        isinstance(pause_seconds, bool)
        or not isinstance(
            pause_seconds,
            (int, float),
        )
        or pause_seconds < 0
    ):
        raise ValueError("pause_seconds must be a non-negative number")

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


def _normalize_optional_slug(
    value: str | None,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    if not isinstance(
        value,
        str,
    ):
        raise ValueError(f"{field_name} must be a string")

    normalized_value = value.strip().lower()

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    return normalized_value


def _normalize_optional_positive_integer(
    value: int | None,
    *,
    field_name: str,
) -> int | None:
    if value is None:
        return None

    return _validate_positive_integer(
        value,
        field_name=field_name,
    )


def _normalize_optional_non_negative_integer(
    value: int | None,
    *,
    field_name: str,
) -> int | None:
    if value is None:
        return None

    return _validate_non_negative_integer(
        value,
        field_name=field_name,
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


def _model_payload(
    model: CarWaleModel,
) -> dict[str, Any]:
    return {
        "makeId": model.make_id,
        "makeName": model.make_name,
        "makeMaskingName": (model.make_masking_name),
        "modelId": model.model_id,
        "modelName": model.model_name,
        "modelMaskingName": (model.model_masking_name),
        "lastRunId": model.last_run_id,
    }


def _build_job(
    *,
    run_id: str,
    model: CarWaleModel,
    city_id: int | None,
    area_id: int | None,
    platform_id: int | None,
    show_offer_upfront: bool,
) -> ScraperJob:
    payload = _model_payload(model)

    payload["showOfferUpfront"] = show_offer_upfront

    if city_id is not None:
        payload["cityId"] = city_id

    if area_id is not None:
        payload["areaId"] = area_id

    if platform_id is not None:
        payload["platformId"] = platform_id

    job_id = f"car:{model.make_id}:{model.model_id}"

    item_key = f"{model.make_masking_name}:{model.model_masking_name}"

    return ScraperJob.create(
        run_id=run_id,
        job_id=job_id,
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        job_type=JOB_TYPE,
        item_key=item_key,
        payload=payload,
        metadata={
            "sourceCollection": ("carwale_models"),
            "targetCollection": ("carwale_cars"),
            "sourceModelRunId": (model.last_run_id),
        },
        priority=100,
        max_attempts=3,
    )


def _build_progress(
    *,
    job_counts: JobStatusCounts,
    total_cars: int,
    matched: int,
    modified: int,
    inserted: int,
) -> dict[str, int]:
    return {
        "produced": job_counts.total,
        "skipped": job_counts.skipped,
        "successful": job_counts.completed,
        "failed": job_counts.failed,
        "written": total_cars,
        "inserted": inserted,
        "matched": matched,
        "modified": modified,
        "failureRecordsWritten": (job_counts.failed),
        "totalJobs": job_counts.total,
        "pendingJobs": job_counts.pending,
        "runningJobs": job_counts.running,
        "completedJobs": (job_counts.completed),
        "failedJobs": job_counts.failed,
        "skippedJobs": job_counts.skipped,
        "cancelledJobs": (job_counts.cancelled),
    }


async def _select_models(
    *,
    brand_filter: str | None,
    model_filter: str | None,
) -> list[CarWaleModel]:
    if model_filter is not None and brand_filter is None:
        raise ValueError("--model requires --brand")

    if brand_filter is not None and model_filter is not None:
        selected_model = await carwale_model_repository.get_by_masking_names(
            make_masking_name=brand_filter,
            model_masking_name=model_filter,
        )

        if selected_model is None:
            raise LookupError(
                "CarWale model was not found in "
                "MongoDB: "
                f"brand={brand_filter!r}, "
                f"model={model_filter!r}. "
                "Run carwale-models first."
            )

        return [selected_model]

    if brand_filter is not None:
        selected_brand = await carwale_brand_repository.get_by_masking_name(
            brand_filter
        )

        if selected_brand is None:
            raise LookupError(
                "CarWale brand was not found in "
                "MongoDB: "
                f"brand={brand_filter!r}. "
                "Run carwale-brands first."
            )

        models = await carwale_model_repository.list_all(
            make_id=(selected_brand.make_id)
        )

        if not models:
            raise LookupError(
                "No CarWale models were found in "
                "MongoDB for brand: "
                f"{brand_filter!r}. "
                "Run carwale-models first."
            )

        return models

    models = await carwale_model_repository.list_all()

    if not models:
        raise LookupError(
            "No CarWale models were found in MongoDB. Run carwale-models first."
        )

    return models


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
                "Unable to cancel CarWale car job: "
                f"run_id={run_id}, "
                f"job_id={job_id}, "
                f"error={type(tracking_error).__name__}: {tracking_error}"
            ),
            context="CarWaleCarsCommand",
        )


async def run_carwale_cars(
    *,
    brand: str | None = None,
    model: str | None = None,
    workers: int = 3,
    requests_per_second: float = 3.0,
    city_id: int | None = None,
    area_id: int | None = None,
    platform_id: int | None = None,
    show_offer_upfront: bool = False,
    pause_every_requests: int = 0,
    pause_seconds: float = 0.0,
) -> dict[str, Any]:
    normalized_brand = _normalize_optional_slug(
        brand,
        field_name="brand",
    )

    normalized_model = _normalize_optional_slug(
        model,
        field_name="model",
    )

    if normalized_model is not None and normalized_brand is None:
        raise ValueError("model requires brand")

    normalized_workers = _validate_workers(workers)

    normalized_requests_per_second = _validate_requests_per_second(requests_per_second)

    normalized_city_id = _normalize_optional_positive_integer(
        city_id,
        field_name="city_id",
    )

    normalized_area_id = _normalize_optional_non_negative_integer(
        area_id,
        field_name="area_id",
    )

    normalized_platform_id = _normalize_optional_positive_integer(
        platform_id,
        field_name="platform_id",
    )

    if not isinstance(
        show_offer_upfront,
        bool,
    ):
        raise ValueError("show_offer_upfront must be a boolean")

    (
        normalized_pause_every_requests,
        normalized_pause_seconds,
    ) = _validate_pause_configuration(
        pause_every_requests=(pause_every_requests),
        pause_seconds=pause_seconds,
    )

    if normalized_model is not None:
        mode = "single-model"
    elif normalized_brand is not None:
        mode = "single-brand"
    else:
        mode = "full"

    run_settings: dict[str, Any] = {
        "workers": normalized_workers,
        "requestsPerSecond": normalized_requests_per_second,
        "showOfferUpfront": show_offer_upfront,
        "pauseEveryRequests": normalized_pause_every_requests,
        "pauseSeconds": normalized_pause_seconds,
    }

    if normalized_city_id is not None:
        run_settings["cityId"] = normalized_city_id

    if normalized_area_id is not None:
        run_settings["areaId"] = normalized_area_id

    if normalized_platform_id is not None:
        run_settings["platformId"] = normalized_platform_id

    run = ScraperRun.create(
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        command=COMMAND_NAME,
        mode=mode,
        filters={
            "brand": normalized_brand,
            "model": normalized_model,
        },
        settings=run_settings,
        metadata={
            "storage": "mongodb",
            "sourceCollection": ("carwale_models"),
            "targetCollection": ("carwale_cars"),
        },
    )

    run_id = run.run_id
    run_created = False

    aggregate_lock = asyncio.Lock()

    aggregate: dict[str, int] = {
        "totalCars": 0,
        "totalVersions": 0,
        "matched": 0,
        "modified": 0,
        "inserted": 0,
    }

    client_metrics: dict[str, Any] = {}

    async def get_aggregate_snapshot() -> dict[str, int]:
        async with aggregate_lock:
            return dict(aggregate)

    async def refresh_run_progress() -> None:
        job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

        aggregate_snapshot = await get_aggregate_snapshot()

        progress = _build_progress(
            job_counts=job_counts,
            total_cars=(aggregate_snapshot["totalCars"]),
            matched=(aggregate_snapshot["matched"]),
            modified=(aggregate_snapshot["modified"]),
            inserted=(aggregate_snapshot["inserted"]),
        )

        await scraper_run_repository.update_progress(
            run_id,
            progress=progress,
        )

    try:
        await mongo_connection.connect()

        await scraper_run_repository.create(run)

        run_created = True

        selected_models = await _select_models(
            brand_filter=(normalized_brand),
            model_filter=(normalized_model),
        )

        jobs = [
            _build_job(
                run_id=run_id,
                model=selected_model,
                city_id=normalized_city_id,
                area_id=normalized_area_id,
                platform_id=normalized_platform_id,
                show_offer_upfront=show_offer_upfront,
            )
            for selected_model in selected_models
        ]

        create_result = await scraper_job_repository.create_many(jobs)

        await scraper_run_repository.mark_started(run_id)

        active_workers = min(
            normalized_workers,
            len(selected_models),
        )

        optional_request_context = []

        if normalized_city_id is not None:
            optional_request_context.append(f"city_id={normalized_city_id}")

        if normalized_area_id is not None:
            optional_request_context.append(f"area_id={normalized_area_id}")

        if normalized_platform_id is not None:
            optional_request_context.append(f"platform_id={normalized_platform_id}")

        optional_request_context_text = (
            f", {', '.join(optional_request_context)}"
            if optional_request_context
            else ""
        )

        logger_service.info(
            (
                "Starting CarWale cars scraping: "
                f"run_id={run_id}, "
                f"mode={mode}, "
                "selected_models="
                f"{len(selected_models)}, "
                f"workers={active_workers}, "
                "requests_per_second="
                f"{normalized_requests_per_second}"
                f"{optional_request_context_text}"
            ),
            context="CarWaleCarsCommand",
        )

        async with create_carwale_async_client(
            concurrency=active_workers,
            requests_per_second=(normalized_requests_per_second),
            pause_every_requests=(normalized_pause_every_requests),
            pause_seconds=(normalized_pause_seconds),
        ) as client:
            executor = CarWaleCarsExecutor(client=client)

            async def worker(
                worker_number: int,
            ) -> None:
                worker_id = f"carwale-cars-worker-{worker_number}"

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

                    make_id: Any = None
                    model_id: Any = None
                    make_masking_name: Any = None
                    model_masking_name: Any = None

                    try:
                        if not isinstance(
                            payload,
                            Mapping,
                        ):
                            raise ValueError("Car job payload must be an object")

                        make_id = payload.get("makeId")
                        model_id = payload.get("modelId")
                        make_masking_name = payload.get("makeMaskingName")
                        model_masking_name = payload.get("modelMaskingName")
                        source_model_run_id = payload.get("lastRunId")

                        car_data = await executor.execute(
                            model=payload,
                            city_id=normalized_city_id,
                            area_id=normalized_area_id,
                            platform_id=normalized_platform_id,
                            show_offer_upfront=show_offer_upfront,
                        )

                        upsert_result = await carwale_car_repository.upsert_one(
                            model=payload,
                            car_data=car_data,
                            run_id=run_id,
                            city_id=normalized_city_id,
                            area_id=normalized_area_id,
                            platform_id=normalized_platform_id,
                            show_offer_upfront=show_offer_upfront,
                            source_model_run_id=(
                                source_model_run_id
                                if isinstance(
                                    source_model_run_id,
                                    str,
                                )
                                else None
                            ),
                        )

                        await scraper_job_repository.mark_completed(
                            run_id=run_id,
                            job_id=job_id,
                            worker_id=worker_id,
                            result={
                                "documentId": (upsert_result.car.document_id),
                                "makeId": make_id,
                                "modelId": model_id,
                                "makeMaskingName": (make_masking_name),
                                "modelMaskingName": (model_masking_name),
                                "totalVersions": (upsert_result.total_versions),
                                "matched": (upsert_result.matched),
                                "modified": (upsert_result.modified),
                                "inserted": (upsert_result.inserted),
                            },
                        )

                        async with aggregate_lock:
                            aggregate["totalCars"] += 1
                            aggregate["totalVersions"] += upsert_result.total_versions
                            aggregate["matched"] += upsert_result.matched
                            aggregate["modified"] += upsert_result.modified
                            aggregate["inserted"] += upsert_result.inserted

                        await refresh_run_progress()

                        logger_service.info(
                            (
                                "CarWale car completed: "
                                f"run_id={run_id}, "
                                "car="
                                f"{make_masking_name}:"
                                f"{model_masking_name}, "
                                "versions="
                                f"{upsert_result.total_versions}, "
                                "inserted="
                                f"{upsert_result.inserted}, "
                                "modified="
                                f"{upsert_result.modified}"
                            ),
                            context="CarWaleCarsCommand",
                        )

                    except asyncio.CancelledError:
                        await _cancel_claimed_job_safely(
                            run_id=run_id,
                            job_id=job_id,
                            reason=("Cars command interrupted"),
                        )

                        raise

                    except Exception as error:
                        retryable_error = _is_retryable_error(error)
                        http_status = _extract_http_status(error)

                        await scraper_job_repository.mark_failed(
                            run_id=run_id,
                            job_id=job_id,
                            error=error,
                            retryable=(retryable_error),
                            http_status=(http_status),
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
                                    "CarWale car retry scheduled: "
                                    f"run_id={run_id}, "
                                    f"make_id={make_id}, "
                                    f"model_id={model_id}, "
                                    "car="
                                    f"{make_masking_name}:"
                                    f"{model_masking_name}, "
                                    "error="
                                    f"{type(error).__name__}: {error}"
                                ),
                                context="CarWaleCarsCommand",
                            )

                            continue

                        logger_service.error(
                            (
                                "CarWale car failed: "
                                f"run_id={run_id}, "
                                f"make_id={make_id}, "
                                f"model_id={model_id}, "
                                "car="
                                f"{make_masking_name}:"
                                f"{model_masking_name}, "
                                "error="
                                f"{type(error).__name__}: {error}"
                            ),
                            context="CarWaleCarsCommand",
                        )

            worker_tasks = [
                asyncio.create_task(
                    worker(worker_number),
                    name=(f"carwale-cars-worker-{worker_number}"),
                )
                for worker_number in range(
                    1,
                    active_workers + 1,
                )
            ]

            await asyncio.gather(*worker_tasks)

            client_metrics = client.metrics_snapshot()

        job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

        aggregate_snapshot = await get_aggregate_snapshot()

        progress = _build_progress(
            job_counts=job_counts,
            total_cars=(aggregate_snapshot["totalCars"]),
            matched=(aggregate_snapshot["matched"]),
            modified=(aggregate_snapshot["modified"]),
            inserted=(aggregate_snapshot["inserted"]),
        )

        finished_run = await scraper_run_repository.mark_completed(
            run_id,
            progress=progress,
        )

        logger_service.info(
            (
                "CarWale cars scraping completed: "
                f"run_id={run_id}, "
                f"status={finished_run.status}, "
                "selected_models="
                f"{len(selected_models)}, "
                "successful="
                f"{job_counts.completed}, "
                f"failed={job_counts.failed}, "
                "total_versions="
                f"{aggregate_snapshot['totalVersions']}"
            ),
            context="CarWaleCarsCommand",
        )

        result: dict[str, Any] = {
            "command": COMMAND_NAME,
            "runId": run_id,
            "status": finished_run.status,
            "mode": mode,
            "brand": normalized_brand,
            "model": normalized_model,
            "selectedModels": (len(selected_models)),
            "workers": active_workers,
            "requestsPerSecond": (normalized_requests_per_second),
            "showOfferUpfront": (show_offer_upfront),
            "pauseEveryRequests": (normalized_pause_every_requests),
            "pauseSeconds": (normalized_pause_seconds),
            "jobsCreated": (create_result.inserted),
            "jobsExisting": (create_result.existing),
            "successfulCars": (job_counts.completed),
            "failedCars": (job_counts.failed),
            "skippedCars": (job_counts.skipped),
            "cancelledCars": (job_counts.cancelled),
            "totalCars": (aggregate_snapshot["totalCars"]),
            "totalVersions": (aggregate_snapshot["totalVersions"]),
            "matched": (aggregate_snapshot["matched"]),
            "modified": (aggregate_snapshot["modified"]),
            "inserted": (aggregate_snapshot["inserted"]),
            "sourceCollection": ("carwale_models"),
            "collection": ("carwale_cars"),
            "httpMetrics": client_metrics,
            "jobs": job_counts.to_dict(),
        }

        if normalized_city_id is not None:
            result["cityId"] = normalized_city_id

        if normalized_area_id is not None:
            result["areaId"] = normalized_area_id

        if normalized_platform_id is not None:
            result["platformId"] = normalized_platform_id

        return result

    except (
        KeyboardInterrupt,
        asyncio.CancelledError,
    ) as error:
        if run_created:
            try:
                job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

                aggregate_snapshot = await get_aggregate_snapshot()

                progress = _build_progress(
                    job_counts=job_counts,
                    total_cars=(aggregate_snapshot["totalCars"]),
                    matched=(aggregate_snapshot["matched"]),
                    modified=(aggregate_snapshot["modified"]),
                    inserted=(aggregate_snapshot["inserted"]),
                )

                await scraper_run_repository.mark_interrupted(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("CarWale cars command interrupted"),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarWale cars run as interrupted: "
                        f"{type(tracking_error).__name__}: {tracking_error}"
                    ),
                    context="CarWaleCarsCommand",
                )

        raise

    except Exception as error:
        if run_created:
            try:
                job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

                aggregate_snapshot = await get_aggregate_snapshot()

                progress = _build_progress(
                    job_counts=job_counts,
                    total_cars=(aggregate_snapshot["totalCars"]),
                    matched=(aggregate_snapshot["matched"]),
                    modified=(aggregate_snapshot["modified"]),
                    inserted=(aggregate_snapshot["inserted"]),
                )

                await scraper_run_repository.mark_failed(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("CarWale cars scraping failed"),
                    stop_http_status=(_extract_http_status(error)),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarWale cars run as failed: "
                        f"{type(tracking_error).__name__}: {tracking_error}"
                    ),
                    context="CarWaleCarsCommand",
                )

        logger_service.error(
            ("CarWale cars scraping failed: " f"{type(error).__name__}: {error}"),
            context="CarWaleCarsCommand",
        )

        raise

    finally:
        await mongo_connection.close()
