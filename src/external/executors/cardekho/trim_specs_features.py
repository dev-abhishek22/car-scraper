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
from src.external.constants.cardekho import (
    CARDEKHO_BASE_URL,
    CARDEKHO_MODEL_SPECS,
)
from src.logger.logger import logger_service

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CarDekhoTrimSpecsFeaturesExecutor:
    """
    Fetch Cardekho specifications and features
    for one variant.

    Only these response sections are returned:

    - data.specs.featured
    - data.specs.specification

    Their internal structures are not modified,
    filtered, or normalized.
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
        if (
            isinstance(
                value,
                bool,
            )
            or not isinstance(
                value,
                int,
            )
            or value <= 0
        ):
            raise ValueError(f"{field_name} must be a " "positive integer")

        return value

    @staticmethod
    def _parse_positive_integer(
        value: Any,
        *,
        field_name: str,
    ) -> int:
        if isinstance(
            value,
            bool,
        ):
            raise ExternalResponseError(f"{field_name} must be a " "positive integer")

        if isinstance(
            value,
            int,
        ):
            normalized_value = value

        elif (
            isinstance(
                value,
                str,
            )
            and value.strip().isdigit()
        ):
            normalized_value = int(value.strip())

        else:
            raise ExternalResponseError(f"{field_name} must be a " "positive integer")

        if normalized_value <= 0:
            raise ExternalResponseError(f"{field_name} must be a " "positive integer")

        return normalized_value

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

        if not SLUG_PATTERN.fullmatch(normalized_value):
            raise ValueError(
                f"{field_name} contains invalid "
                f"characters: "
                f"{normalized_value!r}"
            )

        return normalized_value

    @classmethod
    def _validate_variant_record(
        cls,
        variant_record: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(
            variant_record,
            Mapping,
        ):
            raise ValueError("variant_record must be an object")

        variant = variant_record.get("variant")

        if not isinstance(
            variant,
            Mapping,
        ):
            raise ValueError("variant_record.variant must " "be an object")

        return {
            "brandId": (
                cls._validate_positive_integer(
                    variant_record.get("brandId"),
                    field_name=("variant_record.brandId"),
                )
            ),
            "brandName": (
                cls._validate_non_empty_string(
                    variant_record.get("brandName"),
                    field_name=("variant_record.brandName"),
                )
            ),
            "brandSlug": cls._validate_slug(
                variant_record.get("brandSlug"),
                field_name=("variant_record.brandSlug"),
            ),
            "modelId": (
                cls._validate_positive_integer(
                    variant_record.get("modelId"),
                    field_name=("variant_record.modelId"),
                )
            ),
            "modelName": (
                cls._validate_non_empty_string(
                    variant_record.get("modelName"),
                    field_name=("variant_record.modelName"),
                )
            ),
            "modelSlug": cls._validate_slug(
                variant_record.get("modelSlug"),
                field_name=("variant_record.modelSlug"),
            ),
            "variantId": (
                cls._validate_positive_integer(
                    variant.get("id"),
                    field_name="variant.id",
                )
            ),
            "variantName": (
                cls._validate_non_empty_string(
                    variant.get("name"),
                    field_name="variant.name",
                )
            ),
            "variantSlug": cls._validate_non_empty_string(
                variant.get("slug"),
                field_name="variant.slug",
            ),
        }

    @staticmethod
    def _validate_response_envelope(
        response_data: Any,
    ) -> Mapping[str, Any]:
        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "returned an invalid response. "
                "Expected a JSON object"
            )

        response_status = response_data.get("status")

        if response_status is False:
            raise ExternalResponseError(
                "Cardekho model-specs API " "returned status=false"
            )

        response_status_code = response_data.get("statusCode")

        if response_status_code is not None and (
            isinstance(
                response_status_code,
                bool,
            )
            or not isinstance(
                response_status_code,
                int,
            )
        ):
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "returned an invalid statusCode: "
                f"{response_status_code!r}"
            )

        if (
            isinstance(
                response_status_code,
                int,
            )
            and response_status_code != 200
        ):
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "returned an unsuccessful "
                "statusCode: "
                f"{response_status_code}"
            )

        data = response_data.get("data")

        if not isinstance(
            data,
            Mapping,
        ):
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "response does not contain "
                "a valid data object"
            )

        return data

    @classmethod
    def _validate_response_identity(
        cls,
        *,
        data: Mapping[str, Any],
        expected_model_id: int,
        expected_variant_id: int,
    ) -> None:
        data_layer = data.get("dataLayer")

        if not isinstance(
            data_layer,
            Mapping,
        ):
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "response does not contain "
                "a valid data.dataLayer object"
            )

        response_model_id = cls._parse_positive_integer(
            data_layer.get("model_id_new"),
            field_name=("data.dataLayer." "model_id_new"),
        )

        response_variant_id = cls._parse_positive_integer(
            data_layer.get("variant_id_new"),
            field_name=("data.dataLayer." "variant_id_new"),
        )

        if response_model_id != expected_model_id:
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "returned a different model ID: "
                f"expected={expected_model_id}, "
                f"found={response_model_id}"
            )

        if response_variant_id != expected_variant_id:
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "returned a different variant "
                "ID: "
                f"expected={expected_variant_id}, "
                f"found={response_variant_id}"
            )

    @staticmethod
    def _extract_specs(
        data: Mapping[str, Any],
    ) -> dict[str, Any]:
        specs = data.get("specs")

        if not isinstance(
            specs,
            Mapping,
        ):
            redirect = data.get("redirect")

            if isinstance(
                redirect,
                Mapping,
            ):
                raise ExternalResponseError(
                    "Cardekho model-specs API "
                    "returned a redirect instead "
                    "of specifications: "
                    f"status_code="
                    f"{redirect.get('statusCode')!r}, "
                    f"redirect_url="
                    f"{redirect.get('redirectURL')!r}"
                )

            raise ExternalResponseError(
                "Cardekho model-specs API "
                "response does not contain "
                "a valid data.specs object"
            )

        featured = specs.get("featured")

        specification = specs.get("specification")

        if not isinstance(
            featured,
            list,
        ):
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "response does not contain "
                "a valid "
                "data.specs.featured array"
            )

        if not isinstance(
            specification,
            list,
        ):
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "response does not contain "
                "a valid "
                "data.specs.specification array"
            )

        return {
            "featured": featured,
            "specification": specification,
        }

    async def execute(
        self,
        *,
        variant_record: Mapping[str, Any],
    ) -> dict[str, Any]:
        validated_record = self._validate_variant_record(variant_record)

        brand_id = validated_record["brandId"]

        brand_name = validated_record["brandName"]

        brand_slug = validated_record["brandSlug"]

        model_id = validated_record["modelId"]

        model_name = validated_record["modelName"]

        model_slug = validated_record["modelSlug"]

        variant_id = validated_record["variantId"]

        variant_name = validated_record["variantName"]

        variant_slug = validated_record["variantSlug"]

        endpoint = CARDEKHO_MODEL_SPECS

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method "
                "configured for the Cardekho "
                "model-specs API"
            )

        request_url = f"{brand_slug}/" f"{model_slug}/specs"

        params: dict[str, Any] = {
            **endpoint.default_params,
            "brandSlug": brand_slug,
            "modelSlug": model_slug,
            "variantSlug": variant_slug,
            "url": request_url,
        }

        headers = {
            **endpoint.default_headers,
            "Referer": (f"{CARDEKHO_BASE_URL}/" f"{request_url}"),
        }

        logger_service.info(
            (
                "Scraping Cardekho trim "
                "specs/features: "
                f"brand_id={brand_id}, "
                f"brand={brand_name}, "
                f"model_id={model_id}, "
                f"model={model_name}, "
                f"variant_id={variant_id}, "
                f"variant={variant_name}"
            ),
            context=("CarDekhoTrimSpecsFeaturesExecutor"),
        )

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params=params,
            headers=headers,
        )

        data = self._validate_response_envelope(response_data)

        self._validate_response_identity(
            data=data,
            expected_model_id=model_id,
            expected_variant_id=variant_id,
        )

        result = self._extract_specs(data)

        logger_service.info(
            (
                "Cardekho trim "
                "specs/features scraped: "
                f"brand={brand_slug}, "
                f"model={model_slug}, "
                f"variant={variant_slug}, "
                f"variant_id={variant_id}"
            ),
            context=("CarDekhoTrimSpecsFeaturesExecutor"),
        )

        return result
