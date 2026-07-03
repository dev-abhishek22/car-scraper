from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Literal, Self, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

ModelStatus = Literal[
    "CURRENT",
    "UPCOMING",
    "DISCONTINUED",
]

STORAGE_FIELD_NAMES = {
    "_id",
    "lastRunId",
    "sourceBrandRunId",
    "sourceBrandDocumentId",
    "scrapedAt",
    "createdAt",
    "updatedAt",
}


class CarDekhoModel(BaseModel):
    """
    MongoDB representation of one CarDekho model.

    Example document ID:

        model:3289
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
        alias="id",
        gt=0,
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

    name: str = Field(
        min_length=1,
    )

    slug: str = Field(
        min_length=1,
    )

    model_name: str = Field(
        alias="modelName",
        min_length=1,
    )

    model_status: ModelStatus = Field(
        alias="modelStatus",
    )

    is_upcoming: bool = Field(
        alias="isUpcoming",
    )

    expected_launch_date: str | None = Field(
        default=None,
        alias="expectedLaunchDate",
    )

    data: dict[str, Any] = Field(
        default_factory=dict,
        exclude=True,
    )

    last_run_id: str = Field(
        alias="lastRunId",
        min_length=1,
    )

    source_brand_run_id: str | None = Field(
        default=None,
        alias="sourceBrandRunId",
    )

    source_brand_document_id: str = Field(
        alias="sourceBrandDocumentId",
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
    def rebuild_raw_data(
        cls,
        values: Any,
    ) -> Any:
        if not isinstance(
            values,
            Mapping,
        ):
            return values

        normalized_values = dict(values)

        existing_data = normalized_values.get("data")

        if isinstance(
            existing_data,
            Mapping,
        ):
            normalized_values["data"] = dict(existing_data)

            return normalized_values

        normalized_values["data"] = {
            key: value
            for key, value in normalized_values.items()
            if key not in STORAGE_FIELD_NAMES
        }

        return normalized_values

    @model_validator(
        mode="after",
    )
    def validate_status_fields(
        self,
    ) -> Self:
        expected_is_upcoming = self.model_status == "UPCOMING"

        if self.is_upcoming != expected_is_upcoming:
            raise ValueError(
                "isUpcoming does not match " f"modelStatus={self.model_status!r}"
            )

        if (
            self.model_status
            in {
                "CURRENT",
                "DISCONTINUED",
            }
            and self.expected_launch_date is not None
        ):
            raise ValueError(
                "Current and discontinued models " "cannot have an expectedLaunchDate"
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
        if not isinstance(
            value,
            str,
        ):
            raise ValueError(f"{field_name} must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        return normalized_value

    @staticmethod
    def _normalize_optional_string(
        value: Any,
        *,
        field_name: str,
    ) -> str | None:
        if value is None:
            return None

        if not isinstance(
            value,
            str,
        ):
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

    @staticmethod
    def _validate_boolean(
        value: Any,
        *,
        field_name: str,
    ) -> bool:
        if not isinstance(
            value,
            bool,
        ):
            raise ValueError(f"{field_name} must be a boolean")

        return value

    @staticmethod
    def _validate_model_status(
        value: Any,
    ) -> ModelStatus:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError("model.modelStatus must be a string")

        normalized_status = value.strip().upper()

        if normalized_status not in {
            "CURRENT",
            "UPCOMING",
            "DISCONTINUED",
        }:
            raise ValueError(
                "model.modelStatus must be CURRENT, " "UPCOMING, or DISCONTINUED"
            )

        return cast(
            ModelStatus,
            normalized_status,
        )

    @staticmethod
    def _normalize_optional_run_id(
        value: Any,
    ) -> str | None:
        if value is None:
            return None

        if not isinstance(
            value,
            str,
        ):
            raise ValueError("source_brand_run_id must be a " "string or null")

        normalized_value = value.strip()

        return normalized_value or None

    @staticmethod
    def build_document_id(
        model_id: int,
    ) -> str:
        if isinstance(model_id, bool) or not isinstance(model_id, int) or model_id <= 0:
            raise ValueError("model_id must be a positive integer")

        return f"model:{model_id}"

    @classmethod
    def create(
        cls,
        *,
        brand: Mapping[str, Any],
        model: Mapping[str, Any],
        run_id: str,
        source_brand_run_id: str | None = None,
        created_at: datetime | None = None,
    ) -> Self:
        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        source_brand_slug = cls._validate_slug(
            brand.get("slug"),
            field_name="brand.slug",
        )

        model_request_slug = cls._validate_slug(
            brand.get("modelRequestSlug"),
            field_name="brand.modelRequestSlug",
        )

        model_id = cls._validate_positive_integer(
            model.get("id"),
            field_name="model.id",
        )

        brand_id = cls._validate_positive_integer(
            model.get("brandId"),
            field_name="model.brandId",
        )

        brand_name = cls._validate_non_empty_string(
            model.get("brandName"),
            field_name="model.brandName",
        )

        brand_slug = cls._validate_slug(
            model.get("brandSlug"),
            field_name="model.brandSlug",
        )

        accepted_brand_slugs = {
            source_brand_slug,
            model_request_slug,
        }

        if brand_slug not in accepted_brand_slugs:
            raise ValueError(
                "Model brandSlug does not match the "
                "source brand: "
                f"expected_one_of="
                f"{sorted(accepted_brand_slugs)!r}, "
                f"found={brand_slug!r}"
            )

        name = cls._validate_non_empty_string(
            model.get("name"),
            field_name="model.name",
        )

        slug = cls._validate_slug(
            model.get("slug"),
            field_name="model.slug",
        )

        model_name = cls._validate_non_empty_string(
            model.get("modelName"),
            field_name="model.modelName",
        )

        model_status = cls._validate_model_status(model.get("modelStatus"))

        is_upcoming = cls._validate_boolean(
            model.get("isUpcoming"),
            field_name="model.isUpcoming",
        )

        expected_is_upcoming = model_status == "UPCOMING"

        if is_upcoming != expected_is_upcoming:
            raise ValueError(
                "Model isUpcoming does not match " f"modelStatus={model_status!r}"
            )

        expected_launch_date = cls._normalize_optional_string(
            model.get("expectedLaunchDate"),
            field_name=("model.expectedLaunchDate"),
        )

        if (
            model_status
            in {
                "CURRENT",
                "DISCONTINUED",
            }
            and expected_launch_date is not None
        ):
            raise ValueError(
                "Current and discontinued models " "cannot have an expectedLaunchDate"
            )

        resolved_source_brand_run_id = source_brand_run_id

        if resolved_source_brand_run_id is None:
            resolved_source_brand_run_id = brand.get("lastRunId")

        normalized_source_brand_run_id = cls._normalize_optional_run_id(
            resolved_source_brand_run_id
        )

        source_brand_document_id = brand.get("_id")

        if (
            not isinstance(
                source_brand_document_id,
                str,
            )
            or not source_brand_document_id.strip()
        ):
            source_brand_document_id = f"brand:{source_brand_slug}"
        else:
            source_brand_document_id = source_brand_document_id.strip()

        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        raw_data: dict[str, Any] = {
            "id": model_id,
            "brandId": brand_id,
            "brandName": brand_name,
            "brandSlug": brand_slug,
            "name": name,
            "slug": slug,
            "modelName": model_name,
            "modelStatus": model_status,
            "isUpcoming": is_upcoming,
        }

        if expected_launch_date is not None:
            raw_data["expectedLaunchDate"] = expected_launch_date

        return cls(
            _id=cls.build_document_id(model_id),
            id=model_id,
            brandId=brand_id,
            brandName=brand_name,
            brandSlug=brand_slug,
            name=name,
            slug=slug,
            modelName=model_name,
            modelStatus=model_status,
            isUpcoming=is_upcoming,
            expectedLaunchDate=(expected_launch_date),
            data=raw_data,
            lastRunId=normalized_run_id,
            sourceBrandRunId=(normalized_source_brand_run_id),
            sourceBrandDocumentId=(source_brand_document_id),
            scrapedAt=current_time,
            createdAt=initial_created_at,
            updatedAt=current_time,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        document = dict(self.data)

        document.update(
            {
                "_id": self.document_id,
                "id": self.model_id,
                "brandId": self.brand_id,
                "brandName": self.brand_name,
                "brandSlug": self.brand_slug,
                "name": self.name,
                "slug": self.slug,
                "modelName": self.model_name,
                "modelStatus": self.model_status,
                "isUpcoming": self.is_upcoming,
                "lastRunId": self.last_run_id,
                "sourceBrandRunId": (self.source_brand_run_id),
                "sourceBrandDocumentId": (self.source_brand_document_id),
                "scrapedAt": self.scraped_at,
                "createdAt": self.created_at,
                "updatedAt": self.updated_at,
            }
        )

        if self.expected_launch_date is not None:
            document["expectedLaunchDate"] = self.expected_launch_date
        else:
            document.pop(
                "expectedLaunchDate",
                None,
            )

        return document
