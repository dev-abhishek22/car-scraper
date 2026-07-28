from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class BikeDekhoBrand(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    document_id: str = Field(alias="_id", min_length=1)
    brand_name: str = Field(alias="brandName", min_length=1)
    slug: str = Field(min_length=1, pattern=SLUG_PATTERN.pattern)
    brand_url: str = Field(alias="brandUrl", min_length=1)
    title: str | None = None
    image: str | None = None
    filter_name: str | None = Field(default=None, alias="filterName")
    popularity: int | None = Field(default=None, ge=0)
    model_count: int | None = Field(default=None, alias="modelCount", ge=0)
    data: dict[str, Any]
    last_run_id: str = Field(alias="lastRunId", min_length=1)
    scraped_at: datetime = Field(alias="scrapedAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    @model_validator(mode="before")
    @classmethod
    def restore_data(cls, values: Any) -> Any:
        if not isinstance(values, Mapping):
            return values
        document = dict(values)
        if "data" not in document:
            protected = {
                "_id",
                "lastRunId",
                "scrapedAt",
                "createdAt",
                "updatedAt",
            }
            document["data"] = {
                key: value for key, value in document.items() if key not in protected
            }
        return document

    @staticmethod
    def build_document_id(slug: str) -> str:
        return f"bikedekho:brand:{slug}"

    @classmethod
    def create(
        cls,
        *,
        brand: Mapping[str, Any],
        run_id: str,
        created_at: datetime | None = None,
    ) -> "BikeDekhoBrand":
        normalized_run_id = run_id.strip()
        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        slug_value = brand.get("slug")
        if not isinstance(slug_value, str):
            raise ValueError("slug must be a string")
        slug = slug_value.strip().lower()
        if not SLUG_PATTERN.fullmatch(slug):
            raise ValueError(f"Invalid BikeDekho brand slug: {slug!r}")

        now = datetime.now(timezone.utc)
        raw_data = dict(brand)
        return cls(
            _id=cls.build_document_id(slug),
            **raw_data,
            data=raw_data,
            lastRunId=normalized_run_id,
            scrapedAt=now,
            createdAt=created_at or now,
            updatedAt=now,
        )

    def to_mongo_document(self) -> dict[str, Any]:
        document = self.model_dump(by_alias=True, mode="python")
        raw_data = document.pop("data")
        for key, value in raw_data.items():
            if key not in {
                "_id",
                "lastRunId",
                "scrapedAt",
                "createdAt",
                "updatedAt",
            }:
                document[key] = value
        return document
