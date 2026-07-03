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

MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

STORAGE_FIELD_NAMES = {
    "_id",
    "lastRunId",
    "sourceBrandRunId",
    "scrapedAt",
    "createdAt",
    "updatedAt",
}


class CarWaleModel(BaseModel):
    """
    MongoDB representation of one CarWale model.

    Each model is stored as an individual document.

    Example document ID:

        model:10:124
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

    make_id: int = Field(
        alias="makeId",
        gt=0,
    )

    make_name: str = Field(
        alias="makeName",
        min_length=1,
    )

    make_masking_name: str = Field(
        alias="makeMaskingName",
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

    model_masking_name: str = Field(
        alias="modelMaskingName",
        min_length=1,
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
        """
        Rebuild the raw CarWale model payload when reading
        a flattened MongoDB document.

        The raw API fields are stored at the document's top
        level instead of inside a nested `data` object.
        """
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

    @classmethod
    def _validate_slug(
        cls,
        value: Any,
        *,
        field_name: str,
    ) -> str:
        normalized_value = cls._validate_non_empty_string(
            value,
            field_name=field_name,
        ).lower()

        if not MASKING_NAME_PATTERN.fullmatch(normalized_value):
            raise ValueError(
                f"{field_name} contains invalid characters: {normalized_value!r}"
            )

        return normalized_value

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
            raise ValueError("source_brand_run_id must be a string")

        normalized_value = value.strip()

        return normalized_value or None

    @staticmethod
    def build_document_id(
        *,
        make_id: int,
        model_id: int,
    ) -> str:
        if isinstance(make_id, bool) or not isinstance(make_id, int) or make_id <= 0:
            raise ValueError("make_id must be a positive integer")

        if isinstance(model_id, bool) or not isinstance(model_id, int) or model_id <= 0:
            raise ValueError("model_id must be a positive integer")

        return f"model:{make_id}:{model_id}"

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

        make_id = cls._validate_positive_integer(
            brand.get("makeId"),
            field_name="brand.makeId",
        )

        make_name = cls._validate_non_empty_string(
            brand.get("makeName"),
            field_name="brand.makeName",
        )

        make_masking_name = cls._validate_slug(
            brand.get("maskingName"),
            field_name="brand.maskingName",
        )

        model_id = cls._validate_positive_integer(
            model.get("modelId"),
            field_name="model.modelId",
        )

        model_name = cls._validate_non_empty_string(
            model.get("modelName"),
            field_name="model.modelName",
        )

        model_masking_name = cls._validate_slug(
            model.get("modelMaskingName"),
            field_name="model.modelMaskingName",
        )

        model_make_id = model.get("makeId")

        if model_make_id is not None:
            normalized_model_make_id = cls._validate_positive_integer(
                model_make_id,
                field_name="model.makeId",
            )

            if normalized_model_make_id != make_id:
                raise ValueError(
                    "Model makeId does not match the "
                    "parent brand: "
                    f"expected={make_id}, "
                    f"found={normalized_model_make_id}"
                )

        model_make_masking_name = model.get("makeMaskingName")

        if model_make_masking_name is not None:
            normalized_model_make_masking_name = cls._validate_slug(
                model_make_masking_name,
                field_name=("model.makeMaskingName"),
            )

            if normalized_model_make_masking_name != make_masking_name:
                raise ValueError(
                    "Model makeMaskingName does not "
                    "match the parent brand: "
                    f"expected={make_masking_name!r}, "
                    "found="
                    f"{normalized_model_make_masking_name!r}"
                )

        resolved_source_brand_run_id = source_brand_run_id

        if resolved_source_brand_run_id is None:
            resolved_source_brand_run_id = brand.get("lastRunId")

        normalized_source_brand_run_id = cls._normalize_optional_run_id(
            resolved_source_brand_run_id
        )

        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        raw_data = dict(model)

        raw_data.update(
            {
                "makeId": make_id,
                "makeName": make_name,
                "makeMaskingName": (make_masking_name),
                "modelId": model_id,
                "modelName": model_name,
                "modelMaskingName": (model_masking_name),
            }
        )

        return cls(
            _id=cls.build_document_id(
                make_id=make_id,
                model_id=model_id,
            ),
            makeId=make_id,
            makeName=make_name,
            makeMaskingName=make_masking_name,
            modelId=model_id,
            modelName=model_name,
            modelMaskingName=model_masking_name,
            data=raw_data,
            lastRunId=normalized_run_id,
            sourceBrandRunId=(normalized_source_brand_run_id),
            scrapedAt=current_time,
            createdAt=initial_created_at,
            updatedAt=current_time,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        """
        Flatten the complete CarWale model payload into
        the MongoDB document.

        Canonical identity and tracking fields override
        any conflicting fields from the external API.
        """
        document = dict(self.data)

        document.update(
            {
                "_id": self.document_id,
                "makeId": self.make_id,
                "makeName": self.make_name,
                "makeMaskingName": (self.make_masking_name),
                "modelId": self.model_id,
                "modelName": self.model_name,
                "modelMaskingName": (self.model_masking_name),
                "lastRunId": self.last_run_id,
                "sourceBrandRunId": (self.source_brand_run_id),
                "scrapedAt": self.scraped_at,
                "createdAt": self.created_at,
                "updatedAt": self.updated_at,
            }
        )

        return document
