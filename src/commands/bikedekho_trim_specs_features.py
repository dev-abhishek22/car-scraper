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
from src.external.executors.bikedekho.trim_specs_features import (
    BikeDekhoTrimSpecsFeaturesExecutor,
)
from src.external.executors.bikedekho.trim_specs_features_jobs import (
    COMMAND_NAME,
    JOB_TYPE,
    RESOURCE_NAME,
    SOURCE_COLLECTION,
    SOURCE_NAME,
    TARGET_COLLECTION,
    build_bikedekho_trim_specs_features_jobs,
    load_bikedekho_trim_specs_features_variants,
)
from src.logger.logger import logger_service
from src.models.scraper_run import ScraperRun
from src.repositories.bikedekho_trim_specs_features_repository import (
    bikedekho_trim_specs_features_repository,
)
from src.repositories.scraper_job_repository import (
    JobStatusCounts,
    scraper_job_repository,
)
from src.repositories.scraper_run_repository import (
    scraper_run_repository,
)

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


def _validate_positive_number(
    value: float,
    *,
    field_name: str,
) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(
            value,
            (
                int,
                float,
            ),
        )
        or value <= 0
    ):
        raise ValueError(f"{field_name} must be greater than zero")

    return float(value)


def _validate_non_negative_integer(
    value: int,
    *,
    field_name: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")

    return value


def _validate_non_negative_number(
    value: float,
    *,
    field_name: str,
) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(
            value,
            (
                int,
                float,
            ),
        )
        or value < 0
    ):
        raise ValueError(f"{field_name} must be a non-negative number")

    return float(value)


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


def _normalize_optional_run_id(
    value: str | None,
) -> str | None:
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValueError("resume_run_id must be a string")

    normalized_value = value.strip()

    if not normalized_value:
        raise ValueError("resume_run_id cannot be empty")

    return normalized_value


