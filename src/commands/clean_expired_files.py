from __future__ import annotations

from typing import Any

from src.config.settings import settings
from src.storage.cleanup import ArchiveCleaner

DATA_ROOT_DIRECTORY = "data"


def run_clean_expired_files(
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    retention_days = settings.DATA_RETENTION_DAYS
    cleaner = ArchiveCleaner(
        root_directory=DATA_ROOT_DIRECTORY,
        retention_days=retention_days,
    )

    expired_files = cleaner.clean(
        dry_run=dry_run,
    )

    return {
        "command": "clean-expired-files",
        "root_directory": DATA_ROOT_DIRECTORY,
        "retention_days": retention_days,
        "dry_run": dry_run,
        "files_count": len(expired_files),
        "files": [str(file_path) for file_path in expired_files],
    }
