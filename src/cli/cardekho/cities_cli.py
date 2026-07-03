from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.cardekho_cities import (
    run_cardekho_cities,
)


def _handle_cardekho_cities(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_cardekho_cities(
            requests_per_second=(args.requests_per_second),
            pause_every_requests=(args.pause_every_requests),
            pause_seconds=(args.pause_seconds),
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

    failed_jobs = result.get(
        "failedJobs",
        0,
    )

    if (
        isinstance(failed_jobs, int)
        and not isinstance(
            failed_jobs,
            bool,
        )
        and failed_jobs > 0
    ):
        return 1

    return 0


def add_cardekho_cities_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "cardekho-cities",
        help=("Fetch CarDekho cities from the " "static cities bundle"),
        description=(
            "Download the CarDekho webpack cities "
            "bundle, extract and normalize the city "
            "catalogue, merge duplicate city IDs and "
            "aliases, store the resulting documents "
            "in cardekho_cities, and track the run "
            "through scraper_runs and scraper_jobs."
        ),
    )

    parser.add_argument(
        "--requests-per-second",
        type=float,
        default=1.0,
        metavar="RPS",
        help=(
            "Maximum HTTP request starts per second. "
            "The cities scraper performs one bundle "
            "request. Default: 1"
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
            "Duration of each scheduled HTTP pause. "
            "Use 0 to disable scheduled pauses. "
            "Must be used with "
            "--pause-every-requests. Default: 0"
        ),
    )

    parser.set_defaults(handler=_handle_cardekho_cities)
