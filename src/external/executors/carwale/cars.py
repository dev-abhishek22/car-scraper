from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from src.clients.async_client import (
    AsyncExternalHttpClient,
)
from src.clients.client import (
    ExternalResponseError,
)
from src.external.constants.carwale import (
    CARWALE_BASE_URL,
    CARWALE_MODEL_PAGE_DATA,
)
from src.logger.logger import logger_service

MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

EXCLUDED_VERSION_FIELDS = frozenset(
    {
        "specsSummary",
        "featureSpecs",
    }
)


class CarWaleCarsExecutor:
    """Fetch and validate detailed CarWale model-page data."""

    def __init__(
        self,
        client: AsyncExternalHttpClient,
    ) -> None:
        self._client = client

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
        if not isinstance(value, str):
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
    def _validate_model(
        cls,
        model: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(model, Mapping):
            raise ValueError("model must be an object")

        return {
            "makeId": cls._validate_positive_integer(
                model.get("makeId"),
                field_name="model.makeId",
            ),
            "makeName": cls._validate_non_empty_string(
                model.get("makeName"),
                field_name="model.makeName",
            ),
            "makeMaskingName": cls._validate_masking_name(
                model.get("makeMaskingName"),
                field_name="model.makeMaskingName",
            ),
            "modelId": cls._validate_positive_integer(
                model.get("modelId"),
                field_name="model.modelId",
            ),
            "modelName": cls._validate_non_empty_string(
                model.get("modelName"),
                field_name="model.modelName",
            ),
            "modelMaskingName": cls._validate_masking_name(
                model.get("modelMaskingName"),
                field_name="model.modelMaskingName",
            ),
        }

    @staticmethod
    def _validate_page_validation(
        response: Mapping[str, Any],
        *,
        make_masking_name: str,
        model_masking_name: str,
    ) -> None:
        page_validation = response.get("pageValidation")

        if page_validation is None:
            return

        if not isinstance(page_validation, Mapping):
            raise ExternalResponseError(
                "CarWale model-page API returned invalid pageValidation: "
                f"make={make_masking_name!r}, model={model_masking_name!r}"
            )

        is_valid = page_validation.get("isValid")

        if is_valid is False:
            raise ExternalResponseError(
                "CarWale model page failed page validation: "
                f"make={make_masking_name!r}, model={model_masking_name!r}"
            )

    @staticmethod
    def _get_required_mapping_section(
        response: Mapping[str, Any],
        *,
        field_name: str,
        make_masking_name: str,
        model_masking_name: str,
    ) -> dict[str, Any]:
        value = response.get(field_name)

        if not isinstance(value, Mapping):
            raise ExternalResponseError(
                f"CarWale response does not contain a valid {field_name} object: "
                f"make={make_masking_name!r}, model={model_masking_name!r}"
            )

        return dict(value)

    @staticmethod
    def _get_optional_json_section(
        response: Mapping[str, Any],
        *,
        field_name: str,
        make_masking_name: str,
        model_masking_name: str,
    ) -> dict[str, Any] | list[Any] | None:
        value = response.get(field_name)

        if value is None:
            return None

        if isinstance(value, Mapping):
            return dict(value)

        if isinstance(value, list):
            return list(value)

        raise ExternalResponseError(
            f"CarWale response contains invalid {field_name}: "
            f"make={make_masking_name!r}, model={model_masking_name!r}"
        )

    @classmethod
    def _clean_versions(
        cls,
        response: Mapping[str, Any],
        *,
        make_masking_name: str,
        model_masking_name: str,
    ) -> list[dict[str, Any]]:
        raw_versions = response.get("versions")

        if not isinstance(raw_versions, list):
            raise ExternalResponseError(
                "CarWale response does not contain a valid versions array: "
                f"make={make_masking_name!r}, model={model_masking_name!r}"
            )

        cleaned_versions: list[dict[str, Any]] = []
        seen_version_ids: set[int] = set()

        for index, raw_version in enumerate(raw_versions):
            if not isinstance(raw_version, Mapping):
                raise ExternalResponseError(
                    "CarWale versions contains an invalid record: "
                    f"index={index}, make={make_masking_name!r}, "
                    f"model={model_masking_name!r}"
                )

            cleaned_version = {
                key: value
                for key, value in raw_version.items()
                if key not in EXCLUDED_VERSION_FIELDS
            }

            version_id = cls._validate_positive_integer(
                cleaned_version.get("versionId"),
                field_name=f"versions[{index}].versionId",
            )

            if version_id in seen_version_ids:
                continue

            seen_version_ids.add(version_id)
            cleaned_versions.append(cleaned_version)

        return cleaned_versions

    @classmethod
    def _validate_response_identity(
        cls,
        *,
        model_details: Mapping[str, Any],
        expected_make_masking_name: str,
        expected_model_id: int,
        expected_model_masking_name: str,
    ) -> None:
        response_make_masking_name = model_details.get("makeMaskingName")

        if response_make_masking_name is not None:
            normalized_make_masking_name = cls._validate_masking_name(
                response_make_masking_name,
                field_name="modelDetails.makeMaskingName",
            )

            if normalized_make_masking_name != expected_make_masking_name:
                raise ExternalResponseError(
                    "CarWale response make identity does not match the request"
                )

        response_model_id = model_details.get("modelId")

        if response_model_id is not None:
            normalized_model_id = cls._validate_positive_integer(
                response_model_id,
                field_name="modelDetails.modelId",
            )

            if normalized_model_id != expected_model_id:
                raise ExternalResponseError(
                    "CarWale response model ID does not match the request"
                )

        response_model_masking_name = model_details.get("modelMaskingName")

        if response_model_masking_name is not None:
            normalized_model_masking_name = cls._validate_masking_name(
                response_model_masking_name,
                field_name="modelDetails.modelMaskingName",
            )

            if normalized_model_masking_name != expected_model_masking_name:
                raise ExternalResponseError(
                    "CarWale response model identity does not match the request"
                )

    async def execute(
        self,
        *,
        model: Mapping[str, Any],
        city_id: int | None = None,
        area_id: int | None = None,
        platform_id: int | None = None,
        show_offer_upfront: bool = False,
    ) -> dict[str, Any]:
        validated_model = self._validate_model(model)

        make_id = validated_model["makeId"]
        make_name = validated_model["makeName"]
        make_masking_name = validated_model["makeMaskingName"]
        model_id = validated_model["modelId"]
        model_name = validated_model["modelName"]
        model_masking_name = validated_model["modelMaskingName"]

        normalized_city_id: int | None = None

        if city_id is not None:
            normalized_city_id = self._validate_positive_integer(
                city_id,
                field_name="city_id",
            )

        normalized_area_id: int | None = None

        if area_id is not None:
            normalized_area_id = self._validate_non_negative_integer(
                area_id,
                field_name="area_id",
            )

        normalized_platform_id: int | None = None

        if platform_id is not None:
            normalized_platform_id = self._validate_positive_integer(
                platform_id,
                field_name="platform_id",
            )

        if not isinstance(show_offer_upfront, bool):
            raise ValueError("show_offer_upfront must be a boolean")

        endpoint = CARWALE_MODEL_PAGE_DATA

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for the CarWale model-page API"
            )

        params: dict[str, Any] = {
            **endpoint.default_params,
            "makeMaskingName": make_masking_name,
            "modelMaskingName": model_masking_name,
            "showOfferUpfront": ("true" if show_offer_upfront else "false"),
        }

        if normalized_city_id is not None:
            params["cityId"] = normalized_city_id
        else:
            params.pop("cityId", None)

        if normalized_area_id is not None:
            params["areaId"] = normalized_area_id
        else:
            params.pop("areaId", None)

        if normalized_platform_id is not None:
            params["platformId"] = normalized_platform_id
        else:
            params.pop("platformId", None)

        headers = {
            **endpoint.default_headers,
            "Referer": (
                f"{CARWALE_BASE_URL}/{make_masking_name}-cars/{model_masking_name}/"
            ),
        }

        logger_service.info(
            (
                "Scraping CarWale model page: "
                f"make_id={make_id}, "
                f"make={make_name}, "
                f"model_id={model_id}, "
                f"model={model_name}, "
                f"make_masking_name={make_masking_name}, "
                f"model_masking_name={model_masking_name}"
            ),
            context="CarWaleCarsExecutor",
        )

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params=params,
            headers=headers,
        )

        if not isinstance(response_data, Mapping):
            raise ExternalResponseError(
                "CarWale model-page API returned an invalid response. "
                "Expected an object: "
                f"make={make_masking_name!r}, model={model_masking_name!r}"
            )

        self._validate_page_validation(
            response_data,
            make_masking_name=make_masking_name,
            model_masking_name=model_masking_name,
        )

        model_details = self._get_required_mapping_section(
            response_data,
            field_name="modelDetails",
            make_masking_name=make_masking_name,
            model_masking_name=model_masking_name,
        )

        replaced_model_details = self._get_optional_json_section(
            response_data,
            field_name="replacedModelDetails",
            make_masking_name=make_masking_name,
            model_masking_name=model_masking_name,
        )

        similar_cars = self._get_optional_json_section(
            response_data,
            field_name="similarCars",
            make_masking_name=make_masking_name,
            model_masking_name=model_masking_name,
        )

        versions = self._clean_versions(
            response_data,
            make_masking_name=make_masking_name,
            model_masking_name=model_masking_name,
        )

        self._validate_response_identity(
            model_details=model_details,
            expected_make_masking_name=make_masking_name,
            expected_model_id=model_id,
            expected_model_masking_name=model_masking_name,
        )

        logger_service.info(
            (
                "CarWale model page scraped: "
                f"make={make_name}, "
                f"model={model_name}, "
                f"total_versions={len(versions)}"
            ),
            context="CarWaleCarsExecutor",
        )

        return {
            "modelDetails": model_details,
            "replacedModelDetails": replaced_model_details,
            "similarCars": similar_cars,
            "versions": versions,
        }
