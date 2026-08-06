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
from src.external.executors.bikedekho.async_client_factory import (
    create_bikedekho_async_client,
)
from src.external.executors.bikedekho.scooters import (
    BikeDekhoScootersExecutor,
)
from src.logger.logger import logger_service
from src.models.bikedekho_scooter_model import BikeDekhoScooterModel
from src.models.scraper_job import ScraperJob
from src.models.scraper_run import ScraperRun
from src.repositories.bikedekho_scooter_repository import (
    bikedekho_scooter_repository,
)
from src.repositories.bikedekho_scooter_model_repository import (
    bikedekho_scooter_model_repository,
)
from src.repositories.scraper_job_repository import (
    JobStatusCounts,
    scraper_job_repository,
)
from src.repositories.scraper_run_repository import (
    scraper_run_repository,
)

COMMAND_NAME = "bikedekho-scooters"
SOURCE_NAME = "bikedekho"
RESOURCE_NAME = "scooters"
JOB_TYPE = "fetch-scooter"

SOURCE_COLLECTION = "bikedekho_scooter_models"
TARGET_COLLECTION = "bikedekho_scooters"

MODEL_STATUS_PRIORITIES = {
    "CURRENT": 100,
    "UPCOMING": 90,
    "DISCONTINUED": 80,
}

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


def _validate_positive_integer(
    value: int,
    *,
    field_name: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")

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

    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")

    normalized_value = value.strip().lower().replace("_", "-").replace(" ", "-")

    normalized_value = re.sub(
        r"-+",
        "-",
        normalized_value,
    ).strip("-")

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    return normalized_value


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
    model: BikeDekhoScooterModel,
) -> dict[str, Any]:
    return {
        "_id": model.document_id,
        "id": model.model_id,
        "brandId": model.brand_id,
        "brandName": model.brand_name,
        "brandSlug": model.brand_slug,
        "name": model.name,
        "slug": model.slug,
        "modelName": model.model_name,
        "modelStatus": model.model_status,
        "isUpcoming": model.is_upcoming,
        "lastRunId": model.last_run_id,
    }


def _build_job(
    *,
    run_id: str,
    model: BikeDekhoScooterModel,
) -> ScraperJob:
    return ScraperJob.create(
        run_id=run_id,
        job_id=(f"scooter:{model.brand_slug}:{model.slug}"),
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        job_type=JOB_TYPE,
        item_key=(f"{model.brand_slug}:{model.slug}"),
        payload=_model_payload(model),
        metadata={
            "sourceCollection": SOURCE_COLLECTION,
            "targetCollection": TARGET_COLLECTION,
            "sourceModelRunId": model.last_run_id,
            "sourceModelDocumentId": model.document_id,
            "modelStatus": model.model_status,
        },
        priority=MODEL_STATUS_PRIORITIES.get(
            model.model_status,
            0,
        ),
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
        "written": aggregate["totalScooters"],
        "inserted": aggregate["inserted"],
        "matched": aggregate["matched"],
        "modified": aggregate["modified"],
        "failureRecordsWritten": job_counts.failed,
        "totalJobs": job_counts.total,
        "pendingJobs": job_counts.pending,
        "runningJobs": job_counts.running,
        "completedJobs": job_counts.completed,
        "failedJobs": job_counts.failed,
        "skippedJobs": job_counts.skipped,
        "cancelledJobs": job_counts.cancelled,
    }


def _build_totals_metadata(
    aggregate: Mapping[str, int],
) -> dict[str, Any]:
    return {
        "scooterTotals": {
            "totalScooters": aggregate["totalScooters"],
            "totalVariants": aggregate["totalVariants"],
            "totalComparisons": aggregate["totalComparisons"],
            "totalSimilarScooters": aggregate["totalSimilarScooters"],
            "matched": aggregate["matched"],
            "modified": aggregate["modified"],
            "inserted": aggregate["inserted"],
        }
    }


def _count_selected_statuses(
    models: list[BikeDekhoScooterModel],
) -> dict[str, int]:
    counts = {
        "CURRENT": 0,
        "UPCOMING": 0,
        "DISCONTINUED": 0,
    }

    for selected_model in models:
        if selected_model.model_status in counts:
            counts[selected_model.model_status] += 1

    return counts


