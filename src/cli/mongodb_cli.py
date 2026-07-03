from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.mongodb_indexes import (
    run_mongodb_indexes,
)


def _handle_mongodb_indexes(
    args: argparse.Namespace,
) -> int:
    del args

    result = asyncio.run(run_mongodb_indexes())

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )

    return 0


def add_mongodb_indexes_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "mongodb-indexes",
        help=("Create and verify MongoDB indexes"),
        description=(
            "Create all required indexes for scraper runs, "
            "scraper jobs, and existing CarWale city-price "
            "collections. This command is safe to run repeatedly."
        ),
    )

    parser.set_defaults(
        handler=_handle_mongodb_indexes,
    )
