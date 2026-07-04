from __future__ import annotations

import asyncio
import re
from typing import Any

from pymongo.errors import PyMongoError

from src.clients.client import (
    ExternalClientError,
    ExternalResponseError,
)
from src.databases.mongodb import (
    mongo_connection,
)
from src.external.executors.carwale.cities import (
    scrape_carwale_cities,
)
from src.external.executors.carwale.client_factory import (
    create_carwale_client,
)
from src.logger.logger import logger_service
from src.models.scraper_job import (
    ScraperJob,
)
from src.models.scraper_run import (
    ScraperRun,
)
from src.repositories.carwale_city_repository import (
    carwale_city_repository,
)
from src.repositories.scraper_job_repository import (
    scraper_job_repository,
)
from src.repositories.scraper_run_repository import (
    scraper_run_repository,
)

COMMAND_NAME = "carwale-cities"
SOURCE_NAME = "carwale"
RESOURCE_NAME = "cities"
JOB_TYPE = "fetch-cities"

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


def _validate_min_request_interval(
    value: float,
) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(
            value,
            (int, float),
        )
        or value < 0
    ):
        raise ValueError("min_request_interval must be a non-negative number")

    return float(value)


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


def _build_progress(
    *,
    total_jobs: int,
    pending_jobs: int,
    running_jobs: int,
    completed_jobs: int,
    failed_jobs: int,
    total_cities: int,
    matched: int,
    modified: int,
    inserted: int,
) -> dict[str, int]:
    return {
        "produced": total_jobs,
        "skipped": 0,
        "successful": completed_jobs,
        "failed": failed_jobs,
        "written": total_cities,
        "inserted": inserted,
        "matched": matched,
        "modified": modified,
        "failureRecordsWritten": failed_jobs,
        "totalJobs": total_jobs,
        "pendingJobs": pending_jobs,
        "runningJobs": running_jobs,
        "completedJobs": completed_jobs,
        "failedJobs": failed_jobs,
        "skippedJobs": 0,
        "cancelledJobs": 0,
    }


