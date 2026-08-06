from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BikeDekhoScooter(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

    document_id: str = Field(alias="_id")

    model_id: int | None = Field(
        default=None,
        alias="id",
    )

    brand_id: int | None = Field(
        default=None,
        alias="brandId",
    )

    brand_name: str = Field(alias="brandName")

    brand_slug: str = Field(alias="brandSlug")

    name: str

    slug: str

    scooter_slug: str = Field(alias="scooterSlug")

    model_name: str = Field(alias="modelName")

    model_status: str = Field(alias="modelStatus")

    is_upcoming: bool = Field(alias="isUpcoming")

    overview: dict[str, Any]

    total_variants: int = Field(alias="totalVariants")

    variants: list[dict[str, Any]]

    variant_specs_exist: bool = Field(
        default=False,
        alias="variantSpecsExist",
    )

    total_comparisons: int = Field(alias="totalComparisons")

    compare_with: list[dict[str, Any]] = Field(alias="compareWith")

    total_similar_scooters: int = Field(alias="totalSimilarScooters")

    similar_scooters: list[dict[str, Any]] = Field(alias="similarScooters")

    last_run_id: str = Field(alias="lastRunId")

    source_model_run_id: str | None = Field(alias="sourceModelRunId")

    source_model_document_id: str = Field(alias="sourceModelDocumentId")

    scraped_at: datetime = Field(alias="scrapedAt")

    created_at: datetime = Field(alias="createdAt")

    updated_at: datetime = Field(alias="updatedAt")

    @staticmethod
    def build_document_id(
        brand_slug: str,
        model_slug: str,
    ) -> str:
        return f"bikedekho:scooter:" f"{brand_slug}:" f"{model_slug}"

    @classmethod
    def create(
        cls,
        *,
        model: Mapping[str, Any],
        scooter_data: Mapping[str, Any],
        run_id: str,
        source_model_run_id: str | None = None,
        created_at: datetime | None = None,
    ) -> "BikeDekhoScooter":
        brand_slug = str(model.get("brandSlug"))

        model_slug = str(model.get("slug"))

        overview = dict(scooter_data["overview"])

        now = datetime.now(timezone.utc)

        model_id = model.get("id") or overview.get("id")

        brand_id = model.get("brandId") or overview.get("id_brand")

        return cls(
            _id=cls.build_document_id(
                brand_slug,
                model_slug,
            ),
            id=model_id,
            brandId=brand_id,
            brandName=model.get("brandName"),
            brandSlug=brand_slug,
            name=model.get("name"),
            slug=model_slug,
            scooterSlug=(f"{brand_slug}-" f"{model_slug}"),
            modelName=model.get("modelName"),
            modelStatus=model.get("modelStatus"),
            isUpcoming=model.get("isUpcoming"),
            overview=overview,
            totalVariants=scooter_data.get(
                "totalVariants",
                0,
            ),
            variants=scooter_data.get(
                "variants",
                [],
            ),
            variantSpecsExist=scooter_data.get(
                "variantSpecsExist",
                False,
            ),
            totalComparisons=scooter_data.get(
                "totalComparisons",
                0,
            ),
            compareWith=scooter_data.get(
                "compareWith",
                [],
            ),
            totalSimilarScooters=scooter_data.get(
                "totalSimilarBikes",
                0,
            ),
            similarScooters=scooter_data.get(
                "similarBikes",
                [],
            ),
            lastRunId=run_id,
            sourceModelRunId=(source_model_run_id or model.get("lastRunId")),
            sourceModelDocumentId=model.get("_id"),
            scrapedAt=now,
            createdAt=(created_at or now),
            updatedAt=now,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
