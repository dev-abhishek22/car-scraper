from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ModelStatus = Literal["CURRENT", "UPCOMING", "DISCONTINUED"]
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class BikeDekhoModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore", str_strip_whitespace=True)

    document_id: str = Field(alias="_id")
    model_id: int | None = Field(default=None, alias="id", gt=0)
    brand_id: int | None = Field(default=None, alias="brandId", gt=0)
    brand_name: str = Field(alias="brandName", min_length=1)
    brand_slug: str = Field(alias="brandSlug", pattern=SLUG_PATTERN.pattern)
    name: str = Field(min_length=1)
    slug: str = Field(pattern=SLUG_PATTERN.pattern)
    model_name: str = Field(alias="modelName", min_length=1)
    model_status: ModelStatus = Field(alias="modelStatus")
    is_upcoming: bool = Field(alias="isUpcoming")
    expected_launch_date: str | None = Field(default=None, alias="expectedLaunchDate")
    data: dict[str, Any] = Field(default_factory=dict, exclude=True)
    last_run_id: str = Field(alias="lastRunId")
    source_brand_run_id: str | None = Field(default=None, alias="sourceBrandRunId")
    source_brand_document_id: str = Field(alias="sourceBrandDocumentId")
    scraped_at: datetime = Field(alias="scrapedAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    @staticmethod
    def build_document_id(brand_slug: str, model_slug: str) -> str:
        return f"bikedekho:model:{brand_slug}:{model_slug}"

    @classmethod
    def create(
        cls,
        *,
        brand: Mapping[str, Any],
        model: Mapping[str, Any],
        run_id: str,
        source_brand_run_id: str | None = None,
        created_at: datetime | None = None,
    ) -> "BikeDekhoModel":
        brand_slug = str(brand.get("slug", "")).strip().lower()
        model_slug = str(model.get("slug", "")).strip().lower()
        if not SLUG_PATTERN.fullmatch(brand_slug) or not SLUG_PATTERN.fullmatch(model_slug):
            raise ValueError("brand and model slugs must be valid")
        raw_data = dict(model)
        raw_data.pop("_id", None)
        now = datetime.now(timezone.utc)
        return cls(
            _id=cls.build_document_id(brand_slug, model_slug),
            **raw_data,
            data=raw_data,
            lastRunId=run_id,
            sourceBrandRunId=source_brand_run_id,
            sourceBrandDocumentId=str(brand.get("_id")),
            scrapedAt=now,
            createdAt=created_at or now,
            updatedAt=now,
        )

    def to_mongo_document(self) -> dict[str, Any]:
        document = self.model_dump(by_alias=True, mode="python")
        for key, value in self.data.items():
            if key not in {"_id", "lastRunId", "sourceBrandRunId", "sourceBrandDocumentId", "scrapedAt", "createdAt", "updatedAt"}:
                document[key] = value
        return document
