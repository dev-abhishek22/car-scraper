from __future__ import annotations

from collections.abc import AsyncIterator, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone

from pymongo import UpdateOne
from pymongo.results import BulkWriteResult

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.carwale_city_price_failure import (
    CarWaleCityPriceFailure,
)
from src.models.carwale_city_price_job import (
    CarWaleCityPriceJob,
)

CARWALE_CITY_PRICE_FAILURES_COLLECTION = "carwale_city_price_failures"


@dataclass(frozen=True)
class BulkFailureUpsertResult:
    received: int
    processed: int
    matched: int
    modified: int
    inserted: int


@dataclass(frozen=True)
class FailureResolutionResult:
    requested: int
    matched: int
    modified: int


class CarWaleCityPriceFailureRepository:
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

    @staticmethod
    def _normalize_job_ids(
        job_ids: Sequence[str],
    ) -> list[str]:
        normalized_job_ids: list[str] = []

        seen_job_ids: set[str] = set()

        for job_id in job_ids:
            normalized_job_id = job_id.strip()

            if not normalized_job_id:
                continue

            if normalized_job_id in seen_job_ids:
                continue

            seen_job_ids.add(normalized_job_id)

            normalized_job_ids.append(normalized_job_id)

        return normalized_job_ids

    async def bulk_upsert(
        self,
        failures: Sequence[CarWaleCityPriceFailure],
    ) -> BulkFailureUpsertResult:
        if not failures:
            return BulkFailureUpsertResult(
                received=0,
                processed=0,
                matched=0,
                modified=0,
                inserted=0,
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_FAILURES_COLLECTION)

        deduplicated_failures: dict[
            str,
            CarWaleCityPriceFailure,
        ] = {}

        for failure in failures:
            deduplicated_failures[failure.failure_id] = failure

        operations: list[UpdateOne] = []

        for failure in deduplicated_failures.values():
            operations.append(
                UpdateOne(
                    filter={
                        "_id": failure.failure_id,
                    },
                    update={
                        "$set": {
                            "runId": failure.run_id,
                            "jobId": failure.job_id,
                            "versionId": (failure.version_id),
                            "cityId": failure.city_id,
                            "makeMaskingName": (failure.make_masking_name),
                            "modelMaskingName": (failure.model_masking_name),
                            "cityMaskingName": (failure.city_masking_name),
                            "errorType": (failure.error_type),
                            "errorMessage": (failure.error_message),
                            "httpStatus": (failure.http_status),
                            "retryable": (failure.retryable),
                            "status": "failed",
                            "lastFailedAt": (failure.last_failed_at),
                            "resolvedAt": None,
                        },
                        "$setOnInsert": {
                            "firstFailedAt": (failure.first_failed_at),
                            "attempts": 0,
                        },
                        "$inc": {
                            "attempts": 1,
                        },
                    },
                    upsert=True,
                )
            )

        result: BulkWriteResult = await collection.bulk_write(
            operations,
            ordered=False,
        )

        return BulkFailureUpsertResult(
            received=len(failures),
            processed=len(operations),
            matched=result.matched_count,
            modified=result.modified_count,
            inserted=result.upserted_count,
        )

    async def get_terminal_job_ids(
        self,
        *,
        run_id: str,
        job_ids: Sequence[str],
    ) -> set[str]:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_job_ids = self._normalize_job_ids(job_ids)

        if not normalized_job_ids:
            return set()

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_FAILURES_COLLECTION)

        cursor = collection.find(
            {
                "runId": normalized_run_id,
                "jobId": {
                    "$in": normalized_job_ids,
                },
                "status": "failed",
                "retryable": False,
            },
            {
                "_id": 0,
                "jobId": 1,
            },
        )

        terminal_job_ids: set[str] = set()

        async for document in cursor:
            job_id = document.get("jobId")

            if isinstance(job_id, str):
                terminal_job_ids.add(job_id)

        return terminal_job_ids

    async def iter_unresolved_jobs(
        self,
        *,
        run_id: str,
        retryable_only: bool = True,
    ) -> AsyncIterator[CarWaleCityPriceJob]:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_FAILURES_COLLECTION)

        query: dict[str, object] = {
            "runId": normalized_run_id,
            "status": "failed",
        }

        if retryable_only:
            query["retryable"] = True

        cursor = collection.find(
            query,
            {
                "_id": 0,
                "versionId": 1,
                "cityId": 1,
                "makeMaskingName": 1,
                "modelMaskingName": 1,
                "cityMaskingName": 1,
            },
        ).sort(
            [
                ("versionId", 1),
                ("cityId", 1),
            ]
        )

        async for document in cursor:
            yield CarWaleCityPriceJob(
                version_id=document["versionId"],
                city_id=document["cityId"],
                make_masking_name=document["makeMaskingName"],
                model_masking_name=document["modelMaskingName"],
                city_masking_name=document["cityMaskingName"],
            )

    async def count_unresolved(
        self,
        *,
        run_id: str,
        retryable_only: bool = False,
    ) -> int:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_FAILURES_COLLECTION)

        query: dict[str, object] = {
            "runId": normalized_run_id,
            "status": "failed",
        }

        if retryable_only:
            query["retryable"] = True

        return await collection.count_documents(query)

    async def mark_resolved(
        self,
        *,
        run_id: str,
        job_ids: Sequence[str],
    ) -> FailureResolutionResult:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_job_ids = self._normalize_job_ids(job_ids)

        if not normalized_job_ids:
            return FailureResolutionResult(
                requested=0,
                matched=0,
                modified=0,
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_FAILURES_COLLECTION)

        current_time = datetime.now(timezone.utc)

        result = await collection.update_many(
            {
                "runId": normalized_run_id,
                "jobId": {
                    "$in": normalized_job_ids,
                },
                "status": "failed",
            },
            {
                "$set": {
                    "status": "resolved",
                    "resolvedAt": current_time,
                }
            },
        )

        return FailureResolutionResult(
            requested=len(normalized_job_ids),
            matched=result.matched_count,
            modified=result.modified_count,
        )


carwale_city_price_failure_repository = CarWaleCityPriceFailureRepository()
