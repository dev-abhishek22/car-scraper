from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CarWaleCityPrice(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
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

    version_details: dict[str, Any] = Field(
        alias="versionDetails",
    )

    price_breakup: list[dict[str, Any]] = Field(
        alias="priceBreakup",
    )

    scraped_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        alias="scrapedAt",
    )

    @property
    def document_id(self) -> str:
        """
        Permanent MongoDB document ID for one version-city combination.
        """
        return f"v:{self.version_id}:c:{self.city_id}"

    def to_mongo_document(self) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
