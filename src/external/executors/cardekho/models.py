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
    CARDEKHO_BRAND_MODELS,
)

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CarDekhoModelsExecutor:
    """
    Fetch and normalize current, upcoming, and
    discontinued CarDekho models for one brand.

    Current or discontinued models:

        data.carModels

    Upcoming models:

        data.upcomingCars.items
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

    @staticmethod
    def _normalize_optional_string(
        value: Any,
    ) -> str | None:
        if not isinstance(
            value,
            str,
        ):
            return None

        normalized_value = value.strip()

        return normalized_value or None

    @classmethod
    def _validate_slug(
        cls,
        value: Any,
        *,
        field_name: str,
    ) -> str:
        normalized_value = (
            cls._validate_non_empty_string(
                value,
                field_name=field_name,
            )
            .lower()
            .replace("_", "-")
            .replace(" ", "-")
        )

        normalized_value = re.sub(
            r"-+",
            "-",
            normalized_value,
        ).strip("-")

        if not SLUG_PATTERN.fullmatch(normalized_value):
            raise ValueError(
                f"{field_name} contains invalid characters: {normalized_value!r}"
            )

        return normalized_value

    @staticmethod
    def _validate_brand_status(
        value: Any,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError("brand.brandStatus must be a string")

        normalized_status = value.strip().upper()

        if normalized_status not in {
            "CURRENT",
            "UPCOMING",
            "EXPIRED",
        }:
            raise ValueError("brand.brandStatus must be CURRENT, UPCOMING, or EXPIRED")

        return normalized_status

    @classmethod
    def _validate_brand(
        cls,
        brand: Mapping[str, Any],
    ) -> tuple[
        str,
        str,
        str,
        str,
        str,
    ]:
        brand_name = cls._validate_non_empty_string(
            brand.get("brandName"),
            field_name="brand.brandName",
        )

        source_brand_slug = cls._validate_slug(
            brand.get("slug"),
            field_name="brand.slug",
        )

        model_request_slug = cls._validate_slug(
            brand.get("modelRequestSlug"),
            field_name="brand.modelRequestSlug",
        )

        brand_url = cls._validate_non_empty_string(
            brand.get("brandUrl"),
            field_name="brand.brandUrl",
        )

        brand_status = cls._validate_brand_status(brand.get("brandStatus"))

        return (
            brand_name,
            source_brand_slug,
            model_request_slug,
            brand_url,
            brand_status,
        )

    @classmethod
    def _validate_response_brand(
        cls,
        data: Mapping[str, Any],
        *,
        expected_source_brand_slug: str,
        expected_model_request_slug: str,
    ) -> tuple[
        int,
        str,
        str,
    ]:
        brand_id = cls._validate_positive_integer(
            data.get("brandId"),
            field_name="data.brandId",
        )

        brand_name = cls._validate_non_empty_string(
            data.get("brandName"),
            field_name="data.brandName",
        )

        brand_slug = cls._validate_slug(
            data.get("brandSlug"),
            field_name="data.brandSlug",
        )

        accepted_brand_slugs = {
            expected_source_brand_slug,
            expected_model_request_slug,
        }

        if brand_slug not in accepted_brand_slugs:
            raise ExternalResponseError(
                "CarDekho brand-model API returned a "
                "different brand slug: "
                f"expected_one_of="
                f"{sorted(accepted_brand_slugs)!r}, "
                f"returned={brand_slug!r}"
            )

        return (
            brand_id,
            brand_name,
            brand_slug,
        )

    @classmethod
    def _resolve_model_name(
        cls,
        model: Mapping[str, Any],
        *,
        index: int,
        source_name: str,
    ) -> str:
        for field_name in (
            "modelName",
            "displayName",
            "upcomingCarName",
            "title",
            "name",
        ):
            value = model.get(field_name)

            if isinstance(value, str) and value.strip():
                return value.strip()

        raise ExternalResponseError(
            "CarDekho model does not contain a valid "
            f"model name: source={source_name}, "
            f"index={index}"
        )

    @classmethod
    def _normalize_model(
        cls,
        model: Mapping[str, Any],
        *,
        brand_id: int,
        brand_name: str,
        brand_slug: str,
        model_status: str,
        is_upcoming: bool,
        index: int,
        source_name: str,
    ) -> dict[str, Any]:
        model_id = cls._validate_positive_integer(
            model.get("id"),
            field_name=(f"{source_name}[{index}].id"),
        )

        name = cls._validate_non_empty_string(
            model.get("name"),
            field_name=(f"{source_name}[{index}].name"),
        )

        slug = cls._validate_slug(
            model.get("slug"),
            field_name=(f"{source_name}[{index}].slug"),
        )

        model_name = cls._resolve_model_name(
            model,
            index=index,
            source_name=source_name,
        )

        normalized_model: dict[str, Any] = {
            "id": model_id,
            "brandId": brand_id,
            "brandName": brand_name,
            "brandSlug": brand_slug,
            "name": name,
            "slug": slug,
            "modelName": model_name,
            "modelStatus": model_status,
            "isUpcoming": is_upcoming,
        }

        if is_upcoming:
            expected_launch_date = cls._normalize_optional_string(
                model.get("launchedAt")
            )

            if expected_launch_date is not None:
                normalized_model["expectedLaunchDate"] = expected_launch_date

        return normalized_model

    @classmethod
    def _parse_current_models(
        cls,
        data: Mapping[str, Any],
        *,
        brand_id: int,
        brand_name: str,
        brand_slug: str,
        model_status: str,
    ) -> list[dict[str, Any]]:
        raw_models = data.get("carModels")

        if raw_models is None:
            return []

        if not isinstance(
            raw_models,
            list,
        ):
            raise ExternalResponseError(
                "CarDekho brand-model API response "
                "contains an invalid data.carModels field"
            )

        models: list[dict[str, Any]] = []

        for index, raw_model in enumerate(raw_models):
            if not isinstance(
                raw_model,
                Mapping,
            ):
                raise ExternalResponseError(
                    f"CarDekho data.carModels contains an invalid item: index={index}"
                )

            models.append(
                cls._normalize_model(
                    raw_model,
                    brand_id=brand_id,
                    brand_name=brand_name,
                    brand_slug=brand_slug,
                    model_status=model_status,
                    is_upcoming=False,
                    index=index,
                    source_name="data.carModels",
                )
            )

        return models

    @classmethod
    def _parse_upcoming_models(
        cls,
        data: Mapping[str, Any],
        *,
        brand_id: int,
        brand_name: str,
        brand_slug: str,
        model_status: str,
        is_upcoming: bool,
    ) -> list[dict[str, Any]]:
        raw_upcoming_cars = data.get("upcomingCars")

        if raw_upcoming_cars is None:
            return []

        if not isinstance(
            raw_upcoming_cars,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho brand-model API response "
                "contains an invalid "
                "data.upcomingCars object"
            )

        raw_items = raw_upcoming_cars.get("items")

        if raw_items is None:
            return []

        if not isinstance(
            raw_items,
            list,
        ):
            raise ExternalResponseError(
                "CarDekho brand-model API response "
                "contains an invalid "
                "data.upcomingCars.items field"
            )

        models: list[dict[str, Any]] = []

        for index, raw_model in enumerate(raw_items):
            if not isinstance(
                raw_model,
                Mapping,
            ):
                raise ExternalResponseError(
                    "CarDekho upcomingCars.items "
                    "contains an invalid item: "
                    f"index={index}"
                )

            models.append(
                cls._normalize_model(
                    raw_model,
                    brand_id=brand_id,
                    brand_name=brand_name,
                    brand_slug=brand_slug,
                    model_status=model_status,
                    is_upcoming=is_upcoming,
                    index=index,
                    source_name=("data.upcomingCars.items"),
                )
            )

        return models

    @staticmethod
    def _merge_models(
        *,
        current_models: list[dict[str, Any]],
        upcoming_models: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        deduplicated_models: dict[
            int,
            dict[str, Any],
        ] = {}

        for model in current_models:
            model_id = model["id"]

            deduplicated_models[model_id] = model

        for model in upcoming_models:
            model_id = model["id"]

            if model_id in deduplicated_models:
                continue

            deduplicated_models[model_id] = model

        return list(deduplicated_models.values())

    async def execute(
        self,
        *,
        brand: Mapping[str, Any],
    ) -> list[dict[str, Any]]:
        (
            _stored_brand_name,
            source_brand_slug,
            model_request_slug,
            brand_url,
            source_brand_status,
        ) = self._validate_brand(brand)

        endpoint = CARDEKHO_BRAND_MODELS

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for the CarDekho brand-model API"
            )

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params={
                **endpoint.default_params,
                "slug": model_request_slug,
                "url": brand_url,
            },
            headers={
                **endpoint.default_headers,
                "Referer": (f"{CARDEKHO_BASE_URL}{brand_url}"),
            },
        )

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho brand-model API returned "
                "an invalid response. Expected an object"
            )

        data = response_data.get("data")

        if not isinstance(
            data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho brand-model API response does not contain a valid data object"
            )

        (
            brand_id,
            brand_name,
            brand_slug,
        ) = self._validate_response_brand(
            data,
            expected_source_brand_slug=(source_brand_slug),
            expected_model_request_slug=(model_request_slug),
        )

        current_model_status = (
            "DISCONTINUED" if source_brand_status == "EXPIRED" else "CURRENT"
        )

        upcoming_model_status = (
            "DISCONTINUED" if source_brand_status == "EXPIRED" else "UPCOMING"
        )

        upcoming_is_upcoming = source_brand_status != "EXPIRED"

        current_models = self._parse_current_models(
            data,
            brand_id=brand_id,
            brand_name=brand_name,
            brand_slug=brand_slug,
            model_status=current_model_status,
        )

        upcoming_models = self._parse_upcoming_models(
            data,
            brand_id=brand_id,
            brand_name=brand_name,
            brand_slug=brand_slug,
            model_status=upcoming_model_status,
            is_upcoming=upcoming_is_upcoming,
        )

        models = self._merge_models(
            current_models=current_models,
            upcoming_models=upcoming_models,
        )

        if not models:
            raise ExternalResponseError(
                "CarDekho brand-model API returned "
                "no models: "
                f"brand={source_brand_slug!r}, "
                f"brand_status={source_brand_status!r}"
            )

        return models
