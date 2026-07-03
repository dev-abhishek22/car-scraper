from __future__ import annotations

from collections.abc import AsyncIterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from pymongo import ReturnDocument, UpdateOne
from pymongo.results import BulkWriteResult

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.scraper_job import (
    ScraperJob,
    ScraperJobStatus,
)

SCRAPER_JOBS_COLLECTION = "scraper_jobs"

SCRAPER_JOB_STATUSES: tuple[ScraperJobStatus, ...] = (
    "pending",
    "running",
    "completed",
    "failed",
    "skipped",
    "cancelled",
)


@dataclass(frozen=True, slots=True)
class BulkJobCreateResult:
    received: int
    processed: int
    existing: int
    inserted: int


@dataclass(frozen=True, slots=True)
class JobStatusCounts:
    total: int
    pending: int
    running: int
    completed: int
    failed: int
    skipped: int
    cancelled: int

    def to_dict(self) -> dict[str, int]:
        return {
            "totalJobs": self.total,
            "pendingJobs": self.pending,
            "runningJobs": self.running,
            "completedJobs": self.completed,
            "failedJobs": self.failed,
            "skippedJobs": self.skipped,
            "cancelledJobs": self.cancelled,
        }


class ScraperJobNotFoundError(LookupError):
    """Raised when a scraper job cannot be found."""


class ScraperJobStateError(ValueError):
    """Raised when a scraper job has an invalid lifecycle state."""


