from __future__ import annotations

import asyncio
import re
from collections.abc import Mapping
from typing import Any

from src.clients.client import (
    ExternalClientError,
)
from src.databases.mongodb import (
    mongo_connection,
)
from src.external.executors.carwale.async_client_factory import (
    create_carwale_async_client,
)
from src.external.executors.carwale.models import (
    CarWaleModelsExecutor,
)
from src.logger.logger import logger_service
from src.models.carwale_brand import (
    CarWaleBrand,
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

COMMAND_NAME = "carwale-models"
SOURCE_NAME = "carwale"
RESOURCE_NAME = "models"
JOB_TYPE = "fetch-models"

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


def _validate_workers(
    workers: int,
) -> int:
    if isinstance(workers, bool) or not isinstance(workers, int) or workers < 1:
        raise ValueError("workers must be a positive integer")

    if workers > 1000:
        raise ValueError("workers cannot exceed 1000")

    return workers


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

    requests_pause_enabled = pause_every_requests > 0

    seconds_pause_enabled = normalized_pause_seconds > 0

    if requests_pause_enabled != seconds_pause_enabled:
        raise ValueError(
            "pause_every_requests and pause_seconds "
            "must both be greater than zero or both "
            "be zero"
        )

    return (
        pause_every_requests,
        normalized_pause_seconds,
    )


def _normalize_brand_filter(
    brand: str | None,
) -> str | None:
    if brand is None:
        return None

    normalized_brand = brand.strip().lower()

    if not normalized_brand:
        raise ValueError("brand cannot be empty")

    return normalized_brand


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

    return isinstance(
        error,
        ExternalClientError,
    )


def _brand_payload(
    brand: CarWaleBrand,
) -> dict[str, Any]:
    return {
        "makeId": brand.make_id,
        "makeName": brand.make_name,
        "maskingName": brand.masking_name,
        "lastRunId": brand.last_run_id,
    }


def _build_job(
    *,
    run_id: str,
    brand: CarWaleBrand,
) -> ScraperJob:
    payload = _brand_payload(brand)

    job_id = f"model:{brand.make_id}"

    return ScraperJob.create(
        run_id=run_id,
        job_id=job_id,
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        job_type=JOB_TYPE,
        item_key=brand.masking_name,
        payload=payload,
        metadata={
            "sourceCollection": ("carwale_brands"),
            "targetCollection": ("carwale_models"),
            "sourceBrandRunId": (brand.last_run_id),
        },
        priority=100,
        max_attempts=3,
    )


def _build_progress(
    *,
    job_counts: JobStatusCounts,
    total_models: int,
    matched: int,
    modified: int,
    inserted: int,
) -> dict[str, int]:
    return {
        "produced": job_counts.total,
        "skipped": job_counts.skipped,
        "successful": job_counts.completed,
        "failed": job_counts.failed,
        "written": total_models,
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


async def _select_brands(
    *,
    brand_filter: str | None,
) -> list[CarWaleBrand]:
    if brand_filter is not None:
        brand = await carwale_brand_repository.get_by_masking_name(brand_filter)

        if brand is None:
            raise LookupError(
                "CarWale brand was not found in "
                "MongoDB: "
                f"masking_name={brand_filter!r}. "
                "Run carwale-brands first."
            )

        return [
            brand,
        ]

    brands = await carwale_brand_repository.list_all()

    if not brands:
        raise LookupError(
            "No CarWale brands were found in MongoDB. Run carwale-brands first."
        )

    return brands


async def _mark_claimed_job_cancelled(
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
            (f"Unable to cancel CarWale models job: run_id={run_id}, job_id={job_id}"),
            exception=tracking_error,
            context="CarWaleModelsCommand",
        )


async def run_carwale_models(
    *,
    brand: str | None = None,
    workers: int = 5,
    requests_per_second: float = 5.0,
    pause_every_requests: int = 0,
    pause_seconds: float = 0.0,
) -> dict[str, Any]:
    normalized_brand = _normalize_brand_filter(brand)

    normalized_workers = _validate_workers(workers)

    normalized_requests_per_second = _validate_requests_per_second(requests_per_second)

    (
        normalized_pause_every_requests,
        normalized_pause_seconds,
    ) = _validate_pause_configuration(
        pause_every_requests=(pause_every_requests),
        pause_seconds=pause_seconds,
    )

    mode = "single" if normalized_brand is not None else "full"

    run = ScraperRun.create(
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        command=COMMAND_NAME,
        mode=mode,
        filters={
            "brand": normalized_brand,
        },
        settings={
            "workers": normalized_workers,
            "requestsPerSecond": (normalized_requests_per_second),
            "pauseEveryRequests": (normalized_pause_every_requests),
            "pauseSeconds": (normalized_pause_seconds),
        },
        metadata={
            "storage": "mongodb",
            "sourceCollection": ("carwale_brands"),
            "targetCollection": ("carwale_models"),
        },
    )

    run_id = run.run_id
    run_created = False

    aggregate_lock = asyncio.Lock()

    aggregate: dict[str, int] = {
        "totalModels": 0,
        "matched": 0,
        "modified": 0,
        "inserted": 0,
    }

    client_metrics: dict[str, Any] = {}

    async def refresh_run_progress() -> None:
        async with aggregate_lock:
            job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

            progress = _build_progress(
                job_counts=job_counts,
                total_models=(aggregate["totalModels"]),
                matched=aggregate["matched"],
                modified=aggregate["modified"],
                inserted=aggregate["inserted"],
            )

            await scraper_run_repository.update_progress(
                run_id,
                progress=progress,
            )

    try:
        await mongo_connection.connect()

        await scraper_run_repository.create(run)

        run_created = True

        selected_brands = await _select_brands(brand_filter=normalized_brand)

        jobs = [
            _build_job(
                run_id=run_id,
                brand=selected_brand,
            )
            for selected_brand in selected_brands
        ]

        create_result = await scraper_job_repository.create_many(jobs)

        await scraper_run_repository.mark_started(run_id)

        active_workers = min(
            normalized_workers,
            len(selected_brands),
        )

        logger_service.info(
            (
                "Starting CarWale models scraping: "
                f"run_id={run_id}, "
                f"mode={mode}, "
                f"selected_brands="
                f"{len(selected_brands)}, "
                f"workers={active_workers}, "
                "requests_per_second="
                f"{normalized_requests_per_second}"
            ),
            context="CarWaleModelsCommand",
        )

        async with create_carwale_async_client(
            concurrency=active_workers,
            requests_per_second=(normalized_requests_per_second),
            pause_every_requests=(normalized_pause_every_requests),
            pause_seconds=(normalized_pause_seconds),
        ) as client:
            executor = CarWaleModelsExecutor(client=client)

            async def worker(
                worker_number: int,
            ) -> None:
                worker_id = f"carwale-models-worker-{worker_number}"

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

                    if not isinstance(
                        payload,
                        Mapping,
                    ):
                        payload_error = ValueError(
                            "Model job payload must be an object"
                        )

                        await scraper_job_repository.mark_failed(
                            run_id=run_id,
                            job_id=job_id,
                            error=payload_error,
                            retryable=False,
                            worker_id=worker_id,
                        )

                        await refresh_run_progress()
                        continue

                    make_id = payload.get("makeId")

                    make_name = payload.get("makeName")

                    masking_name = payload.get("maskingName")

                    source_brand_run_id = payload.get("lastRunId")

                    try:
                        models = await executor.execute(brand=payload)

                        upsert_result = await carwale_model_repository.bulk_upsert(
                            brand=payload,
                            models=models,
                            run_id=run_id,
                            source_brand_run_id=(
                                source_brand_run_id
                                if isinstance(
                                    source_brand_run_id,
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
                                "makeId": make_id,
                                "makeName": make_name,
                                "maskingName": (masking_name),
                                "modelsReceived": (upsert_result.received),
                                "modelsProcessed": (upsert_result.processed),
                                "matched": (upsert_result.matched),
                                "modified": (upsert_result.modified),
                                "inserted": (upsert_result.inserted),
                            },
                        )

                        async with aggregate_lock:
                            aggregate["totalModels"] += upsert_result.processed

                            aggregate["matched"] += upsert_result.matched

                            aggregate["modified"] += upsert_result.modified

                            aggregate["inserted"] += upsert_result.inserted

                        await refresh_run_progress()

                        logger_service.info(
                            (
                                "CarWale models brand "
                                "completed: "
                                f"run_id={run_id}, "
                                f"brand={masking_name}, "
                                "models="
                                f"{upsert_result.processed}, "
                                "inserted="
                                f"{upsert_result.inserted}, "
                                "modified="
                                f"{upsert_result.modified}"
                            ),
                            context=("CarWaleModelsCommand"),
                        )

                    except asyncio.CancelledError:
                        await _mark_claimed_job_cancelled(
                            run_id=run_id,
                            job_id=job_id,
                            reason=("Models command interrupted"),
                        )

                        raise

                    except Exception as error:
                        http_status = _extract_http_status(error)

                        await scraper_job_repository.mark_failed(
                            run_id=run_id,
                            job_id=job_id,
                            error=error,
                            retryable=(_is_retryable_error(error)),
                            http_status=http_status,
                            worker_id=worker_id,
                        )

                        await refresh_run_progress()

                        logger_service.error(
                            (
                                "CarWale models brand failed: "
                                f"run_id={run_id}, "
                                f"brand={masking_name}, "
                                f"make_id={make_id}, "
                                f"error={type(error).__name__}: {error}"
                            ),
                            context="CarWaleModelsCommand",
                        )

            worker_tasks = [
                asyncio.create_task(
                    worker(worker_number),
                    name=(f"carwale-models-worker-{worker_number}"),
                )
                for worker_number in range(
                    1,
                    active_workers + 1,
                )
            ]

            await asyncio.gather(*worker_tasks)

            client_metrics = client.metrics_snapshot()

        job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

        progress = _build_progress(
            job_counts=job_counts,
            total_models=(aggregate["totalModels"]),
            matched=aggregate["matched"],
            modified=aggregate["modified"],
            inserted=aggregate["inserted"],
        )

        finished_run = await scraper_run_repository.mark_completed(
            run_id,
            progress=progress,
        )

        logger_service.info(
            (
                "CarWale models scraping completed: "
                f"run_id={run_id}, "
                f"status={finished_run.status}, "
                f"selected_brands="
                f"{len(selected_brands)}, "
                f"successful="
                f"{job_counts.completed}, "
                f"failed={job_counts.failed}, "
                "total_models="
                f"{aggregate['totalModels']}"
            ),
            context="CarWaleModelsCommand",
        )

        return {
            "command": COMMAND_NAME,
            "runId": run_id,
            "status": finished_run.status,
            "mode": mode,
            "brand": normalized_brand,
            "selectedBrands": (len(selected_brands)),
            "workers": active_workers,
            "requestsPerSecond": (normalized_requests_per_second),
            "pauseEveryRequests": (normalized_pause_every_requests),
            "pauseSeconds": (normalized_pause_seconds),
            "jobsCreated": (create_result.inserted),
            "jobsExisting": (create_result.existing),
            "successfulBrands": (job_counts.completed),
            "failedBrands": job_counts.failed,
            "skippedBrands": (job_counts.skipped),
            "cancelledBrands": (job_counts.cancelled),
            "totalModels": (aggregate["totalModels"]),
            "matched": aggregate["matched"],
            "modified": aggregate["modified"],
            "inserted": aggregate["inserted"],
            "sourceCollection": ("carwale_brands"),
            "collection": ("carwale_models"),
            "httpMetrics": client_metrics,
            "jobs": job_counts.to_dict(),
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
                    total_models=(aggregate["totalModels"]),
                    matched=aggregate["matched"],
                    modified=aggregate["modified"],
                    inserted=aggregate["inserted"],
                )

                await scraper_run_repository.mark_interrupted(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("CarWale models command interrupted"),
                )

            except Exception as tracking_error:
                logger_service.error(
                    ("Unable to mark CarWale models run as interrupted"),
                    exception=tracking_error,
                    context=("CarWaleModelsCommand"),
                )

        raise

    except Exception as error:
        if run_created:
            try:
                job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

                progress = _build_progress(
                    job_counts=job_counts,
                    total_models=(aggregate["totalModels"]),
                    matched=aggregate["matched"],
                    modified=aggregate["modified"],
                    inserted=aggregate["inserted"],
                )

                await scraper_run_repository.mark_failed(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("CarWale models scraping failed"),
                    stop_http_status=(_extract_http_status(error)),
                )

            except Exception as tracking_error:
                logger_service.error(
                    ("Unable to mark CarWale models run as failed"),
                    exception=tracking_error,
                    context=("CarWaleModelsCommand"),
                )

            logger_service.error(
                (f"CarWale models scraping failed: {type(error).__name__}: {error}"),
                context="CarWaleModelsCommand",
            )

        raise

    finally:
        await mongo_connection.close()
