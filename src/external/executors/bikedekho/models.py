from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from src.clients.async_client import AsyncExternalHttpClient
from src.clients.client import ExternalResponseError
from src.external.constants.bikedekho import BIKEDEKHO_BRAND_PAGE

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class BikeDekhoModelsExecutor:
    def __init__(self, client: AsyncExternalHttpClient) -> None:
        self._client = client

    @staticmethod
    def _mapping(value: Any, field: str) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            raise ExternalResponseError(f"BikeDekho {field} must be an object")
        return value

    @staticmethod
    def _items(container: Any, field: str) -> list[Any]:
        if container in (None, False, "") or container == []:
            return []
        mapping = BikeDekhoModelsExecutor._mapping(container, field)
        items = mapping.get("items")
        if items is None:
            return []
        if not isinstance(items, list):
            raise ExternalResponseError(f"BikeDekho {field}.items must be a list")
        return items

    @classmethod
    def _normalize(
        cls,
        value: Any,
        *,
        status: str,
        brand_name: str,
        brand_slug: str,
        index: int,
        source: str,
    ) -> dict[str, Any]:
        item = cls._mapping(value, f"{source}[{index}]")
        raw_slug = item.get("modelSlug") or item.get("slug")
        if not isinstance(raw_slug, str):
            raise ExternalResponseError(f"BikeDekho {source}[{index}] has no slug")
        slug = raw_slug.strip().lower().replace("_", "-")
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = re.sub(r"-+", "-", slug).strip("-")
        if not SLUG_PATTERN.fullmatch(slug):
            raise ExternalResponseError(f"Invalid BikeDekho model slug: {slug!r}")

        raw_name = item.get("modelName") or item.get("name") or item.get("text")
        if not isinstance(raw_name, str) or not raw_name.strip():
            raise ExternalResponseError(f"BikeDekho {source}[{index}] has no name")

        model_id = item.get("modelId", item.get("id", item.get("_id")))
        if isinstance(model_id, bool) or not isinstance(model_id, int) or model_id <= 0:
            model_id = None

        brand_id = item.get("idBrand", item.get("brandId"))
        if isinstance(brand_id, bool) or not isinstance(brand_id, int) or brand_id <= 0:
            brand_id = None

        return {
            "id": model_id,
            "brandId": brand_id,
            "brandName": brand_name,
            "brandSlug": brand_slug,
            "name": raw_name.strip(),
            "slug": slug,
            "modelName": raw_name.strip(),
            "modelStatus": status,
            "isUpcoming": status == "UPCOMING",
        }

    async def execute(self, *, brand: Mapping[str, Any]) -> list[dict[str, Any]]:
        brand_name = brand.get("brandName")
        brand_slug = brand.get("slug")
        if not isinstance(brand_name, str) or not brand_name.strip():
            raise ValueError("brand.brandName must be a non-empty string")
        if not isinstance(brand_slug, str) or not SLUG_PATTERN.fullmatch(brand_slug):
            raise ValueError("brand.slug must be a valid slug")

        # Build the request from the slug read from MongoDB. This avoids
        # depending on stale or malformed stored brand URLs.
        brand_url = f"/{brand_slug}-bikes"

        endpoint = BIKEDEKHO_BRAND_PAGE
        response = await self._client.get_json(
            endpoint=endpoint.path,
            params={**endpoint.default_params, "url": brand_url},
            headers=endpoint.default_headers,
        )
        root = self._mapping(response, "response")
        data = self._mapping(root.get("data"), "data")

        sources = (
            (self._items(data.get("primaryData"), "data.primaryData"), "CURRENT", "primaryData.items"),
            (self._items(data.get("upcoming"), "data.upcoming"), "UPCOMING", "upcoming.items"),
            (self._items(data.get("discontinueBikes"), "data.discontinueBikes"), "DISCONTINUED", "discontinueBikes.items"),
        )
        priority = {"DISCONTINUED": 1, "UPCOMING": 2, "CURRENT": 3}
        deduplicated: dict[str, dict[str, Any]] = {}
        for items, status, source in sources:
            for index, item in enumerate(items):
                model = self._normalize(
                    item,
                    status=status,
                    brand_name=brand_name.strip(),
                    brand_slug=brand_slug,
                    index=index,
                    source=source,
                )
                existing = deduplicated.get(model["slug"])
                if existing is None or priority[status] > priority[existing["modelStatus"]]:
                    deduplicated[model["slug"]] = model
        return list(deduplicated.values())
