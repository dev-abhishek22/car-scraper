from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pymongo import UpdateOne
from pymongo.results import BulkWriteResult

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.goodreturns_fuel_graph_price import (
    GoodReturnsFuelGraphPrice,
)

GOODRETURNS_FUEL_GRAPH_PRICES_COLLECTION = "goodreturns_fuel_graph_prices"


@dataclass(frozen=True, slots=True)
class FuelGraphPriceBulkUpsertResult:
    received: int
    processed: int
    matched: int
    modified: int
    inserted: int

    def to_dict(self) -> dict[str, int]:
        return {
            "received": self.received,
            "processed": self.processed,
            "matched": self.matched,
            "modified": self.modified,
            "inserted": self.inserted,
        }


class GoodReturnsFuelGraphRepository:
    def __init__(
        self,
        connection: MongoConnection = mongo_connection,
    ) -> None:
        self._connection = connection

    async def ensure_indexes(self) -> None:
        await self._connection.connect()

        collection = self._connection.collection(
            GOODRETURNS_FUEL_GRAPH_PRICES_COLLECTION,
        )

        await collection.create_index(
            [
                ("source", 1),
                ("fuelType", 1),
                ("citySlug", 1),
                ("timeframe", 1),
            ],
            name="idx_goodreturns_fuel_graph_identity",
        )

        await collection.create_index(
            [
                ("cityId", 1),
                ("fuelType", 1),
                ("timeframe", 1),
            ],
            name="idx_goodreturns_fuel_graph_city_fuel",
        )

        await collection.create_index(
            [
                ("scrapedAt", -1),
            ],
            name="idx_goodreturns_fuel_graph_scraped_at",
        )

        await collection.create_index(
            [
                ("lastRunId", 1),
            ],
            name="idx_goodreturns_fuel_graph_last_run_id",
        )

    async def get_existing_price_ids(
        self,
        document_ids: list[str],
    ) -> set[str]:
        if not document_ids:
            return set()

        await self._connection.connect()

        collection = self._connection.collection(
            GOODRETURNS_FUEL_GRAPH_PRICES_COLLECTION,
        )

        existing_ids: set[str] = set()

        cursor = collection.find(
            {
                "_id": {
                    "$in": document_ids,
                }
            },
            {
                "_id": 1,
            },
        )

        async for document in cursor:
            document_id = document.get("_id")

            if isinstance(document_id, str):
                existing_ids.add(document_id)

        return existing_ids

    async def bulk_upsert_prices(
        self,
        prices: list[GoodReturnsFuelGraphPrice],
    ) -> FuelGraphPriceBulkUpsertResult:
        if not prices:
            return FuelGraphPriceBulkUpsertResult(
                received=0,
                processed=0,
                matched=0,
                modified=0,
                inserted=0,
            )

        await self._connection.connect()

        collection = self._connection.collection(
            GOODRETURNS_FUEL_GRAPH_PRICES_COLLECTION,
        )

        operations: list[UpdateOne] = []

        for price in prices:
            document = price.to_mongo()

            document_id = document.pop(
                "_id",
            )

            created_at = document.pop(
                "createdAt",
                price.created_at,
            )

            operations.append(
                UpdateOne(
                    {
                        "_id": document_id,
                    },
                    {
                        "$set": document,
                        "$setOnInsert": {
                            "createdAt": created_at,
                        },
                    },
                    upsert=True,
                )
            )

        result: BulkWriteResult = await collection.bulk_write(
            operations,
            ordered=False,
        )

        return FuelGraphPriceBulkUpsertResult(
            received=len(prices),
            processed=len(operations),
            matched=result.matched_count,
            modified=result.modified_count,
            inserted=result.upserted_count,
        )

    async def get_by_document_id(
        self,
        document_id: str,
    ) -> dict[str, Any] | None:
        normalized_document_id = document_id.strip()

        if not normalized_document_id:
            raise ValueError("document_id cannot be empty")

        await self._connection.connect()

        collection = self._connection.collection(
            GOODRETURNS_FUEL_GRAPH_PRICES_COLLECTION,
        )

        document = await collection.find_one(
            {
                "_id": normalized_document_id,
            }
        )

        if document is None:
            return None

        return dict(document)

    async def count(
        self,
        *,
        fuel_type: str | None = None,
        timeframe: str | None = None,
    ) -> int:
        query: dict[str, Any] = {}

        if fuel_type is not None:
            normalized_fuel_type = fuel_type.strip().lower()

            if not normalized_fuel_type:
                raise ValueError("fuel_type cannot be empty")

            query["fuelType"] = normalized_fuel_type

        if timeframe is not None:
            normalized_timeframe = timeframe.strip()

            if not normalized_timeframe:
                raise ValueError("timeframe cannot be empty")

            query["timeframe"] = normalized_timeframe

        await self._connection.connect()

        collection = self._connection.collection(
            GOODRETURNS_FUEL_GRAPH_PRICES_COLLECTION,
        )

        return await collection.count_documents(query)


goodreturns_fuel_graph_repository = GoodReturnsFuelGraphRepository()
