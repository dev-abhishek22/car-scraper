from __future__ import annotations

import html
import re
from collections.abc import Mapping
from typing import Any
from urllib.parse import unquote, urlsplit

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

REDIRECT_STATUS_CODES = {
    301,
    302,
    307,
    308,
}


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
            raise ValueError(f"{field_name} must be a positive integer")

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
            raise ExternalResponseError(f"{field_name} must be a positive integer")

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
            raise ExternalResponseError(f"{field_name} must be a positive integer")

        if normalized_value <= 0:
            raise ExternalResponseError(f"{field_name} must be a positive integer")

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
                f"{field_name} contains invalid characters: {normalized_value!r}"
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
            raise ValueError("variant_record.variant must be an object")

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
                "Cardekho model-specs API returned status=false"
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
                "Cardekho model-specs API response does not contain a valid data object"
            )

        return data

    @staticmethod
    def _normalize_identity_text(
        value: Any,
    ) -> str | None:
        if not isinstance(value, str):
            return None

        normalized_value = " ".join(value.strip().casefold().split())

        return normalized_value or None

    @classmethod
    def _try_parse_positive_integer(
        cls,
        value: Any,
    ) -> int | None:
        try:
            return cls._parse_positive_integer(
                value,
                field_name="response identity",
            )
        except ExternalResponseError:
            return None

    @staticmethod
    def _iter_variant_table_rows(
        variant_table: Any,
    ) -> list[Mapping[str, Any]]:
        if not isinstance(
            variant_table,
            Mapping,
        ):
            return []

        rows: list[Mapping[str, Any]] = []

        variant_list = variant_table.get(
            "variantList",
        )

        if isinstance(variant_list, list):
            for item in variant_list:
                if isinstance(item, Mapping):
                    rows.append(item)

        children = variant_table.get(
            "childs",
        )

        if isinstance(children, list):
            for child in children:
                if not isinstance(child, Mapping):
                    continue

                child_items = child.get(
                    "items",
                )

                if isinstance(child_items, list):
                    for item in child_items:
                        if isinstance(item, Mapping):
                            rows.append(item)
                else:
                    rows.append(child)

        return rows

    @classmethod
    def _validate_response_identity(
        cls,
        *,
        data: Mapping[str, Any],
        expected_model_id: int,
        expected_variant_id: int,
        expected_variant_name: str,
        expected_variant_slug: str,
    ) -> None:
        """
        Validate model and selected-variant identity.

        Cardekho does not consistently provide
        dataLayer.variant_id_new. For model-level specs
        responses, variant identity is available through:

        - data.selectedVariant
        - data.variantTable rows
        - row.dcbDto.carVariantCentralId

        The response is accepted only when it can be tied
        to the requested variant. This prevents storing one
        default variant's specs under every variant ID.
        """

        model_ids: list[int] = []

        data_layer = data.get(
            "dataLayer",
        )

        if isinstance(data_layer, Mapping):
            model_id = cls._try_parse_positive_integer(
                data_layer.get(
                    "model_id_new",
                )
            )

            if model_id is not None:
                model_ids.append(model_id)

        for container_name, field_name in (
            ("overviewData", "id"),
            ("overView", "id"),
            ("DCB", "modelId"),
        ):
            container = data.get(
                container_name,
            )

            if not isinstance(container, Mapping):
                continue

            model_id = cls._try_parse_positive_integer(container.get(field_name))

            if model_id is not None:
                model_ids.append(model_id)

        if not model_ids:
            raise ExternalResponseError(
                "Cardekho model-specs API response does not contain a usable model ID"
            )

        if any(model_id != expected_model_id for model_id in model_ids):
            raise ExternalResponseError(
                "Cardekho model-specs API returned "
                "a different model ID: "
                f"expected={expected_model_id}, "
                f"found={sorted(set(model_ids))}"
            )

        data_layer_variant_id: int | None = None

        if isinstance(data_layer, Mapping):
            data_layer_variant_id = cls._try_parse_positive_integer(
                data_layer.get(
                    "variant_id_new",
                )
            )

            if (
                data_layer_variant_id is not None
                and data_layer_variant_id != expected_variant_id
            ):
                raise ExternalResponseError(
                    "Cardekho model-specs API "
                    "returned a different variant ID: "
                    f"expected={expected_variant_id}, "
                    f"found={data_layer_variant_id}"
                )

        variant_rows = cls._iter_variant_table_rows(
            data.get(
                "variantTable",
            )
        )

        matching_row: Mapping[str, Any] | None = None

        for row in variant_rows:
            row_slug = row.get(
                "variantSlug",
            )

            if isinstance(row_slug, str) and row_slug.strip() == expected_variant_slug:
                matching_row = row
                break

        if matching_row is None:
            if data_layer_variant_id == expected_variant_id:
                return

            raise ExternalResponseError(
                "Cardekho model-specs API response "
                "does not contain the requested variant "
                "in data.variantTable: "
                f"variant_slug={expected_variant_slug!r}, "
                f"variant_id={expected_variant_id}"
            )

        response_variant_ids: list[int] = []

        for raw_id in (
            matching_row.get("centralId"),
            matching_row.get("id"),
        ):
            parsed_id = cls._try_parse_positive_integer(
                raw_id,
            )

            if parsed_id is not None:
                response_variant_ids.append(parsed_id)

        row_dcb = matching_row.get(
            "dcbDto",
        )

        if isinstance(row_dcb, Mapping):
            dcb_variant_id = cls._try_parse_positive_integer(
                row_dcb.get(
                    "carVariantCentralId",
                )
            )

            if dcb_variant_id is not None:
                response_variant_ids.append(
                    dcb_variant_id,
                )

        if data_layer_variant_id is not None:
            response_variant_ids.append(
                data_layer_variant_id,
            )

        if response_variant_ids and any(
            variant_id != expected_variant_id for variant_id in response_variant_ids
        ):
            raise ExternalResponseError(
                "Cardekho model-specs API returned "
                "a different variant ID for the "
                "requested variant slug: "
                f"expected={expected_variant_id}, "
                f"found={sorted(set(response_variant_ids))}, "
                f"variant_slug={expected_variant_slug!r}"
            )

        selected_variant = cls._normalize_identity_text(
            data.get(
                "selectedVariant",
            )
        )

        row_identity_values: list[str] = []

        for value in (
            matching_row.get("carVariantId"),
            matching_row.get("displayCarVariantId"),
        ):
            normalized_value = cls._normalize_identity_text(value)

            if normalized_value is not None:
                row_identity_values.append(
                    normalized_value,
                )

        if isinstance(row_dcb, Mapping):
            normalized_dcb_name = cls._normalize_identity_text(
                row_dcb.get(
                    "carVariantId",
                )
            )

            if normalized_dcb_name is not None:
                row_identity_values.append(
                    normalized_dcb_name,
                )

        expected_variant_name_normalized = cls._normalize_identity_text(
            expected_variant_name,
        )

        if expected_variant_name_normalized is not None:
            row_identity_values.append(
                expected_variant_name_normalized,
            )

        if selected_variant is not None:
            if row_identity_values and selected_variant not in set(row_identity_values):
                raise ExternalResponseError(
                    "Cardekho model-specs API returned "
                    "specifications for a different "
                    "selected variant: "
                    f"expected_slug="
                    f"{expected_variant_slug!r}, "
                    f"selected_variant="
                    f"{data.get('selectedVariant')!r}"
                )

        elif data_layer_variant_id is None:
            raise ExternalResponseError(
                "Cardekho model-specs API response "
                "does not provide enough selected-variant "
                "identity to safely store specifications: "
                f"variant_slug={expected_variant_slug!r}, "
                f"variant_id={expected_variant_id}"
            )

    @classmethod
    def _parse_redirect_request(
        cls,
        *,
        data: Mapping[str, Any],
    ) -> dict[str, str] | None:
        redirect = data.get(
            "redirect",
        )

        if not isinstance(
            redirect,
            Mapping,
        ):
            return None

        status_code = redirect.get(
            "statusCode",
        )

        if status_code is not None and status_code not in REDIRECT_STATUS_CODES:
            return None

        redirect_url = redirect.get(
            "redirectURL",
        )

        if not isinstance(
            redirect_url,
            str,
        ):
            return None

        normalized_redirect_url = html.unescape(
            redirect_url,
        ).strip()

        if not normalized_redirect_url:
            return None

        split_result = urlsplit(
            normalized_redirect_url,
        )

        if split_result.scheme or split_result.netloc:
            return None

        redirect_path = unquote(
            split_result.path,
        )

        if not redirect_path.startswith("/"):
            redirect_path = f"/{redirect_path}"

        request_url = redirect_path.lstrip("/")

        if split_result.query:
            request_url = f"{request_url}?{split_result.query}"

        return {
            "url": request_url,
            "refererPath": redirect_path,
        }

    async def _fetch_response(
        self,
        *,
        brand_slug: str,
        model_slug: str,
        variant_slug: str,
        request_url: str,
        referer_path: str,
    ) -> Mapping[str, Any]:
        endpoint = CARDEKHO_MODEL_SPECS

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for the Cardekho model-specs API"
            )

        normalized_referer_path = referer_path

        if not normalized_referer_path.startswith("/"):
            normalized_referer_path = f"/{normalized_referer_path}"

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params={
                **endpoint.default_params,
                "brandSlug": brand_slug,
                "modelSlug": model_slug,
                "variantSlug": variant_slug,
                "url": request_url,
            },
            headers={
                **endpoint.default_headers,
                "Referer": (f"{CARDEKHO_BASE_URL}{normalized_referer_path}"),
            },
        )

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "Cardekho model-specs API "
                "returned an invalid response. "
                "Expected a JSON object"
            )

        return response_data

    async def _fetch_data_with_redirect(
        self,
        *,
        brand_slug: str,
        model_slug: str,
        variant_slug: str,
    ) -> Mapping[str, Any]:
        initial_request_url = f"{brand_slug}/{model_slug}/specs"

        initial_referer_path = f"/{initial_request_url}"

        response_data = await self._fetch_response(
            brand_slug=brand_slug,
            model_slug=model_slug,
            variant_slug=variant_slug,
            request_url=initial_request_url,
            referer_path=initial_referer_path,
        )

        data = self._validate_response_envelope(
            response_data,
        )

        if isinstance(
            data.get("specs"),
            Mapping,
        ):
            return data

        redirect_request = self._parse_redirect_request(
            data=data,
        )

        if redirect_request is None:
            data_keys = sorted(str(key) for key in data.keys())

            raise ExternalResponseError(
                "Cardekho model-specs API "
                "response does not contain "
                "specifications or a usable redirect: "
                f"brand={brand_slug!r}, "
                f"model={model_slug!r}, "
                f"variant={variant_slug!r}, "
                f"data_keys={data_keys}"
            )

        redirected_response_data = await self._fetch_response(
            brand_slug=brand_slug,
            model_slug=model_slug,
            variant_slug=variant_slug,
            request_url=redirect_request["url"],
            referer_path=(redirect_request["refererPath"]),
        )

        redirected_data = self._validate_response_envelope(
            redirected_response_data,
        )

        if not isinstance(
            redirected_data.get("specs"),
            Mapping,
        ):
            second_redirect = self._parse_redirect_request(
                data=redirected_data,
            )

            data_keys = sorted(str(key) for key in redirected_data.keys())

            second_redirect_url = (
                second_redirect["refererPath"] if second_redirect is not None else None
            )

            raise ExternalResponseError(
                "Cardekho model-specs API "
                "response does not contain "
                "a valid data.specs object "
                "after following one redirect: "
                f"brand={brand_slug!r}, "
                f"model={model_slug!r}, "
                f"variant={variant_slug!r}, "
                f"data_keys={data_keys}, "
                f"redirect_url="
                f"{second_redirect_url!r}"
            )

        return redirected_data

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

        data = await self._fetch_data_with_redirect(
            brand_slug=brand_slug,
            model_slug=model_slug,
            variant_slug=variant_slug,
        )

        result = self._extract_specs(
            data,
        )

        self._validate_response_identity(
            data=data,
            expected_model_id=model_id,
            expected_variant_id=variant_id,
            expected_variant_name=variant_name,
            expected_variant_slug=variant_slug,
        )

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
