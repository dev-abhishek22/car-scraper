from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Literal

from pymongo import ReturnDocument

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.scraper_run import (
    ScraperRun,
)

SCRAPER_RUNS_COLLECTION = "scraper_runs"

ScraperRunFinishedStatus = Literal[
    "completed",
    "completed_with_failures",
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
    "totalJobs",
    "pendingJobs",
    "runningJobs",
    "completedJobs",
    "failedJobs",
    "skippedJobs",
    "cancelledJobs",
}


class ScraperRunNotFoundError(LookupError):
    """Raised when a scraper run cannot be found."""


class ScraperRunRepository:
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
    def _normalize_optional_text(
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        normalized_value = value.strip()

        return normalized_value or None

    @staticmethod
    def _normalize_http_status(
        http_status: int | None,
    ) -> int | None:
        if http_status is None:
            return None

        if (
            isinstance(http_status, bool)
            or not isinstance(http_status, int)
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

        normalized_progress: dict[str, int] = {}

        for field_name, value in progress.items():
            if field_name not in PROGRESS_FIELD_NAMES:
                raise ValueError(
                    f"Unsupported scraper run progress field: {field_name}"
                )

            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(
                    "Scraper run progress values must be "
                    "non-negative integers: "
                    f"field={field_name}"
                )

            normalized_progress[field_name] = value

        return normalized_progress

    @staticmethod
    def _normalize_metadata(
        metadata: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        if metadata is None:
            return {}

        return dict(metadata)

    async def create(
        self,
        run: ScraperRun,
    ) -> ScraperRun:
        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_RUNS_COLLECTION)

        await collection.insert_one(run.to_mongo_document())

        return run

    async def get(
        self,
        run_id: str,
    ) -> ScraperRun | None:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_RUNS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": normalized_run_id,
            }
        )

        if document is None:
            return None

        return ScraperRun.model_validate(document)

    async def require(
        self,
        run_id: str,
    ) -> ScraperRun:
        run = await self.get(run_id)

        if run is None:
            raise ScraperRunNotFoundError(f"Scraper run was not found: {run_id}")

        return run

    async def mark_started(
        self,
        run_id: str,
    ) -> ScraperRun:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_RUNS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        document = await collection.find_one_and_update(
            {
                "_id": normalized_run_id,
                "status": "pending",
            },
            {
                "$set": {
                    "status": "running",
                    "startedAt": current_time,
                    "updatedAt": current_time,
                },
                "$unset": {
                    "completedAt": "",
                    "stoppedAt": "",
                    "stopReason": "",
                    "stopHttpStatus": "",
                    "errorType": "",
                    "errorMessage": "",
                },
            },
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            existing_run = await self.get(normalized_run_id)

            if existing_run is None:
                raise ScraperRunNotFoundError(
                    f"Scraper run was not found: {normalized_run_id}"
                )

            raise ValueError(
                "Scraper run cannot be started because "
                f"its status is {existing_run.status!r}"
            )

        return ScraperRun.model_validate(document)

    async def mark_resumed(
        self,
        run_id: str,
    ) -> ScraperRun:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_RUNS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        document = await collection.find_one_and_update(
            {
                "_id": normalized_run_id,
                "status": {
                    "$in": [
                        "running",
                        "completed",
                        "completed_with_failures",
                        "interrupted",
                        "failed",
                        "cancelled",
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
                    "stoppedAt": "",
                    "stopReason": "",
                    "stopHttpStatus": "",
                    "errorType": "",
                    "errorMessage": "",
                },
                "$inc": {
                    "resumeCount": 1,
                },
            },
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            existing_run = await self.get(normalized_run_id)

            if existing_run is None:
                raise ScraperRunNotFoundError(
                    f"Scraper run was not found: {normalized_run_id}"
                )

            raise ValueError(
                "Scraper run cannot be resumed because "
                f"its status is {existing_run.status!r}"
            )

        return ScraperRun.model_validate(document)

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

        collection = self._connection.collection(SCRAPER_RUNS_COLLECTION)

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
            raise ScraperRunNotFoundError(
                f"Scraper run was not found: {normalized_run_id}"
            )

    async def increment_progress(
        self,
        run_id: str,
        *,
        increments: Mapping[str, int],
    ) -> None:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_increments = self._normalize_progress(increments)

        if not normalized_increments:
            return

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_RUNS_COLLECTION)

        result = await collection.update_one(
            {
                "_id": normalized_run_id,
            },
            {
                "$inc": normalized_increments,
                "$set": {
                    "updatedAt": datetime.now(timezone.utc),
                },
            },
        )

        if result.matched_count == 0:
            raise ScraperRunNotFoundError(
                f"Scraper run was not found: {normalized_run_id}"
            )

    async def update_metadata(
        self,
        run_id: str,
        *,
        metadata: Mapping[str, Any],
        merge: bool = True,
    ) -> ScraperRun:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_metadata = self._normalize_metadata(metadata)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_RUNS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        if merge:
            set_fields: dict[str, Any] = {
                "updatedAt": current_time,
            }

            for key, value in normalized_metadata.items():
                normalized_key = str(key).strip()

                if not normalized_key:
                    continue

                set_fields[f"metadata.{normalized_key}"] = value

        else:
            set_fields = {
                "metadata": normalized_metadata,
                "updatedAt": current_time,
            }

        document = await collection.find_one_and_update(
            {
                "_id": normalized_run_id,
            },
            {
                "$set": set_fields,
            },
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            raise ScraperRunNotFoundError(
                f"Scraper run was not found: {normalized_run_id}"
            )

        return ScraperRun.model_validate(document)

    async def mark_completed(
        self,
        run_id: str,
        *,
        progress: Mapping[str, int] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> ScraperRun:
        normalized_progress = self._normalize_progress(progress)

        failed_jobs = normalized_progress.get("failedJobs")

        failed = normalized_progress.get("failed")

        has_failures = (failed_jobs is not None and failed_jobs > 0) or (
            failed is not None and failed > 0
        )

        status: ScraperRunFinishedStatus = (
            "completed_with_failures" if has_failures else "completed"
        )

        return await self._mark_finished(
            run_id=run_id,
            status=status,
            progress=normalized_progress,
            metadata=metadata,
        )

    async def mark_interrupted(
        self,
        run_id: str,
        *,
        progress: Mapping[str, int] | None = None,
        error: BaseException | None = None,
        stop_reason: str | None = None,
        stop_http_status: int | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> ScraperRun:
        return await self._mark_finished(
            run_id=run_id,
            status="interrupted",
            progress=progress,
            error=error,
            stop_reason=stop_reason,
            stop_http_status=stop_http_status,
            metadata=metadata,
        )

    async def mark_failed(
        self,
        run_id: str,
        *,
        error: BaseException,
        progress: Mapping[str, int] | None = None,
        stop_reason: str | None = None,
        stop_http_status: int | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> ScraperRun:
        return await self._mark_finished(
            run_id=run_id,
            status="failed",
            progress=progress,
            error=error,
            stop_reason=stop_reason,
            stop_http_status=stop_http_status,
            metadata=metadata,
        )

    async def mark_cancelled(
        self,
        run_id: str,
        *,
        progress: Mapping[str, int] | None = None,
        stop_reason: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> ScraperRun:
        return await self._mark_finished(
            run_id=run_id,
            status="cancelled",
            progress=progress,
            stop_reason=stop_reason,
            metadata=metadata,
        )

    async def _mark_finished(
        self,
        *,
        run_id: str,
        status: ScraperRunFinishedStatus,
        progress: Mapping[str, int] | None = None,
        error: BaseException | None = None,
        stop_reason: str | None = None,
        stop_http_status: int | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> ScraperRun:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_progress = self._normalize_progress(progress)

        normalized_stop_reason = self._normalize_optional_text(stop_reason)

        normalized_stop_http_status = self._normalize_http_status(stop_http_status)

        normalized_metadata = self._normalize_metadata(metadata)

        await self._connection.connect()

        collection = self._connection.collection(SCRAPER_RUNS_COLLECTION)

        current_time = datetime.now(timezone.utc)

        update_fields: dict[str, Any] = {
            **normalized_progress,
            "status": status,
            "updatedAt": current_time,
        }

        unset_fields: dict[str, str] = {}

        if status in {
            "completed",
            "completed_with_failures",
        }:
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

        for key, value in normalized_metadata.items():
            normalized_key = str(key).strip()

            if not normalized_key:
                continue

            update_fields[f"metadata.{normalized_key}"] = value

        update_document: dict[str, Any] = {
            "$set": update_fields,
        }

        if unset_fields:
            update_document["$unset"] = unset_fields

        document = await collection.find_one_and_update(
            {
                "_id": normalized_run_id,
            },
            update_document,
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            raise ScraperRunNotFoundError(
                f"Scraper run was not found: {normalized_run_id}"
            )

        return ScraperRun.model_validate(document)


scraper_run_repository = ScraperRunRepository()
