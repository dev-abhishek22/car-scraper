from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Self
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

CarWaleCityPriceRunStatus = Literal[
    "running",
    "completed",
    "interrupted",
    "failed",
    "cancelled",
]


class CarWaleCityPriceRunFilters(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    brand: str | None = None
    model: str | None = None
    city: str | None = None
    max_jobs: int | None = Field(
        default=None,
        alias="maxJobs",
        gt=0,
    )


class CarWaleCityPriceRunSettings(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )

    cars_directory: str = Field(
        alias="carsDirectory",
        min_length=1,
    )

    cities_file: str = Field(
        alias="citiesFile",
        min_length=1,
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


class CarWaleCityPriceRun(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

    run_id: str = Field(
        alias="_id",
        min_length=1,
    )

    status: CarWaleCityPriceRunStatus

    filters: CarWaleCityPriceRunFilters
    settings: CarWaleCityPriceRunSettings

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

    error_type: str | None = Field(
        default=None,
        alias="errorType",
    )

    error_message: str | None = Field(
        default=None,
        alias="errorMessage",
    )

    @classmethod
    def create(
        cls,
        *,
        cars_directory: str,
        cities_file: str,
        brand: str | None,
        model: str | None,
        city: str | None,
        max_jobs: int | None,
        workers: int,
        requests_per_second: float,
        mongo_batch_size: int,
    ) -> Self:
        current_time = datetime.now(timezone.utc)

        return cls(
            _id=str(uuid4()),
            status="running",
            filters=CarWaleCityPriceRunFilters(
                brand=brand,
                model=model,
                city=city,
                maxJobs=max_jobs,
            ),
            settings=CarWaleCityPriceRunSettings(
                carsDirectory=cars_directory,
                citiesFile=cities_file,
                workers=workers,
                requestsPerSecond=(requests_per_second),
                mongoBatchSize=(mongo_batch_size),
            ),
            startedAt=current_time,
            updatedAt=current_time,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
