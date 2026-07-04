from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.carwale_cities import (
    run_carwale_cities,
)


def _handle_carwale_cities(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_carwale_cities(
            min_request_interval=(args.min_request_interval),
            show_request=args.show_request,
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

    return 0 if result.get("status") == "completed" else 1


def add_carwale_cities_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "carwale-cities",
        help=("Fetch all CarWale cities and store them in MongoDB"),
        description=(
            "Fetch all cities from the CarWale "
            "cities API in one request, upsert "
            "them into carwale_cities, and track "
            "the operation through scraper_runs "
            "and scraper_jobs."
        ),
    )

    parser.add_argument(
        "--min-request-interval",
        type=float,
        default=2.0,
        metavar="SECONDS",
        help=("Minimum interval between CarWale request starts. Default: 2"),
    )

    parser.add_argument(
        "--show-request",
        action="store_true",
        help=("Print the prepared HTTP request before sending it"),
    )

    parser.set_defaults(
        handler=_handle_carwale_cities,
    )
