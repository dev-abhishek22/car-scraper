from __future__ import annotations

import asyncio
from typing import Any

from src.external.executors.bikedekho.models import BikeDekhoModelsExecutor
from src.models.bikedekho_model import BikeDekhoModel


class StubClient:
    def __init__(self, response: dict[str, Any]) -> None:
        self.response = response
        self.last_request: dict[str, Any] | None = None

    async def get_json(self, **request: Any) -> dict[str, Any]:
        self.last_request = request
        return self.response


def test_executor_extracts_all_three_model_statuses() -> None:
    response = {
        "status": "true",
        "data": {
            "primaryData": {
                "items": [
                    {
                        "_id": 2294,
                        "modelId": 2294,
                        "idBrand": 28,
                        "modelName": "Honda SP 125",
                        "modelSlug": "sp125",
                        "modelUrl": "/honda/sp125",
                        "status": "Launched",
                        "upcoming": True,
                    }
                ]
            },
            "upcoming": {
                "items": [
                    {
                        "modelId": 2460,
                        "idBrand": 28,
                        "modelName": "Honda Shine Electric",
                        "modelSlug": "shine-electric",
                        "modelUrl": "/honda/shine-electric",
                        "launchedAt": "Jan, 2028",
                        "upcoming": False,
                    }
                ]
            },
            "discontinueBikes": {
                "items": [
                    {
                        "name": "Honda CBR650R",
                        "slug": "cbr650r",
                        "url": "/honda/cbr650r",
                    }
                ]
            },
        },
    }
    brand = {
        "_id": "bikedekho:brand:honda",
        "brandName": "Honda",
        "slug": "honda",
        "brandUrl": "/honda-bikes",
    }
    client = StubClient(response)
    executor = BikeDekhoModelsExecutor(client=client)  # type: ignore[arg-type]

    models = asyncio.run(executor.execute(brand=brand))

    assert {model["modelStatus"] for model in models} == {
        "CURRENT",
        "UPCOMING",
        "DISCONTINUED",
    }
    current = next(model for model in models if model["modelStatus"] == "CURRENT")
    upcoming = next(model for model in models if model["modelStatus"] == "UPCOMING")
    discontinued = next(
        model for model in models if model["modelStatus"] == "DISCONTINUED"
    )
    assert current["isUpcoming"] is False
    assert upcoming["expectedLaunchDate"] == "Jan, 2028"
    assert discontinued["id"] is None
    assert "_id" not in current
    assert client.last_request is not None
    assert client.last_request["params"]["url"] == "/honda-bikes"


def test_executor_accepts_empty_optional_sections_and_normalizes_slug() -> None:
    response = {
        "data": {
            "primaryData": {
                "items": [
                    {
                        "modelId": 1,
                        "modelName": "Royal Enfield Bullet Electra",
                        "modelSlug": "royal_enfield_bullet_electra",
                    }
                ]
            },
            "upcoming": [],
            "discontinueBikes": False,
        }
    }
    executor = BikeDekhoModelsExecutor(client=StubClient(response))  # type: ignore[arg-type]

    models = asyncio.run(
        executor.execute(
            brand={
                "brandName": "Royal Enfield",
                "slug": "royal-enfield",
                "brandUrl": "/ignored",
            }
        )
    )

    assert models[0]["slug"] == "royal-enfield-bullet-electra"


def test_discontinued_model_uses_slug_based_document_id() -> None:
    model = BikeDekhoModel.create(
        brand={"_id": "bikedekho:brand:honda", "slug": "honda"},
        model={
            "id": None,
            "brandId": None,
            "brandName": "Honda",
            "brandSlug": "honda",
            "name": "Honda CBR650R",
            "slug": "cbr650r",
            "modelName": "Honda CBR650R",
            "modelStatus": "DISCONTINUED",
            "isUpcoming": False,
            "modelUrl": "/honda/cbr650r",
        },
        run_id="run-1",
    )

    assert model.document_id == "bikedekho:model:honda:cbr650r"
    assert model.to_mongo_document()["modelUrl"] == "/honda/cbr650r"
