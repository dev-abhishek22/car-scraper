from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.bikedekho_scooters import (
    run_bikedekho_scooters,
)


def _handle_bikedekho_scooters(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_bikedekho_scooters(
            brand=args.brand,
            model=args.model,
            workers=args.workers,
            requests_per_second=args.requests_per_second,
            pause_every_requests=args.pause_every_requests,
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

    failed_scooters = result.get(
        "failedScooters",
        0,
    )

    if (
        isinstance(failed_scooters, int)
        and not isinstance(failed_scooters, bool)
        and failed_scooters > 0
    ):
        return 1

    return 0


def add_bikedekho_scooters_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "bikedekho-scooters",
        help=("Fetch BikeDekho scooters using models stored in MongoDB"),
        description=(
            "Read scooter models from the BikeDekho "
            "MongoDB source collection, fetch scooter "
            "model overview data asynchronously using "
            "the BikeDekho modelOverview API, and store "
            "the results in the scooter collection."
        ),
    )

    parser.add_argument(
        "--brand",
        type=str,
        default=None,
        metavar="BRAND_SLUG",
        help=(
            "Process scooter models from one BikeDekho "
            "brand. By default, models from all brands "
            "are processed."
        ),
    )

    parser.add_argument(
        "--model",
        type=str,
        default=None,
        metavar="MODEL_SLUG",
        help=("Process one BikeDekho scooter model. This option requires --brand."),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        metavar="COUNT",
        help=("Number of concurrent scooter workers. Default: 1"),
    )

    parser.add_argument(
        "--requests-per-second",
        type=float,
        default=3.0,
        metavar="RPS",
        help=(
            "Maximum global HTTP request starts per "
            "second across all workers. Default: 3"
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
            "Default: 0"
        ),
    )

    parser.set_defaults(
        handler=_handle_bikedekho_scooters,
    )
