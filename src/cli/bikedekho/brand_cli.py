from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.bikedekho_brands import (
    run_bikedekho_brands,
)


def _handle_bikedekho_brands(
    args: argparse.Namespace,
) -> int:
    del args

    result = asyncio.run(run_bikedekho_brands())

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )

    return 0


def add_bikedekho_brands_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "bikedekho-brands",
        help=("Fetch BikeDekho brands and store them in MongoDB"),
        description=(
            "Fetch the BikeDekho brand list, store the "
            "brands in the bikedekho_brands MongoDB "
            "collection, and track the operation using "
            "scraper_runs and scraper_jobs."
        ),
    )

    parser.set_defaults(
        handler=_handle_bikedekho_brands,
    )
