from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence

from pymongo import UpdateOne
from pymongo.results import BulkWriteResult

from src.databases.mongodb import MongoConnection, mongo_connection
from src.models.carwale_city_price import CarWaleCityPrice

CARWALE_CITY_PRICES_COLLECTION = "carwale_city_prices"


@dataclass(frozen=True)
class BulkUpsertResult:
    received: int
    processed: int
    matched: int
    modified: int
    inserted: int


class CarWaleCityPriceRepository:
    def __init__(
        self,
        connection: MongoConnection = mongo_connection,
    ) -> None:
        self._connection = connection

    async def bulk_upsert(
        self,
        records: Sequence[CarWaleCityPrice],
    ) -> BulkUpsertResult:
        if not records:
            return BulkUpsertResult(
                received=0,
                processed=0,
                matched=0,
                modified=0,
                inserted=0,
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICES_COLLECTION)

        deduplicated_records: dict[
            tuple[int, int],
            CarWaleCityPrice,
        ] = {}

        for record in records:
            key = (
                record.version_id,
                record.city_id,
            )

            deduplicated_records[key] = record

        created_at = datetime.now(timezone.utc)

        operations = []

        for record in deduplicated_records.values():
            document = record.to_mongo_document()

            operations.append(
                UpdateOne(
                    filter={
                        "versionId": record.version_id,
                        "cityId": record.city_id,
                    },
                    update={
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

        return BulkUpsertResult(
            received=len(records),
            processed=len(operations),
            matched=result.matched_count,
            modified=result.modified_count,
            inserted=result.upserted_count,
        )


carwale_city_price_repository = CarWaleCityPriceRepository()
