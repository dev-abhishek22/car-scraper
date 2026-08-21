from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class BikeDekhoScooterTrimSpecsFeatures(BaseModel):
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
        pattern=SLUG_PATTERN.pattern,
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
        pattern=SLUG_PATTERN.pattern,
    )

    scooter_slug: str = Field(
        alias="scooterSlug",
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
        pattern=SLUG_PATTERN.pattern,
    )

    variant_url: str | None = Field(
        default=None,
        alias="variantUrl",
    )

    variant_status: str = Field(
        alias="variantStatus",
        min_length=1,
    )

    specs: Mapping[str, Any] = Field(
        default_factory=dict,
    )

    variant_table: Any = Field(
        default_factory=list,
        alias="variantTable",
    )

    source_scooter_document_id: str | None = Field(
        default=None,
        alias="sourceScooterDocumentId",
    )

    source_scooter_run_id: str | None = Field(
        default=None,
        alias="sourceScooterRunId",
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

    @staticmethod
    def build_document_id(
        variant_id: int,
    ) -> str:
        if (
            isinstance(variant_id, bool)
            or not isinstance(variant_id, int)
            or variant_id <= 0
        ):
            raise ValueError("variant_id must be a positive integer")

        return f"scooter-variant:{variant_id}"

    @staticmethod
    def _normalize_string(
        value: Any,
        *,
        field_name: str,
        required: bool = True,
    ) -> str | None:
        if value is None:
            if required:
                raise ValueError(f"{field_name} must be a string")

            return None

        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            if required:
                raise ValueError(f"{field_name} cannot be empty")

            return None

        return normalized_value

    @classmethod
    def _normalize_slug(
        cls,
        value: Any,
        *,
        field_name: str,
    ) -> str:
        normalized_value = cls._normalize_string(
            value,
            field_name=field_name,
        )

        if normalized_value is None:
            raise ValueError(f"{field_name} cannot be empty")

        normalized_value = normalized_value.lower()

        if not SLUG_PATTERN.fullmatch(normalized_value):
            raise ValueError(
                f"{field_name} contains invalid characters: " f"{normalized_value!r}"
            )

        return normalized_value

    @staticmethod
    def _validate_positive_integer(
        value: Any,
        *,
        field_name: str,
    ) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field_name} must be a positive integer")

        return value

    @classmethod
    def create(
        cls,
        *,
        variant_record: Mapping[str, Any],
        response_data: Mapping[str, Any],
        run_id: str,
        created_at: datetime | None = None,
    ) -> "BikeDekhoScooterTrimSpecsFeatures":
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

        normalized_run_id = cls._normalize_string(
            run_id,
            field_name="run_id",
        )

        if normalized_run_id is None:
            raise ValueError("run_id cannot be empty")

        brand_id = cls._validate_positive_integer(
            variant_record.get("brandId"),
            field_name="brandId",
        )

        brand_name = cls._normalize_string(
            variant_record.get("brandName"),
            field_name="brandName",
        )

        brand_slug = cls._normalize_slug(
            variant_record.get("brandSlug"),
            field_name="brandSlug",
        )

        model_id = cls._validate_positive_integer(
            variant_record.get("modelId"),
            field_name="modelId",
        )

        model_name = cls._normalize_string(
            variant_record.get("modelName"),
            field_name="modelName",
        )

        model_slug = cls._normalize_slug(
            variant_record.get("modelSlug"),
            field_name="modelSlug",
        )

        scooter_slug = cls._normalize_string(
            variant_record.get("scooterSlug"),
            field_name="scooterSlug",
        )

        model_status = cls._normalize_string(
            variant_record.get("modelStatus"),
            field_name="modelStatus",
        )

        variant_id = cls._validate_positive_integer(
            variant.get("variantId"),
            field_name="variant.variantId",
        )

        variant_name = (
            cls._normalize_string(
                variant.get("variantName"),
                field_name="variant.variantName",
                required=False,
            )
            or cls._normalize_string(
                variant.get("displayName"),
                field_name="variant.displayName",
                required=False,
            )
            or cls._normalize_string(
                variant.get("title"),
                field_name="variant.title",
                required=False,
            )
            or cls._normalize_string(
                variant.get("text"),
                field_name="variant.text",
                required=False,
            )
            or str(variant_id)
        )

        variant_short_name = (
            cls._normalize_string(
                variant.get("variantShortName"),
                field_name="variant.variantShortName",
                required=False,
            )
            or variant_name
        )

        variant_slug = cls._normalize_slug(
            variant.get("variantSlug"),
            field_name="variant.variantSlug",
        )

        variant_url = cls._normalize_string(
            variant.get("url"),
            field_name="variant.url",
            required=False,
        )

        variant_status = (
            cls._normalize_string(
                variant.get("variantStatus"),
                field_name="variant.variantStatus",
                required=False,
            )
            or cls._normalize_string(
                variant.get("status"),
                field_name="variant.status",
                required=False,
            )
            or model_status
        )

        source_scooter_document_id = cls._normalize_string(
            variant_record.get("scooterDocumentId"),
            field_name="scooterDocumentId",
            required=False,
        )

        source_scooter_run_id = cls._normalize_string(
            variant_record.get("sourceScooterRunId"),
            field_name="sourceScooterRunId",
            required=False,
        )

        data = response_data.get("data", {})

        if not isinstance(
            data,
            Mapping,
        ):
            raise ValueError("response_data.data must be an object")

        specs = data.get(
            "specs",
            {},
        )

        if not isinstance(
            specs,
            Mapping,
        ):
            raise ValueError("response_data.data.specs must be an object")

        variant_table = data.get(
            "variantTable",
            [],
        )

        if not isinstance(
            variant_table,
            (Mapping, list),
        ):
            raise ValueError(
                "response_data.data.variantTable must be an object or array"
            )

        now = datetime.now(timezone.utc)
        initial_created_at = created_at if created_at is not None else now

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
            scooterSlug=scooter_slug,
            modelStatus=model_status,
            variantId=variant_id,
            variantName=variant_name,
            variantShortName=variant_short_name,
            variantSlug=variant_slug,
            variantUrl=variant_url,
            variantStatus=variant_status,
            specs=specs,
            variantTable=variant_table,
            sourceScooterDocumentId=source_scooter_document_id,
            sourceScooterRunId=source_scooter_run_id,
            lastRunId=normalized_run_id,
            scrapedAt=now,
            createdAt=initial_created_at,
            updatedAt=now,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
