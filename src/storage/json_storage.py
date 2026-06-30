from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class JsonStorage:
    @staticmethod
    def save(
        *,
        directory: str | Path,
        file_name: str,
        data: Any,
        create_archive: bool = True,
    ) -> dict[str, Path | None]:
        base_directory = Path(directory)

        latest_file = base_directory / f"{file_name.removesuffix('.json')}.json"

        latest_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        serialized_data = json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        )

        latest_file.write_text(
            serialized_data,
            encoding="utf-8",
        )

        archive_file: Path | None = None

        if create_archive:
            now = datetime.now(timezone.utc)

            date_directory = now.strftime("%Y-%m-%d")

            timestamp = now.strftime("%Y%m%d_%H%M%S_%f")

            archive_file = (
                base_directory
                / "archive"
                / date_directory
                / (f"{file_name.removesuffix('.json')}_" f"{timestamp}.json")
            )

            archive_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            archive_file.write_text(
                serialized_data,
                encoding="utf-8",
            )

        return {
            "latest_file": latest_file,
            "archive_file": archive_file,
        }
