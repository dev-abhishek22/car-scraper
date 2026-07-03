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


class CarWaleTrimSpecsFeatures(BaseModel):
    """
    MongoDB representation of one CarWale version's
    trim details, specifications, and features.

    One document represents one unique versionId.

    Example document ID:

        version:23115
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

    trim_id: int = Field(
        alias="trimId",
        gt=0,
    )

    trim_name: str = Field(
        alias="trimName",
        min_length=1,
    )

    trim_masking_name: str = Field(
        alias="trimMaskingName",
        min_length=1,
    )

    version_id: int = Field(
        alias="versionId",
        gt=0,
    )

    version_name: str = Field(
        alias="versionName",
        min_length=1,
    )

    version_masking_name: str = Field(
        alias="versionMaskingName",
        min_length=1,
    )

    version_detail: Any = Field(
        default=None,
        alias="versionDetail",
    )

    trim_detail: Any = Field(
        default=None,
        alias="trimDetail",
    )

    specifications: Any = None

    features: Any = None

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
            version_id=self.version_id,
        )

        if self.document_id != expected_document_id:
            raise ValueError(
                "CarWale trim specs/features document ID "
                "does not match versionId: "
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
    def _validate_masking_name(
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

    @classmethod
    def _normalize_optional_string(
        cls,
        value: Any,
        *,
        field_name: str,
    ) -> str | None:
        if value is None:
            return None

        return cls._validate_non_empty_string(
            value,
            field_name=field_name,
        )

    @staticmethod
    def build_document_id(
        *,
        version_id: int,
    ) -> str:
        if (
            isinstance(version_id, bool)
            or not isinstance(version_id, int)
            or version_id <= 0
        ):
            raise ValueError("version_id must be a positive integer")

        return f"version:{version_id}"

    @classmethod
    def create(
        cls,
        *,
        version_record: Mapping[str, Any],
        response_data: Mapping[str, Any],
        run_id: str,
        created_at: datetime | None = None,
    ) -> Self:
        if not isinstance(
            version_record,
            Mapping,
        ):
            raise ValueError("version_record must be an object")

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ValueError("response_data must be an object")

        version = version_record.get("version")

        if not isinstance(
            version,
            Mapping,
        ):
            raise ValueError("version_record.version must be an object")

        normalized_run_id = cls._validate_non_empty_string(
            run_id,
            field_name="run_id",
        )

        make_id = cls._validate_positive_integer(
            version_record.get("makeId"),
            field_name="version_record.makeId",
        )

        make_name = cls._validate_non_empty_string(
            version_record.get("makeName"),
            field_name="version_record.makeName",
        )

        make_masking_name = cls._validate_masking_name(
            version_record.get("makeMaskingName"),
            field_name=("version_record.makeMaskingName"),
        )

        model_id = cls._validate_positive_integer(
            version_record.get("modelId"),
            field_name="version_record.modelId",
        )

        model_name = cls._validate_non_empty_string(
            version_record.get("modelName"),
            field_name="version_record.modelName",
        )

        model_masking_name = cls._validate_masking_name(
            version_record.get("modelMaskingName"),
            field_name=("version_record.modelMaskingName"),
        )

        trim_id = cls._validate_positive_integer(
            version.get("trimId"),
            field_name="version.trimId",
        )

        trim_name = cls._validate_non_empty_string(
            version.get("trimName"),
            field_name="version.trimName",
        )

        trim_masking_name = cls._validate_masking_name(
            version.get("trimMaskingName"),
            field_name=("version.trimMaskingName"),
        )

        version_id = cls._validate_positive_integer(
            version.get("versionId"),
            field_name="version.versionId",
        )

        version_name = cls._validate_non_empty_string(
            version.get("versionName"),
            field_name="version.versionName",
        )

        version_masking_name = cls._validate_masking_name(
            version.get("versionMaskingName"),
            field_name=("version.versionMaskingName"),
        )

        source_car_document_id = cls._normalize_optional_string(
            version_record.get("carDocumentId"),
            field_name=("version_record.carDocumentId"),
        )

        source_car_run_id = cls._normalize_optional_string(
            version_record.get("sourceCarRunId"),
            field_name=("version_record.sourceCarRunId"),
        )

        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        return cls(
            _id=cls.build_document_id(
                version_id=version_id,
            ),
            makeId=make_id,
            makeName=make_name,
            makeMaskingName=make_masking_name,
            modelId=model_id,
            modelName=model_name,
            modelMaskingName=(model_masking_name),
            trimId=trim_id,
            trimName=trim_name,
            trimMaskingName=(trim_masking_name),
            versionId=version_id,
            versionName=version_name,
            versionMaskingName=(version_masking_name),
            versionDetail=response_data.get("versionDetail"),
            trimDetail=response_data.get("trimDetail"),
            specifications=response_data.get("specifications"),
            features=response_data.get("features"),
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
