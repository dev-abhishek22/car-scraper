from __future__ import annotations

import asyncio
import re
from collections.abc import Mapping
from typing import Any

from src.clients.client import ExternalClientError
from src.databases.mongodb import mongo_connection
from src.external.executors.cardekho.async_client_factory import (
    create_cardekho_async_client,
)
from src.external.executors.cardekho.model_images import (
    CarDekhoModelImagesExecutor,
)
from src.logger.logger import logger_service
from src.models.cardekho_model import CarDekhoModel
from src.models.scraper_job import ScraperJob
from src.models.scraper_run import ScraperRun
from src.repositories.cardekho_model_images_repository import (
    cardekho_model_images_repository,
)
from src.repositories.cardekho_model_repository import (
    cardekho_model_repository,
)
from src.repositories.scraper_job_repository import (
    JobStatusCounts,
    scraper_job_repository,
)
from src.repositories.scraper_run_repository import (
    scraper_run_repository,
)

COMMAND_NAME = "cardekho-model-images"
SOURCE_NAME = "cardekho"
RESOURCE_NAME = "model-images"
JOB_TYPE = "fetch-model-images"

SOURCE_COLLECTION = "cardekho_models"
TARGET_COLLECTION = "cardekho_model_images"

HTTP_STATUS_PATTERN = re.compile(
    r"(?:status|status_code|http_status)"
    r"\s*[=:]\s*(\d{3})",
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


def _validate_workers(workers: int) -> int:
    if (
        isinstance(workers, bool)
        or not isinstance(workers, int)
        or workers < 1
    ):
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
        raise ValueError(
            "requests_per_second must be greater than zero"
        )

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
        raise ValueError(
            "pause_every_requests must be a non-negative integer"
        )

    if (
        isinstance(pause_seconds, bool)
        or not isinstance(
            pause_seconds,
            (int, float),
        )
        or pause_seconds < 0
    ):
        raise ValueError(
            "pause_seconds must be a non-negative number"
        )

    normalized_pause_seconds = float(pause_seconds)

    requests_pause_enabled = pause_every_requests > 0
    seconds_pause_enabled = normalized_pause_seconds > 0

    if requests_pause_enabled != seconds_pause_enabled:
        raise ValueError(
            "pause_every_requests and pause_seconds "
            "must both be greater than zero or both be zero"
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

    return isinstance(
        error,
        ExternalClientError,
    )


def _model_payload(
    model: CarDekhoModel,
) -> dict[str, Any]:
    return {
        "_id": model.document_id,
        "id": model.model_id,
        "brandId": model.brand_id,
        "brandName": model.brand_name,
        "brandSlug": model.brand_slug,
        "name": model.name,
        "slug": model.slug,
        "carSlug": f"{model.brand_slug}-{model.slug}",
        "modelName": model.model_name,
        "modelStatus": model.model_status,
        "lastRunId": model.last_run_id,
    }


def _build_job(
    *,
    run_id: str,
    model: CarDekhoModel,
) -> ScraperJob:
    priority_by_status = {
        "CURRENT": 100,
        "UPCOMING": 90,
        "DISCONTINUED": 80,
    }

    priority = priority_by_status.get(
        model.model_status,
        0,
    )

    return ScraperJob.create(
        run_id=run_id,
        job_id=f"model:{model.model_id}",
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        job_type=JOB_TYPE,
        item_key=str(model.model_id),
        payload=_model_payload(model),
        metadata={
            "sourceCollection": SOURCE_COLLECTION,
            "targetCollection": TARGET_COLLECTION,
            "sourceModelRunId": model.last_run_id,
            "sourceModelDocumentId": model.document_id,
            "modelStatus": model.model_status,
            "sourceModelSlug": model.slug,
            "brandSlug": model.brand_slug,
        },
        priority=priority,
        max_attempts=3,
    )


def _build_progress(
    *,
    job_counts: JobStatusCounts,
    total_models: int,
    inserted: int,
    modified: int,
) -> dict[str, int]:
    return {
        "produced": job_counts.total,
        "skipped": job_counts.skipped,
        "successful": job_counts.completed,
        "failed": job_counts.failed,
        "written": total_models,
        "inserted": inserted,
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


async def _select_models() -> list[CarDekhoModel]:
    current_models = await cardekho_model_repository.list_all(
        model_status="CURRENT",
    )

    upcoming_models = await cardekho_model_repository.list_all(
        model_status="UPCOMING",
    )

    expired_models = await cardekho_model_repository.list_all(
        model_status="DISCONTINUED",
    )

    deduplicated_models: dict[str, CarDekhoModel] = {}

    for selected_model in [
        *current_models,
        *upcoming_models,
        *expired_models,
    ]:
        deduplicated_models[selected_model.document_id] = selected_model

    models = list(deduplicated_models.values())

    if not models:
        raise LookupError(
            "No CarDekho models were found in MongoDB. "
            "Run cardekho-models first."
        )

    return models


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
            (
                "Unable to cancel CarDekho model images "
                "job: "
                f"run_id={run_id}, "
                f"job_id={job_id}, "
                "error="
                f"{type(tracking_error).__name__}: "
                f"{tracking_error}"
            ),
            context="CarDekhoModelImagesCommand",
        )


async def run_cardekho_model_images(
    *,
    workers: int = 5,
    requests_per_second: float = 5.0,
    pause_every_requests: int = 0,
    pause_seconds: float = 0.0,
) -> dict[str, Any]:
    normalized_workers = _validate_workers(workers)

    normalized_requests_per_second = (
        _validate_requests_per_second(
            requests_per_second
        )
    )

    (
        normalized_pause_every_requests,
        normalized_pause_seconds,
    ) = _validate_pause_configuration(
        pause_every_requests=pause_every_requests,
        pause_seconds=pause_seconds,
    )

    run = ScraperRun.create(
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        command=COMMAND_NAME,
        mode="full",
        filters={},
        settings={
            "workers": normalized_workers,
            "requestsPerSecond": normalized_requests_per_second,
            "pauseEveryRequests": normalized_pause_every_requests,
            "pauseSeconds": normalized_pause_seconds,
        },
        metadata={
            "storage": "mongodb",
            "sourceCollection": SOURCE_COLLECTION,
            "targetCollection": TARGET_COLLECTION,
        },
    )

    run_id = run.run_id
    run_created = False

    aggregate_lock = asyncio.Lock()

    aggregate: dict[str, int] = {
        "totalModels": 0,
        "inserted": 0,
        "modified": 0,
    }

    client_metrics: dict[str, Any] = {}

    async def refresh_run_progress() -> None:
        async with aggregate_lock:
            job_counts = (
                await scraper_job_repository.count_by_status(
                    run_id=run_id
                )
            )

            progress = _build_progress(
                job_counts=job_counts,
                total_models=aggregate["totalModels"],
                inserted=aggregate["inserted"],
                modified=aggregate["modified"],
            )

            await scraper_run_repository.update_progress(
                run_id,
                progress=progress,
            )

    try:
        await mongo_connection.connect()

        await scraper_run_repository.create(run)

        run_created = True

        selected_models = await _select_models()

        jobs = [
            _build_job(
                run_id=run_id,
                model=model,
            )
            for model in selected_models
        ]

        create_result = await scraper_job_repository.create_many(jobs)

        await scraper_run_repository.mark_started(run_id)

        active_workers = min(
            normalized_workers,
            len(selected_models),
        )

        logger_service.info(
            (
                "Starting CarDekho model images scraping: "
                f"run_id={run_id}, "
                f"selected_models={len(selected_models)}, "
                f"workers={active_workers}, "
                "requests_per_second="
                f"{normalized_requests_per_second}"
            ),
            context="CarDekhoModelImagesCommand",
        )

        async with create_cardekho_async_client(
            concurrency=active_workers,
            requests_per_second=normalized_requests_per_second,
            pause_every_requests=normalized_pause_every_requests,
            pause_seconds=normalized_pause_seconds,
        ) as client:
            executor = CarDekhoModelImagesExecutor(
                client=client
            )

            async def worker(
                worker_number: int,
            ) -> None:
                worker_id = (
                    f"cardekho-model-images-worker-"
                    f"{worker_number}"
                )

                while True:
                    claimed_job = (
                        await scraper_job_repository.claim_next(
                            run_id=run_id,
                            worker_id=worker_id,
                            resource=RESOURCE_NAME,
                            job_type=JOB_TYPE,
                        )
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
                            "Model images job payload must be an object"
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

                    model_id = payload.get("id")
                    brand_id = payload.get("brandId")
                    brand_slug = payload.get("brandSlug")
                    model_slug = payload.get("carSlug")

                    try:
                        if (
                            isinstance(model_id, bool)
                            or not isinstance(model_id, int)
                            or model_id <= 0
                        ):
                            raise ValueError(
                                "Model job payload has invalid model id"
                            )

                        if (
                            not isinstance(brand_id, int)
                            or brand_id <= 0
                        ):
                            raise ValueError(
                                "Model job payload has invalid brand id"
                            )

                        if (
                            not isinstance(brand_slug, str)
                            or not brand_slug.strip()
                        ):
                            raise ValueError(
                                "Model job payload has invalid brand slug"
                            )

                        if (
                            not isinstance(model_slug, str)
                            or not model_slug.strip()
                        ):
                            raise ValueError(
                                "Model job payload has invalid model slug"
                            )

                        gallery_data = await executor.execute(
                            model_slug=model_slug
                        )

                        title = gallery_data.get("title")

                        if not isinstance(title, str) or not title.strip():
                            title = payload.get("modelName")

                        if not isinstance(title, str) or not title.strip():
                            raise ValueError(
                                "Model job payload has invalid model name"
                            )

                        existing = (
                            await cardekho_model_images_repository
                            .exists_by_model_id(model_id)
                        )

                        stored_document = (
                            await cardekho_model_images_repository
                            .upsert_one(
                                model={
                                    "modelId": model_id,
                                    "brandId": brand_id,
                                    "brandSlug": brand_slug,
                                    "modelSlug": model_slug,
                                },
                                images_data=gallery_data["images"],
                                title=title.strip(),
                                run_id=run_id,
                            )
                        )

                        await scraper_job_repository.mark_completed(
                            run_id=run_id,
                            job_id=job_id,
                            worker_id=worker_id,
                            result={
                                "modelId": model_id,
                                "brandId": brand_id,
                                "brandSlug": brand_slug,
                                "modelSlug": model_slug,
                                "title": stored_document.title,
                                "imageGroups": len(
                                    stored_document.images
                                ),
                                "inserted": 1 if existing is None else 0,
                                "modified": 0 if existing is None else 1,
                            },
                        )

                        async with aggregate_lock:
                            aggregate["totalModels"] += 1

                            if existing is None:
                                aggregate["inserted"] += 1
                            else:
                                aggregate["modified"] += 1

                        await refresh_run_progress()

                        logger_service.info(
                            (
                                "CarDekho model images "
                                "completed: "
                                f"model_id={model_id}, "
                                f"model_slug={model_slug}, "
                                "image_groups="
                                f"{len(stored_document.images)}, "
                                f"inserted={existing is None}, "
                                f"modified={existing is not None}"
                            ),
                            context="CarDekhoModelImagesCommand",
                        )

                    except asyncio.CancelledError:
                        await _mark_claimed_job_cancelled(
                            run_id=run_id,
                            job_id=job_id,
                            reason=(
                                "Model images command interrupted"
                            ),
                        )

                        raise

                    except Exception as error:
                        http_status = _extract_http_status(error)

                        await scraper_job_repository.mark_failed(
                            run_id=run_id,
                            job_id=job_id,
                            error=error,
                            retryable=_is_retryable_error(error),
                            http_status=http_status,
                            worker_id=worker_id,
                        )

                        await refresh_run_progress()

                        logger_service.error(
                            (
                                "CarDekho model images "
                                "failed: "
                                f"model_id={model_id}, "
                                f"model_slug={model_slug}, "
                                "error="
                                f"{type(error).__name__}: "
                                f"{error}"
                            ),
                            context="CarDekhoModelImagesCommand",
                        )

            worker_tasks = [
                asyncio.create_task(
                    worker(worker_number),
                    name=(
                        "cardekho-model-images-worker-"
                        f"{worker_number}"
                    ),
                )
                for worker_number in range(
                    1,
                    active_workers + 1,
                )
            ]

            await asyncio.gather(*worker_tasks)

            client_metrics = client.metrics_snapshot()

            status_counts = client_metrics.get(
                "status_counts"
            )

            if isinstance(
                status_counts,
                dict,
            ):
                client_metrics["status_counts"] = {
                    str(status_code): count
                    for status_code, count in status_counts.items()
                }

        job_counts = await scraper_job_repository.count_by_status(
            run_id=run_id
        )

        progress = _build_progress(
            job_counts=job_counts,
            total_models=aggregate["totalModels"],
            inserted=aggregate["inserted"],
            modified=aggregate["modified"],
        )

        finished_run = (
            await scraper_run_repository.mark_completed(
                run_id,
                progress=progress,
            )
        )

        logger_service.info(
            (
                "CarDekho model images scraping completed: "
                f"run_id={run_id}, "
                f"status={finished_run.status}, "
                "selected_models="
                f"{len(selected_models)}, "
                f"successful={job_counts.completed}, "
                f"failed={job_counts.failed}, "
                "total_models="
                f"{aggregate['totalModels']}"
            ),
            context="CarDekhoModelImagesCommand",
        )

        return {
            "command": COMMAND_NAME,
            "runId": run_id,
            "status": finished_run.status,
            "mode": "full",
            "selectedModels": len(selected_models),
            "workers": active_workers,
            "requestsPerSecond": normalized_requests_per_second,
            "pauseEveryRequests": normalized_pause_every_requests,
            "pauseSeconds": normalized_pause_seconds,
            "jobsCreated": create_result.inserted,
            "jobsExisting": create_result.existing,
            "successfulModels": job_counts.completed,
            "failedModels": job_counts.failed,
            "skippedModels": job_counts.skipped,
            "cancelledModels": job_counts.cancelled,
            "totalModels": aggregate["totalModels"],
            "inserted": aggregate["inserted"],
            "modified": aggregate["modified"],
            "sourceCollection": SOURCE_COLLECTION,
            "collection": TARGET_COLLECTION,
            "httpMetrics": client_metrics,
            "jobs": job_counts.to_dict(),
        }

    except (
        KeyboardInterrupt,
        asyncio.CancelledError,
    ) as error:
        if run_created:
            try:
                job_counts = (
                    await scraper_job_repository.count_by_status(
                        run_id=run_id
                    )
                )

                progress = _build_progress(
                    job_counts=job_counts,
                    total_models=aggregate["totalModels"],
                    inserted=aggregate["inserted"],
                    modified=aggregate["modified"],
                )

                await scraper_run_repository.mark_interrupted(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=(
                        "CarDekho model images command interrupted"
                    ),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarDekho model images "
                        "run as interrupted: "
                        f"{type(tracking_error).__name__}: "
                        f"{tracking_error}"
                    ),
                    context="CarDekhoModelImagesCommand",
                )

        raise

    except Exception as error:
        if run_created:
            try:
                job_counts = (
                    await scraper_job_repository.count_by_status(
                        run_id=run_id
                    )
                )

                progress = _build_progress(
                    job_counts=job_counts,
                    total_models=aggregate["totalModels"],
                    inserted=aggregate["inserted"],
                    modified=aggregate["modified"],
                )

                await scraper_run_repository.mark_failed(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=(
                        "CarDekho model images scraping failed"
                    ),
                    stop_http_status=_extract_http_status(error),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarDekho model images "
                        "run as failed: "
                        f"{type(tracking_error).__name__}: "
                        f"{tracking_error}"
                    ),
                    context="CarDekhoModelImagesCommand",
                )

            logger_service.error(
                (
                    "CarDekho model images scraping failed: "
                    f"{type(error).__name__}: {error}"
                ),
                context="CarDekhoModelImagesCommand",
            )

        raise

    finally:
        await mongo_connection.close()
