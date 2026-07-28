from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.bikedekho_bikes import (
    run_bikedekho_bikes,
)


def _handle_bikedekho_bikes(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_bikedekho_bikes(
            brand=args.brand,
            model=args.model,
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

    failed_cars = result.get(
        "failedBikes",
        0,
    )

    if (
        isinstance(failed_cars, int)
        and not isinstance(
            failed_cars,
            bool,
        )
        and failed_cars > 0
    ):
        return 1

    return 0


def add_bikedekho_bikes_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "bikedekho-bikes",
        help=("Fetch BikeDekho bikes using models stored in MongoDB"),
        description=(
            "Read models from the bikedekho_models "
            "MongoDB collection, fetch model overview "
            "data from BikeDekho asynchronously, store "
            "model overview, minimal variants, related "
            "comparisons, similar bikes, and variants "
            "comparison data in bikedekho_bikes, and "
            "track the operation through scraper_runs "
            "and scraper_jobs."
        ),
    )

    parser.add_argument(
        "--brand",
        type=str,
        default=None,
        metavar="BRAND_SLUG",
        help=(
            "Process models from one BikeDekho brand. "
            "Examples: 'honda', 'hero', or "
            "'royal-enfield'. By default, models "
            "from all brands are processed."
        ),
    )

    parser.add_argument(
        "--model",
        type=str,
        default=None,
        metavar="MODEL_SLUG",
        help=(
            "Process one BikeDekho model. "
            "Examples: 'shine', 'sp125', or "
            "'classic-350'. This option requires --brand."
        ),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        metavar="COUNT",
        help=("Number of concurrent model workers. Default: 1"),
    )

    parser.add_argument(
        "--requests-per-second",
        type=float,
        default=3.0,
        metavar="RPS",
        help=(
            "Maximum global HTTP request starts "
            "per second across all workers. "
            "Default: 3"
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
            "Scheduled pause duration in seconds. "
            "Use 0 to disable scheduled pauses. "
            "Must be used with "
            "--pause-every-requests. Default: 0"
        ),
    )

    parser.set_defaults(
        handler=_handle_bikedekho_bikes,
    )
