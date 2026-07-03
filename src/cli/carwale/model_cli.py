from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.carwale_models import (
    run_carwale_models,
)


def _handle_carwale_models(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_carwale_models(
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
        and not isinstance(failed_brands, bool)
        and failed_brands > 0
    ):
        return 1

    return 0


def add_carwale_models_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "carwale-models",
        help=("Fetch CarWale models using brands stored in MongoDB"),
        description=(
            "Read brands from the carwale_brands "
            "MongoDB collection, fetch model lists "
            "from CarWale asynchronously, store each "
            "model in carwale_models, and track the "
            "run through scraper_runs and scraper_jobs."
        ),
    )

    parser.add_argument(
        "--brand",
        type=str,
        default=None,
        metavar="MASKING_NAME",
        help=(
            "Scrape models for one MongoDB brand, "
            "for example 'tata' or "
            "'maruti-suzuki'. By default all brands "
            "from carwale_brands are processed."
        ),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        metavar="COUNT",
        help=("Number of concurrent brand workers. Default: 5"),
    )

    parser.add_argument(
        "--requests-per-second",
        type=float,
        default=5.0,
        metavar="RPS",
        help=(
            "Maximum global request starts per second across all workers. Default: 5"
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
        handler=_handle_carwale_models,
    )
