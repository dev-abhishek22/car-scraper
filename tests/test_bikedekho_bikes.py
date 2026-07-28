from __future__ import annotations

import asyncio
from typing import Any

from src.external.executors.bikedekho.bikes import BikeDekhoBikesExecutor
from src.models.bikedekho_bike import BikeDekhoBike


class StubClient:
    def __init__(self, response: dict[str, Any]) -> None:
        self.response = response
        self.request: dict[str, Any] | None = None

    async def get_json(self, **request: Any) -> dict[str, Any]:
        self.request = request
        return self.response


class SequenceStubClient:
    def __init__(self, responses: list[dict[str, Any]]) -> None:
        self.responses = responses
        self.requests: list[dict[str, Any]] = []

    async def get_json(self, **request: Any) -> dict[str, Any]:
        self.requests.append(request)
        return self.responses.pop(0)


def test_executor_extracts_requested_bike_sections() -> None:
    response = {
        "data": {
            "overview": {
                "id": 1294,
                "id_brand": 28,
                "brandName": "Honda",
                "brandSlug": "honda",
                "modelSlug": "shine",
                "name": "Honda Shine",
                "fuelType": "Petrol",
            },
            "variantTable": [
                {
                    "childs": [
                        {
                            "items": [
                                {
                                    "variantId": 4637,
                                    "variantSlug": "shine-125-drum",
                                }
                            ]
                        }
                    ]
                }
            ],
            "navComapre": [{"modelName2": "Hero Splendor Plus"}],
            "similarBikes": {
                "items": [{"modelId": 999, "modelName": "Must not be stored"}]
            },
            "specsComparisonV2": {
                "list": [
                    {
                        "modelName": "Hero Glamour",
                        "modelSlug": "glamour",
                        "brandSlug": "hero",
                        "specs": {
                            "Mileage": "55 kmpl",
                            "Engine": "124.7 cc",
                        },
                    }
                ]
            },
            "newsAndCollection": {"items": [{"title": "Must not be stored"}]},
        }
    }
    client = StubClient(response)
    executor = BikeDekhoBikesExecutor(client=client)  # type: ignore[arg-type]

    bike = asyncio.run(
        executor.execute(model={"brandSlug": "honda", "slug": "shine"})
    )

    assert bike["totalVariants"] == 1
    assert bike["totalComparisons"] == 1
    assert bike["totalSimilarBikes"] == 1
    assert bike["similarBikes"][0]["modelSlug"] == "glamour"
    assert bike["similarBikes"][0]["specs"]["Engine"] == "124.7 cc"
    assert "newsAndCollection" not in bike
    assert client.request is not None
    assert client.request["params"]["url"] == "honda/shine"


def test_bike_model_supports_source_model_without_numeric_id() -> None:
    bike = BikeDekhoBike.create(
        model={
            "_id": "bikedekho:model:honda:cbr650r",
            "id": None,
            "brandId": None,
            "brandName": "Honda",
            "brandSlug": "honda",
            "name": "Honda CBR650R",
            "slug": "cbr650r",
            "modelName": "Honda CBR650R",
            "modelStatus": "DISCONTINUED",
            "isUpcoming": False,
            "lastRunId": "models-run",
        },
        bike_data={
            "overview": {"id": 2000, "id_brand": 28},
            "variants": [],
            "compareWith": [],
            "similarBikes": [],
            "totalVariants": 0,
            "totalComparisons": 0,
            "totalSimilarBikes": 0,
        },
        run_id="bikes-run",
    )

    assert bike.document_id == "bikedekho:bike:honda:cbr650r"
    assert bike.model_id == 2000
    assert bike.brand_id == 28


def test_executor_follows_application_redirect() -> None:
    client = SequenceStubClient(
        [
            {
                "status": "true",
                "data": {
                    "redirect": {
                        "redirectURL": "/bmw-scooters/c-400-gt",
                        "statusCode": 301,
                        "error": True,
                    }
                },
            },
            {
                "status": "true",
                "data": {
                    "overview": {
                        "id": 2402,
                        "id_brand": 46,
                        "brandSlug": "bmw",
                        "modelSlug": "c-400-gt",
                    },
                    "variantTable": [],
                    "navComapre": [],
                    "specsComparisonV2": {"list": []},
                },
            },
        ]
    )
    executor = BikeDekhoBikesExecutor(client=client)  # type: ignore[arg-type]

    bike = asyncio.run(
        executor.execute(model={"brandSlug": "bmw", "slug": "c-400-gt"})
    )

    assert bike["overview"]["id"] == 2402
    assert len(client.requests) == 2
    assert client.requests[0]["params"]["url"] == "bmw/c-400-gt"
    assert client.requests[1]["params"]["url"] == "bmw-scooters/c-400-gt"
