from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

from src.clients.async_client import AsyncExternalHttpClient
from src.clients.client import ExternalResponseError
from src.external.constants.bikedekho import BIKEDEKHO_MODEL_OVERVIEW


class BikeDekhoBikesExecutor:
    MAX_REDIRECTS = 5

    def __init__(self, client: AsyncExternalHttpClient) -> None:
        self._client = client

    @staticmethod
    def _mapping(value: Any, field: str) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            raise ExternalResponseError(f"BikeDekho {field} must be an object")
        return value

    @staticmethod
    def _list(value: Any, field: str) -> list[Any]:
        if value in (None, False, ""):
            return []
        if not isinstance(value, list):
            raise ExternalResponseError(f"BikeDekho {field} must be an array")
        return value

    async def _fetch_data(
        self,
        *,
        brand_slug: str,
        model_slug: str,
    ) -> Mapping[str, Any]:
        endpoint = BIKEDEKHO_MODEL_OVERVIEW
        request_url = f"{brand_slug}/{model_slug}"
        visited_urls: set[str] = set()

        for redirect_count in range(self.MAX_REDIRECTS + 1):
            if request_url in visited_urls:
                raise ExternalResponseError(
                    f"BikeDekho modelOverview redirect loop: url={request_url!r}"
                )
            visited_urls.add(request_url)

            response = await self._client.get_json(
                endpoint=endpoint.path,
                params={
                    **endpoint.default_params,
                    "brandSlug": brand_slug,
                    "modelSlug": model_slug,
                    "url": request_url,
                },
                headers=endpoint.default_headers,
            )
            data = self._mapping(
                self._mapping(response, "response").get("data"),
                "data",
            )
            overview = data.get("overview")
            if isinstance(overview, Mapping):
                return data

            redirect = data.get("redirect")
            if not isinstance(redirect, Mapping):
                raise ExternalResponseError(
                    "BikeDekho data.overview must be an object"
                )

            redirect_url = redirect.get("redirectURL")
            status_code = redirect.get("statusCode")
            if (
                not isinstance(redirect_url, str)
                or not redirect_url.strip()
                or status_code not in {301, 302, 307, 308}
            ):
                raise ExternalResponseError(
                    "BikeDekho modelOverview returned an invalid redirect"
                )

            path = urlsplit(redirect_url).path.strip("/")
            if not path:
                raise ExternalResponseError(
                    "BikeDekho modelOverview redirect URL has no path"
                )
            request_url = path

            if redirect_count == self.MAX_REDIRECTS:
                raise ExternalResponseError(
                    "BikeDekho modelOverview exceeded the redirect limit"
                )

        raise ExternalResponseError(
            "BikeDekho modelOverview exceeded the redirect limit"
        )

    @classmethod
    def _variants(cls, value: Any) -> list[dict[str, Any]]:
        variants: list[dict[str, Any]] = []
        for group_index, group in enumerate(cls._list(value, "data.variantTable")):
            group_map = cls._mapping(group, f"variantTable[{group_index}]")
            for child_index, child in enumerate(
                cls._list(group_map.get("childs"), "variantTable.childs")
            ):
                child_map = cls._mapping(child, f"childs[{child_index}]")
                for item_index, item in enumerate(
                    cls._list(child_map.get("items"), "variantTable.childs.items")
                ):
                    variants.append(
                        dict(
                            cls._mapping(
                                item,
                                f"variantTable.childs.items[{item_index}]",
                            )
                        )
                    )
        return variants

    async def execute(self, *, model: Mapping[str, Any]) -> dict[str, Any]:
        brand_slug = model.get("brandSlug")
        model_slug = model.get("slug")
        if not isinstance(brand_slug, str) or not brand_slug:
            raise ValueError("model.brandSlug must be a non-empty string")
        if not isinstance(model_slug, str) or not model_slug:
            raise ValueError("model.slug must be a non-empty string")

        data = await self._fetch_data(
            brand_slug=brand_slug,
            model_slug=model_slug,
        )
        overview = dict(self._mapping(data.get("overview"), "data.overview"))
        response_brand_slug = overview.get("brandSlug")
        response_model_slug = overview.get("modelSlug")
        if response_brand_slug != brand_slug or response_model_slug != model_slug:
            raise ExternalResponseError(
                "BikeDekho modelOverview identity does not match the requested model"
            )

        variants = self._variants(data.get("variantTable"))
        comparisons = [
            dict(self._mapping(item, f"data.navComapre[{index}]"))
            for index, item in enumerate(
                self._list(data.get("navComapre"), "data.navComapre")
            )
        ]
        similar_container = data.get("specsComparisonV2")
        if similar_container in (None, False, ""):
            similar_bikes: list[dict[str, Any]] = []
        else:
            similar_map = self._mapping(
                similar_container,
                "data.specsComparisonV2",
            )
            similar_bikes = [
                dict(
                    self._mapping(
                        item,
                        f"data.specsComparisonV2.list[{index}]",
                    )
                )
                for index, item in enumerate(
                    self._list(
                        similar_map.get("list"),
                        "data.specsComparisonV2.list",
                    )
                )
            ]

        return {
            "overview": overview,
            "variants": variants,
            "compareWith": comparisons,
            "similarBikes": similar_bikes,
            "totalVariants": len(variants),
            "totalComparisons": len(comparisons),
            "totalSimilarBikes": len(similar_bikes),
        }