async def _select_models(
    *,
    brand_filter: str | None,
    model_filter: str | None,
) -> list[BikeDekhoScooterModel]:
    if model_filter is not None and brand_filter is None:
        raise ValueError("--model requires --brand")

    if brand_filter is not None and model_filter is not None:
        selected_model = await bikedekho_scooter_model_repository.get_by_slugs(
            brand_slug=brand_filter,
            model_slug=model_filter,
        )

        if selected_model is None:
            raise LookupError(
                "BikeDekho scooter model was not "
                "found in MongoDB: "
                f"brand={brand_filter!r}, "
                f"model={model_filter!r}"
            )

        return [selected_model]

    if brand_filter is not None:
        models = await bikedekho_scooter_model_repository.list_all(
            brand_slug=brand_filter,
        )

        if not models:
            raise LookupError(
                f"No BikeDekho models were found for brand: {brand_filter!r}"
            )

        return models

    models = await bikedekho_scooter_model_repository.list_all()

    if not models:
        raise LookupError("No BikeDekho models were found in MongoDB.")

    return models


async def run_bikedekho_scooters(
    *,
    brand: str | None = None,
    model: str | None = None,
    workers: int = 1,
    requests_per_second: float = 3.0,
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

    (
        normalized_pause_every_requests,
        normalized_pause_seconds,
    ) = _validate_pause_configuration(
        pause_every_requests=(pause_every_requests),
        pause_seconds=(pause_seconds),
    )

    if normalized_model is not None:
        mode = "single-model"
    elif normalized_brand is not None:
        mode = "single-brand"
    else:
        mode = "full"

    run = ScraperRun.create(
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        command=COMMAND_NAME,
        mode=mode,
        filters={
            "brand": normalized_brand,
            "model": normalized_model,
        },
        settings={
            "workers": normalized_workers,
            "requestsPerSecond": (normalized_requests_per_second),
            "pauseEveryRequests": (normalized_pause_every_requests),
            "pauseSeconds": (normalized_pause_seconds),
        },
        metadata={
            "storage": "mongodb",
            "sourceCollection": (SOURCE_COLLECTION),
            "targetCollection": (TARGET_COLLECTION),
        },
    )

    run_id = run.run_id
    run_created = False

    aggregate_lock = asyncio.Lock()

    aggregate: dict[str, int] = {
        "totalScooters": 0,
        "totalVariants": 0,
        "totalComparisons": 0,
        "totalSimilarScooters": 0,
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

        selected_models = await _select_models(
            brand_filter=normalized_brand,
            model_filter=normalized_model,
        )

        selected_status_counts = _count_selected_statuses(selected_models)

        jobs = [
            _build_job(
                run_id=run_id,
                model=selected_model,
            )
            for selected_model in selected_models
        ]

        create_result = await scraper_job_repository.create_many(jobs)

        await scraper_run_repository.mark_started(run_id)

        active_workers = min(
            normalized_workers,
            len(selected_models),
        )

        logger_service.info(
            (
                "Starting BikeDekho scooters scraping: "
                f"run_id={run_id}, "
                f"mode={mode}, "
                f"selected_models={len(selected_models)}, "
                f"workers={active_workers}, "
                f"requests_per_second={normalized_requests_per_second}"
            ),
            context="BikeDekhoScootersCommand",
        )

        async with create_bikedekho_async_client(
            concurrency=active_workers,
            requests_per_second=(normalized_requests_per_second),
            pause_every_requests=(normalized_pause_every_requests),
            pause_seconds=(normalized_pause_seconds),
        ) as client:
            executor = BikeDekhoScootersExecutor(client=client)

            async def worker(
                worker_number: int,
            ) -> None:
                worker_id = f"bikedekho-scooters-worker-{worker_number}"

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

                    try:
                        if not isinstance(
                            payload,
                            Mapping,
                        ):
                            raise ValueError("Scooter job payload must be an object")

                        bike_data = await executor.execute(model=payload)

                        upsert_result = await bikedekho_scooter_repository.upsert_one(
                            model=payload,
                            scooter_data=bike_data,
                            run_id=run_id,
                            source_model_run_id=(
                                payload.get("lastRunId")
                                if isinstance(
                                    payload.get("lastRunId"),
                                    str,
                                )
                                else None
                            ),
                        )

                        async with aggregate_lock:
                            aggregate["totalScooters"] += 1

                            aggregate["totalVariants"] += upsert_result.total_variants

                            aggregate["totalComparisons"] += (
                                upsert_result.total_comparisons
                            )

                            aggregate["totalSimilarScooters"] += (
                                upsert_result.total_similar_scooters
                            )

                            aggregate["matched"] += upsert_result.matched

                            aggregate["modified"] += upsert_result.modified

                            aggregate["inserted"] += upsert_result.inserted

                        await scraper_job_repository.mark_completed(
                            run_id=run_id,
                            job_id=job_id,
                            worker_id=worker_id,
                            result={
                                "documentId": (upsert_result.scooter.document_id),
                                "modelId": (upsert_result.scooter.model_id),
                                "brandSlug": (upsert_result.scooter.brand_slug),
                                "modelSlug": (upsert_result.scooter.slug),
                                "totalVariants": (upsert_result.total_variants),
                                "totalComparisons": (upsert_result.total_comparisons),
                                "totalSimilarScooters": (
                                    upsert_result.total_similar_scooters
                                ),
                            },
                        )

                        logger_service.info(
                            (
                                "BikeDekho scooter completed: "
                                f"run_id={run_id}, "
                                f"scooter={upsert_result.scooter.brand_slug}:"
                                f"{upsert_result.scooter.slug}, "
                                f"status={upsert_result.scooter.model_status}, "
                                f"variants={upsert_result.total_variants}, "
                                f"comparisons={upsert_result.total_comparisons}, "
                                "similar_scooters="
                                f"{upsert_result.total_similar_scooters}, "
                                f"inserted={upsert_result.inserted}, "
                                f"modified={upsert_result.modified}"
                            ),
                            context="BikeDekhoScootersCommand",
                        )

                    except asyncio.CancelledError:
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

                        logger_service.error(
                            (
                                "BikeDekho scooter failed: "
                                f"run_id={run_id}, "
                                f"job_id={job_id}, "
                                "error="
                                f"{type(error).__name__}: "
                                f"{error}"
                            ),
                            context="BikeDekhoScootersCommand",
                        )

            worker_tasks = [
                asyncio.create_task(
                    worker(worker_number),
                    name=(f"bikedekho-scooters-worker-{worker_number}"),
                )
                for worker_number in range(
                    1,
                    active_workers + 1,
                )
            ]

            await asyncio.gather(*worker_tasks)

            client_metrics = client.metrics_snapshot()

        job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

        finished_run = await scraper_run_repository.mark_completed(
            run_id,
            progress={
                "produced": job_counts.total,
                "successful": job_counts.completed,
                "failed": job_counts.failed,
                "written": aggregate["totalScooters"],
            },
            metadata=_build_totals_metadata(aggregate),
        )

        logger_service.info(
            (
                "BikeDekho scooters scraping completed: "
                f"run_id={run_id}, "
                f"status={finished_run.status}, "
                f"successful={job_counts.completed}, "
                f"failed={job_counts.failed}, "
                f"total_scooters={aggregate['totalScooters']}"
            ),
            context="BikeDekhoScootersCommand",
        )

        return {
            "command": COMMAND_NAME,
            "runId": run_id,
            "status": finished_run.status,
            "mode": mode,
            "brand": normalized_brand,
            "model": normalized_model,
            "selectedModels": len(selected_models),
            "selectedCurrentModels": (selected_status_counts["CURRENT"]),
            "selectedUpcomingModels": (selected_status_counts["UPCOMING"]),
            "selectedDiscontinuedModels": (selected_status_counts["DISCONTINUED"]),
            "workers": active_workers,
            "requestsPerSecond": (normalized_requests_per_second),
            "jobsCreated": (create_result.inserted),
            "jobsExisting": (create_result.existing),
            "successfulScooters": (job_counts.completed),
            "failedScooters": (job_counts.failed),
            "totalScooters": (aggregate["totalScooters"]),
            "totalVariants": (aggregate["totalVariants"]),
            "totalComparisons": (aggregate["totalComparisons"]),
            "totalSimilarScooters": (aggregate["totalSimilarScooters"]),
            "matched": aggregate["matched"],
            "modified": aggregate["modified"],
            "inserted": aggregate["inserted"],
            "sourceCollection": (SOURCE_COLLECTION),
            "collection": (TARGET_COLLECTION),
            "httpMetrics": client_metrics,
            "jobs": job_counts.to_dict(),
        }

    except Exception as error:
        if run_created:
            try:
                await scraper_run_repository.mark_failed(
                    run_id,
                    error=error,
                    stop_reason=("BikeDekho scooters scraping failed"),
                    stop_http_status=(_extract_http_status(error)),
                )
            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark BikeDekho "
                        "scooters run as failed: "
                        f"{type(tracking_error).__name__}: "
                        f"{tracking_error}"
                    ),
                    context=("BikeDekhoScootersCommand"),
                )

        logger_service.error(
            f"BikeDekho scooters scraping failed: {type(error).__name__}: {error}",
            exception=error,
            context="BikeDekhoScootersCommand",
        )

        raise

    finally:
        await mongo_connection.close()
