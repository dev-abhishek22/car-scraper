from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field

from src.models.carwale_city_price_job import (
    CarWaleCityPriceJob,
)

CarWaleCityPriceFailureStatus = Literal[
    "failed",
    "resolved",
]


class CarWaleCityPriceFailure(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    failure_id: str = Field(
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

    version_id: int = Field(
        alias="versionId",
        gt=0,
    )

    city_id: int = Field(
        alias="cityId",
        gt=0,
    )

    make_masking_name: str = Field(
        alias="makeMaskingName",
        min_length=1,
    )

    model_masking_name: str = Field(
        alias="modelMaskingName",
        min_length=1,
    )

    city_masking_name: str = Field(
        alias="cityMaskingName",
        min_length=1,
    )

    error_type: str = Field(
        alias="errorType",
        min_length=1,
    )

    error_message: str = Field(
        alias="errorMessage",
        min_length=1,
    )

    http_status: int | None = Field(
        default=None,
        alias="httpStatus",
        ge=100,
        le=599,
    )

    retryable: bool

    status: CarWaleCityPriceFailureStatus = "failed"

    attempts: int = Field(
        default=1,
        ge=1,
    )

    first_failed_at: datetime = Field(
        alias="firstFailedAt",
    )

    last_failed_at: datetime = Field(
        alias="lastFailedAt",
    )

    resolved_at: datetime | None = Field(
        default=None,
        alias="resolvedAt",
    )

    @staticmethod
    def build_failure_id(
        *,
        run_id: str,
        job_id: str,
    ) -> str:
        normalized_run_id = run_id.strip()
        normalized_job_id = job_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        if not normalized_job_id:
            raise ValueError("job_id cannot be empty")

        return f"{normalized_run_id}:" f"{normalized_job_id}"

    @classmethod
    def create(
        cls,
        *,
        run_id: str,
        job: CarWaleCityPriceJob,
        error: BaseException,
        retryable: bool,
        http_status: int | None = None,
    ) -> Self:
        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        current_time = datetime.now(timezone.utc)

        error_message = str(error).strip()

        if not error_message:
            error_message = "Unknown city-price failure"

        return cls(
            _id=cls.build_failure_id(
                run_id=normalized_run_id,
                job_id=job.item_key,
            ),
            runId=normalized_run_id,
            jobId=job.item_key,
            versionId=job.version_id,
            cityId=job.city_id,
            makeMaskingName=(job.make_masking_name),
            modelMaskingName=(job.model_masking_name),
            cityMaskingName=(job.city_masking_name),
            errorType=type(error).__name__,
            errorMessage=error_message,
            httpStatus=http_status,
            retryable=retryable,
            status="failed",
            attempts=1,
            firstFailedAt=current_time,
            lastFailedAt=current_time,
            resolvedAt=None,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
