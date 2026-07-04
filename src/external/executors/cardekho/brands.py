from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

from src.clients.async_client import (
    AsyncExternalHttpClient,
)
from src.clients.client import (
    ExternalResponseError,
)
from src.external.constants.cardekho import (
    CARDEKHO_NEW_CARS,
)

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

BRAND_STATUS_MAP: dict[str, str] = {
    "current": "CURRENT",
    "upcoming": "UPCOMING",
    "expired": "EXPIRED",
    "discontinued": "EXPIRED",
}

BRAND_STATUS_PRIORITY: dict[str, int] = {
    "CURRENT": 3,
    "UPCOMING": 2,
    "EXPIRED": 1,
}


class CarDekhoBrandsExecutor:
    """
    Fetch and normalize the complete CarDekho brand list.

    Primary brand data is read from:

        data.newCars.carBrands

    Optional offer and popularity information is read from:

        data.brands.items

    Both sources are merged using the normalized brand slug.
    """

    def __init__(
        self,
        client: AsyncExternalHttpClient,
    ) -> None:
        self._client = client

    @staticmethod
    def _require_mapping(
        value: Any,
        *,
        field_name: str,
    ) -> Mapping[str, Any]:
        if not isinstance(
            value,
            Mapping,
        ):
            raise ExternalResponseError(
                f"CarDekho response does not contain a valid {field_name} object"
            )

        return value

    @staticmethod
    def _validate_string(
        value: Any,
        *,
        field_name: str,
        allow_empty: bool = False,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ExternalResponseError(f"{field_name} must be a string")

        normalized_value = value.strip()

        if not allow_empty and not normalized_value:
            raise ExternalResponseError(f"{field_name} cannot be empty")

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
    def _normalize_optional_positive_integer(
        value: Any,
    ) -> int | None:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            return None

        return value

    @staticmethod
    def _normalize_optional_non_negative_integer(
        value: Any,
    ) -> int | None:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            return None

        return value

    @staticmethod
    def _normalize_slug(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ExternalResponseError(f"{field_name} must be a string")

        normalized_slug = value.strip().lower().replace("_", "-").replace(" ", "-")

        normalized_slug = re.sub(
            r"-+",
            "-",
            normalized_slug,
        ).strip("-")

        if not normalized_slug:
            raise ExternalResponseError(f"{field_name} cannot be empty")

        if not SLUG_PATTERN.fullmatch(normalized_slug):
            raise ExternalResponseError(
                f"{field_name} contains invalid characters: {normalized_slug!r}"
            )

        return normalized_slug

    @classmethod
    def _extract_model_request_slug(
        cls,
        *,
        brand_url: str,
        fallback_slug: str,
    ) -> str:
        parsed_url = urlsplit(brand_url)

        path = parsed_url.path.strip("/")

        if not path:
            return fallback_slug

        path_parts = [part for part in path.split("/") if part]

        if len(path_parts) >= 2 and path_parts[0].lower() == "cars":
            return cls._normalize_slug(
                path_parts[1],
                field_name="modelRequestSlug",
            )

        last_part = path_parts[-1]

        if last_part.lower().endswith("-cars"):
            last_part = last_part[:-5]

        try:
            return cls._normalize_slug(
                last_part,
                field_name="modelRequestSlug",
            )

        except ExternalResponseError:
            return fallback_slug

    @staticmethod
    def _build_status_flags(
        brand_status: str,
    ) -> dict[str, bool]:
        return {
            "isCurrent": (brand_status == "CURRENT"),
            "isUpcoming": (brand_status == "UPCOMING"),
            "isExpired": (brand_status == "EXPIRED"),
        }

    @classmethod
    def _parse_offer_items(
        cls,
        data: Mapping[str, Any],
    ) -> dict[str, dict[str, Any]]:
        raw_brands = data.get("brands")

        if not isinstance(
            raw_brands,
            Mapping,
        ):
            return {}

        raw_items = raw_brands.get("items")

        if not isinstance(
            raw_items,
            list,
        ):
            return {}

        offer_items: dict[
            str,
            dict[str, Any],
        ] = {}

        for index, raw_item in enumerate(raw_items):
            if not isinstance(
                raw_item,
                Mapping,
            ):
                raise ExternalResponseError(
                    "CarDekho data.brands.items "
                    "contains an invalid item at "
                    f"index {index}"
                )

            raw_slug = raw_item.get("slug")

            if not isinstance(
                raw_slug,
                str,
            ):
                continue

            try:
                slug = cls._normalize_slug(
                    raw_slug,
                    field_name=("data.brands.items.slug"),
                )
            except ExternalResponseError:
                continue

            offer_items[slug] = {
                "id": (cls._normalize_optional_positive_integer(raw_item.get("id"))),
                "image": (cls._normalize_optional_string(raw_item.get("image"))),
                "isPopular": (
                    cls._normalize_optional_non_negative_integer(
                        raw_item.get("isPopular")
                    )
                ),
                "popularity": (
                    cls._normalize_optional_non_negative_integer(
                        raw_item.get("popularity")
                    )
                ),
                "totalOfferCount": (
                    cls._normalize_optional_non_negative_integer(
                        raw_item.get("totalOfferCount")
                    )
                ),
                "offerUrl": (cls._normalize_optional_string(raw_item.get("offerUrl"))),
            }

        return offer_items

    @classmethod
    def _normalize_catalogue_brand(
        cls,
        raw_brand: Mapping[str, Any],
        *,
        brand_status: str,
        index: int,
    ) -> dict[str, Any]:
        brand_name = cls._validate_string(
            raw_brand.get("brandName"),
            field_name=(f"CarDekho catalogue brandName at index {index}"),
        )

        slug = cls._normalize_slug(
            raw_brand.get("slug"),
            field_name=(f"CarDekho catalogue slug at index {index}"),
        )

        brand_url = cls._validate_string(
            raw_brand.get("brandUrl"),
            field_name=(f"CarDekho catalogue brandUrl at index {index}"),
        )

        tool_tip_text = cls._normalize_optional_string(raw_brand.get("toolTipText"))

        image = cls._normalize_optional_string(raw_brand.get("imgUrl"))

        model_request_slug = cls._extract_model_request_slug(
            brand_url=brand_url,
            fallback_slug=slug,
        )

        return {
            "id": None,
            "brandName": brand_name,
            "slug": slug,
            "modelRequestSlug": (model_request_slug),
            "brandStatus": brand_status,
            **cls._build_status_flags(brand_status),
            "brandUrl": brand_url,
            "toolTipText": tool_tip_text,
            "image": image,
            "isPopular": None,
            "popularity": None,
            "totalOfferCount": None,
            "offerUrl": None,
            "hasOfferData": False,
        }

    @classmethod
    def _parse_catalogue_items(
        cls,
        data: Mapping[str, Any],
    ) -> dict[str, dict[str, Any]]:
        new_cars = cls._require_mapping(
            data.get("newCars"),
            field_name="data.newCars",
        )

        raw_groups = new_cars.get("carBrands")

        if not isinstance(
            raw_groups,
            list,
        ):
            raise ExternalResponseError(
                "CarDekho response does not contain "
                "a valid data.newCars.carBrands array"
            )

        catalogue: dict[
            str,
            dict[str, Any],
        ] = {}

        for group_index, raw_group in enumerate(raw_groups):
            if not isinstance(
                raw_group,
                Mapping,
            ):
                raise ExternalResponseError(
                    "CarDekho carBrands contains an "
                    "invalid group at index "
                    f"{group_index}"
                )

            raw_title = raw_group.get("title")

            if not isinstance(
                raw_title,
                str,
            ):
                raise ExternalResponseError(
                    "CarDekho carBrands group title "
                    "must be a string at index "
                    f"{group_index}"
                )

            normalized_title = raw_title.strip().lower()

            brand_status = BRAND_STATUS_MAP.get(normalized_title)

            if brand_status is None:
                continue

            raw_items = raw_group.get("items")

            if not isinstance(
                raw_items,
                list,
            ):
                raise ExternalResponseError(
                    "CarDekho carBrands group does not "
                    "contain a valid items array: "
                    f"title={raw_title!r}"
                )

            for item_index, raw_brand in enumerate(raw_items):
                if not isinstance(
                    raw_brand,
                    Mapping,
                ):
                    raise ExternalResponseError(
                        "CarDekho carBrands items "
                        "contains an invalid brand: "
                        f"group={raw_title!r}, "
                        f"index={item_index}"
                    )

                normalized_brand = cls._normalize_catalogue_brand(
                    raw_brand,
                    brand_status=brand_status,
                    index=item_index,
                )

                slug = normalized_brand["slug"]

                existing_brand = catalogue.get(slug)

                if existing_brand is None:
                    catalogue[slug] = normalized_brand
                    continue

                existing_priority = BRAND_STATUS_PRIORITY[existing_brand["brandStatus"]]

                new_priority = BRAND_STATUS_PRIORITY[brand_status]

                if new_priority > existing_priority:
                    catalogue[slug] = normalized_brand

        if not catalogue:
            raise ExternalResponseError("CarDekho brand catalogue is empty")

        return catalogue

    @classmethod
    def _merge_brand_sources(
        cls,
        *,
        catalogue: dict[
            str,
            dict[str, Any],
        ],
        offer_items: dict[
            str,
            dict[str, Any],
        ],
    ) -> list[dict[str, Any]]:
        merged_brands: list[dict[str, Any]] = []

        for slug, catalogue_brand in catalogue.items():
            merged_brand = dict(catalogue_brand)

            offer_data = offer_items.get(slug)

            if offer_data is not None:
                merged_brand["id"] = offer_data.get("id")

                offer_image = offer_data.get("image")

                if not merged_brand.get("image") and offer_image:
                    merged_brand["image"] = offer_image

                merged_brand["isPopular"] = offer_data.get("isPopular")

                merged_brand["popularity"] = offer_data.get("popularity")

                merged_brand["totalOfferCount"] = offer_data.get("totalOfferCount")

                merged_brand["offerUrl"] = offer_data.get("offerUrl")

                merged_brand["hasOfferData"] = True

            merged_brands.append(merged_brand)

        merged_brands.sort(
            key=lambda brand: (
                -BRAND_STATUS_PRIORITY[brand["brandStatus"]],
                brand["brandName"].lower(),
                brand["slug"],
            )
        )

        return merged_brands

    async def execute(
        self,
    ) -> list[dict[str, Any]]:
        endpoint = CARDEKHO_NEW_CARS

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for the CarDekho brands API"
            )

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params=endpoint.default_params,
            headers=endpoint.default_headers,
        )

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarDekho brands API returned an invalid response. Expected an object"
            )

        data = self._require_mapping(
            response_data.get("data"),
            field_name="data",
        )

        catalogue = self._parse_catalogue_items(data)

        offer_items = self._parse_offer_items(data)

        return self._merge_brand_sources(
            catalogue=catalogue,
            offer_items=offer_items,
        )
