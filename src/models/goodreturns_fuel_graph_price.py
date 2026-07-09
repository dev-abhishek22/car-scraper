from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class GoodReturnsFuelGraphPoint(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    date: str | None = None

    timestamp_ms: int | None = Field(
        default=None,
        alias="timestampMs",
        ge=0,
    )

    price: float | None = Field(
        default=None,
        ge=0,
    )

    raw: Any = None

    def to_mongo_document(self) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )

    def to_mongo(self) -> dict[str, Any]:
        return self.to_mongo_document()


class GoodReturnsFuelGraphPrice(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    document_id: str | None = Field(
        default=None,
        alias="_id",
    )

    source: str = Field(
        default="goodreturns",
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

    city_slug: str = Field(
        alias="citySlug",
        min_length=1,
    )

    fuel_type: str = Field(
        alias="fuelType",
        min_length=1,
    )

    timeframe: str = Field(
        min_length=1,
    )

    page_url: str | None = Field(
        default=None,
        alias="pageUrl",
    )

    points: list[GoodReturnsFuelGraphPoint] = Field(
        default_factory=list,
    )

    points_count: int = Field(
        default=0,
        alias="pointsCount",
        ge=0,
    )

    raw_response: Any = Field(
        alias="rawResponse",
    )

    last_http_status: int | None = Field(
        default=None,
        alias="lastHttpStatus",
        ge=100,
        le=599,
    )

    last_run_id: str = Field(
        alias="lastRunId",
        min_length=1,
    )

    scraped_at: datetime = Field(
        alias="scrapedAt",
    )

    created_at: datetime = Field(
        alias="createdAt",
    )

    updated_at: datetime = Field(
        alias="updatedAt",
    )

    @model_validator(
        mode="before",
    )
    @classmethod
    def normalize_input(
        cls,
        values: Any,
    ) -> Any:
        if not isinstance(
            values,
            Mapping,
        ):
            raise ValueError("Goodreturns fuel graph price must be an object")

        current_time = datetime.now(timezone.utc)

        mutable_values = dict(values)

        points = mutable_values.get(
            "points",
            [],
        )

        if points is None:
            points = []

        if not isinstance(
            points,
            list,
        ):
            raise ValueError("points must be an array")

        mutable_values["points"] = points
        mutable_values["pointsCount"] = len(points)

        mutable_values.setdefault(
            "source",
            "goodreturns",
        )

        mutable_values.setdefault(
            "scrapedAt",
            current_time,
        )

        mutable_values.setdefault(
            "createdAt",
            current_time,
        )

        mutable_values.setdefault(
            "updatedAt",
            current_time,
        )

        return mutable_values

    @model_validator(
        mode="after",
    )
    def validate_document_id(
        self,
    ) -> Self:
        expected_document_id = self.build_document_id(
            fuel_type=self.fuel_type,
            city_slug=self.city_slug,
            timeframe=self.timeframe,
            source=self.source,
        )

        if self.document_id is not None and self.document_id != expected_document_id:
            raise ValueError(
                "Goodreturns fuel graph document ID does not match "
                "source, fuelType, citySlug and timeframe: "
                f"expected={expected_document_id!r}, "
                f"found={self.document_id!r}"
            )

        if self.points_count != len(self.points):
            raise ValueError(
                "pointsCount does not match points length: "
                f"expected={len(self.points)}, "
                f"found={self.points_count}"
            )

        return self

    @staticmethod
    def _normalize_text(
        value: str,
        *,
        field_name: str,
        lower: bool = False,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError(f"{field_name} must be a string")

        normalized_value = value.strip()

        if lower:
            normalized_value = normalized_value.lower()

        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        return normalized_value

    @classmethod
    def build_document_id(
        cls,
        *,
        fuel_type: str,
        city_slug: str,
        timeframe: str,
        source: str = "goodreturns",
    ) -> str:
        normalized_source = cls._normalize_text(
            source,
            field_name="source",
            lower=True,
        )

        normalized_fuel_type = cls._normalize_text(
            fuel_type,
            field_name="fuel_type",
            lower=True,
        )

        normalized_city_slug = cls._normalize_text(
            city_slug,
            field_name="city_slug",
            lower=True,
        )

        normalized_timeframe = cls._normalize_text(
            timeframe,
            field_name="timeframe",
        )

        return (
            f"{normalized_source}:"
            f"{normalized_fuel_type}:"
            f"{normalized_city_slug}:"
            f"{normalized_timeframe}"
        )

    @property
    def id(self) -> str:
        return self.build_document_id(
            source=self.source,
            fuel_type=self.fuel_type,
            city_slug=self.city_slug,
            timeframe=self.timeframe,
        )

    @classmethod
    def create(
        cls,
        *,
        city_id: int,
        city_name: str,
        city_slug: str,
        fuel_type: str,
        timeframe: str,
        page_url: str | None,
        points: list[GoodReturnsFuelGraphPoint],
        raw_response: Any,
        last_run_id: str,
        last_http_status: int | None = None,
        created_at: datetime | None = None,
    ) -> Self:
        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        return cls(
            _id=cls.build_document_id(
                fuel_type=fuel_type,
                city_slug=city_slug,
                timeframe=timeframe,
            ),
            source="goodreturns",
            cityId=city_id,
            cityName=city_name,
            citySlug=city_slug,
            fuelType=fuel_type,
            timeframe=timeframe,
            pageUrl=page_url,
            points=points,
            pointsCount=len(points),
            rawResponse=raw_response,
            lastHttpStatus=last_http_status,
            lastRunId=last_run_id,
            scrapedAt=current_time,
            createdAt=initial_created_at,
            updatedAt=current_time,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        document = self.model_dump(
            by_alias=True,
            mode="python",
        )

        document["_id"] = self.id
        document["pointsCount"] = len(self.points)

        return document

    def to_mongo(
        self,
    ) -> dict[str, Any]:
        return self.to_mongo_document()
