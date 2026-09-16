from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.clients.async_client import AsyncExternalHttpClient
from src.external.constants.cardekho import CARDEKHO_MODEL_GALLERY_POPUP
from src.external.executors.base import BaseApiExecutor


class CarDekhoModelImagesExecutor(BaseApiExecutor):
    def __init__(
        self,
        client: AsyncExternalHttpClient,
    ) -> None:
        self.client = client

    async def execute(
        self,
        *,
        model_slug: str,
    ) -> dict[str, Any]:
        if not isinstance(model_slug, str) or not model_slug.strip():
            raise ValueError("model_slug cannot be empty")

        endpoint = CARDEKHO_MODEL_GALLERY_POPUP

        params = {
            **endpoint.default_params,
            "modelSlug": model_slug.strip().lower(),
        }

        headers = dict(
            endpoint.default_headers,
        )

        response = await self.client.get_json(
            endpoint.path,
            params=params,
            headers=headers,
        )

        if not isinstance(response, Mapping):
            raise ValueError(
                "CarDekho gallery response must be an object"
            )

        if response.get("status") is not True:
            raise ValueError(
                "CarDekho gallery API returned unsuccessful status"
            )

        data = response.get("data")

        if not isinstance(data, Mapping):
            raise ValueError(
                "CarDekho gallery response data must be an object"
            )

        images = data.get("images")

        if images is None:
            redirect = data.get("redirect")

            if isinstance(redirect, Mapping):
                return {
                    "images": [],
                    "title": "",
                }

            raise ValueError(
                "CarDekho gallery response images are missing"
            )

        if not isinstance(images, list):
            raise ValueError(
                "CarDekho gallery response images must be an array"
            )

        title = data.get("title")

        if not isinstance(title, str):
            title = ""

        return {
            "images": images,
            "title": title.strip(),
        }
