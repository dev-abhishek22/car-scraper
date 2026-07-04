from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


def _validate_positive_integer(
    value: Any,
    *,
    field_name: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")

    return value


def _validate_boolean(
    value: Any,
    *,
    field_name: str,
) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a boolean")

    return value


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


def _normalize_string_list(
    value: Any,
    *,
    field_name: str,
) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be an array")

    normalized_values: list[str] = []
    seen_values: set[str] = set()

    for index, item in enumerate(value):
        normalized_item = _validate_non_empty_string(
            item,
            field_name=(f"{field_name}[{index}]"),
        )

        comparison_value = normalized_item.casefold()

        if comparison_value in seen_values:
            continue

        seen_values.add(comparison_value)

        normalized_values.append(normalized_item)

    if not normalized_values:
        raise ValueError(f"{field_name} cannot be empty")

    return normalized_values


class CarDekhoCityRegion(BaseModel):
    """
    One CarDekho city region.

    Regions are available only for some major cities.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    region_id: int = Field(
        alias="regionId",
        gt=0,
    )

    region_name: str = Field(
        alias="regionName",
        min_length=1,
    )

    @field_validator(
        "region_name",
        mode="before",
    )
    @classmethod
    def normalize_region_name(
        cls,
        value: Any,
    ) -> str:
        return _validate_non_empty_string(
            value,
            field_name="regionName",
        )


class CarDekhoCity(BaseModel):
    """
    MongoDB representation of one normalized
    CarDekho city.

    Multiple source rows with the same CID are merged
    into one document.

    Example document ID:

        city:105
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

    city_id: int = Field(
        alias="cityId",
        gt=0,
    )

    city_name: str = Field(
        alias="cityName",
        min_length=1,
    )

    display_name: str = Field(
        alias="displayName",
        min_length=1,
    )

    aliases: list[str] = Field(
        default_factory=list,
    )

    is_popular: bool = Field(
        alias="isPopular",
    )

    is_prime: bool = Field(
        alias="isPrime",
    )

    regions: list[CarDekhoCityRegion] = Field(
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

    @field_validator(
        "city_name",
        mode="before",
    )
    @classmethod
    def normalize_city_name(
        cls,
        value: Any,
    ) -> str:
        return _validate_non_empty_string(
            value,
            field_name="cityName",
        )

    @field_validator(
        "display_name",
        mode="before",
    )
    @classmethod
    def normalize_display_name(
        cls,
        value: Any,
    ) -> str:
        return _validate_non_empty_string(
            value,
            field_name="displayName",
        )

    @field_validator(
        "aliases",
        mode="before",
    )
    @classmethod
    def normalize_aliases(
        cls,
        value: Any,
    ) -> list[str]:
        return _normalize_string_list(
            value,
            field_name="aliases",
        )

    @field_validator(
        "last_run_id",
        mode="before",
    )
    @classmethod
    def normalize_last_run_id(
        cls,
        value: Any,
    ) -> str:
        return _validate_non_empty_string(
            value,
            field_name="lastRunId",
        )

    @model_validator(
        mode="after",
    )
    def validate_document(
        self,
    ) -> Self:
        expected_document_id = self.build_document_id(self.city_id)

        if self.document_id != expected_document_id:
            raise ValueError(
                "CarDekho city document ID does not "
                "match cityId: "
                f"expected={expected_document_id!r}, "
                f"found={self.document_id!r}"
            )

        alias_values = {alias.casefold() for alias in self.aliases}

        if self.city_name.casefold() not in alias_values:
            raise ValueError("cityName must be included in aliases")

        if self.display_name.casefold() not in alias_values:
            raise ValueError("displayName must be included in aliases")

        seen_region_ids: set[int] = set()

        for region in self.regions:
            if region.region_id in seen_region_ids:
                raise ValueError(
                    f"regions contains duplicate regionId={region.region_id}"
                )

            seen_region_ids.add(region.region_id)

        return self

    @staticmethod
    def build_document_id(
        city_id: int,
    ) -> str:
        normalized_city_id = _validate_positive_integer(
            city_id,
            field_name="city_id",
        )

        return f"city:{normalized_city_id}"

    @classmethod
    def create(
        cls,
        *,
        city_data: Mapping[str, Any],
        run_id: str,
        created_at: datetime | None = None,
    ) -> Self:
        if not isinstance(
            city_data,
            Mapping,
        ):
            raise ValueError("city_data must be an object")

        normalized_run_id = _validate_non_empty_string(
            run_id,
            field_name="run_id",
        )

        city_id = _validate_positive_integer(
            city_data.get("cityId"),
            field_name="city_data.cityId",
        )

        city_name = _validate_non_empty_string(
            city_data.get("cityName"),
            field_name=("city_data.cityName"),
        )

        display_name = _validate_non_empty_string(
            city_data.get("displayName"),
            field_name=("city_data.displayName"),
        )

        aliases = _normalize_string_list(
            city_data.get("aliases"),
            field_name="city_data.aliases",
        )

        is_popular = _validate_boolean(
            city_data.get("isPopular"),
            field_name=("city_data.isPopular"),
        )

        is_prime = _validate_boolean(
            city_data.get("isPrime"),
            field_name="city_data.isPrime",
        )

        raw_regions = city_data.get(
            "regions",
            [],
        )

        if not isinstance(raw_regions, list):
            raise ValueError("city_data.regions must be an array")

        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        return cls(
            _id=cls.build_document_id(city_id),
            cityId=city_id,
            cityName=city_name,
            displayName=display_name,
            aliases=aliases,
            isPopular=is_popular,
            isPrime=is_prime,
            regions=raw_regions,
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
