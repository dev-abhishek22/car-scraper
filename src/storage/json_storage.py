from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class JsonStorage:
    @staticmethod
    def _write_atomically(
        *,
        file_path: Path,
        serialized_data: str,
    ) -> None:
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_path: Path | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=file_path.parent,
                prefix=f".{file_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)

                temporary_file.write(serialized_data)

                temporary_file.flush()
                os.fsync(temporary_file.fileno())

            temporary_path.replace(file_path)

        except Exception:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink(missing_ok=True)

            raise

    @classmethod
    def save(
        cls,
        *,
        directory: str | Path,
        file_name: str,
        data: Any,
        create_archive: bool = True,
        archive_directory: str | Path | None = None,
    ) -> dict[str, Path | None]:
        base_directory = Path(directory)

        normalized_file_name = file_name.removesuffix(".json")

        latest_file = base_directory / f"{normalized_file_name}.json"

        serialized_data = json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        )

        cls._write_atomically(
            file_path=latest_file,
            serialized_data=serialized_data,
        )

        archive_file: Path | None = None

        if create_archive:
            now = datetime.now(timezone.utc)

            date_directory = now.strftime("%Y-%m-%d")

            timestamp = now.strftime("%Y%m%d_%H%M%S_%f")

            archive_base_directory = (
                Path(archive_directory)
                if archive_directory is not None
                else base_directory / "archive"
            )

            archive_file = (
                archive_base_directory
                / date_directory
                / (f"{normalized_file_name}_{timestamp}.json")
            )

            cls._write_atomically(
                file_path=archive_file,
                serialized_data=serialized_data,
            )

        return {
            "latest_file": latest_file,
            "archive_file": archive_file,
        }
