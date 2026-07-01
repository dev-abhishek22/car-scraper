from __future__ import annotations

import argparse
from typing import Any

from src.commands.clean_expired_files import (
    run_clean_expired_files,
)


def add_cleanup_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "clean-expired-files",
        help=("Delete expired JSON files from archive directories"),
        description=(
            "Find JSON files inside directories named "
            "'archive' and delete files older than the "
            "configured DATA_RETENTION_DAYS value."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=("Show expired files without deleting them"),
    )

    parser.set_defaults(
        handler=handle_cleanup,
    )


def handle_cleanup(
    args: argparse.Namespace,
) -> int:
    result = run_clean_expired_files(
        dry_run=args.dry_run,
    )

    print_cleanup_result(
        result=result,
    )

    return 0


def print_cleanup_result(
    *,
    result: dict[str, Any],
) -> None:
    print()
    print(f"Command: {result['command']}")
    print(f"Root directory: {result['root_directory']}")
    print(f"Retention: {result['retention_days']} days")
    print(f"Expired files found: {result['files_count']}")

    files = result["files"]

    if files:
        print()
        print("Files:")

        for file_path in files:
            print(f"- {file_path}")

    print()

    if result["dry_run"]:
        print("Status: dry run completed; no files were deleted")
    else:
        print("Status: cleanup completed")
