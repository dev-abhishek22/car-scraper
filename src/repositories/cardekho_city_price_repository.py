from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from pymongo import UpdateOne
from pymongo.results import BulkWriteResult

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.cardekho_city_price import (
    CardekhoCityPrice,
)

CARDEKHO_CITY_PRICES_COLLECTION = "cardekho_city_prices"


@dataclass(
    frozen=True,
    slots=True,
)
class BulkUpsertResult:
    received: int
    processed: int
    matched: int
    modified: int
    inserted: int


class CardekhoCityPriceRepository:
    def __init__(
        self,
        connection: MongoConnection = (mongo_connection),
    ) -> None:
        self._connection = connection

    @staticmethod
    def _normalize_run_id(
        run_id: str,
    ) -> str:
        if not isinstance(
            run_id,
            str,
        ):
            raise ValueError("run_id must be a string")

        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        return normalized_run_id

    @staticmethod
    def _normalize_document_id(
        document_id: str,
    ) -> str:
        if not isinstance(
            document_id,
            str,
        ):
            raise ValueError("document_id must be a string")

        normalized_document_id = document_id.strip()

        if not normalized_document_id:
            raise ValueError("document_id cannot be empty")

        return normalized_document_id

    @staticmethod
    def _normalize_job_ids(
        job_ids: Sequence[str],
    ) -> list[str]:
        normalized_job_ids: list[str] = []

        seen_job_ids: set[str] = set()

        for job_id in job_ids:
            if not isinstance(
                job_id,
                str,
            ):
                continue

            normalized_job_id = job_id.strip()

            if not normalized_job_id:
                continue

            if normalized_job_id in seen_job_ids:
                continue

            seen_job_ids.add(normalized_job_id)

            normalized_job_ids.append(normalized_job_id)

        return normalized_job_ids

    async def get_completed_job_ids(
        self,
        *,
        job_ids: Sequence[str],
        run_id: str,
    ) -> set[str]:
        """
        Return jobs already completed during
        the requested run.

        Successful runs are permanently recorded
        in completedRunIds. The lastRunId fallback
        supports documents written by the older
        repository implementation.
        """

        if not job_ids:
            return set()

        normalized_run_id = self._normalize_run_id(run_id)

        normalized_job_ids = self._normalize_job_ids(job_ids)

        if not normalized_job_ids:
            return set()

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITY_PRICES_COLLECTION)

        cursor = collection.find(
            {
                "_id": {
                    "$in": (normalized_job_ids),
                },
                "$or": [
                    {
                        "completedRunIds": (normalized_run_id),
                    },
                    {
                        "lastRunId": (normalized_run_id),
                    },
                ],
            },
            {
                "_id": 1,
            },
        )

        completed_job_ids: set[str] = set()

        async for document in cursor:
            document_id = document.get("_id")

            if isinstance(
                document_id,
                str,
            ):
                completed_job_ids.add(document_id)

        return completed_job_ids

    async def find_by_id(
        self,
        document_id: str,
    ) -> CardekhoCityPrice | None:
        normalized_document_id = self._normalize_document_id(document_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITY_PRICES_COLLECTION)

        document = await collection.find_one(
            {
                "_id": (normalized_document_id),
            }
        )

        if document is None:
            return None

        return CardekhoCityPrice.model_validate(document)

    async def count(
        self,
        *,
        query: (
            dict[
                str,
                Any,
            ]
            | None
        ) = None,
    ) -> int:
        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITY_PRICES_COLLECTION)

        return await collection.count_documents(query or {})

    async def bulk_upsert(
        self,
        records: Sequence[CardekhoCityPrice],
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

        collection = self._connection.collection(CARDEKHO_CITY_PRICES_COLLECTION)

        deduplicated_records: dict[
            str,
            CardekhoCityPrice,
        ] = {}

        for record in records:
            if not isinstance(
                record,
                CardekhoCityPrice,
            ):
                raise TypeError("records must contain only CardekhoCityPrice objects")

            deduplicated_records[record.document_id] = record

        current_time = datetime.now(timezone.utc)

        operations: list[UpdateOne] = []

        for record in deduplicated_records.values():
            document = record.to_mongo_document()

            document["lastRunId"] = normalized_run_id

            document["updatedAt"] = current_time

            operations.append(
                UpdateOne(
                    filter={
                        "_id": (record.document_id),
                    },
                    update={
                        "$set": document,
                        "$setOnInsert": {
                            "createdAt": (current_time),
                        },
                        "$addToSet": {
                            "completedRunIds": (normalized_run_id),
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
            matched=(result.matched_count),
            modified=(result.modified_count),
            inserted=(result.upserted_count),
        )


cardekho_city_price_repository = CardekhoCityPriceRepository()
