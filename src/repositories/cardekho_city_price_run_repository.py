from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Literal

from pymongo import ReturnDocument

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.cardekho_city_price_run import (
    CardekhoCityPriceRun,
)

CARDEKHO_CITY_PRICE_RUNS_COLLECTION = "cardekho_city_price_runs"

CardekhoCityPriceFinishedStatus = Literal[
    "completed",
    "interrupted",
    "failed",
    "cancelled",
]

PROGRESS_FIELD_NAMES = {
    "produced",
    "skipped",
    "successful",
    "failed",
    "written",
    "inserted",
    "matched",
    "modified",
    "failureRecordsWritten",
}


class CardekhoCityPriceRunNotFoundError(
    LookupError,
):
    """Raised when a Cardekho city-price run cannot be found."""


class CardekhoCityPriceRunRepository:
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
    def _normalize_optional_text(
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        if not isinstance(
            value,
            str,
        ):
            raise ValueError("Optional text value must be a string or null")

        normalized_value = value.strip()

        return normalized_value or None

    @staticmethod
    def _normalize_http_status(
        http_status: int | None,
    ) -> int | None:
        if http_status is None:
            return None

        if (
            isinstance(
                http_status,
                bool,
            )
            or not isinstance(
                http_status,
                int,
            )
            or not 100 <= http_status <= 599
        ):
            raise ValueError("http_status must be an integer between 100 and 599")

        return http_status

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

        for (
            field_name,
            value,
        ) in progress.items():
            if field_name not in PROGRESS_FIELD_NAMES:
                raise ValueError(
                    f"Unsupported Cardekho city-price run progress field: {field_name}"
                )

            if (
                isinstance(
                    value,
                    bool,
                )
                or not isinstance(
                    value,
                    int,
                )
                or value < 0
            ):
                raise ValueError(
                    "Cardekho city-price run "
                    "progress values must be "
                    "non-negative integers: "
                    f"field={field_name}"
                )

            normalized_progress[field_name] = value

        return normalized_progress

    async def create(
        self,
        run: CardekhoCityPriceRun,
    ) -> CardekhoCityPriceRun:
        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITY_PRICE_RUNS_COLLECTION)

        await collection.insert_one(run.to_mongo_document())

        return run

    async def get(
        self,
        run_id: str,
    ) -> CardekhoCityPriceRun | None:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITY_PRICE_RUNS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": (normalized_run_id),
            }
        )

        if document is None:
            return None

        return CardekhoCityPriceRun.model_validate(document)

    async def require(
        self,
        run_id: str,
    ) -> CardekhoCityPriceRun:
        run = await self.get(run_id)

        if run is None:
            raise (
                CardekhoCityPriceRunNotFoundError(
                    f"Cardekho city-price run was not found: {run_id}"
                )
            )

        return run

    async def mark_resumed(
        self,
        run_id: str,
    ) -> CardekhoCityPriceRun:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITY_PRICE_RUNS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        document = await collection.find_one_and_update(
            {
                "_id": (normalized_run_id),
                "status": {
                    "$in": [
                        "running",
                        "completed",
                        "interrupted",
                        "failed",
                        "cancelled",
                    ],
                },
            },
            {
                "$set": {
                    "status": "running",
                    "resumedAt": (current_time),
                    "updatedAt": (current_time),
                    "completedAt": None,
                },
                "$unset": {
                    "errorType": "",
                    "errorMessage": "",
                    "stopReason": "",
                    "stopHttpStatus": "",
                    "stoppedAt": "",
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
                    CardekhoCityPriceRunNotFoundError(
                        f"Cardekho city-price run was not found: {normalized_run_id}"
                    )
                )

            raise ValueError(
                "Cardekho city-price run "
                "cannot be resumed because "
                "its status is "
                f"{existing_run.status!r}"
            )

        return CardekhoCityPriceRun.model_validate(document)

    async def update_progress(
        self,
        run_id: str,
        *,
        progress: Mapping[
            str,
            int,
        ],
    ) -> None:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_progress = self._normalize_progress(progress)

        if not normalized_progress:
            return

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITY_PRICE_RUNS_COLLECTION)

        update_fields: dict[
            str,
            Any,
        ] = {
            **normalized_progress,
            "updatedAt": datetime.now(timezone.utc),
        }

        result = await collection.update_one(
            {
                "_id": (normalized_run_id),
            },
            {
                "$set": update_fields,
            },
        )

        if result.matched_count == 0:
            raise (
                CardekhoCityPriceRunNotFoundError(
                    f"Cardekho city-price run was not found: {normalized_run_id}"
                )
            )

    async def update_pause_settings(
        self,
        run_id: str,
        *,
        pause_every_requests: int,
        pause_seconds: float,
    ) -> CardekhoCityPriceRun:
        normalized_run_id = self._normalize_run_id(run_id)

        if (
            isinstance(
                pause_every_requests,
                bool,
            )
            or not isinstance(
                pause_every_requests,
                int,
            )
            or pause_every_requests < 0
        ):
            raise ValueError("pause_every_requests must be a non-negative integer")

        if (
            isinstance(
                pause_seconds,
                bool,
            )
            or not isinstance(
                pause_seconds,
                int | float,
            )
            or pause_seconds < 0
        ):
            raise ValueError("pause_seconds must be a non-negative number")

        pause_enabled = pause_every_requests > 0

        duration_enabled = pause_seconds > 0

        if pause_enabled != duration_enabled:
            raise ValueError(
                "pause_every_requests and "
                "pause_seconds must both be "
                "greater than zero or both "
                "be zero"
            )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITY_PRICE_RUNS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        document = await collection.find_one_and_update(
            {
                "_id": (normalized_run_id),
            },
            {
                "$set": {
                    ("settings.pauseEveryRequests"): pause_every_requests,
                    ("settings.pauseSeconds"): float(pause_seconds),
                    "updatedAt": (current_time),
                }
            },
            return_document=(ReturnDocument.AFTER),
        )

        if document is None:
            raise (
                CardekhoCityPriceRunNotFoundError(
                    f"Cardekho city-price run was not found: {normalized_run_id}"
                )
            )

        return CardekhoCityPriceRun.model_validate(document)

    async def mark_completed(
        self,
        run_id: str,
        *,
        progress: Mapping[
            str,
            int,
        ],
    ) -> CardekhoCityPriceRun:
        return await self._mark_finished(
            run_id=run_id,
            status="completed",
            progress=progress,
        )

    async def mark_interrupted(
        self,
        run_id: str,
        *,
        progress: Mapping[
            str,
            int,
        ],
        error: BaseException | None = None,
        stop_reason: str | None = None,
        stop_http_status: int | None = None,
    ) -> CardekhoCityPriceRun:
        return await self._mark_finished(
            run_id=run_id,
            status="interrupted",
            progress=progress,
            error=error,
            stop_reason=(stop_reason),
            stop_http_status=(stop_http_status),
        )

    async def mark_failed(
        self,
        run_id: str,
        *,
        progress: Mapping[
            str,
            int,
        ],
        error: BaseException,
        stop_reason: str | None = None,
        stop_http_status: int | None = None,
    ) -> CardekhoCityPriceRun:
        return await self._mark_finished(
            run_id=run_id,
            status="failed",
            progress=progress,
            error=error,
            stop_reason=(stop_reason),
            stop_http_status=(stop_http_status),
        )

    async def mark_cancelled(
        self,
        run_id: str,
        *,
        progress: Mapping[
            str,
            int,
        ],
        stop_reason: str | None = None,
    ) -> CardekhoCityPriceRun:
        return await self._mark_finished(
            run_id=run_id,
            status="cancelled",
            progress=progress,
            stop_reason=(stop_reason),
        )

    async def _mark_finished(
        self,
        *,
        run_id: str,
        status: CardekhoCityPriceFinishedStatus,
        progress: Mapping[
            str,
            int,
        ],
        error: BaseException | None = None,
        stop_reason: str | None = None,
        stop_http_status: int | None = None,
    ) -> CardekhoCityPriceRun:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_progress = self._normalize_progress(progress)

        normalized_stop_reason = self._normalize_optional_text(stop_reason)

        normalized_stop_http_status = self._normalize_http_status(stop_http_status)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITY_PRICE_RUNS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        update_fields: dict[
            str,
            Any,
        ] = {
            **normalized_progress,
            "status": status,
            "updatedAt": current_time,
        }

        unset_fields: dict[
            str,
            str,
        ] = {}

        if status == "completed":
            update_fields["completedAt"] = current_time

            unset_fields["stoppedAt"] = ""

            unset_fields["stopReason"] = ""

            unset_fields["stopHttpStatus"] = ""

        else:
            update_fields["completedAt"] = None

            update_fields["stoppedAt"] = current_time

            if normalized_stop_reason is not None:
                update_fields["stopReason"] = normalized_stop_reason

            else:
                unset_fields["stopReason"] = ""

            if normalized_stop_http_status is not None:
                update_fields["stopHttpStatus"] = normalized_stop_http_status

            else:
                unset_fields["stopHttpStatus"] = ""

        if error is not None:
            update_fields["errorType"] = type(error).__name__

            error_message = str(error).strip()

            update_fields["errorMessage"] = error_message or type(error).__name__

        else:
            unset_fields["errorType"] = ""

            unset_fields["errorMessage"] = ""

        update_document: dict[
            str,
            Any,
        ] = {
            "$set": update_fields,
        }

        if unset_fields:
            update_document["$unset"] = unset_fields

        document = await collection.find_one_and_update(
            {
                "_id": (normalized_run_id),
            },
            update_document,
            return_document=(ReturnDocument.AFTER),
        )

        if document is None:
            raise (
                CardekhoCityPriceRunNotFoundError(
                    f"Cardekho city-price run was not found: {normalized_run_id}"
                )
            )

        return CardekhoCityPriceRun.model_validate(document)


cardekho_city_price_run_repository = CardekhoCityPriceRunRepository()
