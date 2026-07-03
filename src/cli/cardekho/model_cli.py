from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.cardekho_models import (
    run_cardekho_models,
)


def _handle_cardekho_models(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_cardekho_models(
            brand=args.brand,
            workers=args.workers,
            requests_per_second=(args.requests_per_second),
            pause_every_requests=(args.pause_every_requests),
            pause_seconds=args.pause_seconds,
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

    failed_brands = result.get(
        "failedBrands",
        0,
    )

    if (
        isinstance(failed_brands, int)
        and not isinstance(
            failed_brands,
            bool,
        )
        and failed_brands > 0
    ):
        return 1

    return 0


def add_cardekho_models_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "cardekho-models",
        help=("Fetch CarDekho models using brands " "stored in MongoDB"),
        description=(
            "Read current and upcoming brands from "
            "the cardekho_brands MongoDB collection, "
            "fetch current and upcoming model lists "
            "from CarDekho asynchronously, store each "
            "model in cardekho_models, and track the "
            "run through scraper_runs and scraper_jobs."
        ),
    )

    parser.add_argument(
        "--brand",
        type=str,
        default=None,
        metavar="SLUG",
        help=(
            "Scrape models for one CarDekho brand "
            "using its source slug or model request "
            "slug. Examples: 'tata', 'maruti', or "
            "'maruti-suzuki'. By default all current "
            "and upcoming brands are processed."
        ),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        metavar="COUNT",
        help=("Number of concurrent brand workers. " "Default: 5"),
    )

    parser.add_argument(
        "--requests-per-second",
        type=float,
        default=5.0,
        metavar="RPS",
        help=(
            "Maximum global request starts per second " "across all workers. Default: 5"
        ),
    )

    parser.add_argument(
        "--pause-every-requests",
        type=int,
        default=0,
        metavar="COUNT",
        help=(
            "Pause after this many HTTP requests. "
            "Use 0 to disable scheduled pauses. "
            "Must be used with --pause-seconds. "
            "Default: 0"
        ),
    )

    parser.add_argument(
        "--pause-seconds",
        type=float,
        default=0.0,
        metavar="SECONDS",
        help=(
            "Scheduled pause duration. Use 0 to "
            "disable scheduled pauses. Must be used "
            "with --pause-every-requests. Default: 0"
        ),
    )

    parser.set_defaults(
        handler=_handle_cardekho_models,
    )
