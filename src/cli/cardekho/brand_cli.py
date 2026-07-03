from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.cardekho_brands import (
    run_cardekho_brands,
)


def _handle_cardekho_brands(
    args: argparse.Namespace,
) -> int:
    del args

    result = asyncio.run(run_cardekho_brands())

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )

    return 0


def add_cardekho_brands_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "cardekho-brands",
        help=("Fetch CarDekho brands and store " "them in MongoDB"),
        description=(
            "Fetch the CarDekho brand list, store the "
            "brands in the cardekho_brands MongoDB "
            "collection, and track the operation using "
            "scraper_runs and scraper_jobs."
        ),
    )

    parser.set_defaults(
        handler=_handle_cardekho_brands,
    )
