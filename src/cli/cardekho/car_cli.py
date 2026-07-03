from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.cardekho_cars import (
    run_cardekho_cars,
)


def _handle_cardekho_cars(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_cardekho_cars(
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
        "failedCars",
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


def add_cardekho_cars_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "cardekho-cars",
        help=("Fetch CarDekho cars using models " "stored in MongoDB"),
        description=(
            "Read models from the cardekho_models "
            "MongoDB collection, fetch model overview "
            "data from CarDekho asynchronously, store "
            "model overview, minimal variants, related "
            "cars, similar cars, and old-generation "
            "comparison data in cardekho_cars, and "
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
            "Process models from one CarDekho brand. "
            "Examples: 'tata', 'maruti', or "
            "'ashok-leyland'. By default, models "
            "from all brands are processed."
        ),
    )

    parser.add_argument(
        "--model",
        type=str,
        default=None,
        metavar="MODEL_SLUG",
        help=(
            "Process one CarDekho model. "
            "Examples: 'nexon', 'brezza', or "
            "'tekton'. This option requires --brand."
        ),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=3,
        metavar="COUNT",
        help=("Number of concurrent model workers. " "Default: 3"),
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
        handler=_handle_cardekho_cars,
    )