async def run_carwale_cities(
    *,
    min_request_interval: float = 2.0,
    show_request: bool = False,
) -> dict[str, Any]:
    normalized_min_request_interval = _validate_min_request_interval(
        min_request_interval
    )

    if not isinstance(
        show_request,
        bool,
    ):
        raise ValueError("show_request must be a boolean")

    run = ScraperRun.create(
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        command=COMMAND_NAME,
        mode="full",
        filters={},
        settings={
            "minRequestInterval": (normalized_min_request_interval),
            "showRequest": show_request,
        },
        metadata={
            "storage": "mongodb",
            "targetCollection": ("carwale_cities"),
        },
    )

    run_id = run.run_id
    run_created = False
    claimed_job_id: str | None = None
    worker_id = "carwale-cities-worker-1"

    try:
        await mongo_connection.connect()

        await scraper_run_repository.create(run)

        run_created = True

        job = ScraperJob.create(
            run_id=run_id,
            job_id="cities:all",
            source=SOURCE_NAME,
            resource=RESOURCE_NAME,
            job_type=JOB_TYPE,
            item_key="all-cities",
            payload={
                "minRequestInterval": (normalized_min_request_interval),
            },
            metadata={
                "targetCollection": ("carwale_cities"),
            },
            priority=100,
            max_attempts=1,
        )

        await scraper_job_repository.create(job)

        await scraper_run_repository.mark_started(run_id)

        claimed_job = await scraper_job_repository.claim_next(
            run_id=run_id,
            worker_id=worker_id,
            resource=RESOURCE_NAME,
            job_type=JOB_TYPE,
        )

        if claimed_job is None:
            raise RuntimeError("Unable to claim the CarWale cities job")

        claimed_job_id = claimed_job.job_id

        logger_service.info(
            (
                "Starting CarWale cities scraping: "
                f"run_id={run_id}, "
                "mode=single-request, "
                "minimum_request_interval="
                f"{normalized_min_request_interval:.2f}s"
            ),
            context="CarWaleCitiesCommand",
        )

        with create_carwale_client(
            workers=1,
            min_request_interval=(normalized_min_request_interval),
        ) as client:
            cities = scrape_carwale_cities(
                client=client,
                show_request=show_request,
            )

        upsert_result = await carwale_city_repository.bulk_upsert(
            cities=cities,
            run_id=run_id,
        )

        await scraper_job_repository.mark_completed(
            run_id=run_id,
            job_id=claimed_job_id,
            worker_id=worker_id,
            result={
                "received": upsert_result.received,
                "processed": upsert_result.processed,
                "matched": upsert_result.matched,
                "modified": upsert_result.modified,
                "inserted": upsert_result.inserted,
                "collection": "carwale_cities",
            },
        )

        job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

        progress = _build_progress(
            total_jobs=job_counts.total,
            pending_jobs=job_counts.pending,
            running_jobs=job_counts.running,
            completed_jobs=job_counts.completed,
            failed_jobs=job_counts.failed,
            total_cities=upsert_result.processed,
            matched=upsert_result.matched,
            modified=upsert_result.modified,
            inserted=upsert_result.inserted,
        )

        finished_run = await scraper_run_repository.mark_completed(
            run_id,
            progress=progress,
        )

        logger_service.info(
            (
                "CarWale cities scraping completed: "
                f"run_id={run_id}, "
                f"status={finished_run.status}, "
                f"total_cities={upsert_result.processed}, "
                f"inserted={upsert_result.inserted}, "
                f"modified={upsert_result.modified}"
            ),
            context="CarWaleCitiesCommand",
        )

        return {
            "command": COMMAND_NAME,
            "runId": run_id,
            "status": finished_run.status,
            "totalCities": upsert_result.processed,
            "received": upsert_result.received,
            "processed": upsert_result.processed,
            "matched": upsert_result.matched,
            "modified": upsert_result.modified,
            "inserted": upsert_result.inserted,
            "collection": "carwale_cities",
            "jobs": job_counts.to_dict(),
        }

    except (
        KeyboardInterrupt,
        asyncio.CancelledError,
    ) as error:
        if run_created:
            try:
                if claimed_job_id is not None:
                    current_job = await scraper_job_repository.get(
                        run_id=run_id,
                        job_id=claimed_job_id,
                    )

                    if current_job is not None and current_job.status in {
                        "pending",
                        "running",
                    }:
                        await scraper_job_repository.mark_cancelled(
                            run_id=run_id,
                            job_id=claimed_job_id,
                            reason=("CarWale cities command interrupted"),
                        )

                job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

                progress = _build_progress(
                    total_jobs=job_counts.total,
                    pending_jobs=job_counts.pending,
                    running_jobs=job_counts.running,
                    completed_jobs=job_counts.completed,
                    failed_jobs=job_counts.failed,
                    total_cities=0,
                    matched=0,
                    modified=0,
                    inserted=0,
                )

                await scraper_run_repository.mark_interrupted(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("CarWale cities command interrupted"),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarWale cities "
                        "run as interrupted: "
                        f"{type(tracking_error).__name__}: "
                        f"{tracking_error}"
                    ),
                    context="CarWaleCitiesCommand",
                )

        raise

    except Exception as error:
        if run_created:
            try:
                if claimed_job_id is not None:
                    current_job = await scraper_job_repository.get(
                        run_id=run_id,
                        job_id=claimed_job_id,
                    )

                    if current_job is not None and current_job.status == "running":
                        await scraper_job_repository.mark_failed(
                            run_id=run_id,
                            job_id=claimed_job_id,
                            error=error,
                            retryable=(_is_retryable_error(error)),
                            http_status=(_extract_http_status(error)),
                            worker_id=worker_id,
                        )

                job_counts = await scraper_job_repository.count_by_status(run_id=run_id)

                progress = _build_progress(
                    total_jobs=job_counts.total,
                    pending_jobs=job_counts.pending,
                    running_jobs=job_counts.running,
                    completed_jobs=job_counts.completed,
                    failed_jobs=job_counts.failed,
                    total_cities=0,
                    matched=0,
                    modified=0,
                    inserted=0,
                )

                await scraper_run_repository.mark_failed(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("CarWale cities scraping failed"),
                    stop_http_status=(_extract_http_status(error)),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarWale cities "
                        "run as failed: "
                        f"{type(tracking_error).__name__}: "
                        f"{tracking_error}"
                    ),
                    context="CarWaleCitiesCommand",
                )

        logger_service.error(
            (f"CarWale cities scraping failed: {type(error).__name__}: {error}"),
            context="CarWaleCitiesCommand",
        )

        raise

    finally:
        await mongo_connection.close()
