from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.carwale_cars import (
    run_carwale_cars,
)


def _handle_carwale_cars(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_carwale_cars(
            brand=args.brand,
            model=args.model,
            workers=args.workers,
            requests_per_second=(args.requests_per_second),
            city_id=args.city_id,
            area_id=args.area_id,
            platform_id=args.platform_id,
            show_offer_upfront=(args.show_offer_upfront),
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


def add_carwale_cars_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "carwale-cars",
        help=("Fetch CarWale cars using models stored in MongoDB"),
        description=(
            "Read models from the carwale_models "
            "MongoDB collection, fetch detailed "
            "CarWale model-page data asynchronously, "
            "store each make-model response in "
            "carwale_cars, and track the operation "
            "through scraper_runs and scraper_jobs."
        ),
    )

    parser.add_argument(
        "--brand",
        type=str,
        default=None,
        metavar="BRAND_SLUG",
        help=(
            "Process one brand, for example "
            "'tata' or 'maruti-suzuki'. "
            "By default, models from all brands "
            "are processed."
        ),
    )

    parser.add_argument(
        "--model",
        type=str,
        default=None,
        metavar="MODEL_SLUG",
        help=("Process one model, for example 'nexon'. This option requires --brand."),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=3,
        metavar="COUNT",
        help=("Number of concurrent model workers. Default: 3"),
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
        "--city-id",
        type=int,
        default=None,
        metavar="CITY_ID",
        help=("Optional CarWale city ID used for model-page requests."),
    )

    parser.add_argument(
        "--area-id",
        type=int,
        default=None,
        metavar="AREA_ID",
        help=("Optional CarWale area ID used for model-page requests."),
    )

    parser.add_argument(
        "--platform-id",
        type=int,
        default=None,
        metavar="PLATFORM_ID",
        help=("Optional CarWale platform ID used for model-page requests."),
    )

    parser.add_argument(
        "--show-offer-upfront",
        action="store_true",
        help=("Request CarWale offer information upfront. Disabled by default."),
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
        handler=_handle_carwale_cars,
    )
