from __future__ import annotations

import re
from collections.abc import (
    Iterator,
    Mapping,
)
from datetime import datetime, timezone
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

EXCLUDED_VERSION_FIELDS = frozenset(
    {
        "specsSummary",
        "featureSpecs",
    }
)


class CarWaleCarRequestContext(BaseModel):
    """
    Request parameters used when fetching the model-page
    response from CarWale.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )

    city_id: int | None = Field(
        default=None,
        alias="cityId",
        gt=0,
    )

    area_id: int | None = Field(
        default=None,
        alias="areaId",
        ge=0,
    )

    platform_id: int | None = Field(
        default=None,
        alias="platformId",
        gt=0,
    )

    show_offer_upfront: bool = Field(
        alias="showOfferUpfront",
    )


class CarWaleCarData(BaseModel):
    """
    Cleaned data returned by the CarWale model-page API.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

    model_details: dict[str, Any] = Field(
        alias="modelDetails",
    )

    replaced_model_details: dict[str, Any] | list[Any] | None = Field(
        default=None,
        alias="replacedModelDetails",
    )

    similar_cars: dict[str, Any] | list[Any] | None = Field(
        default=None,
        alias="similarCars",
    )

    versions: list[dict[str, Any]] = Field(
        default_factory=list,
    )

    @model_validator(
        mode="before",
    )
    @classmethod
    def normalize_data(
        cls,
        values: Any,
    ) -> Any:
        if not isinstance(
            values,
            Mapping,
        ):
            raise ValueError("CarWale car data must be an object")

        raw_model_details = values.get(
            "modelDetails",
            values.get("model_details"),
        )

        if not isinstance(
            raw_model_details,
            Mapping,
        ):
            raise ValueError("modelDetails must be an object")

        raw_replaced_model_details = values.get(
            "replacedModelDetails",
            values.get("replaced_model_details"),
        )

        if raw_replaced_model_details is not None and not isinstance(
            raw_replaced_model_details,
            (
                Mapping,
                list,
            ),
        ):
            raise ValueError("replacedModelDetails must be an object, array, or null")

        raw_similar_cars = values.get(
            "similarCars",
            values.get("similar_cars"),
        )

        if raw_similar_cars is not None and not isinstance(
            raw_similar_cars,
            (
                Mapping,
                list,
            ),
        ):
            raise ValueError("similarCars must be an object, array, or null")

        raw_versions = values.get("versions")

        if not isinstance(
            raw_versions,
            list,
        ):
            raise ValueError("versions must be an array")

        cleaned_versions: list[dict[str, Any]] = []

        seen_version_ids: set[int] = set()

        for index, raw_version in enumerate(raw_versions):
            if not isinstance(
                raw_version,
                Mapping,
            ):
                raise ValueError(f"versions contains an invalid record: index={index}")

            cleaned_version = {
                key: value
                for key, value in raw_version.items()
                if key not in EXCLUDED_VERSION_FIELDS
            }

            version_id = cleaned_version.get("versionId")

            if (
                isinstance(version_id, bool)
                or not isinstance(version_id, int)
                or version_id <= 0
            ):
                raise ValueError(
                    f"Version versionId must be a positive integer: index={index}"
                )

            if version_id in seen_version_ids:
                continue

            seen_version_ids.add(version_id)
            cleaned_version["versionId"] = version_id
            cleaned_versions.append(cleaned_version)

        return {
            "modelDetails": dict(raw_model_details),
            "replacedModelDetails": (
                dict(raw_replaced_model_details)
                if isinstance(
                    raw_replaced_model_details,
                    Mapping,
                )
                else raw_replaced_model_details
            ),
            "similarCars": (
                dict(raw_similar_cars)
                if isinstance(
                    raw_similar_cars,
                    Mapping,
                )
                else raw_similar_cars
            ),
            "versions": cleaned_versions,
        }

    def iter_versions(
        self,
    ) -> Iterator[dict[str, Any]]:
        yield from self.versions

    def get_version_ids(
        self,
    ) -> set[int]:
        version_ids: set[int] = set()

        for version in self.versions:
            version_id = version.get("versionId")

            if (
                isinstance(version_id, int)
                and not isinstance(
                    version_id,
                    bool,
                )
                and version_id > 0
            ):
                version_ids.add(version_id)

        return version_ids


