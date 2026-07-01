from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.carwale_city_prices import (
    DEFAULT_CARS_DIRECTORY,
    DEFAULT_CITIES_FILE,
    run_carwale_city_prices,
)


def _handle_carwale_city_prices(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_carwale_city_prices(
            cars_directory=args.cars_directory,
            cities_file=args.cities_file,
            brand=args.brand,
            model=args.model,
            city=args.city,
            workers=args.workers,
            requests_per_second=(args.requests_per_second),
            mongo_batch_size=(args.mongo_batch_size),
            max_jobs=args.max_jobs,
            resume_run_id=(args.resume_run_id),
            failed_only=args.failed_only,
            retry_terminal_failures=(args.retry_terminal_failures),
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

    unresolved_failures = result.get(
        "unresolvedFailures",
        0,
    )

    if (
        isinstance(
            unresolved_failures,
            int,
        )
        and unresolved_failures > 0
    ):
        return 1

    return 0


def add_carwale_city_prices_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "carwale-city-prices",
        help=("Fetch CarWale version prices " "for saved cities"),
        description=(
            "Read saved CarWale car and city "
            "files, generate every version-city "
            "combination, fetch PIC-page pricing, "
            "and save results to MongoDB. "
            "Supports resumable runs and "
            "failed-page retries."
        ),
    )

    parser.add_argument(
        "--brand",
        type=str,
        default=None,
        metavar="MAKE_MASKING_NAME",
        help=("Scrape one saved CarWale brand, " "for example 'audi'."),
    )

    parser.add_argument(
        "--model",
        type=str,
        default=None,
        metavar="MODEL_MASKING_NAME",
        help=(
            "Scrape one model from the selected "
            "brand, for example 'a4'. "
            "Requires --brand."
        ),
    )

    parser.add_argument(
        "--city",
        type=str,
        default=None,
        metavar="CITY_MASKING_NAME",
        help=("Scrape one city only, " "for example 'mumbai'."),
    )

    parser.add_argument(
        "--cars-directory",
        type=str,
        default=str(DEFAULT_CARS_DIRECTORY),
        help=(
            "Directory containing saved "
            "CarWale car JSON files. "
            f"Default: {DEFAULT_CARS_DIRECTORY}"
        ),
    )

    parser.add_argument(
        "--cities-file",
        type=str,
        default=str(DEFAULT_CITIES_FILE),
        help=(
            "Path to the saved CarWale "
            "cities JSON file. "
            f"Default: {DEFAULT_CITIES_FILE}"
        ),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        choices=range(
            1,
            501,
        ),
        metavar="[1-500]",
        help=("Number of concurrent HTTP workers. " "Allowed: 1-500. Default: 5"),
    )

    parser.add_argument(
        "--requests-per-second",
        type=float,
        default=2.0,
        metavar="RPS",
        help=("Maximum global request-start rate " "across all workers. Default: 2"),
    )

    parser.add_argument(
        "--mongo-batch-size",
        type=int,
        default=100,
        metavar="COUNT",
        help=(
            "Number of successful or failed "
            "records written to MongoDB per "
            "batch. Default: 100"
        ),
    )

    parser.add_argument(
        "--max-jobs",
        type=int,
        default=None,
        metavar="COUNT",
        help=(
            "Stop after generating this many "
            "version-city jobs. Useful for "
            "testing."
        ),
    )

    parser.add_argument(
        "--resume-run-id",
        type=str,
        default=None,
        metavar="RUN_ID",
        help=(
            "Resume an existing CarWale " "city-price run using its saved " "run ID."
        ),
    )

    parser.add_argument(
        "--failed-only",
        action="store_true",
        help=("Retry only unresolved failures " "stored for --resume-run-id."),
    )

    parser.add_argument(
        "--retry-terminal-failures",
        action="store_true",
        help=(
            "Retry terminal failures such as "
            "invalid responses and HTTP 404 "
            "instead of skipping them."
        ),
    )

    parser.set_defaults(
        handler=(_handle_carwale_city_prices),
    )
