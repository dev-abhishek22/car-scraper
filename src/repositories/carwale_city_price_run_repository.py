from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from pymongo import ReturnDocument

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.carwale_city_price_run import (
    CarWaleCityPriceRun,
)

CARWALE_CITY_PRICE_RUNS_COLLECTION = "carwale_city_price_runs"

PROGRESS_FIELD_NAMES = {
    "produced",
    "skipped",
    "successful",
    "failed",
    "written",
    "inserted",
    "matched",
    "modified",
}


class CarWaleCityPriceRunNotFoundError(LookupError):
    """Raised when a city-price run cannot be found."""


class CarWaleCityPriceRunRepository:
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
    def _normalize_progress(
        progress: Mapping[str, int] | None,
    ) -> dict[str, int]:
        if progress is None:
            return {}

        normalized_progress: dict[
            str,
            int,
        ] = {}

        for field_name, value in progress.items():
            if field_name not in PROGRESS_FIELD_NAMES:
                raise ValueError("Unsupported run progress field: " f"{field_name}")

            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(
                    "Run progress values must be "
                    "non-negative integers: "
                    f"field={field_name}"
                )

            normalized_progress[field_name] = value

        return normalized_progress

    async def create(
        self,
        run: CarWaleCityPriceRun,
    ) -> CarWaleCityPriceRun:
        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_RUNS_COLLECTION)

        await collection.insert_one(run.to_mongo_document())

        return run

    async def get(
        self,
        run_id: str,
    ) -> CarWaleCityPriceRun | None:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_RUNS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": normalized_run_id,
            }
        )

        if document is None:
            return None

        return CarWaleCityPriceRun.model_validate(document)

    async def require(
        self,
        run_id: str,
    ) -> CarWaleCityPriceRun:
        run = await self.get(run_id)

        if run is None:
            raise (
                CarWaleCityPriceRunNotFoundError(
                    "CarWale city-price run " f"was not found: {run_id}"
                )
            )

        return run

    async def mark_resumed(
        self,
        run_id: str,
    ) -> CarWaleCityPriceRun:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_RUNS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        document = await collection.find_one_and_update(
            {
                "_id": normalized_run_id,
                "status": {
                    "$in": [
                        "running",
                        "interrupted",
                        "failed",
                    ]
                },
            },
            {
                "$set": {
                    "status": "running",
                    "resumedAt": current_time,
                    "updatedAt": current_time,
                    "completedAt": None,
                },
                "$unset": {
                    "errorType": "",
                    "errorMessage": "",
                },
                "$inc": {
                    "resumeCount": 1,
                },
            },
            return_document=(ReturnDocument.AFTER),
        )

        if document is None:
            existing_run = await self.get(normalized_run_id)

            if existing_run is None:
                raise (
                    CarWaleCityPriceRunNotFoundError(
                        "CarWale city-price run "
                        "was not found: "
                        f"{normalized_run_id}"
                    )
                )

            raise ValueError(
                "CarWale city-price run cannot "
                "be resumed because its status is "
                f"{existing_run.status!r}"
            )

        return CarWaleCityPriceRun.model_validate(document)

    async def update_progress(
        self,
        run_id: str,
        *,
        progress: Mapping[str, int],
    ) -> None:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_progress = self._normalize_progress(progress)

        if not normalized_progress:
            return

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_RUNS_COLLECTION)

        update_fields: dict[str, Any] = {
            **normalized_progress,
            "updatedAt": datetime.now(timezone.utc),
        }

        result = await collection.update_one(
            {
                "_id": normalized_run_id,
            },
            {
                "$set": update_fields,
            },
        )

        if result.matched_count == 0:
            raise (
                CarWaleCityPriceRunNotFoundError(
                    "CarWale city-price run " "was not found: " f"{normalized_run_id}"
                )
            )

    async def mark_completed(
        self,
        run_id: str,
        *,
        progress: Mapping[str, int],
    ) -> CarWaleCityPriceRun:
        return await self._mark_finished(
            run_id=run_id,
            status="completed",
            progress=progress,
        )

    async def mark_interrupted(
        self,
        run_id: str,
        *,
        progress: Mapping[str, int],
        error: BaseException | None = None,
    ) -> CarWaleCityPriceRun:
        return await self._mark_finished(
            run_id=run_id,
            status="interrupted",
            progress=progress,
            error=error,
        )

    async def mark_failed(
        self,
        run_id: str,
        *,
        progress: Mapping[str, int],
        error: BaseException,
    ) -> CarWaleCityPriceRun:
        return await self._mark_finished(
            run_id=run_id,
            status="failed",
            progress=progress,
            error=error,
        )

    async def mark_cancelled(
        self,
        run_id: str,
        *,
        progress: Mapping[str, int],
    ) -> CarWaleCityPriceRun:
        return await self._mark_finished(
            run_id=run_id,
            status="cancelled",
            progress=progress,
        )

    async def _mark_finished(
        self,
        *,
        run_id: str,
        status: str,
        progress: Mapping[str, int],
        error: BaseException | None = None,
    ) -> CarWaleCityPriceRun:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_progress = self._normalize_progress(progress)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITY_PRICE_RUNS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        update_fields: dict[str, Any] = {
            **normalized_progress,
            "status": status,
            "updatedAt": current_time,
        }

        if status == "completed":
            update_fields["completedAt"] = current_time
        else:
            update_fields["completedAt"] = None

        update_document: dict[str, Any] = {
            "$set": update_fields,
        }

        if error is not None:
            update_fields["errorType"] = type(error).__name__

            update_fields["errorMessage"] = str(error)
        else:
            update_document["$unset"] = {
                "errorType": "",
                "errorMessage": "",
            }

        document = await collection.find_one_and_update(
            {
                "_id": normalized_run_id,
            },
            update_document,
            return_document=(ReturnDocument.AFTER),
        )

        if document is None:
            raise (
                CarWaleCityPriceRunNotFoundError(
                    "CarWale city-price run " "was not found: " f"{normalized_run_id}"
                )
            )

        return CarWaleCityPriceRun.model_validate(document)


carwale_city_price_run_repository = CarWaleCityPriceRunRepository()
