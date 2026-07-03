from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field

ScraperJobStatus = Literal[
    "pending",
    "running",
    "completed",
    "failed",
    "skipped",
    "cancelled",
]


class ScraperJob(BaseModel):
    """
    Generic persisted scraper job.

    One document represents one fetch task inside one scraper run.

    The failure-related fields intentionally follow the existing
    CarWale city-price failure document structure:

    - runId
    - jobId
    - attempts
    - errorType
    - errorMessage
    - httpStatus
    - retryable
    - firstFailedAt
    - lastFailedAt
    - resolvedAt
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    document_id: str = Field(
        alias="_id",
        min_length=1,
    )

    run_id: str = Field(
        alias="runId",
        min_length=1,
    )

    job_id: str = Field(
        alias="jobId",
        min_length=1,
    )

    source: str = Field(
        min_length=1,
    )

    resource: str = Field(
        min_length=1,
    )

    job_type: str = Field(
        alias="jobType",
        min_length=1,
    )

    item_key: str = Field(
        alias="itemKey",
        min_length=1,
    )

    status: ScraperJobStatus = "pending"

    priority: int = Field(
        default=0,
        ge=0,
    )

    payload: dict[str, Any] = Field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    result: dict[str, Any] | None = None

    attempts: int = Field(
        default=0,
        ge=0,
    )

    max_attempts: int = Field(
        default=1,
        alias="maxAttempts",
        ge=1,
    )

    retryable: bool = True

    worker_id: str | None = Field(
        default=None,
        alias="workerId",
    )

    queued_at: datetime = Field(
        alias="queuedAt",
    )

    started_at: datetime | None = Field(
        default=None,
        alias="startedAt",
    )

    last_heartbeat_at: datetime | None = Field(
        default=None,
        alias="lastHeartbeatAt",
    )

    completed_at: datetime | None = Field(
        default=None,
        alias="completedAt",
    )

    failed_at: datetime | None = Field(
        default=None,
        alias="failedAt",
    )

    skipped_at: datetime | None = Field(
        default=None,
        alias="skippedAt",
    )

    cancelled_at: datetime | None = Field(
        default=None,
        alias="cancelledAt",
    )

    first_failed_at: datetime | None = Field(
        default=None,
        alias="firstFailedAt",
    )

    last_failed_at: datetime | None = Field(
        default=None,
        alias="lastFailedAt",
    )

    resolved_at: datetime | None = Field(
        default=None,
        alias="resolvedAt",
    )

    error_type: str | None = Field(
        default=None,
        alias="errorType",
    )

    error_message: str | None = Field(
        default=None,
        alias="errorMessage",
    )

    http_status: int | None = Field(
        default=None,
        alias="httpStatus",
        ge=100,
        le=599,
    )

    skip_reason: str | None = Field(
        default=None,
        alias="skipReason",
    )

    cancel_reason: str | None = Field(
        default=None,
        alias="cancelReason",
    )

    created_at: datetime = Field(
        alias="createdAt",
    )

    updated_at: datetime = Field(
        alias="updatedAt",
    )

    @property
    def is_terminal(self) -> bool:
        return self.status in {
            "completed",
            "failed",
            "skipped",
            "cancelled",
        }

    @property
    def can_retry(self) -> bool:
        return (
            self.status == "failed"
            and self.retryable
            and self.attempts < self.max_attempts
        )

    @staticmethod
    def build_document_id(
        *,
        run_id: str,
        job_id: str,
    ) -> str:
        """
        Build the same deterministic run/job identifier pattern
        currently used by CarWale city-price failures.
        """
        normalized_run_id = run_id.strip()
        normalized_job_id = job_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        if not normalized_job_id:
            raise ValueError("job_id cannot be empty")

        return f"{normalized_run_id}:{normalized_job_id}"

    @classmethod
    def create(
        cls,
        *,
        run_id: str,
        source: str,
        resource: str,
        job_type: str,
        item_key: str,
        job_id: str | None = None,
        payload: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        priority: int = 0,
        max_attempts: int = 1,
        retryable: bool = True,
    ) -> Self:
        normalized_run_id = run_id.strip()
        normalized_source = source.strip().lower()
        normalized_resource = resource.strip().lower()
        normalized_job_type = job_type.strip().lower()
        normalized_item_key = item_key.strip().lower()

        normalized_job_id = (
            job_id.strip() if job_id is not None else normalized_item_key
        )

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        if not normalized_source:
            raise ValueError("source cannot be empty")

        if not normalized_resource:
            raise ValueError("resource cannot be empty")

        if not normalized_job_type:
            raise ValueError("job_type cannot be empty")

        if not normalized_item_key:
            raise ValueError("item_key cannot be empty")

        if not normalized_job_id:
            raise ValueError("job_id cannot be empty")

        if isinstance(priority, bool) or priority < 0:
            raise ValueError("priority must be a non-negative integer")

        if isinstance(max_attempts, bool) or max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        current_time = datetime.now(timezone.utc)

        return cls(
            _id=cls.build_document_id(
                run_id=normalized_run_id,
                job_id=normalized_job_id,
            ),
            runId=normalized_run_id,
            jobId=normalized_job_id,
            source=normalized_source,
            resource=normalized_resource,
            jobType=normalized_job_type,
            itemKey=normalized_item_key,
            status="pending",
            priority=priority,
            payload=dict(payload or {}),
            metadata=dict(metadata or {}),
            result=None,
            attempts=0,
            maxAttempts=max_attempts,
            retryable=retryable,
            workerId=None,
            queuedAt=current_time,
            startedAt=None,
            lastHeartbeatAt=None,
            completedAt=None,
            failedAt=None,
            skippedAt=None,
            cancelledAt=None,
            firstFailedAt=None,
            lastFailedAt=None,
            resolvedAt=None,
            errorType=None,
            errorMessage=None,
            httpStatus=None,
            skipReason=None,
            cancelReason=None,
            createdAt=current_time,
            updatedAt=current_time,
        )

    def to_mongo_document(self) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
