from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Self
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


ScraperRunStatus = Literal[
    "pending",
    "running",
    "completed",
    "completed_with_failures",
    "interrupted",
    "failed",
    "cancelled",
]


class ScraperRun(BaseModel):
    """
    Generic MongoDB run document used by all scrapers.

    Every new run begins in the pending state.
    ScraperRunRepository.mark_started() transitions it
    from pending to running.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    run_id: str = Field(
        alias="_id",
        min_length=1,
    )

    source: str = Field(
        min_length=1,
    )

    resource: str = Field(
        min_length=1,
    )

    command: str = Field(
        min_length=1,
    )

    mode: str = Field(
        min_length=1,
    )

    status: ScraperRunStatus

    filters: dict[str, Any] = Field(
        default_factory=dict,
    )

    settings: dict[str, Any] = Field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    produced: int = Field(
        default=0,
        ge=0,
    )

    skipped: int = Field(
        default=0,
        ge=0,
    )

    successful: int = Field(
        default=0,
        ge=0,
    )

    failed: int = Field(
        default=0,
        ge=0,
    )

    written: int = Field(
        default=0,
        ge=0,
    )

    inserted: int = Field(
        default=0,
        ge=0,
    )

    matched: int = Field(
        default=0,
        ge=0,
    )

    modified: int = Field(
        default=0,
        ge=0,
    )

    failure_records_written: int = Field(
        default=0,
        alias="failureRecordsWritten",
        ge=0,
    )

    total_jobs: int = Field(
        default=0,
        alias="totalJobs",
        ge=0,
    )

    pending_jobs: int = Field(
        default=0,
        alias="pendingJobs",
        ge=0,
    )

    running_jobs: int = Field(
        default=0,
        alias="runningJobs",
        ge=0,
    )

    completed_jobs: int = Field(
        default=0,
        alias="completedJobs",
        ge=0,
    )

    failed_jobs: int = Field(
        default=0,
        alias="failedJobs",
        ge=0,
    )

    skipped_jobs: int = Field(
        default=0,
        alias="skippedJobs",
        ge=0,
    )

    cancelled_jobs: int = Field(
        default=0,
        alias="cancelledJobs",
        ge=0,
    )

    resume_count: int = Field(
        default=0,
        alias="resumeCount",
        ge=0,
    )

    created_at: datetime = Field(
        alias="createdAt",
    )

    started_at: datetime | None = Field(
        default=None,
        alias="startedAt",
    )

    updated_at: datetime = Field(
        alias="updatedAt",
    )

    resumed_at: datetime | None = Field(
        default=None,
        alias="resumedAt",
    )

    completed_at: datetime | None = Field(
        default=None,
        alias="completedAt",
    )

    stopped_at: datetime | None = Field(
        default=None,
        alias="stoppedAt",
    )

    stop_reason: str | None = Field(
        default=None,
        alias="stopReason",
    )

    stop_http_status: int | None = Field(
        default=None,
        alias="stopHttpStatus",
        ge=100,
        le=599,
    )

    error_type: str | None = Field(
        default=None,
        alias="errorType",
    )

    error_message: str | None = Field(
        default=None,
        alias="errorMessage",
    )

    @property
    def processed_jobs(self) -> int:
        return (
            self.completed_jobs
            + self.failed_jobs
            + self.skipped_jobs
            + self.cancelled_jobs
        )

    @property
    def unfinished_jobs(self) -> int:
        return self.pending_jobs + self.running_jobs

    @property
    def is_resumable(self) -> bool:
        return self.status in {
            "running",
            "completed",
            "completed_with_failures",
            "interrupted",
            "failed",
            "cancelled",
        }

    @property
    def was_stopped_early(self) -> bool:
        return (
            self.status
            not in {
                "completed",
                "completed_with_failures",
            }
            and self.stop_reason is not None
        )

    @classmethod
    def create(
        cls,
        *,
        source: str,
        resource: str,
        command: str,
        mode: str,
        filters: dict[str, Any] | None = None,
        settings: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Self:
        current_time = datetime.now(timezone.utc)

        normalized_source = source.strip().lower()

        normalized_resource = resource.strip().lower()

        normalized_command = command.strip()

        normalized_mode = mode.strip().lower()

        if not normalized_source:
            raise ValueError("source cannot be empty")

        if not normalized_resource:
            raise ValueError("resource cannot be empty")

        if not normalized_command:
            raise ValueError("command cannot be empty")

        if not normalized_mode:
            raise ValueError("mode cannot be empty")

        return cls(
            _id=uuid4().hex,
            source=normalized_source,
            resource=normalized_resource,
            command=normalized_command,
            mode=normalized_mode,
            status="pending",
            filters=dict(filters or {}),
            settings=dict(settings or {}),
            metadata=dict(metadata or {}),
            produced=0,
            skipped=0,
            successful=0,
            failed=0,
            written=0,
            inserted=0,
            matched=0,
            modified=0,
            failureRecordsWritten=0,
            totalJobs=0,
            pendingJobs=0,
            runningJobs=0,
            completedJobs=0,
            failedJobs=0,
            skippedJobs=0,
            cancelledJobs=0,
            resumeCount=0,
            createdAt=current_time,
            startedAt=None,
            updatedAt=current_time,
            resumedAt=None,
            completedAt=None,
            stoppedAt=None,
            stopReason=None,
            stopHttpStatus=None,
            errorType=None,
            errorMessage=None,
        )

    def progress_dict(
        self,
    ) -> dict[str, int]:
        return {
            "produced": self.produced,
            "skipped": self.skipped,
            "successful": self.successful,
            "failed": self.failed,
            "written": self.written,
            "inserted": self.inserted,
            "matched": self.matched,
            "modified": self.modified,
            "failureRecordsWritten": (self.failure_records_written),
            "totalJobs": self.total_jobs,
            "pendingJobs": self.pending_jobs,
            "runningJobs": self.running_jobs,
            "completedJobs": (self.completed_jobs),
            "failedJobs": self.failed_jobs,
            "skippedJobs": self.skipped_jobs,
            "cancelledJobs": (self.cancelled_jobs),
        }

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
