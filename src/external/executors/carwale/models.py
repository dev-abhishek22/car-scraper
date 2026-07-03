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
    CARWALE_MAKE_PAGE_DATA,
)

MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CarWaleModelsExecutor:
    """
    Fetch and validate CarWale models for one brand.

    This executor only handles the external API request
    and response validation.

    It does not:

    - Read brand JSON files
    - Write model JSON files
    - Create archive files
    - Update MongoDB
    - Manage scraper run/job state
    """

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
    def _validate_brand(
        cls,
        brand: Mapping[str, Any],
    ) -> tuple[int, str, str]:
        make_id = cls._validate_positive_integer(
            brand.get("makeId"),
            field_name="brand.makeId",
        )

        make_name = cls._validate_non_empty_string(
            brand.get("makeName"),
            field_name="brand.makeName",
        )

        masking_name = cls._validate_masking_name(
            brand.get("maskingName"),
            field_name="brand.maskingName",
        )

        return (
            make_id,
            make_name,
            masking_name,
        )

    @classmethod
    def _validate_model(
        cls,
        model: Mapping[str, Any],
        *,
        make_id: int,
        make_name: str,
        make_masking_name: str,
        index: int,
    ) -> dict[str, Any]:
        model_id = cls._validate_positive_integer(
            model.get("modelId"),
            field_name=f"models[{index}].modelId",
        )

        model_name = cls._validate_non_empty_string(
            model.get("modelName"),
            field_name=f"models[{index}].modelName",
        )

        model_masking_name = cls._validate_masking_name(
            model.get("modelMaskingName"),
            field_name=(f"models[{index}].modelMaskingName"),
        )

        response_make_id = model.get("makeId")

        if response_make_id is not None:
            normalized_response_make_id = cls._validate_positive_integer(
                response_make_id,
                field_name=(f"models[{index}].makeId"),
            )

            if normalized_response_make_id != make_id:
                raise ExternalResponseError(
                    "CarWale model belongs to a "
                    "different brand: "
                    f"index={index}, "
                    f"expected_make_id={make_id}, "
                    "returned_make_id="
                    f"{normalized_response_make_id}"
                )

        response_make_masking_name = model.get("makeMaskingName")

        if response_make_masking_name is not None:
            normalized_response_make_masking_name = cls._validate_masking_name(
                response_make_masking_name,
                field_name=(f"models[{index}].makeMaskingName"),
            )

            if normalized_response_make_masking_name != make_masking_name:
                raise ExternalResponseError(
                    "CarWale model belongs to a "
                    "different brand slug: "
                    f"index={index}, "
                    f"expected={make_masking_name!r}, "
                    "returned="
                    f"{normalized_response_make_masking_name!r}"
                )

        validated_model = dict(model)

        validated_model.update(
            {
                "makeId": make_id,
                "makeName": make_name,
                "makeMaskingName": (make_masking_name),
                "modelId": model_id,
                "modelName": model_name,
                "modelMaskingName": (model_masking_name),
            }
        )

        return validated_model

    @classmethod
    def _parse_models_response(
        cls,
        response: Mapping[str, Any],
        *,
        make_id: int,
        make_name: str,
        make_masking_name: str,
    ) -> list[dict[str, Any]]:
        raw_models = response.get("models")

        if not isinstance(
            raw_models,
            list,
        ):
            raise ExternalResponseError(
                "CarWale make-page response does "
                "not contain a valid models array: "
                f"brand={make_masking_name!r}"
            )

        models: list[dict[str, Any]] = []

        seen_model_ids: set[int] = set()

        for index, raw_model in enumerate(raw_models):
            if not isinstance(
                raw_model,
                Mapping,
            ):
                raise ExternalResponseError(
                    "CarWale models array contains "
                    "an invalid item: "
                    f"brand={make_masking_name!r}, "
                    f"index={index}"
                )

            validated_model = cls._validate_model(
                raw_model,
                make_id=make_id,
                make_name=make_name,
                make_masking_name=(make_masking_name),
                index=index,
            )

            model_id = validated_model["modelId"]

            if model_id in seen_model_ids:
                continue

            seen_model_ids.add(model_id)

            models.append(validated_model)

        return models

    async def execute(
        self,
        *,
        brand: Mapping[str, Any],
    ) -> list[dict[str, Any]]:
        (
            make_id,
            make_name,
            masking_name,
        ) = self._validate_brand(brand)

        endpoint = CARWALE_MAKE_PAGE_DATA

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for the CarWale make-page API"
            )

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params={
                **endpoint.default_params,
                "maskingName": masking_name,
            },
            headers={
                **endpoint.default_headers,
                "Referer": (f"{CARWALE_BASE_URL}/{masking_name}-cars/"),
            },
        )

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarWale make-page API returned "
                "an invalid response. Expected "
                "an object: "
                f"brand={masking_name!r}"
            )

        return self._parse_models_response(
            response_data,
            make_id=make_id,
            make_name=make_name,
            make_masking_name=masking_name,
        )
