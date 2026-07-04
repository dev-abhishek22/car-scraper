from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field

from src.models.cardekho_city_price_job import (
    CardekhoCityPriceJob,
)

CardekhoCityPriceFailureStatus = Literal[
    "failed",
    "resolved",
]

ACCESS_DENIED_HTTP_STATUS_CODES = {
    401,
    403,
}


class CardekhoCityPriceFailure(BaseModel):
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

    model_id: int = Field(
        alias="modelId",
        gt=0,
    )

    model_name: str = Field(
        alias="modelName",
        min_length=1,
    )

    model_slug: str = Field(
        alias="modelSlug",
        min_length=1,
    )

    model_status: str = Field(
        alias="modelStatus",
        min_length=1,
    )

    brand_id: int = Field(
        alias="brandId",
        gt=0,
    )

    brand_name: str = Field(
        alias="brandName",
        min_length=1,
    )

    brand_slug: str = Field(
        alias="brandSlug",
        min_length=1,
    )

    car_slug: str = Field(
        alias="carSlug",
        min_length=1,
    )

    city_id: int = Field(
        alias="cityId",
        gt=0,
    )

    city_name: str = Field(
        alias="cityName",
        min_length=1,
    )

    city_display_name: str = Field(
        alias="cityDisplayName",
        min_length=1,
    )

    city_slug: str = Field(
        alias="citySlug",
        min_length=1,
    )

    is_popular_city: bool = Field(
        default=False,
        alias="isPopularCity",
    )

    source_car_document_id: str = Field(
        alias="sourceCarDocumentId",
        min_length=1,
    )

    source_car_run_id: str | None = Field(
        default=None,
        alias="sourceCarRunId",
    )

    source_city_document_id: str = Field(
        alias="sourceCityDocumentId",
        min_length=1,
    )

    source_city_run_id: str | None = Field(
        default=None,
        alias="sourceCityRunId",
    )

    request_url: str = Field(
        alias="requestUrl",
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

    status: CardekhoCityPriceFailureStatus = "failed"

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

    updated_at: datetime = Field(
        alias="updatedAt",
    )

    @property
    def is_access_denied(
        self,
    ) -> bool:
        return self.http_status in ACCESS_DENIED_HTTP_STATUS_CODES

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

        return f"{normalized_run_id}:{normalized_job_id}"

    @classmethod
    def create(
        cls,
        *,
        run_id: str,
        job: CardekhoCityPriceJob,
        error: BaseException,
        retryable: bool,
        http_status: int | None = None,
    ) -> Self:
        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        if http_status is not None and (
            isinstance(
                http_status,
                bool,
            )
            or not isinstance(
                http_status,
                int,
            )
            or not 100 <= http_status <= 599
        ):
            raise ValueError("http_status must be an integer between 100 and 599")

        current_time = datetime.now(timezone.utc)

        error_message = str(error).strip()

        if not error_message:
            error_message = "Unknown Cardekho city-price failure"

        retryable_for_later = (
            True if http_status in ACCESS_DENIED_HTTP_STATUS_CODES else retryable
        )

        return cls(
            _id=cls.build_failure_id(
                run_id=normalized_run_id,
                job_id=job.item_key,
            ),
            runId=normalized_run_id,
            jobId=job.item_key,
            modelId=job.model_id,
            modelName=job.model_name,
            modelSlug=job.model_slug,
            modelStatus=job.model_status,
            brandId=job.brand_id,
            brandName=job.brand_name,
            brandSlug=job.brand_slug,
            carSlug=job.car_slug,
            cityId=job.city_id,
            cityName=job.city_name,
            cityDisplayName=(job.city_display_name),
            citySlug=job.city_slug,
            isPopularCity=(job.is_popular_city),
            sourceCarDocumentId=(job.source_car_document_id),
            sourceCarRunId=(job.source_car_run_id),
            sourceCityDocumentId=(job.source_city_document_id),
            sourceCityRunId=(job.source_city_run_id),
            requestUrl=(job.request_url_value),
            errorType=type(error).__name__,
            errorMessage=error_message,
            httpStatus=http_status,
            retryable=(retryable_for_later),
            status="failed",
            attempts=1,
            firstFailedAt=current_time,
            lastFailedAt=current_time,
            resolvedAt=None,
            updatedAt=current_time,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
