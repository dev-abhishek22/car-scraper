from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CarWaleCityPrice(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

    version_id: int = Field(alias="versionId")
    city_id: int = Field(alias="cityId")

    make_masking_name: str = Field(alias="makeMaskingName")
    model_masking_name: str = Field(alias="modelMaskingName")
    city_masking_name: str = Field(alias="cityMaskingName")

    version_details: dict[str, Any] = Field(alias="versionDetails")
    price_breakup: list[dict[str, Any]] = Field(alias="priceBreakup")

    scraped_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        alias="scrapedAt",
    )

    def to_mongo_document(self) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
