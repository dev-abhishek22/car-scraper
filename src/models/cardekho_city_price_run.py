from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Self
from uuid import uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

CardekhoCityPriceRunStatus = Literal[
    "running",
    "completed",
    "interrupted",
    "failed",
    "cancelled",
]


class CardekhoCityPriceRunFilters(
    BaseModel,
):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    brand: str | None = None

    model: str | None = None

    model_id: int | None = Field(
        default=None,
        alias="modelId",
        gt=0,
    )

    city: str | None = None

    city_id: int | None = Field(
        default=None,
        alias="cityId",
        gt=0,
    )

    popular_cities_only: bool = Field(
        default=False,
        alias="popularCitiesOnly",
    )

    tier: int | None = Field(
        default=None,
        ge=1,
        le=3,
    )

    max_jobs: int | None = Field(
        default=None,
        alias="maxJobs",
        gt=0,
    )

    @model_validator(
        mode="after",
    )
    def validate_filters(
        self,
    ) -> Self:
        if self.model is not None and self.brand is None:
            raise ValueError("model requires brand")

        return self


class CardekhoCityPriceRunSettings(
    BaseModel,
):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    workers: int = Field(
        ge=1,
    )

    requests_per_second: float = Field(
        alias="requestsPerSecond",
        gt=0,
    )

    mongo_batch_size: int = Field(
        alias="mongoBatchSize",
        ge=1,
    )

    pause_every_requests: int = Field(
        default=0,
        alias="pauseEveryRequests",
        ge=0,
    )

    pause_seconds: float = Field(
        default=0.0,
        alias="pauseSeconds",
        ge=0,
    )

    @model_validator(
        mode="after",
    )
    def validate_pause_configuration(
        self,
    ) -> Self:
        request_pause_enabled = self.pause_every_requests > 0

        duration_pause_enabled = self.pause_seconds > 0

        if request_pause_enabled != duration_pause_enabled:
            raise ValueError(
                "pauseEveryRequests and "
                "pauseSeconds must both be "
                "greater than zero or both "
                "be zero"
            )

        return self


class CardekhoCityPriceRun(
    BaseModel,
):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    run_id: str = Field(
        alias="_id",
        min_length=1,
    )

    status: CardekhoCityPriceRunStatus

    filters: CardekhoCityPriceRunFilters

    settings: CardekhoCityPriceRunSettings

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

    resume_count: int = Field(
        default=0,
        alias="resumeCount",
        ge=0,
    )

    started_at: datetime = Field(
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
    def is_resumable(
        self,
    ) -> bool:
        return self.status in {
            "running",
            "completed",
            "interrupted",
            "failed",
            "cancelled",
        }

    @property
    def was_stopped_early(
        self,
    ) -> bool:
        return self.status != "completed" and self.stop_reason is not None

    @classmethod
    def create(
        cls,
        *,
        brand: str | None,
        model: str | None,
        model_id: int | None,
        city: str | None,
        city_id: int | None,
        popular_cities_only: bool,
        tier: int | None,
        max_jobs: int | None,
        workers: int,
        requests_per_second: float,
        mongo_batch_size: int,
        pause_every_requests: int = 0,
        pause_seconds: float = 0.0,
    ) -> Self:
        current_time = datetime.now(timezone.utc)

        return cls(
            _id=str(uuid4()),
            status="running",
            filters=(
                CardekhoCityPriceRunFilters(
                    brand=brand,
                    model=model,
                    modelId=model_id,
                    city=city,
                    cityId=city_id,
                    popularCitiesOnly=(popular_cities_only),
                    tier=tier,
                    maxJobs=max_jobs,
                )
            ),
            settings=(
                CardekhoCityPriceRunSettings(
                    workers=workers,
                    requestsPerSecond=(requests_per_second),
                    mongoBatchSize=(mongo_batch_size),
                    pauseEveryRequests=(pause_every_requests),
                    pauseSeconds=(pause_seconds),
                )
            ),
            produced=0,
            skipped=0,
            successful=0,
            failed=0,
            written=0,
            inserted=0,
            matched=0,
            modified=0,
            failureRecordsWritten=0,
            resumeCount=0,
            startedAt=current_time,
            updatedAt=current_time,
            resumedAt=None,
            completedAt=None,
            stoppedAt=None,
            stopReason=None,
            stopHttpStatus=None,
            errorType=None,
            errorMessage=None,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
