from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path


class ArchiveCleaner:
    def __init__(
        self,
        *,
        root_directory: str | Path,
        retention_days: int,
    ) -> None:
        if retention_days < 1:
            raise ValueError("retention_days must be greater than zero")

        self.root_directory = Path(root_directory)

        self.retention_days = retention_days

    def clean(
        self,
        *,
        dry_run: bool = False,
    ) -> list[Path]:
        if not self.root_directory.exists():
            return []

        cutoff = datetime.now(timezone.utc) - timedelta(days=self.retention_days)

        expired_files: list[Path] = []

        for archive_directory in self.root_directory.rglob("archive"):
            if not archive_directory.is_dir():
                continue

            if archive_directory.is_symlink():
                continue

            for file_path in archive_directory.rglob("*.json"):
                if not file_path.is_file():
                    continue

                if file_path.is_symlink():
                    continue

                modified_at = datetime.fromtimestamp(
                    file_path.stat().st_mtime,
                    tz=timezone.utc,
                )

                if modified_at >= cutoff:
                    continue

                expired_files.append(file_path)

                if not dry_run:
                    file_path.unlink()

            if not dry_run:
                self._remove_empty_directories(archive_directory)

        return expired_files

    @staticmethod
    def _remove_empty_directories(
        archive_directory: Path,
    ) -> None:
        directories = sorted(
            (
                path
                for path in archive_directory.rglob("*")
                if path.is_dir() and not path.is_symlink()
            ),
            key=lambda path: len(path.parts),
            reverse=True,
        )

        for directory in directories:
            try:
                directory.rmdir()
            except OSError:
                continue
