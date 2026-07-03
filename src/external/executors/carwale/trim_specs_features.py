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
    CARWALE_TRIM_PAGE_DATA,
)
from src.logger.logger import logger_service

MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CarWaleTrimSpecsFeaturesExecutor:
    """
    Fetch CarWale trim-page data for one version.

    Only these response sections are returned:

    - versionDetail
    - trimDetail
    - specifications
    - features

    Their internal structures are not validated,
    modified, filtered, or normalized.
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
    def _validate_version_record(
        cls,
        version_record: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(
            version_record,
            Mapping,
        ):
            raise ValueError("version_record must be an object")

        version = version_record.get("version")

        if not isinstance(
            version,
            Mapping,
        ):
            raise ValueError("version_record.version must be an object")

        return {
            "makeId": cls._validate_positive_integer(
                version_record.get("makeId"),
                field_name="version_record.makeId",
            ),
            "makeName": cls._validate_non_empty_string(
                version_record.get("makeName"),
                field_name="version_record.makeName",
            ),
            "makeMaskingName": (
                cls._validate_masking_name(
                    version_record.get("makeMaskingName"),
                    field_name=("version_record.makeMaskingName"),
                )
            ),
            "modelId": cls._validate_positive_integer(
                version_record.get("modelId"),
                field_name="version_record.modelId",
            ),
            "modelName": (
                cls._validate_non_empty_string(
                    version_record.get("modelName"),
                    field_name=("version_record.modelName"),
                )
            ),
            "modelMaskingName": (
                cls._validate_masking_name(
                    version_record.get("modelMaskingName"),
                    field_name=("version_record.modelMaskingName"),
                )
            ),
            "trimId": cls._validate_positive_integer(
                version.get("trimId"),
                field_name="version.trimId",
            ),
            "trimName": (
                cls._validate_non_empty_string(
                    version.get("trimName"),
                    field_name="version.trimName",
                )
            ),
            "trimMaskingName": (
                cls._validate_masking_name(
                    version.get("trimMaskingName"),
                    field_name=("version.trimMaskingName"),
                )
            ),
            "versionId": (
                cls._validate_positive_integer(
                    version.get("versionId"),
                    field_name="version.versionId",
                )
            ),
            "versionName": (
                cls._validate_non_empty_string(
                    version.get("versionName"),
                    field_name="version.versionName",
                )
            ),
            "versionMaskingName": (
                cls._validate_masking_name(
                    version.get("versionMaskingName"),
                    field_name=("version.versionMaskingName"),
                )
            ),
        }

    async def execute(
        self,
        *,
        version_record: Mapping[str, Any],
    ) -> dict[str, Any]:
        validated_record = self._validate_version_record(version_record)

        make_id = validated_record["makeId"]
        make_name = validated_record["makeName"]
        make_masking_name = validated_record["makeMaskingName"]

        model_id = validated_record["modelId"]
        model_name = validated_record["modelName"]
        model_masking_name = validated_record["modelMaskingName"]

        trim_id = validated_record["trimId"]
        trim_name = validated_record["trimName"]
        trim_masking_name = validated_record["trimMaskingName"]

        version_id = validated_record["versionId"]
        version_name = validated_record["versionName"]

        endpoint = CARWALE_TRIM_PAGE_DATA

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for the CarWale trim-page API"
            )

        params: dict[str, Any] = {
            **endpoint.default_params,
            "makeMaskingName": (make_masking_name),
            "modelMaskingName": (model_masking_name),
            "trimMaskingName": (trim_masking_name),
            "versionId": version_id,
        }

        headers = {
            **endpoint.default_headers,
            "Referer": (
                f"{CARWALE_BASE_URL}/"
                f"{make_masking_name}-cars/"
                f"{model_masking_name}/"
                f"{trim_masking_name}/"
            ),
        }

        logger_service.info(
            (
                "Scraping CarWale trim specs/features: "
                f"make_id={make_id}, "
                f"make={make_name}, "
                f"model_id={model_id}, "
                f"model={model_name}, "
                f"trim_id={trim_id}, "
                f"trim={trim_name}, "
                f"version_id={version_id}, "
                f"version={version_name}"
            ),
            context=("CarWaleTrimSpecsFeaturesExecutor"),
        )

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params=params,
            headers=headers,
        )

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarWale trim-page API returned "
                "an invalid response. Expected "
                "a JSON object: "
                f"make={make_masking_name!r}, "
                f"model={model_masking_name!r}, "
                f"trim={trim_masking_name!r}, "
                f"version_id={version_id}"
            )

        result = {
            "versionDetail": response_data.get("versionDetail"),
            "trimDetail": response_data.get("trimDetail"),
            "specifications": response_data.get("specifications"),
            "features": response_data.get("features"),
        }

        logger_service.info(
            (
                "CarWale trim specs/features "
                "scraped: "
                f"make={make_masking_name}, "
                f"model={model_masking_name}, "
                f"trim={trim_masking_name}, "
                f"version_id={version_id}"
            ),
            context=("CarWaleTrimSpecsFeaturesExecutor"),
        )

        return result
