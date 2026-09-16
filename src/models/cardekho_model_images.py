from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CarDekhoModelImages(BaseModel):
    """
    MongoDB representation of CarDekho model gallery images.

    One document represents one CarDekho model.
    The images array is stored in the same nested structure
    returned by the galleryPopup API.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    document_id: str = Field(
        alias="_id",
        min_length=1,
    )

    model_id: int = Field(
        alias="modelId",
        gt=0,
    )

    brand_id: int = Field(
        alias="brandId",
        gt=0,
    )

    brand_slug: str = Field(
        alias="brandSlug",
        min_length=1,
    )

    model_slug: str = Field(
        alias="modelSlug",
        min_length=1,
    )

    car_slug: str = Field(
        alias="carSlug",
        min_length=1,
    )

    title: str = Field(
        min_length=1,
    )

    images: list[dict[str, Any]] = Field(
        default_factory=list,
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
        mode="after",
    )
    def validate_document(
        self,
    ) -> Self:
        expected_document_id = self.build_document_id(
            self.model_id,
        )

        if self.document_id != expected_document_id:
            raise ValueError(
                "CarDekho model images document ID does not "
                "match modelId: "
                f"expected={expected_document_id!r}, "
                f"found={self.document_id!r}"
            )

        expected_car_slug = self.model_slug

        if self.car_slug != expected_car_slug:
            raise ValueError(
                "CarDekho model images carSlug does not "
                "match brandSlug and modelSlug: "
                f"expected={expected_car_slug!r}, "
                f"found={self.car_slug!r}"
            )

        return self

    @staticmethod
    def build_document_id(
        model_id: int,
    ) -> str:
        if isinstance(model_id, bool) or not isinstance(model_id, int):
            raise ValueError("model_id must be a positive integer")

        if model_id <= 0:
            raise ValueError("model_id must be a positive integer")

        return f"model:{model_id}"

    @classmethod
    def create(
        cls,
        *,
        model: Mapping[str, Any],
        images_data: list[dict[str, Any]],
        title: str,
        run_id: str,
        created_at: datetime | None = None,
    ) -> Self:
        if not isinstance(model, Mapping):
            raise ValueError("model must be an object")

        if not isinstance(images_data, list):
            raise ValueError("images_data must be an array")

        if not isinstance(title, str) or not title.strip():
            raise ValueError("title cannot be empty")

        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError("run_id cannot be empty")

        model_id = model.get("modelId")

        if isinstance(model_id, bool) or not isinstance(model_id, int) or model_id <= 0:
            raise ValueError("model.modelId must be a positive integer")

        brand_id = model.get("brandId")

        if isinstance(brand_id, bool) or not isinstance(brand_id, int) or brand_id <= 0:
            raise ValueError("model.brandId must be a positive integer")

        brand_slug = model.get("brandSlug")

        if not isinstance(brand_slug, str) or not brand_slug.strip():
            raise ValueError("model.brandSlug cannot be empty")

        model_slug = model.get("modelSlug")

        if not isinstance(model_slug, str) or not model_slug.strip():
            raise ValueError("model.modelSlug cannot be empty")

        car_slug = model_slug.strip().lower()

        current_time = datetime.now(timezone.utc)

        initial_created_at = (
            created_at
            if created_at is not None
            else current_time
        )

        return cls(
            _id=cls.build_document_id(model_id),
            modelId=model_id,
            brandId=brand_id,
            brandSlug=brand_slug.strip().lower(),
            modelSlug=model_slug.strip().lower(),
            carSlug=car_slug,
            title=title.strip(),
            images=images_data,
            lastRunId=run_id.strip(),
            scrapedAt=current_time,
            createdAt=initial_created_at,
            updatedAt=current_time,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
