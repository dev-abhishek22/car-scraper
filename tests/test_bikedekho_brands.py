from __future__ import annotations

import asyncio
from typing import Any

from src.external.executors.bikedekho.brands import (
    BikeDekhoBrandsExecutor,
    BikeDekhoScooterBrandsExecutor,
)
from src.models.bikedekho_brand import BikeDekhoBrand


class StubClient:
    def __init__(self, response: dict[str, Any]) -> None:
        self.response = response

    async def get_json(self, **_: Any) -> dict[str, Any]:
        return self.response


class RecordingStubClient(StubClient):
    params: dict[str, Any] | None = None

    async def get_json(self, **kwargs: Any) -> dict[str, Any]:
        self.params = kwargs["params"]
        return self.response


def test_executor_extracts_only_bike_brand_items() -> None:
    response = {
        "status": "true",
        "data": {
            "newCars": {
                "latestCars": {"items": [{"brandName": "Ignore Me"}]},
                "bikeBrands": {
                    "title": "Search New Bikes By Brand",
                    "items": [
                        {
                            "text": "Honda",
                            "url": "/honda-bikes",
                            "title": "Honda Bikes in India",
                            "popularity": 229007,
                            "imgUrl": "https://cdn.bikedekho.com/honda.jpg",
                            "filtername": "Honda",
                            "name": "Honda",
                            "link_rewrite": "honda",
                            "count": 31,
                        }
                    ],
                },
            }
        },
    }

    executor = BikeDekhoBrandsExecutor(client=StubClient(response))  # type: ignore[arg-type]
    brands = asyncio.run(executor.execute())

    assert brands == [
        {
            "brandName": "Honda",
            "slug": "honda",
            "brandUrl": "/honda-bikes",
            "title": "Honda Bikes in India",
            "image": "https://cdn.bikedekho.com/honda.jpg",
            "filterName": "Honda",
            "popularity": 229007,
            "modelCount": 31,
        }
    ]


def test_brand_model_builds_bikedekho_document_id() -> None:
    brand = BikeDekhoBrand.create(
        brand={
            "brandName": "Royal Enfield",
            "slug": "royal-enfield",
            "brandUrl": "/royal-enfield-bikes",
            "title": "Royal Enfield Bikes in India",
            "image": None,
            "filterName": "Royal Enfield",
            "popularity": 229006,
            "modelCount": 59,
        },
        run_id="run-1",
    )

    assert brand.document_id == "bikedekho:brand:royal-enfield"
    assert brand.to_mongo_document()["modelCount"] == 59


def test_scooter_executor_uses_scooters_landing_page() -> None:
    response = {
        "status": "true",
        "data": {
            "newCars": {
                "bikeBrands": {
                    "title": "Search Scooters By Brand",
                    "items": [
                        {
                            "name": "Honda",
                            "url": "/honda-scooters",
                            "title": "Honda Scooters in India",
                            "popularity": 229007,
                            "imgUrl": "https://cdn.bikedekho.com/honda.jpg",
                            "filtername": "Honda",
                            "link_rewrite": "honda",
                            "count": 15,
                        }
                    ],
                }
            }
        },
    }
    client = RecordingStubClient(response)
    brands = asyncio.run(
        BikeDekhoScooterBrandsExecutor(client=client).execute()  # type: ignore[arg-type]
    )

    assert client.params is not None
    assert client.params["url"] == "/scooters"
    assert brands[0]["brandUrl"] == "/honda-scooters"
    assert brands[0]["modelCount"] == 15
