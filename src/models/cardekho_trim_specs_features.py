from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CarDekhoTrimSpecsFeatures(BaseModel):
    """
    MongoDB representation of one Cardekho
    variant's specifications and features.

    One document represents one unique variantId.

    Example document ID:

        variant:10387
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
        arbitrary_types_allowed=True,
    )

    document_id: str = Field(
        alias="_id",
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

    car_slug: str = Field(
        alias="carSlug",
        min_length=1,
    )

    model_status: str = Field(
        alias="modelStatus",
        min_length=1,
    )

    variant_id: int = Field(
        alias="variantId",
        gt=0,
    )

    variant_name: str = Field(
        alias="variantName",
        min_length=1,
    )

    variant_short_name: str = Field(
        alias="variantShortName",
        min_length=1,
    )

    variant_slug: str = Field(
        alias="variantSlug",
        min_length=1,
    )

    variant_url: str | None = Field(
        default=None,
        alias="variantUrl",
    )

    variant_status: str = Field(
        alias="variantStatus",
        min_length=1,
    )

    featured: Any = None

    specification: Any = None

    source_car_document_id: str | None = Field(
        default=None,
        alias="sourceCarDocumentId",
    )

    source_car_run_id: str | None = Field(
        default=None,
        alias="sourceCarRunId",
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
    def validate_document_identity(
        self,
    ) -> Self:
        expected_document_id = self.build_document_id(
            variant_id=self.variant_id,
        )

        if self.document_id != expected_document_id:
            raise ValueError(
                "Cardekho trim specs/features "
                "document ID does not match variantId: "
                f"expected={expected_document_id!r}, "
                f"found={self.document_id!r}"
            )

        return self

    @staticmethod
    def _validate_positive_integer(
        value: Any,
        *,
        field_name: str,
    ) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field_name} must be a positive integer")

        return value

    @staticmethod
    def _validate_non_empty_string(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        return normalized_value

    @classmethod
    def _normalize_optional_string(
        cls,
        value: Any,
        *,
        field_name: str,
    ) -> str | None:
        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string or null")

        normalized_value = value.strip()

        return normalized_value or None

    @classmethod
    def _validate_slug(
        cls,
        value: Any,
        *,
        field_name: str,
    ) -> str:
        normalized_value = (
            cls._validate_non_empty_string(
                value,
                field_name=field_name,
            )
            .lower()
            .replace("_", "-")
            .replace(" ", "-")
        )

        normalized_value = re.sub(
            r"-+",
            "-",
            normalized_value,
        ).strip("-")

        if not SLUG_PATTERN.fullmatch(normalized_value):
            raise ValueError(
                f"{field_name} contains invalid " f"characters: {normalized_value!r}"
            )

        return normalized_value

    @classmethod
    def _normalize_status(
        cls,
        value: Any,
        *,
        field_name: str,
    ) -> str:
        return cls._validate_non_empty_string(
            value,
            field_name=field_name,
        ).upper()

    @staticmethod
    def build_document_id(
        *,
        variant_id: int,
    ) -> str:
        if (
            isinstance(variant_id, bool)
            or not isinstance(variant_id, int)
            or variant_id <= 0
        ):
            raise ValueError("variant_id must be a positive integer")

        return f"variant:{variant_id}"

    @classmethod
    def create(
        cls,
        *,
        variant_record: Mapping[str, Any],
        response_data: Mapping[str, Any],
        run_id: str,
        created_at: datetime | None = None,
    ) -> Self:
        if not isinstance(
            variant_record,
            Mapping,
        ):
            raise ValueError("variant_record must be an object")

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ValueError("response_data must be an object")

        variant = variant_record.get("variant")

        if not isinstance(
            variant,
            Mapping,
        ):
            raise ValueError("variant_record.variant must be an object")

        normalized_run_id = cls._validate_non_empty_string(
            run_id,
            field_name="run_id",
        )

        brand_id = cls._validate_positive_integer(
            variant_record.get("brandId"),
            field_name="variant_record.brandId",
        )

        brand_name = cls._validate_non_empty_string(
            variant_record.get("brandName"),
            field_name="variant_record.brandName",
        )

        brand_slug = cls._validate_slug(
            variant_record.get("brandSlug"),
            field_name="variant_record.brandSlug",
        )

        model_id = cls._validate_positive_integer(
            variant_record.get("modelId"),
            field_name="variant_record.modelId",
        )

        model_name = cls._validate_non_empty_string(
            variant_record.get("modelName"),
            field_name="variant_record.modelName",
        )

        model_slug = cls._validate_slug(
            variant_record.get("modelSlug"),
            field_name="variant_record.modelSlug",
        )

        car_slug = cls._validate_slug(
            variant_record.get("carSlug"),
            field_name="variant_record.carSlug",
        )

        model_status = cls._normalize_status(
            variant_record.get("modelStatus"),
            field_name="variant_record.modelStatus",
        )

        variant_id = cls._validate_positive_integer(
            variant.get("id"),
            field_name="variant.id",
        )

        variant_slug = cls._validate_non_empty_string(
            variant.get("slug"),
            field_name="variant.slug",
        )

        raw_variant_name = cls._normalize_optional_string(
            variant.get("name"),
            field_name="variant.name",
        )

        raw_variant_short_name = cls._normalize_optional_string(
            variant.get("shortName"),
            field_name="variant.shortName",
        )

        variant_name = raw_variant_name or raw_variant_short_name or variant_slug

        variant_short_name = raw_variant_short_name or variant_name

        variant_url = cls._normalize_optional_string(
            variant.get("url"),
            field_name="variant.url",
        )

        variant_status = cls._normalize_status(
            variant.get("status"),
            field_name="variant.status",
        )

        source_car_document_id = cls._normalize_optional_string(
            variant_record.get("carDocumentId"),
            field_name=("variant_record.carDocumentId"),
        )

        source_car_run_id = cls._normalize_optional_string(
            variant_record.get("sourceCarRunId"),
            field_name=("variant_record.sourceCarRunId"),
        )

        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        return cls(
            _id=cls.build_document_id(
                variant_id=variant_id,
            ),
            brandId=brand_id,
            brandName=brand_name,
            brandSlug=brand_slug,
            modelId=model_id,
            modelName=model_name,
            modelSlug=model_slug,
            carSlug=car_slug,
            modelStatus=model_status,
            variantId=variant_id,
            variantName=variant_name,
            variantShortName=variant_short_name,
            variantSlug=variant_slug,
            variantUrl=variant_url,
            variantStatus=variant_status,
            featured=response_data.get("featured"),
            specification=response_data.get("specification"),
            sourceCarDocumentId=(source_car_document_id),
            sourceCarRunId=(source_car_run_id),
            lastRunId=normalized_run_id,
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
