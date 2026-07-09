from __future__ import annotations

import re
import zlib
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlparse

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

    @staticmethod
    def _slugify(
        value: Any,
    ) -> str | None:
        if not isinstance(
            value,
            str,
        ):
            return None

        normalized_value = value.strip().lower()

        if not normalized_value:
            return None

        normalized_value = normalized_value.replace("&", "and")
        normalized_value = normalized_value.replace("_", "-")
        normalized_value = re.sub(
            r"[^a-z0-9]+",
            "-",
            normalized_value,
        )
        normalized_value = re.sub(
            r"-+",
            "-",
            normalized_value,
        ).strip("-")

        return normalized_value or None

    @classmethod
    def _validate_slug(
        cls,
        value: Any,
        *,
        field_name: str,
    ) -> str:
        normalized_value = cls._slugify(value)

        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        if not SLUG_PATTERN.fullmatch(normalized_value):
            raise ValueError(
                f"{field_name} contains invalid characters: {normalized_value!r}"
            )

        return normalized_value

    @staticmethod
    def _strip_brand_name_prefix(
        value: str,
        brand_name: str,
    ) -> str:
        normalized_value = value.strip()

        if not normalized_value:
            return normalized_value

        normalized_brand_name = brand_name.strip()

        if not normalized_brand_name:
            return normalized_value

        pattern = re.compile(
            rf"^{re.escape(normalized_brand_name)}\s+",
            re.IGNORECASE,
        )

        return pattern.sub(
            "",
            normalized_value,
        ).strip()

    @staticmethod
    def _strip_brand_slug_prefix(
        value: str | None,
        brand_slug: str,
    ) -> str | None:
        if not value:
            return None

        normalized_brand_slug = brand_slug.strip().lower()

        if normalized_brand_slug and value.startswith(f"{normalized_brand_slug}-"):
            value = value[len(normalized_brand_slug) + 1 :]

        return value or None

    @classmethod
    def _extract_slug_from_url(
        cls,
        url: Any,
        *,
        brand_slug: str,
    ) -> str | None:
        if not isinstance(
            url,
            str,
        ):
            return None

        path = urlparse(url).path.strip("/")

        if not path:
            return None

        raw_segments = [segment for segment in path.split("/") if segment]

        if not raw_segments:
            return None

        segments = [
            cls._slugify(segment.removesuffix(".htm")) for segment in raw_segments
        ]

        segments = [segment for segment in segments if segment]

        if not segments:
            return None

        candidates: list[str] = []

        if "carmodels" in segments:
            candidates.append(segments[-1])

        if len(segments) >= 2 and segments[0] == brand_slug:
            candidates.append(segments[1])

        if segments[0].startswith(f"{brand_slug}-"):
            candidates.append(segments[0])

        candidates.append(segments[-1])

        for candidate in candidates:
            slug = cls._strip_brand_slug_prefix(
                candidate,
                brand_slug,
            )

            if slug and SLUG_PATTERN.fullmatch(slug):
                return slug

        return None

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
        int | None,
        str,
        str,
        str,
        str,
        str,
    ]:
        brand_id_value = brand.get("id")

        if brand_id_value is None:
            brand_id_value = brand.get("brandId")

        brand_id: int | None = None

        if brand_id_value is not None:
            brand_id = cls._validate_positive_integer(
                brand_id_value,
                field_name="brand.id",
            )

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
            brand_id,
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
        fallback_brand_id: int | None,
        fallback_brand_name: str,
        expected_source_brand_slug: str,
        expected_model_request_slug: str,
    ) -> tuple[
        int,
        str,
        str,
    ]:
        brand_id_value = data.get("brandId")

        if brand_id_value is None:
            brand_id_value = data.get("id")

        if brand_id_value is None:
            brand_id_value = fallback_brand_id

        brand_id = cls._validate_positive_integer(
            brand_id_value,
            field_name="data.brandId",
        )

        brand_name_value = data.get("brandName")

        if not isinstance(brand_name_value, str) or not brand_name_value.strip():
            brand_name_value = fallback_brand_name

        brand_name = cls._validate_non_empty_string(
            brand_name_value,
            field_name="data.brandName",
        )

        brand_slug_value = data.get("brandSlug")

        if not isinstance(brand_slug_value, str) or not brand_slug_value.strip():
            brand_slug_value = expected_source_brand_slug

        brand_slug = cls._validate_slug(
            brand_slug_value,
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

    @staticmethod
    def _stable_generated_model_id(
        *,
        brand_slug: str,
        link: str | None,
        text: str | None,
    ) -> int:
        raw_key = f"{brand_slug}|{link or ''}|{text or ''}".strip()

        checksum = zlib.crc32(raw_key.encode("utf-8")) & 0xFFFFFFFF

        return 900_000_000 + checksum

    @classmethod
    def _resolve_model_id(
        cls,
        model: Mapping[str, Any],
        *,
        brand_slug: str,
        index: int,
        source_name: str,
    ) -> int:
        for field_name in (
            "id",
            "modelId",
        ):
            value = model.get(field_name)

            if isinstance(value, int) and not isinstance(value, bool) and value > 0:
                return value

        link = cls._normalize_optional_string(model.get("link"))

        text = cls._normalize_optional_string(
            model.get("text")
        ) or cls._normalize_optional_string(model.get("title"))

        if source_name == "data.ExpiredCars.list" and (link or text):
            return cls._stable_generated_model_id(
                brand_slug=brand_slug,
                link=link,
                text=text,
            )

        raise ExternalResponseError(
            "CarDekho model does not contain a valid id: "
            f"source={source_name}, "
            f"index={index}"
        )

    @classmethod
    def _resolve_name(
        cls,
        model: Mapping[str, Any],
        *,
        brand_name: str,
        index: int,
        source_name: str,
    ) -> str:
        for field_name in (
            "name",
            "text",
            "title",
            "modelName",
            "upcomingCarName",
            "displayName",
            "modelText",
        ):
            value = model.get(field_name)

            if isinstance(value, str) and value.strip():
                cleaned_value = cls._strip_brand_name_prefix(
                    value,
                    brand_name,
                )

                if cleaned_value:
                    return cleaned_value

        raise ExternalResponseError(
            "CarDekho model does not contain a valid name: "
            f"source={source_name}, "
            f"index={index}"
        )

    @classmethod
    def _resolve_model_name(
        cls,
        model: Mapping[str, Any],
        *,
        brand_name: str,
        name: str,
    ) -> str:
        for field_name in (
            "modelName",
            "upcomingCarName",
            "title",
            "text",
            "displayName",
            "modelText",
        ):
            value = model.get(field_name)

            if isinstance(value, str) and value.strip():
                return value.strip()

        if name.lower().startswith(f"{brand_name.lower()} "):
            return name

        return f"{brand_name} {name}"

    @classmethod
    def _resolve_model_slug(
        cls,
        model: Mapping[str, Any],
        *,
        brand_slug: str,
        name: str,
        model_name: str,
    ) -> str | None:
        for field_name in (
            "slug",
            "variantSlug",
        ):
            slug = cls._strip_brand_slug_prefix(
                cls._slugify(model.get(field_name)),
                brand_slug,
            )

            if slug and SLUG_PATTERN.fullmatch(slug):
                return slug

        for field_name in (
            "modelUrl",
            "upcomingCarUrl",
            "modelPriceURL",
            "reviewPageURL",
            "modelPictureURL",
            "modelOfferURL",
            "link",
            "url",
        ):
            slug = cls._extract_slug_from_url(
                model.get(field_name),
                brand_slug=brand_slug,
            )

            if slug:
                return slug

        for candidate in (
            name,
            model_name,
        ):
            slug = cls._strip_brand_slug_prefix(
                cls._slugify(candidate),
                brand_slug,
            )

            if slug and SLUG_PATTERN.fullmatch(slug):
                return slug

        return None

    @classmethod
    def _resolve_expected_launch_date(
        cls,
        model: Mapping[str, Any],
    ) -> str | None:
        for field_name in (
            "expectedLaunchDate",
            "launchDate",
            "launchedAt",
            "launchedDate",
        ):
            value = cls._normalize_optional_string(model.get(field_name))

            if value is not None:
                return value

        return None

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
        model_id = cls._resolve_model_id(
            model,
            brand_slug=brand_slug,
            index=index,
            source_name=source_name,
        )

        name = cls._resolve_name(
            model,
            brand_name=brand_name,
            index=index,
            source_name=source_name,
        )

        model_name = cls._resolve_model_name(
            model,
            brand_name=brand_name,
            name=name,
        )

        slug = cls._resolve_model_slug(
            model,
            brand_slug=brand_slug,
            name=name,
            model_name=model_name,
        )

        if not slug:
            raise ExternalResponseError(
                "CarDekho model slug could not be resolved: "
                f"source={source_name}, "
                f"index={index}, "
                f"model_id={model_id}, "
                f"name={name!r}, "
                f"model_name={model_name!r}"
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
            expected_launch_date = cls._resolve_expected_launch_date(model)

            if expected_launch_date is not None:
                normalized_model["expectedLaunchDate"] = expected_launch_date

        return normalized_model

    @classmethod
    def _parse_car_models(
        cls,
        data: Mapping[str, Any],
        *,
        brand_id: int,
        brand_name: str,
        brand_slug: str,
        model_status: str,
        is_upcoming: bool,
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
                    is_upcoming=is_upcoming,
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
                "contains an invalid data.upcomingCars object"
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
                "contains an invalid data.upcomingCars.items field"
            )

        models: list[dict[str, Any]] = []

        for index, raw_model in enumerate(raw_items):
            if not isinstance(
                raw_model,
                Mapping,
            ):
                raise ExternalResponseError(
                    "CarDekho upcomingCars.items contains an invalid item: "
                    f"index={index}"
                )

            models.append(
                cls._normalize_model(
                    raw_model,
                    brand_id=brand_id,
                    brand_name=brand_name,
                    brand_slug=brand_slug,
                    model_status="UPCOMING",
                    is_upcoming=True,
                    index=index,
                    source_name="data.upcomingCars.items",
                )
            )

        return models

    @classmethod
    def _parse_expired_models(
        cls,
        data: Mapping[str, Any],
        *,
        brand_id: int,
        brand_name: str,
        brand_slug: str,
    ) -> list[dict[str, Any]]:
        raw_expired_cars = data.get("ExpiredCars")

        if raw_expired_cars is None:
            raw_expired_cars = data.get("expiredCars")

        if raw_expired_cars is None:
            return []

        if not isinstance(
            raw_expired_cars,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho brand-model API response "
                "contains an invalid data.ExpiredCars object"
            )

        raw_items = raw_expired_cars.get("list")

        if raw_items is None:
            raw_items = raw_expired_cars.get("items")

        if raw_items is None:
            return []

        if not isinstance(
            raw_items,
            list,
        ):
            raise ExternalResponseError(
                "CarDekho brand-model API response "
                "contains an invalid data.ExpiredCars.list field"
            )

        models: list[dict[str, Any]] = []

        for index, raw_model in enumerate(raw_items):
            if not isinstance(
                raw_model,
                Mapping,
            ):
                raise ExternalResponseError(
                    "CarDekho ExpiredCars.list contains an invalid item: "
                    f"index={index}"
                )

            models.append(
                cls._normalize_model(
                    raw_model,
                    brand_id=brand_id,
                    brand_name=brand_name,
                    brand_slug=brand_slug,
                    model_status="DISCONTINUED",
                    is_upcoming=False,
                    index=index,
                    source_name="data.ExpiredCars.list",
                )
            )

        return models

    @staticmethod
    def _merge_models(
        *,
        car_models: list[dict[str, Any]],
        upcoming_models: list[dict[str, Any]],
        expired_models: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        deduplicated_models: dict[
            int,
            dict[str, Any],
        ] = {}

        for model in car_models:
            deduplicated_models[model["id"]] = model

        for model in upcoming_models:
            model_id = model["id"]

            if model_id not in deduplicated_models:
                deduplicated_models[model_id] = model

        for model in expired_models:
            model_id = model["id"]

            if model_id not in deduplicated_models:
                deduplicated_models[model_id] = model

        return list(deduplicated_models.values())

    async def execute(
        self,
        *,
        brand: Mapping[str, Any],
    ) -> list[dict[str, Any]]:
        (
            stored_brand_id,
            stored_brand_name,
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
            fallback_brand_id=stored_brand_id,
            fallback_brand_name=stored_brand_name,
            expected_source_brand_slug=(source_brand_slug),
            expected_model_request_slug=(model_request_slug),
        )

        if source_brand_status == "EXPIRED":
            car_model_status = "DISCONTINUED"
            car_is_upcoming = False
        elif source_brand_status == "UPCOMING":
            car_model_status = "UPCOMING"
            car_is_upcoming = True
        else:
            car_model_status = "CURRENT"
            car_is_upcoming = False

        car_models = self._parse_car_models(
            data,
            brand_id=brand_id,
            brand_name=brand_name,
            brand_slug=brand_slug,
            model_status=car_model_status,
            is_upcoming=car_is_upcoming,
        )

        upcoming_models = self._parse_upcoming_models(
            data,
            brand_id=brand_id,
            brand_name=brand_name,
            brand_slug=brand_slug,
        )

        expired_models = self._parse_expired_models(
            data,
            brand_id=brand_id,
            brand_name=brand_name,
            brand_slug=brand_slug,
        )

        models = self._merge_models(
            car_models=car_models,
            upcoming_models=upcoming_models,
            expired_models=expired_models,
        )

        if not models:
            raise ExternalResponseError(
                "CarDekho brand-model API returned "
                "no models: "
                f"brand={source_brand_slug!r}, "
                f"brand_status={source_brand_status!r}"
            )

        return models
