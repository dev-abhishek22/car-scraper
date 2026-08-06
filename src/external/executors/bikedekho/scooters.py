from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.external.executors.bikedekho.bikes import BikeDekhoBikesExecutor


class BikeDekhoScootersExecutor(BikeDekhoBikesExecutor):
    """Fetch scooter model-overview data from BikeDekho."""

    async def execute(self, *, model: Mapping[str, Any]) -> dict[str, Any]:
        normalized_model = dict(model)
        brand_slug = normalized_model.get("brandSlug")
        model_slug = normalized_model.get("slug")
        if (
            isinstance(brand_slug, str)
            and isinstance(model_slug, str)
            and model_slug.startswith(f"{brand_slug}-")
        ):
            normalized_model["slug"] = model_slug[len(brand_slug) + 1 :]

        return await super().execute(model=normalized_model)
