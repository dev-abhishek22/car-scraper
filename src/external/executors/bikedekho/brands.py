from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from src.clients.async_client import AsyncExternalHttpClient
from src.clients.client import ExternalResponseError
from src.external.constants.base import ApiEndpoint
from src.external.constants.bikedekho import (
    BIKEDEKHO_NEW_BIKES,
    BIKEDEKHO_SCOOTERS,
)

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class BikeDekhoBrandsExecutor:
    """Fetch only ``data.newCars.bikeBrands.items`` from BikeDekho."""

    def __init__(
        self,
        client: AsyncExternalHttpClient,
        endpoint: ApiEndpoint = BIKEDEKHO_NEW_BIKES,
    ) -> None:
        self._client = client
        self._endpoint = endpoint

    @staticmethod
    def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            raise ExternalResponseError(
                f"BikeDekho response does not contain a valid {field_name} object"
            )
        return value

    @staticmethod
    def _string(value: Any, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ExternalResponseError(f"{field_name} must be a non-empty string")
        return value.strip()

    @classmethod
    def _parse_item(cls, value: Any, index: int) -> dict[str, Any]:
        item = cls._mapping(value, f"bikeBrands.items[{index}]")
        name = cls._string(item.get("name") or item.get("text"), "name")
        slug = cls._string(item.get("link_rewrite"), "link_rewrite").lower()

        if not SLUG_PATTERN.fullmatch(slug):
            raise ExternalResponseError(f"Invalid BikeDekho brand slug: {slug!r}")

        url = cls._string(item.get("url"), "url")
        title = item.get("title")
        image_url = item.get("imgUrl")
        filter_name = item.get("filtername")
        popularity = item.get("popularity")
        model_count = item.get("count")

        for field_name, field_value in (
            ("title", title),
            ("imgUrl", image_url),
            ("filtername", filter_name),
        ):
            if field_value is not None and not isinstance(field_value, str):
                raise ExternalResponseError(f"{field_name} must be a string or null")

        for field_name, field_value in (
            ("popularity", popularity),
            ("count", model_count),
        ):
            if (
                field_value is not None
                and (
                    isinstance(field_value, bool)
                    or not isinstance(field_value, int)
                    or field_value < 0
                )
            ):
                raise ExternalResponseError(
                    f"{field_name} must be a non-negative integer or null"
                )

        return {
            "brandName": name,
            "slug": slug,
            "brandUrl": url,
            "title": title.strip() if isinstance(title, str) else None,
            "image": image_url.strip() if isinstance(image_url, str) else None,
            "filterName": (
                filter_name.strip() if isinstance(filter_name, str) else None
            ),
            "popularity": popularity,
            "modelCount": model_count,
        }

    async def execute(self) -> list[dict[str, Any]]:
        endpoint = self._endpoint
        response = await self._client.get_json(
            endpoint=endpoint.path,
            params=endpoint.default_params,
            headers=endpoint.default_headers,
        )

        root = self._mapping(response, "response")
        data = self._mapping(root.get("data"), "data")
        new_cars = self._mapping(data.get("newCars"), "data.newCars")
        bike_brands = self._mapping(
            new_cars.get("bikeBrands"), "data.newCars.bikeBrands"
        )
        items = bike_brands.get("items")

        if not isinstance(items, list):
            raise ExternalResponseError(
                "BikeDekho data.newCars.bikeBrands.items must be a list"
            )

        deduplicated: dict[str, dict[str, Any]] = {}
        for index, value in enumerate(items):
            brand = self._parse_item(value, index)
            deduplicated[brand["slug"]] = brand

        return sorted(
            deduplicated.values(),
            key=lambda brand: (
                -(brand["popularity"] or 0),
                brand["brandName"].lower(),
            ),
        )


class BikeDekhoScooterBrandsExecutor(BikeDekhoBrandsExecutor):
    """Fetch scooter brands from BikeDekho's scooters landing page."""

    def __init__(self, client: AsyncExternalHttpClient) -> None:
        super().__init__(client=client, endpoint=BIKEDEKHO_SCOOTERS)
