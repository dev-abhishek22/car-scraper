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

CITY_MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

STORAGE_FIELD_NAMES = {
    "_id",
    "lastRunId",
    "scrapedAt",
    "createdAt",
    "updatedAt",
}

KNOWN_API_FIELD_NAMES = {
    "CityId",
    "CityName",
    "StateId",
    "IsDeleted",
    "Lattitude",
    "Latitude",
    "Longitude",
    "StdCode",
    "IsPopular",
    "CityEntryDate",
    "CityMaskingName",
    "BWCityOrder",
    "StateName",
}


class CarWaleCity(BaseModel):
    """
    MongoDB representation of one CarWale city.

    Example document ID:

        city:1
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

    state_id: int = Field(
        alias="stateId",
        gt=0,
    )

    is_deleted: bool = Field(
        alias="isDeleted",
    )

    latitude: float | None = None

    longitude: float | None = None

    std_code: int | str | None = Field(
        default=None,
        alias="stdCode",
    )

    is_popular: bool = Field(
        alias="isPopular",
    )

    city_entry_date: str | None = Field(
        default=None,
        alias="cityEntryDate",
    )

    city_masking_name: str = Field(
        alias="cityMaskingName",
        min_length=1,
    )

    bw_city_order: int = Field(
        alias="bwCityOrder",
        ge=0,
    )

    state_name: str = Field(
        alias="stateName",
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
    def rebuild_data(
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
    def validate_document_identity(
        self,
    ) -> Self:
        expected_document_id = self.build_document_id(
            city_id=self.city_id,
        )

        if self.document_id != expected_document_id:
            raise ValueError(
                "CarWale city document ID does not match "
                "cityId: "
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

        if not CITY_MASKING_NAME_PATTERN.fullmatch(normalized_value):
            raise ValueError(
                f"{field_name} contains invalid characters: {normalized_value!r}"
            )

        return normalized_value

    @staticmethod
    def _normalize_optional_coordinate(
        value: Any,
        *,
        field_name: str,
        minimum: float,
        maximum: float,
    ) -> float | None:
        if value is None:
            return None

        if isinstance(value, bool) or not isinstance(
            value,
            (int, float),
        ):
            raise ValueError(f"{field_name} must be a number or null")

        normalized_value = float(value)

        if not minimum <= normalized_value <= maximum:
            raise ValueError(f"{field_name} must be between {minimum} and {maximum}")

        return normalized_value

    @staticmethod
    def _normalize_std_code(
        value: Any,
    ) -> int | str | None:
        if value is None:
            return None

        if isinstance(value, bool):
            raise ValueError("StdCode must be an integer, string, or null")

        if isinstance(value, int):
            if value < 0:
                raise ValueError("StdCode cannot be negative")

            return value

        if isinstance(value, str):
            normalized_value = value.strip()

            if not normalized_value:
                return None

            if normalized_value.isdigit():
                return int(normalized_value)

            return normalized_value

        raise ValueError("StdCode must be an integer, string, or null")

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

    @staticmethod
    def build_document_id(
        *,
        city_id: int,
    ) -> str:
        if isinstance(city_id, bool) or not isinstance(city_id, int) or city_id <= 0:
            raise ValueError("city_id must be a positive integer")

        return f"city:{city_id}"

    @classmethod
    def create(
        cls,
        *,
        city: Mapping[str, Any],
        run_id: str,
        created_at: datetime | None = None,
    ) -> Self:
        if not isinstance(
            city,
            Mapping,
        ):
            raise ValueError("city must be an object")

        normalized_run_id = cls._validate_non_empty_string(
            run_id,
            field_name="run_id",
        )

        city_id = cls._validate_positive_integer(
            city.get("CityId"),
            field_name="city.CityId",
        )

        city_name = cls._validate_non_empty_string(
            city.get("CityName"),
            field_name="city.CityName",
        )

        state_id = cls._validate_positive_integer(
            city.get("StateId"),
            field_name="city.StateId",
        )

        is_deleted = city.get("IsDeleted")

        if not isinstance(
            is_deleted,
            bool,
        ):
            raise ValueError("city.IsDeleted must be a boolean")

        latitude = cls._normalize_optional_coordinate(
            city.get(
                "Lattitude",
                city.get("Latitude"),
            ),
            field_name="city.Lattitude",
            minimum=-90.0,
            maximum=90.0,
        )

        longitude = cls._normalize_optional_coordinate(
            city.get("Longitude"),
            field_name="city.Longitude",
            minimum=-180.0,
            maximum=180.0,
        )

        std_code = cls._normalize_std_code(city.get("StdCode"))

        is_popular = city.get("IsPopular")

        if not isinstance(
            is_popular,
            bool,
        ):
            raise ValueError("city.IsPopular must be a boolean")

        city_entry_date = cls._normalize_optional_string(
            city.get("CityEntryDate"),
            field_name="city.CityEntryDate",
        )

        city_masking_name = cls._validate_masking_name(
            city.get("CityMaskingName"),
            field_name="city.CityMaskingName",
        )

        bw_city_order = cls._validate_non_negative_integer(
            city.get("BWCityOrder"),
            field_name="city.BWCityOrder",
        )

        state_name = cls._validate_non_empty_string(
            city.get("StateName"),
            field_name="city.StateName",
        )

        current_time = datetime.now(timezone.utc)

        initial_created_at = created_at if created_at is not None else current_time

        raw_data = {
            key: value
            for key, value in city.items()
            if key not in KNOWN_API_FIELD_NAMES
        }

        raw_data.update(
            {
                "cityId": city_id,
                "cityName": city_name,
                "stateId": state_id,
                "isDeleted": is_deleted,
                "latitude": latitude,
                "longitude": longitude,
                "stdCode": std_code,
                "isPopular": is_popular,
                "cityEntryDate": city_entry_date,
                "cityMaskingName": city_masking_name,
                "bwCityOrder": bw_city_order,
                "stateName": state_name,
            }
        )

        return cls(
            _id=cls.build_document_id(
                city_id=city_id,
            ),
            cityId=city_id,
            cityName=city_name,
            stateId=state_id,
            isDeleted=is_deleted,
            latitude=latitude,
            longitude=longitude,
            stdCode=std_code,
            isPopular=is_popular,
            cityEntryDate=city_entry_date,
            cityMaskingName=city_masking_name,
            bwCityOrder=bw_city_order,
            stateName=state_name,
            data=raw_data,
            lastRunId=normalized_run_id,
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
                "cityId": self.city_id,
                "cityName": self.city_name,
                "stateId": self.state_id,
                "isDeleted": self.is_deleted,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "stdCode": self.std_code,
                "isPopular": self.is_popular,
                "cityEntryDate": self.city_entry_date,
                "cityMaskingName": (self.city_masking_name),
                "bwCityOrder": self.bw_city_order,
                "stateName": self.state_name,
                "lastRunId": self.last_run_id,
                "scrapedAt": self.scraped_at,
                "createdAt": self.created_at,
                "updatedAt": self.updated_at,
            }
        )

        return document