class ScraperJobRepository:
    def __init__(
        self,
        connection: MongoConnection = mongo_connection,
    ) -> None:
        self._connection = connection

    @staticmethod
    def _normalize_run_id(
        run_id: str,
    ) -> str:
        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        return normalized_run_id

    @staticmethod
    def _normalize_job_id(
        job_id: str,
    ) -> str:
        normalized_job_id = job_id.strip()

        if not normalized_job_id:
            raise ValueError("job_id cannot be empty")

        return normalized_job_id

    @staticmethod
    def _normalize_worker_id(
        worker_id: str,
    ) -> str:
        normalized_worker_id = worker_id.strip()

        if not normalized_worker_id:
            raise ValueError("worker_id cannot be empty")

        return normalized_worker_id

    @staticmethod
    def _normalize_optional_text(
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        normalized_value = value.strip()

        return normalized_value or None

    @staticmethod
    def _normalize_http_status(
        http_status: int | None,
    ) -> int | None:
        if http_status is None:
            return None

        if (
            isinstance(http_status, bool)
            or not isinstance(http_status, int)
            or not 100 <= http_status <= 599
        ):
            raise ValueError("http_status must be an integer between 100 and 599")

        return http_status

    @staticmethod
    def _normalize_status(
        status: str,
    ) -> ScraperJobStatus:
        normalized_status = status.strip().lower()

        if normalized_status not in SCRAPER_JOB_STATUSES:
            raise ValueError(f"Unsupported scraper job status: {status!r}")

        return normalized_status  # type: ignore[return-value]

    @classmethod
    def _build_document_id(
        cls,
        *,
        run_id: str,
        job_id: str,
    ) -> str:
        return ScraperJob.build_document_id(
            run_id=cls._normalize_run_id(run_id),
            job_id=cls._normalize_job_id(job_id),
        )

    async def create(
        self,
        job: ScraperJob,
    ) -> ScraperJob:
        result = await self.create_many([job])

        if result.inserted == 0:
            existing_job = await self.require(
                run_id=job.run_id,
                job_id=job.job_id,
            )

            return existing_job

        return job

    async def create_many(
        self,
        jobs: Sequence[ScraperJob],
    ) -> BulkJobCreateResult:
        if not jobs:
            return BulkJobCreateResult(
                received=0,
                processed=0,
                existing=0,
                inserted=0,
            )

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        deduplicated_jobs: dict[str, ScraperJob] = {}

        for job in jobs:
            deduplicated_jobs[job.document_id] = job

        operations: list[UpdateOne] = []

        for job in deduplicated_jobs.values():
            operations.append(
                UpdateOne(
                    {
                        "_id": job.document_id,
                    },
                    {
                        "$setOnInsert": (job.to_mongo_document()),
                    },
                    upsert=True,
                )
            )

        result: BulkWriteResult = await collection.bulk_write(
            operations,
            ordered=False,
        )

        return BulkJobCreateResult(
            received=len(jobs),
            processed=len(operations),
            existing=result.matched_count,
            inserted=result.upserted_count,
        )

    async def get(
        self,
        *,
        run_id: str,
        job_id: str,
    ) -> ScraperJob | None:
        document_id = self._build_document_id(
            run_id=run_id,
            job_id=job_id,
        )

        return await self.get_by_document_id(document_id)

    async def get_by_document_id(
        self,
        document_id: str,
    ) -> ScraperJob | None:
        normalized_document_id = document_id.strip()

        if not normalized_document_id:
            raise ValueError("document_id cannot be empty")

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": normalized_document_id,
            }
        )

        if document is None:
            return None

        return ScraperJob.model_validate(document)

    async def require(
        self,
        *,
        run_id: str,
        job_id: str,
    ) -> ScraperJob:
        job = await self.get(
            run_id=run_id,
            job_id=job_id,
        )

        if job is None:
            raise ScraperJobNotFoundError(
                f"Scraper job was not found: run_id={run_id}, job_id={job_id}"
            )

        return job

    async def claim_next(
        self,
        *,
        run_id: str,
        worker_id: str,
        resource: str | None = None,
        job_type: str | None = None,
    ) -> ScraperJob | None:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_worker_id = self._normalize_worker_id(worker_id)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        query: dict[str, Any] = {
            "runId": normalized_run_id,
            "status": "pending",
        }

        if resource is not None:
            normalized_resource = resource.strip().lower()

            if not normalized_resource:
                raise ValueError("resource cannot be empty")

            query["resource"] = normalized_resource

        if job_type is not None:
            normalized_job_type = job_type.strip().lower()

            if not normalized_job_type:
                raise ValueError("job_type cannot be empty")

            query["jobType"] = normalized_job_type

        current_time = datetime.now(timezone.utc)

        document = await collection.find_one_and_update(
            query,
            {
                "$set": {
                    "status": "running",
                    "workerId": normalized_worker_id,
                    "startedAt": current_time,
                    "lastHeartbeatAt": current_time,
                    "updatedAt": current_time,
                    "completedAt": None,
                    "failedAt": None,
                    "skippedAt": None,
                    "cancelledAt": None,
                    "resolvedAt": None,
                },
                "$unset": {
                    "errorType": "",
                    "errorMessage": "",
                    "httpStatus": "",
                    "skipReason": "",
                    "cancelReason": "",
                },
                "$inc": {
                    "attempts": 1,
                },
            },
            sort=[
                (
                    "priority",
                    -1,
                ),
                (
                    "queuedAt",
                    1,
                ),
                (
                    "_id",
                    1,
                ),
            ],
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            return None

        return ScraperJob.model_validate(document)

    async def heartbeat(
        self,
        *,
        run_id: str,
        job_id: str,
        worker_id: str,
    ) -> None:
        document_id = self._build_document_id(
            run_id=run_id,
            job_id=job_id,
        )

        normalized_worker_id = self._normalize_worker_id(worker_id)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        result = await collection.update_one(
            {
                "_id": document_id,
                "status": "running",
                "workerId": normalized_worker_id,
            },
            {
                "$set": {
                    "lastHeartbeatAt": current_time,
                    "updatedAt": current_time,
                }
            },
        )

        if result.matched_count == 0:
            existing_job = await self.get_by_document_id(document_id)

            if existing_job is None:
                raise ScraperJobNotFoundError(
                    f"Scraper job was not found: {document_id}"
                )

            raise ScraperJobStateError(
                "Cannot update scraper job heartbeat: "
                f"status={existing_job.status!r}, "
                f"worker_id={existing_job.worker_id!r}"
            )

    async def mark_completed(
        self,
        *,
        run_id: str,
        job_id: str,
        result: Mapping[str, Any] | None = None,
        worker_id: str | None = None,
    ) -> ScraperJob:
        document_id = self._build_document_id(
            run_id=run_id,
            job_id=job_id,
        )

        existing_job = await self.get_by_document_id(document_id)

        if existing_job is None:
            raise ScraperJobNotFoundError(f"Scraper job was not found: {document_id}")

        query: dict[str, Any] = {
            "_id": document_id,
            "status": "running",
        }

        if worker_id is not None:
            query["workerId"] = self._normalize_worker_id(worker_id)

        current_time = datetime.now(timezone.utc)

        resolved_at = (
            current_time
            if existing_job.first_failed_at is not None
            else existing_job.resolved_at
        )

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        document = await collection.find_one_and_update(
            query,
            {
                "$set": {
                    "status": "completed",
                    "result": dict(result or {}),
                    "completedAt": current_time,
                    "lastHeartbeatAt": current_time,
                    "resolvedAt": resolved_at,
                    "updatedAt": current_time,
                },
                "$unset": {
                    "failedAt": "",
                    "skippedAt": "",
                    "cancelledAt": "",
                    "errorType": "",
                    "errorMessage": "",
                    "httpStatus": "",
                    "skipReason": "",
                    "cancelReason": "",
                },
            },
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            latest_job = await self.get_by_document_id(document_id)

            if latest_job is None:
                raise ScraperJobNotFoundError(
                    f"Scraper job was not found: {document_id}"
                )

            raise ScraperJobStateError(
                "Scraper job cannot be completed because "
                f"its status is {latest_job.status!r}"
            )

        return ScraperJob.model_validate(document)

    async def mark_failed(
        self,
        *,
        run_id: str,
        job_id: str,
        error: BaseException,
        retryable: bool,
        http_status: int | None = None,
        result: Mapping[str, Any] | None = None,
        worker_id: str | None = None,
    ) -> ScraperJob:
        document_id = self._build_document_id(
            run_id=run_id,
            job_id=job_id,
        )

        normalized_http_status = self._normalize_http_status(http_status)

        existing_job = await self.get_by_document_id(document_id)

        if existing_job is None:
            raise ScraperJobNotFoundError(f"Scraper job was not found: {document_id}")

        query: dict[str, Any] = {
            "_id": document_id,
            "status": "running",
        }

        if worker_id is not None:
            query["workerId"] = self._normalize_worker_id(worker_id)

        current_time = datetime.now(timezone.utc)

        error_message = str(error).strip()

        if not error_message:
            error_message = type(error).__name__

        first_failed_at = existing_job.first_failed_at or current_time

        update_fields: dict[str, Any] = {
            "status": "failed",
            "retryable": retryable,
            "errorType": type(error).__name__,
            "errorMessage": error_message,
            "httpStatus": normalized_http_status,
            "failedAt": current_time,
            "firstFailedAt": first_failed_at,
            "lastFailedAt": current_time,
            "lastHeartbeatAt": current_time,
            "resolvedAt": None,
            "updatedAt": current_time,
        }

        if result is not None:
            update_fields["result"] = dict(result)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        document = await collection.find_one_and_update(
            query,
            {
                "$set": update_fields,
                "$unset": {
                    "completedAt": "",
                    "skippedAt": "",
                    "cancelledAt": "",
                    "skipReason": "",
                    "cancelReason": "",
                },
            },
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            latest_job = await self.get_by_document_id(document_id)

            if latest_job is None:
                raise ScraperJobNotFoundError(
                    f"Scraper job was not found: {document_id}"
                )

            raise ScraperJobStateError(
                "Scraper job cannot be marked failed because "
                f"its status is {latest_job.status!r}"
            )

        return ScraperJob.model_validate(document)

    async def mark_skipped(
        self,
        *,
        run_id: str,
        job_id: str,
        reason: str,
        result: Mapping[str, Any] | None = None,
    ) -> ScraperJob:
        document_id = self._build_document_id(
            run_id=run_id,
            job_id=job_id,
        )

        normalized_reason = self._normalize_optional_text(reason)

        if normalized_reason is None:
            raise ValueError("reason cannot be empty")

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        document = await collection.find_one_and_update(
            {
                "_id": document_id,
                "status": {
                    "$in": [
                        "pending",
                        "running",
                    ]
                },
            },
            {
                "$set": {
                    "status": "skipped",
                    "skipReason": normalized_reason,
                    "result": dict(result or {}),
                    "skippedAt": current_time,
                    "updatedAt": current_time,
                },
                "$unset": {
                    "completedAt": "",
                    "failedAt": "",
                    "cancelledAt": "",
                    "errorType": "",
                    "errorMessage": "",
                    "httpStatus": "",
                    "cancelReason": "",
                },
            },
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            existing_job = await self.get_by_document_id(document_id)

            if existing_job is None:
                raise ScraperJobNotFoundError(
                    f"Scraper job was not found: {document_id}"
                )

            raise ScraperJobStateError(
                "Scraper job cannot be skipped because "
                f"its status is {existing_job.status!r}"
            )

        return ScraperJob.model_validate(document)

    async def mark_cancelled(
        self,
        *,
        run_id: str,
        job_id: str,
        reason: str | None = None,
    ) -> ScraperJob:
        document_id = self._build_document_id(
            run_id=run_id,
            job_id=job_id,
        )

        normalized_reason = self._normalize_optional_text(reason)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        update_fields: dict[str, Any] = {
            "status": "cancelled",
            "cancelledAt": current_time,
            "updatedAt": current_time,
        }

        unset_fields: dict[str, str] = {
            "completedAt": "",
            "failedAt": "",
            "skippedAt": "",
            "skipReason": "",
        }

        if normalized_reason is not None:
            update_fields["cancelReason"] = normalized_reason
        else:
            unset_fields["cancelReason"] = ""

        document = await collection.find_one_and_update(
            {
                "_id": document_id,
                "status": {
                    "$in": [
                        "pending",
                        "running",
                    ]
                },
            },
            {
                "$set": update_fields,
                "$unset": unset_fields,
            },
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            existing_job = await self.get_by_document_id(document_id)

            if existing_job is None:
                raise ScraperJobNotFoundError(
                    f"Scraper job was not found: {document_id}"
                )

            raise ScraperJobStateError(
                "Scraper job cannot be cancelled because "
                f"its status is {existing_job.status!r}"
            )

        return ScraperJob.model_validate(document)

    async def requeue_failed(
        self,
        *,
        run_id: str,
        include_non_retryable: bool = False,
        ignore_max_attempts: bool = False,
        reset_attempts: bool = False,
    ) -> int:
        normalized_run_id = self._normalize_run_id(run_id)

        query: dict[str, Any] = {
            "runId": normalized_run_id,
            "status": "failed",
        }

        if not include_non_retryable:
            query["retryable"] = True

        if not ignore_max_attempts:
            query["$expr"] = {
                "$lt": [
                    "$attempts",
                    "$maxAttempts",
                ]
            }

        current_time = datetime.now(timezone.utc)

        set_fields: dict[str, Any] = {
            "status": "pending",
            "queuedAt": current_time,
            "updatedAt": current_time,
            "workerId": None,
            "startedAt": None,
            "lastHeartbeatAt": None,
            "resolvedAt": None,
        }

        if reset_attempts:
            set_fields["attempts"] = 0

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        result = await collection.update_many(
            query,
            {
                "$set": set_fields,
                "$unset": {
                    "completedAt": "",
                    "failedAt": "",
                    "skippedAt": "",
                    "cancelledAt": "",
                    "skipReason": "",
                    "cancelReason": "",
                },
            },
        )

        return result.modified_count

    async def requeue_stale_running(
        self,
        *,
        run_id: str,
        stale_after_seconds: float,
    ) -> int:
        normalized_run_id = self._normalize_run_id(run_id)

        if (
            isinstance(stale_after_seconds, bool)
            or not isinstance(
                stale_after_seconds,
                (int, float),
            )
            or stale_after_seconds <= 0
        ):
            raise ValueError("stale_after_seconds must be greater than zero")

        current_time = datetime.now(timezone.utc)

        stale_before = current_time - timedelta(seconds=float(stale_after_seconds))

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        result = await collection.update_many(
            {
                "runId": normalized_run_id,
                "status": "running",
                "$or": [
                    {
                        "lastHeartbeatAt": {
                            "$lte": stale_before,
                        }
                    },
                    {
                        "lastHeartbeatAt": None,
                    },
                    {
                        "lastHeartbeatAt": {
                            "$exists": False,
                        }
                    },
                ],
            },
            {
                "$set": {
                    "status": "pending",
                    "queuedAt": current_time,
                    "updatedAt": current_time,
                    "workerId": None,
                    "startedAt": None,
                    "lastHeartbeatAt": None,
                }
            },
        )

        return result.modified_count

    async def count_by_status(
        self,
        *,
        run_id: str,
    ) -> JobStatusCounts:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        pipeline = [
            {
                "$match": {
                    "runId": normalized_run_id,
                }
            },
            {
                "$group": {
                    "_id": "$status",
                    "count": {
                        "$sum": 1,
                    },
                }
            },
        ]

        counts: dict[str, int] = {status: 0 for status in SCRAPER_JOB_STATUSES}

        cursor = await collection.aggregate(pipeline)

        async for document in cursor:
            status = document.get("_id")
            count = document.get("count")

            if isinstance(status, str) and status in counts and isinstance(count, int):
                counts[status] = count

        total = sum(counts.values())

        return JobStatusCounts(
            total=total,
            pending=counts["pending"],
            running=counts["running"],
            completed=counts["completed"],
            failed=counts["failed"],
            skipped=counts["skipped"],
            cancelled=counts["cancelled"],
        )

    async def iter_jobs(
        self,
        *,
        run_id: str,
        statuses: Sequence[str] | None = None,
    ) -> AsyncIterator[ScraperJob]:
        normalized_run_id = self._normalize_run_id(run_id)

        query: dict[str, Any] = {
            "runId": normalized_run_id,
        }

        if statuses is not None:
            normalized_statuses = list(
                dict.fromkeys(self._normalize_status(status) for status in statuses)
            )

            if not normalized_statuses:
                return

            query["status"] = {
                "$in": normalized_statuses,
            }

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_JOBS_COLLECTION)

        cursor = collection.find(query).sort(
            [
                (
                    "priority",
                    -1,
                ),
                (
                    "queuedAt",
                    1,
                ),
                (
                    "_id",
                    1,
                ),
            ]
        )

        async for document in cursor:
            yield ScraperJob.model_validate(document)


scraper_job_repository = ScraperJobRepository()
