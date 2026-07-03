from __future__ import annotations

import asyncio
import re
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
from src.external.executors.carwale.brands import (
    CarWaleBrandsExecutor,
)
from src.logger.logger import logger_service
from src.models.scraper_job import (
    ScraperJob,
)
from src.models.scraper_run import (
    ScraperRun,
)
from src.repositories.carwale_brand_repository import (
    carwale_brand_repository,
)
from src.repositories.scraper_job_repository import (
    JobStatusCounts,
    scraper_job_repository,
)
from src.repositories.scraper_run_repository import (
    scraper_run_repository,
)

COMMAND_NAME = "carwale-brands"
SOURCE_NAME = "carwale"
RESOURCE_NAME = "brands"

BRANDS_JOB_ID = "brand:all"
BRANDS_ITEM_KEY = "brand:all"
BRANDS_WORKER_ID = "carwale-brands-worker-1"

HTTP_STATUS_PATTERN = re.compile(
    r"(?:status|status_code|http_status)" r"\s*[=:]\s*(\d{3})",
    re.IGNORECASE,
)


def _validate_positive_integer(
    value: int,
    *,
    field_name: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")

    return value


def _extract_http_status(
    error: BaseException,
) -> int | None:
    status_code = getattr(
        error,
        "status_code",
        None,
    )

    if (
        isinstance(status_code, int)
        and not isinstance(status_code, bool)
        and 100 <= status_code <= 599
    ):
        return status_code

    match = HTTP_STATUS_PATTERN.search(str(error))

    if match is None:
        return None

    try:
        parsed_status = int(match.group(1))
    except ValueError:
        return None

    if not 100 <= parsed_status <= 599:
        return None

    return parsed_status


def _is_retryable_error(
    error: BaseException,
) -> bool:
    if isinstance(
        error,
        ExternalClientError,
    ):
        return True

    http_status = _extract_http_status(error)

    return http_status in {
        408,
        425,
        429,
        500,
        502,
        503,
        504,
    }


def _build_progress(
    *,
    job_counts: JobStatusCounts,
    brands_count: int,
    matched: int,
    modified: int,
    inserted: int,
) -> dict[str, int]:
    return {
        "produced": job_counts.total,
        "skipped": job_counts.skipped,
        "successful": job_counts.completed,
        "failed": job_counts.failed,
        "written": brands_count,
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


async def _mark_job_failed_safely(
    *,
    run_id: str,
    error: BaseException,
) -> None:
    try:
        current_job = await scraper_job_repository.get(
            run_id=run_id,
            job_id=BRANDS_JOB_ID,
        )

        if current_job is None or current_job.status != "running":
            return

        await scraper_job_repository.mark_failed(
            run_id=run_id,
            job_id=BRANDS_JOB_ID,
            error=error,
            retryable=_is_retryable_error(error),
            http_status=_extract_http_status(error),
            worker_id=BRANDS_WORKER_ID,
        )

    except Exception as tracking_error:
        logger_service.error(
            ("Unable to mark CarWale brands job as failed"),
            exception=tracking_error,
            context="CarWaleBrandsCommand",
        )


async def _mark_job_cancelled_safely(
    *,
    run_id: str,
    reason: str,
) -> None:
    try:
        current_job = await scraper_job_repository.get(
            run_id=run_id,
            job_id=BRANDS_JOB_ID,
        )

        if current_job is None or current_job.status not in {
            "pending",
            "running",
        }:
            return

        await scraper_job_repository.mark_cancelled(
            run_id=run_id,
            job_id=BRANDS_JOB_ID,
            reason=reason,
        )

    except Exception as tracking_error:
        logger_service.error(
            ("Unable to mark CarWale brands job as cancelled"),
            exception=tracking_error,
            context="CarWaleBrandsCommand",
        )


async def run_carwale_brands(
    *,
    page_id: int = 2,
    platform_id: int = 1,
) -> dict[str, Any]:
    normalized_page_id = _validate_positive_integer(
        page_id,
        field_name="page_id",
    )

    normalized_platform_id = _validate_positive_integer(
        platform_id,
        field_name="platform_id",
    )

    run = ScraperRun.create(
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        command=COMMAND_NAME,
        mode="full",
        filters={},
        settings={
            "pageId": normalized_page_id,
            "platformId": normalized_platform_id,
            "workers": 1,
        },
        metadata={
            "storage": "mongodb",
            "collection": "carwale_brands",
        },
    )

    run_id = run.run_id

    brands_count = 0
    matched = 0
    modified = 0
    inserted = 0

    try:
        await mongo_connection.connect()

        await scraper_run_repository.create(run)

        job = ScraperJob.create(
            run_id=run_id,
            job_id=BRANDS_JOB_ID,
            source=SOURCE_NAME,
            resource=RESOURCE_NAME,
            job_type="fetch-brands",
            item_key=BRANDS_ITEM_KEY,
            payload={
                "pageId": normalized_page_id,
                "platformId": normalized_platform_id,
            },
            metadata={
                "collection": "carwale_brands",
            },
            priority=100,
            max_attempts=3,
        )

        await scraper_job_repository.create(job)

        await scraper_run_repository.mark_started(run_id)

        claimed_job = await scraper_job_repository.claim_next(
            run_id=run_id,
            worker_id=BRANDS_WORKER_ID,
            resource=RESOURCE_NAME,
            job_type="fetch-brands",
        )

        if claimed_job is None:
            raise RuntimeError("Unable to claim the CarWale brands job")

        logger_service.info(
            (
                "Starting CarWale brands scraping: "
                f"run_id={run_id}, "
                f"page_id={normalized_page_id}, "
                f"platform_id={normalized_platform_id}"
            ),
            context="CarWaleBrandsCommand",
        )

        async with create_carwale_async_client(
            concurrency=1,
            requests_per_second=1.0,
        ) as client:
            executor = CarWaleBrandsExecutor(
                client=client,
            )

            brands = await executor.execute(
                page_id=normalized_page_id,
                platform_id=normalized_platform_id,
            )

            upsert_result = await carwale_brand_repository.bulk_upsert(
                brands,
                run_id=run_id,
            )

            client_metrics = client.metrics_snapshot()

            status_counts = client_metrics.get("status_counts")

            if isinstance(status_counts, dict):
                client_metrics["status_counts"] = {
                    str(status_code): count
                    for status_code, count in status_counts.items()
                }

        brands_count = upsert_result.processed
        matched = upsert_result.matched
        modified = upsert_result.modified
        inserted = upsert_result.inserted

        job_result = {
            "brandsReceived": (upsert_result.received),
            "brandsProcessed": (upsert_result.processed),
            "matched": upsert_result.matched,
            "modified": upsert_result.modified,
            "inserted": upsert_result.inserted,
            "httpMetrics": client_metrics,
        }

        await scraper_job_repository.mark_completed(
            run_id=run_id,
            job_id=BRANDS_JOB_ID,
            result=job_result,
            worker_id=BRANDS_WORKER_ID,
        )

        job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

        progress = _build_progress(
            job_counts=job_counts,
            brands_count=brands_count,
            matched=matched,
            modified=modified,
            inserted=inserted,
        )

        finished_run = await scraper_run_repository.mark_completed(
            run_id,
            progress=progress,
        )

        logger_service.info(
            (
                "CarWale brands scraping completed: "
                f"run_id={run_id}, "
                f"brands={brands_count}, "
                f"inserted={inserted}, "
                f"matched={matched}, "
                f"modified={modified}"
            ),
            context="CarWaleBrandsCommand",
        )

        return {
            "command": COMMAND_NAME,
            "runId": run_id,
            "status": finished_run.status,
            "pageId": normalized_page_id,
            "platformId": normalized_platform_id,
            "collection": "carwale_brands",
            "brandsCount": brands_count,
            "matched": matched,
            "modified": modified,
            "inserted": inserted,
            "httpMetrics": client_metrics,
            "jobs": job_counts.to_dict(),
        }

    except (
        KeyboardInterrupt,
        asyncio.CancelledError,
    ) as error:
        await _mark_job_cancelled_safely(
            run_id=run_id,
            reason="Command interrupted",
        )

        try:
            job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

            await scraper_run_repository.mark_interrupted(
                run_id,
                progress=_build_progress(
                    job_counts=job_counts,
                    brands_count=brands_count,
                    matched=matched,
                    modified=modified,
                    inserted=inserted,
                ),
                error=error,
                stop_reason="Command interrupted",
            )

        except Exception as tracking_error:
            logger_service.error(
                ("Unable to mark CarWale brands run as interrupted"),
                exception=tracking_error,
                context="CarWaleBrandsCommand",
            )

        raise

    except Exception as error:
        await _mark_job_failed_safely(
            run_id=run_id,
            error=error,
        )

        try:
            job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

            await scraper_run_repository.mark_failed(
                run_id,
                progress=_build_progress(
                    job_counts=job_counts,
                    brands_count=brands_count,
                    matched=matched,
                    modified=modified,
                    inserted=inserted,
                ),
                error=error,
                stop_reason=("CarWale brands scraping failed"),
                stop_http_status=(_extract_http_status(error)),
            )

        except Exception as tracking_error:
            logger_service.error(
                ("Unable to mark CarWale brands run as failed"),
                exception=tracking_error,
                context="CarWaleBrandsCommand",
            )

        logger_service.error(
            (f"CarWale brands scraping failed: {type(error).__name__}: {error}"),
            context="CarWaleBrandsCommand",
        )

        raise

    finally:
        await mongo_connection.close()
