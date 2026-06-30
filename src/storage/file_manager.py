from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


class FileStorageError(Exception):
    """Raised when a file-storage operation fails."""


class JsonFileManager:
    def __init__(
        self,
        *,
        root_directory: str | Path,
        retention_days: int = 7,
    ) -> None:
        if retention_days < 1:
            raise ValueError("retention_days must be greater than zero")

        self.root_directory = Path(root_directory)
        self.retention_days = retention_days

    @staticmethod
    def create_run_timestamp(
        current_time: datetime | None = None,
    ) -> datetime:
        timestamp = current_time or datetime.now(timezone.utc)

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        return timestamp.astimezone(timezone.utc)

    def create_json_path(
        self,
        *,
        file_name: str,
        timestamp: datetime | None = None,
        subdirectory: str | Path | None = None,
    ) -> Path:
        run_timestamp = self.create_run_timestamp(timestamp)

        date_directory = run_timestamp.strftime("%Y-%m-%d")

        timestamp_suffix = run_timestamp.strftime("%Y%m%d_%H%M%S_%f")

        safe_file_name = file_name.removesuffix(".json")

        output_directory = self.root_directory / date_directory

        if subdirectory is not None:
            output_directory = output_directory / Path(subdirectory)

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return output_directory / (f"{safe_file_name}_" f"{timestamp_suffix}.json")

    @staticmethod
    def save_json(
        *,
        file_path: str | Path,
        data: Any,
    ) -> Path:
        output_file = Path(file_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            output_file.write_text(
                json.dumps(
                    data,
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

        except OSError as error:
            raise FileStorageError(
                f"Unable to write JSON file: " f"{output_file}"
            ) from error

        return output_file

    def delete_expired_files(
        self,
        *,
        dry_run: bool = False,
        current_time: datetime | None = None,
    ) -> list[Path]:
        """
        Delete files whose modification time is older
        than the configured retention period.

        Symbolic links are ignored for safety.
        """
        if not self.root_directory.exists():
            return []

        now = self.create_run_timestamp(current_time)

        cutoff_time = now - timedelta(days=self.retention_days)

        deleted_files: list[Path] = []

        for file_path in self.root_directory.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.is_symlink():
                continue

            try:
                modified_at = datetime.fromtimestamp(
                    file_path.stat().st_mtime,
                    tz=timezone.utc,
                )

            except OSError as error:
                raise FileStorageError(
                    f"Unable to inspect file: " f"{file_path}"
                ) from error

            if modified_at >= cutoff_time:
                continue

            deleted_files.append(file_path)

            if dry_run:
                continue

            try:
                file_path.unlink()

            except OSError as error:
                raise FileStorageError(
                    f"Unable to delete expired file: " f"{file_path}"
                ) from error

        if not dry_run:
            self._delete_empty_directories()

        return deleted_files

    def _delete_empty_directories(
        self,
    ) -> None:
        directories = sorted(
            (
                path
                for path in self.root_directory.rglob("*")
                if path.is_dir() and not path.is_symlink()
            ),
            key=lambda path: len(path.parts),
            reverse=True,
        )

        for directory in directories:
            try:
                directory.rmdir()
            except OSError:
                # The directory is not empty or cannot
                # safely be removed.
                continue
