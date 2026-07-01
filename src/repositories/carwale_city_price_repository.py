from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence

from pymongo import UpdateOne
from pymongo.results import BulkWriteResult

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.carwale_city_price import (
    CarWaleCityPrice,
)

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

    @staticmethod
    def _normalize_run_id(
        run_id: str,
    ) -> str:
        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        return normalized_run_id

    async def get_completed_job_ids(
        self,
        *,
        job_ids: Sequence[str],
        run_id: str,
    ) -> set[str]:
        if not job_ids:
            return set()

        normalized_run_id = self._normalize_run_id(run_id)

        unique_job_ids = list(
            dict.fromkeys(job_id.strip() for job_id in job_ids if job_id.strip())
        )

        if not unique_job_ids:
            return set()

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICES_COLLECTION)

        cursor = collection.find(
            {
                "_id": {
                    "$in": unique_job_ids,
                },
                "lastRunId": normalized_run_id,
            },
            {
                "_id": 1,
            },
        )

        completed_job_ids: set[str] = set()

        async for document in cursor:
            document_id = document.get("_id")

            if isinstance(document_id, str):
                completed_job_ids.add(document_id)

        return completed_job_ids

    async def bulk_upsert(
        self,
        records: Sequence[CarWaleCityPrice],
        *,
        run_id: str,
    ) -> BulkUpsertResult:
        if not records:
            return BulkUpsertResult(
                received=0,
                processed=0,
                matched=0,
                modified=0,
                inserted=0,
            )

        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICES_COLLECTION)

        deduplicated_records: dict[
            str,
            CarWaleCityPrice,
        ] = {}

        for record in records:
            deduplicated_records[record.document_id] = record

        created_at = datetime.now(timezone.utc)

        operations: list[UpdateOne] = []

        for record in deduplicated_records.values():
            document = record.to_mongo_document()

            document["lastRunId"] = normalized_run_id

            operations.append(
                UpdateOne(
                    filter={
                        "_id": (record.document_id),
                    },
                    update={
                        "$set": document,
                        "$setOnInsert": {
                            "createdAt": (created_at),
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
