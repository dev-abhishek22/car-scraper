from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.clients.async_client import AsyncExternalHttpClient
from src.clients.client import ExternalResponseError
from src.external.constants.bikedekho import BIKEDEKHO_TRIM_SPECS_FEATURES


class BikeDekhoTrimSpecsFeaturesExecutor:
    """
    Fetch specifications and features for one BikeDekho variant.
    """

    def __init__(self, client: AsyncExternalHttpClient) -> None:
        self._client = client

    @staticmethod
    def _mapping(value: Any, field: str) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            raise ExternalResponseError(f"BikeDekho {field} must be an object")
        return value

    async def fetch(
        self,
        *,
        brand_slug: str,
        model_slug: str,
        variant_slug: str,
        variant_id: int,
    ) -> Mapping[str, Any]:
        endpoint = BIKEDEKHO_TRIM_SPECS_FEATURES

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured "
                "for the BikeDekho trim specs/features API"
            )

        request_url = f"{brand_slug}/{model_slug}/specifications"

        response = await self._client.get_json(
            endpoint=endpoint.path,
            params={
                **endpoint.default_params,
                "brandSlug": brand_slug,
                "modelSlug": model_slug,
                "variantSlug": variant_slug,
                "variantId": variant_id,
                "url": request_url,
            },
            headers=endpoint.default_headers,
        )

        return self._mapping(
            response,
            "response",
        )
