from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ScrapeStatusStore:
    """
    Generic scraping status manager.

    It can be used by:

    - A single-item scraper
    - A multiple-item scraper
    - A failed-only scraper
    - Any future CarWale scraper

    The store does not contain CarWale-specific logic.
    The caller decides what an item key represents.

    Example item keys:

    - maruti-suzuki
    - bentley
    - model-123
    - city-delhi
    """

    TERMINAL_STATUSES = {
        "success",
        "failed",
        "skipped",
    }

    def __init__(
        self,
        *,
        status_file: str | Path,
        resource_name: str,
    ) -> None:
        normalized_resource_name = resource_name.strip()

        if not normalized_resource_name:
            raise ValueError("resource_name cannot be empty")

        self.status_file = Path(status_file)
        self.resource_name = normalized_resource_name

        self.status_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.data = self._load()

    def _default_data(self) -> dict[str, Any]:
        now = _utc_now()

        return {
            "schemaVersion": 1,
            "resource": self.resource_name,
            "createdAt": now,
            "updatedAt": now,
            "currentRun": None,
            "lastRun": None,
            "items": {},
        }

    def _load(self) -> dict[str, Any]:
        if not self.status_file.exists():
            return self._default_data()

        if not self.status_file.is_file():
            raise ValueError("Scrape status path is not a file: " f"{self.status_file}")

        try:
            payload = json.loads(
                self.status_file.read_text(
                    encoding="utf-8",
                )
            )

        except json.JSONDecodeError as error:
            raise ValueError(
                "Scrape status file contains invalid JSON: " f"{self.status_file}"
            ) from error

        if not isinstance(payload, dict):
            raise ValueError("Scrape status file must contain " "a JSON object")

        existing_resource = payload.get("resource")

        if (
            isinstance(existing_resource, str)
            and existing_resource != self.resource_name
        ):
            raise ValueError(
                "Scrape status resource mismatch: "
                f"expected={self.resource_name!r}, "
                f"found={existing_resource!r}"
            )

        items = payload.get("items")

        if items is None:
            payload["items"] = {}

        elif not isinstance(items, dict):
            raise ValueError("Scrape status items field must " "be a JSON object")

        payload.setdefault(
            "schemaVersion",
            1,
        )
        payload.setdefault(
            "resource",
            self.resource_name,
        )
        payload.setdefault(
            "createdAt",
            _utc_now(),
        )
        payload.setdefault(
            "updatedAt",
            _utc_now(),
        )
        payload.setdefault(
            "currentRun",
            None,
        )
        payload.setdefault(
            "lastRun",
            None,
        )

        return payload

    def _save(self) -> None:
        self.data["updatedAt"] = _utc_now()

        temporary_path: Path | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.status_file.parent,
                prefix=(f".{self.status_file.name}."),
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)

                json.dump(
                    self.data,
                    temporary_file,
                    indent=2,
                    ensure_ascii=False,
                )

                temporary_file.flush()

                os.fsync(temporary_file.fileno())

            temporary_path.replace(self.status_file)

        except Exception:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink(
                    missing_ok=True,
                )

            raise

    @staticmethod
    def _normalize_item_key(
        item_key: str,
    ) -> str:
        if not isinstance(item_key, str):
            raise TypeError("item_key must be a string")

        normalized_item_key = item_key.strip().lower()

        if not normalized_item_key:
            raise ValueError("item_key cannot be empty")

        return normalized_item_key

    @staticmethod
    def _normalize_metadata(
        metadata: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        if metadata is None:
            return {}

        return dict(metadata)

    def _get_current_run(
        self,
    ) -> dict[str, Any] | None:
        current_run = self.data.get("currentRun")

        if isinstance(current_run, dict):
            return current_run

        return None

    def _require_current_run(
        self,
    ) -> dict[str, Any]:
        current_run = self._get_current_run()

        if current_run is None:
            raise RuntimeError("No scraping run is currently active")

        return current_run

    def _close_interrupted_run(
        self,
    ) -> None:
        current_run = self._get_current_run()

        if current_run is None:
            return

        if current_run.get("completedAt"):
            return

        now = _utc_now()

        current_run["status"] = "interrupted"
        current_run["completedAt"] = now
        current_run["updatedAt"] = now

        self.data["lastRun"] = current_run
        self.data["currentRun"] = None

    def start_run(
        self,
        *,
        mode: str,
        selected_items: int,
        total_available_items: int | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        normalized_mode = mode.strip()

        if not normalized_mode:
            raise ValueError("mode cannot be empty")

        if selected_items < 0:
            raise ValueError("selected_items cannot be negative")

        if total_available_items is not None and total_available_items < 0:
            raise ValueError("total_available_items cannot " "be negative")

        self._close_interrupted_run()

        now = _utc_now()
        run_id = uuid4().hex

        self.data["currentRun"] = {
            "runId": run_id,
            "resource": self.resource_name,
            "mode": normalized_mode,
            "status": "running",
            "startedAt": now,
            "updatedAt": now,
            "completedAt": None,
            "selectedItems": selected_items,
            "totalAvailableItems": (total_available_items),
            "processedItems": 0,
            "successfulItems": 0,
            "failedItems": 0,
            "skippedItems": 0,
            "processedKeys": [],
            "metadata": self._normalize_metadata(metadata),
        }

        self._save()

        return run_id

    def mark_started(
        self,
        *,
        item_key: str,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        normalized_key = self._normalize_item_key(item_key)

        items = self.data["items"]

        existing_item = items.get(
            normalized_key,
            {},
        )

        if not isinstance(existing_item, dict):
            existing_item = {}

        previous_attempts = existing_item.get(
            "attempts",
            0,
        )

        if not isinstance(previous_attempts, int):
            previous_attempts = 0

        items[normalized_key] = {
            **existing_item,
            "key": normalized_key,
            "resource": self.resource_name,
            "status": "running",
            "attempts": previous_attempts + 1,
            "startedAt": _utc_now(),
            "updatedAt": _utc_now(),
            "metadata": {
                **existing_item.get(
                    "metadata",
                    {},
                ),
                **self._normalize_metadata(metadata),
            },
            "lastError": None,
        }

        current_run = self._get_current_run()

        if current_run is not None:
            current_run["updatedAt"] = _utc_now()

        self._save()

    def _mark_terminal(
        self,
        *,
        item_key: str,
        status: str,
        metadata: Mapping[str, Any] | None = None,
        result: Mapping[str, Any] | None = None,
        error: Mapping[str, Any] | None = None,
        reason: str | None = None,
    ) -> None:
        if status not in self.TERMINAL_STATUSES:
            raise ValueError(f"Unsupported terminal status: {status}")

        normalized_key = self._normalize_item_key(item_key)

        items = self.data["items"]

        existing_item = items.get(
            normalized_key,
            {},
        )

        if not isinstance(existing_item, dict):
            existing_item = {}

        existing_metadata = existing_item.get(
            "metadata",
            {},
        )

        if not isinstance(
            existing_metadata,
            dict,
        ):
            existing_metadata = {}

        item_payload: dict[str, Any] = {
            **existing_item,
            "key": normalized_key,
            "resource": self.resource_name,
            "status": status,
            "updatedAt": _utc_now(),
            "completedAt": _utc_now(),
            "metadata": {
                **existing_metadata,
                **self._normalize_metadata(metadata),
            },
        }

        if result is not None:
            item_payload["result"] = dict(result)

        if reason is not None:
            item_payload["reason"] = reason

        if error is not None:
            item_payload["lastError"] = {
                **dict(error),
                "occurredAt": _utc_now(),
            }

        elif status != "failed":
            item_payload["lastError"] = None

        items[normalized_key] = item_payload

        self._update_run_counters(
            item_key=normalized_key,
            status=status,
        )

        self._save()

    def _update_run_counters(
        self,
        *,
        item_key: str,
        status: str,
    ) -> None:
        current_run = self._get_current_run()

        if current_run is None:
            return

        processed_keys = current_run.get(
            "processedKeys",
            [],
        )

        if not isinstance(
            processed_keys,
            list,
        ):
            processed_keys = []

        if item_key in processed_keys:
            current_run["updatedAt"] = _utc_now()
            return

        processed_keys.append(item_key)

        current_run["processedKeys"] = processed_keys

        current_run["processedItems"] = (
            current_run.get(
                "processedItems",
                0,
            )
            + 1
        )

        counter_fields = {
            "success": "successfulItems",
            "failed": "failedItems",
            "skipped": "skippedItems",
        }

        counter_field = counter_fields[status]

        current_run[counter_field] = (
            current_run.get(
                counter_field,
                0,
            )
            + 1
        )

        current_run["updatedAt"] = _utc_now()

    def mark_success(
        self,
        *,
        item_key: str,
        metadata: Mapping[str, Any] | None = None,
        result: Mapping[str, Any] | None = None,
    ) -> None:
        self._mark_terminal(
            item_key=item_key,
            status="success",
            metadata=metadata,
            result=result,
        )

    def mark_skipped(
        self,
        *,
        item_key: str,
        metadata: Mapping[str, Any] | None = None,
        result: Mapping[str, Any] | None = None,
        reason: str,
    ) -> None:
        self._mark_terminal(
            item_key=item_key,
            status="skipped",
            metadata=metadata,
            result=result,
            reason=reason,
        )

    def mark_failed(
        self,
        *,
        item_key: str,
        metadata: Mapping[str, Any] | None = None,
        error_type: str,
        error_message: str,
    ) -> None:
        self._mark_terminal(
            item_key=item_key,
            status="failed",
            metadata=metadata,
            error={
                "type": error_type,
                "message": error_message,
            },
        )

    def complete_run(
        self,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        current_run = self._require_current_run()

        now = _utc_now()

        current_run["status"] = "completed"
        current_run["completedAt"] = now
        current_run["updatedAt"] = now

        existing_metadata = current_run.get(
            "metadata",
            {},
        )

        if not isinstance(
            existing_metadata,
            dict,
        ):
            existing_metadata = {}

        current_run["metadata"] = {
            **existing_metadata,
            **self._normalize_metadata(metadata),
        }

        completed_run = dict(current_run)

        self.data["lastRun"] = completed_run
        self.data["currentRun"] = None

        self._save()

        return completed_run

    def get_item(
        self,
        item_key: str,
    ) -> dict[str, Any] | None:
        normalized_key = self._normalize_item_key(item_key)

        item = self.data["items"].get(normalized_key)

        if isinstance(item, dict):
            return dict(item)

        return None

    def get_keys_by_status(
        self,
        status: str,
    ) -> set[str]:
        normalized_status = status.strip().lower()

        if not normalized_status:
            raise ValueError("status cannot be empty")

        matching_keys: set[str] = set()

        for item_key, item in self.data["items"].items():
            if not isinstance(item, dict):
                continue

            if item.get("status") == normalized_status:
                matching_keys.add(item_key)

        return matching_keys

    def get_failed_keys(
        self,
    ) -> set[str]:
        return self.get_keys_by_status("failed")

    def is_successful(
        self,
        item_key: str,
    ) -> bool:
        item = self.get_item(item_key)

        if item is None:
            return False

        return item.get("status") == "success"