def _validate_pause_configuration(
    *,
    pause_every_requests: int,
    pause_seconds: float,
) -> tuple[int, float]:
    normalized_pause_every_requests = _validate_non_negative_integer(
        pause_every_requests,
        field_name="pause_every_requests",
    )

    normalized_pause_seconds = _validate_non_negative_number(
        pause_seconds,
        field_name="pause_seconds",
    )

    if (normalized_pause_every_requests > 0) != (normalized_pause_seconds > 0):
        raise ValueError(
            "pause_every_requests and "
            "pause_seconds must both be greater "
            "than zero or both be zero"
        )

    return (
        normalized_pause_every_requests,
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


def _resolve_mode(
    *,
    brand: str | None,
    model: str | None,
    model_id: int | None,
    variant: str | None,
    variant_id: int | None,
) -> str:
    if variant_id is not None:
        return "single-variant-id"

    if variant is not None:
        return "single-variant"

    if model_id is not None:
        return "single-model-id"

    if model is not None:
        return "single-model"

    if brand is not None:
        return "single-brand"

    return "full"


def _build_progress(
    *,
    job_counts: JobStatusCounts,
    written: int,
    inserted: int,
    matched: int,
    modified: int,
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
                reason=("BikeDekho trim specs/features " "command interrupted"),
            )

    except Exception as tracking_error:
        logger_service.error(
            (
                "Unable to cancel BikeDekho "
                "trim specs/features job: "
                f"run_id={run_id}, "
                f"job_id={job_id}, "
                "error="
                f"{type(tracking_error).__name__}: "
                f"{tracking_error}"
            ),
            context="BikeDekhoTrimSpecsFeaturesCommand",
        )


async def run_bikedekho_trim_specs_features(
    *,
    brand: str | None = None,
    model: str | None = None,
    model_id: int | None = None,
    variant: str | None = None,
    variant_id: int | None = None,
    workers: int = 5,
    requests_per_second: float = 2.0,
    max_jobs: int | None = None,
    pause_every_requests: int = 0,
    pause_seconds: float = 0.0,
    refresh_existing: bool = False,
    resume_run_id: str | None = None,
    failed_only: bool = False,
    retry_terminal_failures: bool = False,
    stale_after_seconds: float = 300.0,
) -> dict[str, Any]:
    normalized_brand = _normalize_optional_slug(
        brand,
        field_name="brand",
    )

    normalized_model = _normalize_optional_slug(
        model,
        field_name="model",
    )

    normalized_model_id = _normalize_optional_positive_integer(
        model_id,
        field_name="model_id",
    )

    normalized_variant = _normalize_optional_slug(
        variant,
        field_name="variant",
    )

    normalized_variant_id = _normalize_optional_positive_integer(
        variant_id,
        field_name="variant_id",
    )

    normalized_max_jobs = _normalize_optional_positive_integer(
        max_jobs,
        field_name="max_jobs",
    )

    normalized_resume_run_id = _normalize_optional_run_id(resume_run_id)

    normalized_workers = _validate_workers(workers)

    normalized_requests_per_second = _validate_positive_number(
        requests_per_second,
        field_name="requests_per_second",
    )

    (
        normalized_pause_every_requests,
        normalized_pause_seconds,
    ) = _validate_pause_configuration(
        pause_every_requests=(pause_every_requests),
        pause_seconds=pause_seconds,
    )

    normalized_stale_after_seconds = _validate_positive_number(
        stale_after_seconds,
        field_name="stale_after_seconds",
    )

    if normalized_model is not None and normalized_brand is None:
        raise ValueError("model requires brand")

    if normalized_variant is not None and (
        normalized_brand is None or normalized_model is None
    ):
        raise ValueError("variant requires brand and model")

    if normalized_variant_id is not None and normalized_brand is None:
        # variantId alone is allowed because the
        # source Mongo document contains the complete
        # request context.
        pass

    if not isinstance(
        refresh_existing,
        bool,
    ):
        raise ValueError("refresh_existing must be a boolean")

    if not isinstance(
        failed_only,
        bool,
    ):
        raise ValueError("failed_only must be a boolean")

    if not isinstance(
        retry_terminal_failures,
        bool,
    ):
        raise ValueError("retry_terminal_failures must be a boolean")

    if failed_only and normalized_resume_run_id is None:
        raise ValueError("failed_only requires resume_run_id")

    if retry_terminal_failures and normalized_resume_run_id is None:
        raise ValueError("retry_terminal_failures " "requires resume_run_id")

    mode = _resolve_mode(
        brand=normalized_brand,
        model=normalized_model,
        model_id=normalized_model_id,
        variant=normalized_variant,
        variant_id=normalized_variant_id,
    )

    run_id = normalized_resume_run_id or ""

    run_created = False

    jobs_created = 0
    jobs_existing = 0
    requeued_jobs = 0
    stale_jobs_requeued = 0

    effective_refresh_existing = refresh_existing

    aggregate_lock = asyncio.Lock()

    aggregate: dict[str, int] = {
        "written": 0,
        "inserted": 0,
        "matched": 0,
        "modified": 0,
    }

    client_metrics: dict[str, Any] = {}

    async def get_aggregate_snapshot(
        *,
        _aggregate: dict[str, int] = aggregate,
    ) -> dict[str, int]:
        async with aggregate_lock:
            return dict(_aggregate)

    async def refresh_run_progress() -> None:
        job_counts = await scraper_job_repository.count_by_status(
            run_id=run_id,
        )

        aggregate_snapshot = await get_aggregate_snapshot()

        progress = _build_progress(
            job_counts=job_counts,
            written=aggregate_snapshot["written"],
            inserted=aggregate_snapshot["inserted"],
            matched=aggregate_snapshot["matched"],
            modified=aggregate_snapshot["modified"],
        )

        await scraper_run_repository.update_progress(
            run_id,
            progress=progress,
        )

    try:
        await mongo_connection.connect()

        if normalized_resume_run_id is not None:
            existing_run = await scraper_run_repository.require(
                normalized_resume_run_id
            )

            if existing_run.source != SOURCE_NAME:
                raise ValueError(f"Run source does not match " f"{SOURCE_NAME!r}")

            if existing_run.resource != RESOURCE_NAME:
                raise ValueError(f"Run resource does not match " f"{RESOURCE_NAME!r}")

            if existing_run.command != COMMAND_NAME:
                raise ValueError(f"Run command does not match " f"{COMMAND_NAME!r}")

            run_id = existing_run.run_id

            mode = existing_run.mode

            stored_refresh_existing = existing_run.settings.get("refreshExisting")

            if isinstance(
                stored_refresh_existing,
                bool,
            ):
                effective_refresh_existing = stored_refresh_existing

            stale_jobs_requeued = await scraper_job_repository.requeue_stale_running(
                run_id=run_id,
                stale_after_seconds=(normalized_stale_after_seconds),
            )

            current_counts = await scraper_job_repository.count_by_status(
                run_id=run_id,
            )

            if failed_only and (
                current_counts.pending > 0 or current_counts.running > 0
            ):
                raise ValueError(
                    "failed_only cannot run while " "pending or running jobs exist"
                )

            requeued_jobs = await scraper_job_repository.requeue_failed(
                run_id=run_id,
                include_non_retryable=(retry_terminal_failures),
                ignore_max_attempts=(retry_terminal_failures),
                reset_attempts=(retry_terminal_failures),
            )

            if existing_run.status == "pending":
                await scraper_run_repository.mark_started(run_id)
            else:
                await scraper_run_repository.mark_resumed(run_id)

        else:
            run = ScraperRun.create(
                source=SOURCE_NAME,
                resource=RESOURCE_NAME,
                command=COMMAND_NAME,
                mode=mode,
                filters={
                    "brand": normalized_brand,
                    "model": normalized_model,
                    "modelId": normalized_model_id,
                    "variant": normalized_variant,
                    "variantId": normalized_variant_id,
                    "maxJobs": normalized_max_jobs,
                },
                settings={
                    "workers": normalized_workers,
                    "requestsPerSecond": (normalized_requests_per_second),
                    "pauseEveryRequests": (normalized_pause_every_requests),
                    "pauseSeconds": (normalized_pause_seconds),
                    "refreshExisting": (refresh_existing),
                    "staleAfterSeconds": (normalized_stale_after_seconds),
                },
                metadata={
                    "storage": "mongodb",
                    "sourceCollection": (SOURCE_COLLECTION),
                    "targetCollection": (TARGET_COLLECTION),
                },
            )

            run_id = run.run_id

            await scraper_run_repository.create(run)

            run_created = True

            variant_records = await load_bikedekho_trim_specs_features_variants(
                selected_brand=(normalized_brand),
                selected_model=(normalized_model),
                selected_model_id=(normalized_model_id),
                selected_variant=(normalized_variant),
                selected_variant_id=(normalized_variant_id),
            )

            if normalized_max_jobs is not None:
                variant_records = variant_records[:normalized_max_jobs]

            jobs = build_bikedekho_trim_specs_features_jobs(
                run_id=run_id,
                variant_records=(variant_records),
            )

            create_result = await scraper_job_repository.create_many(jobs)

            jobs_created = create_result.inserted

            jobs_existing = create_result.existing

            await refresh_run_progress()

        initial_job_counts = await scraper_job_repository.count_by_status(
            run_id=run_id,
        )

        logger_service.info(
            (
                "Starting BikeDekho trim "
                "specs/features scraping: "
                f"run_id={run_id}, "
                f"mode={mode}, "
                f"total_jobs="
                f"{initial_job_counts.total}, "
                f"pending_jobs="
                f"{initial_job_counts.pending}, "
                f"workers={normalized_workers}, "
                "requests_per_second="
                f"{normalized_requests_per_second}, "
                "refresh_existing="
                f"{effective_refresh_existing}, "
                "resumed="
                f"{normalized_resume_run_id is not None}"
            ),
            context=("BikeDekhoTrimSpecsFeaturesCommand"),
        )

        async with create_bikedekho_async_client(
            concurrency=normalized_workers,
            requests_per_second=(normalized_requests_per_second),
            pause_every_requests=(normalized_pause_every_requests),
            pause_seconds=(normalized_pause_seconds),
        ) as client:
            executor = BikeDekhoTrimSpecsFeaturesExecutor(client=client)

            async def worker(
                worker_number: int,
            ) -> None:
                worker_id = "bikedekho-trim-specs-features-worker-" f"{worker_number}"

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

                    variant_id_value: Any = None
                    variant_slug: Any = None
                    model_slug: Any = None
                    brand_slug: Any = None

                    try:
                        if not isinstance(
                            payload,
                            Mapping,
                        ):
                            raise ValueError(
                                "Trim specs/features "
                                "job payload must "
                                "be an object"
                            )

                        variant_value = payload.get("variant")

                        if not isinstance(
                            variant_value,
                            Mapping,
                        ):
                            raise ValueError(
                                "Trim specs/features "
                                "job payload.variant "
                                "must be an object"
                            )

                        variant_id_value = payload.get(
                            "variantId"
                        ) or variant_value.get("variantId")

                        variant_slug = payload.get("variantSlug") or variant_value.get(
                            "variantSlug"
                        )

                        model_slug = payload.get("modelSlug")

                        brand_slug = payload.get("brandSlug")

                        if (
                            isinstance(
                                variant_id_value,
                                bool,
                            )
                            or not isinstance(
                                variant_id_value,
                                int,
                            )
                            or variant_id_value <= 0
                        ):
                            raise ValueError("Invalid variantId " f"for job={job_id}")

                        if (
                            not isinstance(
                                variant_slug,
                                str,
                            )
                            or not variant_slug.strip()
                        ):
                            raise ValueError(
                                "Invalid variantSlug "
                                f"for variantId="
                                f"{variant_id_value}"
                            )

                        if (
                            not isinstance(
                                model_slug,
                                str,
                            )
                            or not model_slug.strip()
                        ):
                            raise ValueError(
                                "Invalid modelSlug "
                                f"for variantId="
                                f"{variant_id_value}"
                            )

                        if (
                            not isinstance(
                                brand_slug,
                                str,
                            )
                            or not brand_slug.strip()
                        ):
                            raise ValueError(
                                "Invalid brandSlug "
                                f"for variantId="
                                f"{variant_id_value}"
                            )

                        if (
                            not effective_refresh_existing
                            and await bikedekho_trim_specs_features_repository.exists_by_variant_id(
                                variant_id_value
                            )
                        ):
                            await scraper_job_repository.mark_skipped(
                                run_id=run_id,
                                job_id=job_id,
                                reason=(
                                    "Trim specs/features " "document already exists"
                                ),
                                result={
                                    "documentId": (f"variant:" f"{variant_id_value}"),
                                    "variantId": (variant_id_value),
                                },
                            )

                            await refresh_run_progress()

                            continue

                        response_data = await executor.fetch(
                            brand_slug=(brand_slug),
                            model_slug=(model_slug),
                            variant_slug=(variant_slug),
                            variant_id=(variant_id_value),
                        )

                        upsert_result = (
                            await (
                                bikedekho_trim_specs_features_repository.upsert_one(
                                    variant_record=(payload),
                                    response_data=(response_data),
                                    run_id=run_id,
                                )
                            )
                        )

                        await scraper_job_repository.mark_completed(
                            run_id=run_id,
                            job_id=job_id,
                            worker_id=worker_id,
                            result=(upsert_result.to_dict()),
                        )

                        async with aggregate_lock:
                            aggregate["written"] += 1

                            aggregate["inserted"] += upsert_result.inserted

                            aggregate["matched"] += upsert_result.matched

                            aggregate["modified"] += upsert_result.modified

                        await refresh_run_progress()

                        logger_service.info(
                            (
                                "BikeDekho trim "
                                "specs/features "
                                "completed: "
                                f"run_id={run_id}, "
                                f"job_id={job_id}, "
                                "brand="
                                f"{brand_slug}, "
                                "model="
                                f"{model_slug}, "
                                "variant="
                                f"{variant_slug}, "
                                "variant_id="
                                f"{variant_id_value}"
                            ),
                            context=("BikeDekhoTrimSpecsFeaturesCommand"),
                        )

                    except asyncio.CancelledError:
                        await _cancel_claimed_job_safely(
                            run_id=run_id,
                            job_id=job_id,
                        )
                        raise

                    except Exception as error:
                        retryable_error = _is_retryable_error(error)

                        http_status = _extract_http_status(error)

                        try:
                            await scraper_job_repository.mark_failed(
                                run_id=run_id,
                                job_id=job_id,
                                error=error,
                                retryable=(retryable_error),
                                http_status=(http_status),
                                worker_id=worker_id,
                            )

                            await refresh_run_progress()

                        except Exception as tracking_error:
                            logger_service.error(
                                (
                                    "Unable to mark "
                                    "BikeDekho trim "
                                    "specs/features "
                                    "job failed: "
                                    f"run_id={run_id}, "
                                    f"job_id={job_id}, "
                                    "error="
                                    f"{type(tracking_error).__name__}: "
                                    f"{tracking_error}"
                                ),
                                context=("BikeDekhoTrimSpecsFeaturesCommand"),
                            )

                        logger_service.error(
                            (
                                "BikeDekho trim "
                                "specs/features "
                                "failed: "
                                f"run_id={run_id}, "
                                "brand="
                                f"{brand_slug}, "
                                "model="
                                f"{model_slug}, "
                                "variant="
                                f"{variant_slug}, "
                                "variant_id="
                                f"{variant_id_value}, "
                                "retryable="
                                f"{retryable_error}, "
                                "http_status="
                                f"{http_status}, "
                                "error="
                                f"{type(error).__name__}: "
                                f"{error}"
                            ),
                            context=("BikeDekhoTrimSpecsFeaturesCommand"),
                        )

            worker_tasks = [
                asyncio.create_task(
                    worker(worker_number),
                    name=("bikedekho-trim-specs-features-worker-" f"{worker_number}"),
                )
                for worker_number in range(
                    1,
                    normalized_workers + 1,
                )
            ]

            try:
                await asyncio.gather(*worker_tasks)
            except asyncio.CancelledError:
                for task in worker_tasks:
                    task.cancel()

                await asyncio.gather(
                    *worker_tasks,
                    return_exceptions=True,
                )

                raise

            client_metrics = client.metrics_snapshot()

        final_job_counts = await scraper_job_repository.count_by_status(
            run_id=run_id,
        )

        aggregate_snapshot = await get_aggregate_snapshot()

        progress = _build_progress(
            job_counts=final_job_counts,
            written=aggregate_snapshot["written"],
            inserted=aggregate_snapshot["inserted"],
            matched=aggregate_snapshot["matched"],
            modified=aggregate_snapshot["modified"],
        )

        finished_run = await scraper_run_repository.mark_completed(
            run_id,
            progress=progress,
        )

        logger_service.info(
            (
                "BikeDekho trim "
                "specs/features scraping "
                "completed: "
                f"run_id={run_id}, "
                f"status={finished_run.status}, "
                "successful="
                f"{final_job_counts.completed}, "
                "failed="
                f"{final_job_counts.failed}, "
                "skipped="
                f"{final_job_counts.skipped}, "
                "written="
                f"{aggregate_snapshot['written']}"
            ),
            context=("BikeDekhoTrimSpecsFeaturesCommand"),
        )

        return {
            "command": COMMAND_NAME,
            "runId": run_id,
            "status": finished_run.status,
            "mode": mode,
            "brand": normalized_brand,
            "model": normalized_model,
            "modelId": normalized_model_id,
            "variant": normalized_variant,
            "variantId": normalized_variant_id,
            "maxJobs": normalized_max_jobs,
            "workers": normalized_workers,
            "requestsPerSecond": (normalized_requests_per_second),
            "pauseEveryRequests": (normalized_pause_every_requests),
            "pauseSeconds": (normalized_pause_seconds),
            "refreshExisting": (effective_refresh_existing),
            "resumed": (normalized_resume_run_id is not None),
            "failedOnly": failed_only,
            "retryTerminalFailures": (retry_terminal_failures),
            "jobsCreated": jobs_created,
            "jobsExisting": jobs_existing,
            "jobsRequeued": requeued_jobs,
            "staleJobsRequeued": (stale_jobs_requeued),
            "successfulVariants": (final_job_counts.completed),
            "failedVariants": (final_job_counts.failed),
            "skippedVariants": (final_job_counts.skipped),
            "cancelledVariants": (final_job_counts.cancelled),
            "written": aggregate_snapshot["written"],
            "inserted": aggregate_snapshot["inserted"],
            "matched": aggregate_snapshot["matched"],
            "modified": aggregate_snapshot["modified"],
            "clientMetrics": client_metrics,
        }

    except asyncio.CancelledError as error:
        if run_created:
            try:
                job_counts = await scraper_job_repository.count_by_status(
                    run_id=run_id,
                )

                aggregate_snapshot = await get_aggregate_snapshot()

                progress = _build_progress(
                    job_counts=job_counts,
                    written=aggregate_snapshot["written"],
                    inserted=aggregate_snapshot["inserted"],
                    matched=aggregate_snapshot["matched"],
                    modified=aggregate_snapshot["modified"],
                )

                await scraper_run_repository.mark_interrupted(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=(
                        "BikeDekho trim " "specs/features " "command interrupted"
                    ),
                    stop_http_status=(_extract_http_status(error)),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark "
                        "BikeDekho trim "
                        "specs/features run "
                        "as interrupted: "
                        f"{type(tracking_error).__name__}: "
                        f"{tracking_error}"
                    ),
                    context=("BikeDekhoTrimSpecsFeaturesCommand"),
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
                    inserted=aggregate_snapshot["inserted"],
                    matched=aggregate_snapshot["matched"],
                    modified=aggregate_snapshot["modified"],
                )

                await scraper_run_repository.mark_failed(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("BikeDekho trim " "specs/features " "scraping failed"),
                    stop_http_status=(_extract_http_status(error)),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark "
                        "BikeDekho trim "
                        "specs/features run "
                        "as failed: "
                        f"{type(tracking_error).__name__}: "
                        f"{tracking_error}"
                    ),
                    context=("BikeDekhoTrimSpecsFeaturesCommand"),
                )

        logger_service.error(
            (
                "BikeDekho trim "
                "specs/features scraping failed: "
                f"{type(error).__name__}: "
                f"{error}"
            ),
            context=("BikeDekhoTrimSpecsFeaturesCommand"),
        )

        raise

    finally:
        await mongo_connection.close()