class CarWaleCar(BaseModel):
    """
    MongoDB representation of one CarWale model-page
    response.

    One document represents one make-model combination.

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

    total_versions: int = Field(
        alias="totalVersions",
        ge=0,
    )

    data: CarWaleCarData

    request_context: CarWaleCarRequestContext = Field(
        alias="requestContext",
    )

    last_run_id: str = Field(
        alias="lastRunId",
        min_length=1,
    )

    source_model_run_id: str | None = Field(
        default=None,
        alias="sourceModelRunId",
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
    def validate_total_versions(
        self,
    ) -> Self:
        actual_total_versions = len(self.data.versions)

        if self.total_versions != actual_total_versions:
            raise ValueError(
                "totalVersions does not match "
                "the number of versions: "
                f"expected={actual_total_versions}, "
                f"found={self.total_versions}"
            )

        expected_document_id = self.build_document_id(
            make_id=self.make_id,
            model_id=self.model_id,
        )

        if self.document_id != expected_document_id:
            raise ValueError(
                "CarWale car document ID does not "
                "match makeId and modelId: "
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
    def _validate_non_negative_integer(
        value: Any,
        *,
        field_name: str,
    ) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{field_name} must be a non-negative integer")

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

    @classmethod
    def _normalize_optional_run_id(
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
        model: Mapping[str, Any],
        car_data: Mapping[str, Any],
        run_id: str,
        city_id: int | None = None,
        area_id: int | None = None,
        platform_id: int | None = None,
        show_offer_upfront: bool = False,
        source_model_run_id: str | None = None,
        created_at: datetime | None = None,
    ) -> Self:
        normalized_run_id = cls._validate_non_empty_string(
            run_id,
            field_name="run_id",
        )

        make_id = cls._validate_positive_integer(
            model.get("makeId"),
            field_name="model.makeId",
        )

        make_name = cls._validate_non_empty_string(
            model.get("makeName"),
            field_name="model.makeName",
        )

        make_masking_name = cls._validate_slug(
            model.get("makeMaskingName"),
            field_name=("model.makeMaskingName"),
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
            field_name=("model.modelMaskingName"),
        )

        normalized_city_id: int | None = None

        if city_id is not None:
            normalized_city_id = cls._validate_positive_integer(
                city_id,
                field_name="city_id",
            )

        normalized_area_id: int | None = None

        if area_id is not None:
            normalized_area_id = cls._validate_non_negative_integer(
                area_id,
                field_name="area_id",
            )

        normalized_platform_id: int | None = None

        if platform_id is not None:
            normalized_platform_id = cls._validate_positive_integer(
                platform_id,
                field_name="platform_id",
            )

        if not isinstance(
            show_offer_upfront,
            bool,
        ):
            raise ValueError("show_offer_upfront must be a boolean")

        resolved_source_model_run_id = source_model_run_id

        if resolved_source_model_run_id is None:
            resolved_source_model_run_id = model.get("lastRunId")

        normalized_source_model_run_id = cls._normalize_optional_run_id(
            resolved_source_model_run_id,
            field_name=("source_model_run_id"),
        )

        normalized_car_data = CarWaleCarData.model_validate(car_data)

        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        return cls(
            _id=cls.build_document_id(
                make_id=make_id,
                model_id=model_id,
            ),
            makeId=make_id,
            makeName=make_name,
            makeMaskingName=(make_masking_name),
            modelId=model_id,
            modelName=model_name,
            modelMaskingName=(model_masking_name),
            totalVersions=len(normalized_car_data.versions),
            data=normalized_car_data,
            requestContext=(
                CarWaleCarRequestContext(
                    cityId=normalized_city_id,
                    areaId=normalized_area_id,
                    platformId=(normalized_platform_id),
                    showOfferUpfront=(show_offer_upfront),
                )
            ),
            lastRunId=normalized_run_id,
            sourceModelRunId=(normalized_source_model_run_id),
            scrapedAt=current_time,
            createdAt=initial_created_at,
            updatedAt=current_time,
        )

    def get_version_ids(
        self,
    ) -> set[int]:
        return self.data.get_version_ids()

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        document = self.model_dump(
            by_alias=True,
            mode="python",
        )

        request_context = document.get("requestContext")

        if isinstance(request_context, dict):
            for field_name in (
                "cityId",
                "areaId",
                "platformId",
            ):
                if request_context.get(field_name) is None:
                    request_context.pop(field_name, None)

        return document
