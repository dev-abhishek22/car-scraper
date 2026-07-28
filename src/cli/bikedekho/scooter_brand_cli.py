from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.bikedekho_scooter_brands import run_bikedekho_scooter_brands


def _handle_bikedekho_scooter_brands(args: argparse.Namespace) -> int:
    del args
    result = asyncio.run(run_bikedekho_scooter_brands())
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return 0


def add_bikedekho_scooter_brands_command(*, subparsers: Any) -> None:
    parser = subparsers.add_parser(
        "bikedekho-scooter-brands",
        help="Fetch BikeDekho scooter brands and store them in MongoDB",
        description=(
            "Fetch scooter brands from the BikeDekho scooters landing page and "
            "store them in the bikedekho_scooter_brands MongoDB collection."
        ),
    )
    parser.set_defaults(handler=_handle_bikedekho_scooter_brands)
