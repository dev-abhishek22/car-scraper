from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.carwale_brands import (
    run_carwale_brands,
)


def _handle_carwale_brands(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_carwale_brands(
            page_id=args.page_id,
            platform_id=args.platform_id,
        )
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )

    return 0


def add_carwale_brands_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "carwale-brands",
        help=("Fetch CarWale brands and store them in MongoDB"),
        description=(
            "Fetch the CarWale brand list, store the "
            "brands in the carwale_brands MongoDB "
            "collection, and track the operation using "
            "scraper_runs and scraper_jobs."
        ),
    )

    parser.add_argument(
        "--page-id",
        type=int,
        default=2,
        help=("CarWale page ID. Default: 2"),
    )

    parser.add_argument(
        "--platform-id",
        type=int,
        default=1,
        help=("CarWale platform ID. Default: 1"),
    )

    parser.set_defaults(
        handler=_handle_carwale_brands,
    )
