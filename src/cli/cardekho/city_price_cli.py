from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any, Callable

from src.commands.cardekho_city_prices import (
    run_cardekho_city_prices,
)

ArgumentParserType = Callable[[str], Any]


def _integer_in_range(
    *,
    minimum: int,
    maximum: int | None = None,
) -> ArgumentParserType:
    def parse(
        value: str,
    ) -> int:
        try:
            parsed_value = int(value)

        except ValueError as error:
            raise argparse.ArgumentTypeError(
                f"Expected an integer, received {value!r}"
            ) from error

        if parsed_value < minimum:
            raise argparse.ArgumentTypeError(f"Value must be at least {minimum}")

        if maximum is not None and parsed_value > maximum:
            raise argparse.ArgumentTypeError(
                f"Value must be between {minimum} and {maximum}"
            )

        return parsed_value

    return parse


def _positive_float(
    value: str,
) -> float:
    try:
        parsed_value = float(value)

    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"Expected a number, received {value!r}"
        ) from error

    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("Value must be greater than zero")

    return parsed_value


def _non_negative_float(
    value: str,
) -> float:
    try:
        parsed_value = float(value)

    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"Expected a number, received {value!r}"
        ) from error

    if parsed_value < 0:
        raise argparse.ArgumentTypeError("Value cannot be negative")

    return parsed_value


def _non_empty_string(
    value: str,
) -> str:
    normalized_value = value.strip()

    if not normalized_value:
        raise argparse.ArgumentTypeError("Value cannot be empty")

    return normalized_value


def _handle_cardekho_city_prices(
    args: argparse.Namespace,
) -> int:
    try:
        result = asyncio.run(
            run_cardekho_city_prices(
                brand=args.brand,
                model=args.model,
                model_id=args.model_id,
                city=args.city,
                city_id=args.city_id,
                popular_cities_only=(args.popular_cities_only),
                workers=args.workers,
                requests_per_second=(args.requests_per_second),
                mongo_batch_size=(args.mongo_batch_size),
                pause_every_requests=(args.pause_every_requests),
                pause_seconds=(args.pause_seconds),
                max_jobs=args.max_jobs,
                resume_run_id=(args.resume_run_id),
                failed_only=(args.failed_only),
                retry_terminal_failures=(args.retry_terminal_failures),
            )
        )

    except KeyboardInterrupt:
        print(
            json.dumps(
                {
                    "command": ("cardekho-city-prices"),
                    "status": ("interrupted"),
                    "stopReason": ("keyboard_interrupt"),
                },
                indent=2,
                ensure_ascii=False,
            )
        )

        return 130

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )

    status = result.get("status")

    if status == "interrupted":
        return 2

    if status in {
        "failed",
        "cancelled",
    }:
        return 1

    unresolved_failures = result.get(
        "unresolvedFailures",
        0,
    )

    if (
        isinstance(
            unresolved_failures,
            int,
        )
        and not isinstance(
            unresolved_failures,
            bool,
        )
        and unresolved_failures > 0
    ):
        return 1

    return 0


def add_cardekho_city_prices_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "cardekho-city-prices",
        help=("Fetch Cardekho model prices for saved cities"),
        description=(
            "Read CURRENT Cardekho cars and "
            "saved Cardekho cities from MongoDB, "
            "generate model-city combinations, "
            "fetch pricing for every variant, "
            "save normalized results to MongoDB, "
            "and support resumable runs."
        ),
    )

    parser.add_argument(
        "--brand",
        type=_non_empty_string,
        default=None,
        metavar="BRAND_SLUG",
        help=("Scrape one Cardekho brand, for example 'tata' or 'maruti'."),
    )

    parser.add_argument(
        "--model",
        type=_non_empty_string,
        default=None,
        metavar="MODEL_SLUG",
        help=(
            "Scrape one model from the "
            "selected brand, for example "
            "'punch'. Requires --brand."
        ),
    )

    parser.add_argument(
        "--model-id",
        type=_integer_in_range(
            minimum=1,
        ),
        default=None,
        metavar="MODEL_ID",
        help=("Scrape one Cardekho model using its numeric model ID."),
    )

    parser.add_argument(
        "--city",
        type=_non_empty_string,
        default=None,
        metavar="CITY_SLUG",
        help=("Scrape one city using its name or slug, for example 'new-delhi'."),
    )

    parser.add_argument(
        "--city-id",
        type=_integer_in_range(
            minimum=1,
        ),
        default=None,
        metavar="CITY_ID",
        help=("Scrape one Cardekho city using its numeric city ID."),
    )

    parser.add_argument(
        "--popular-cities-only",
        action="store_true",
        help=("Generate jobs only for cities marked as popular in cardekho_cities."),
    )

    parser.add_argument(
        "--workers",
        type=_integer_in_range(
            minimum=1,
            maximum=500,
        ),
        default=5,
        metavar="COUNT",
        help=("Number of concurrent HTTP workers. Allowed: 1-500. Default: 5"),
    )

    parser.add_argument(
        "--requests-per-second",
        type=_positive_float,
        default=2.0,
        metavar="RPS",
        help=("Maximum global request-start rate across all workers. Default: 2"),
    )

    parser.add_argument(
        "--mongo-batch-size",
        type=_integer_in_range(
            minimum=1,
        ),
        default=100,
        metavar="COUNT",
        help=(
            "Number of successful records "
            "written to MongoDB per batch. "
            "Failure records use a smaller "
            "protected batch internally. "
            "Default: 100"
        ),
    )

    parser.add_argument(
        "--pause-every-requests",
        type=_integer_in_range(
            minimum=0,
        ),
        default=None,
        metavar="COUNT",
        help=(
            "Pause all new HTTP request "
            "starts after this many actual "
            "request attempts. Use together "
            "with --pause-seconds. Use 0 with "
            "--pause-seconds 0 to disable a "
            "saved pause while resuming."
        ),
    )

    parser.add_argument(
        "--pause-seconds",
        "--pause",
        dest="pause_seconds",
        type=_non_negative_float,
        default=None,
        metavar="SECONDS",
        help=(
            "Global pause duration after "
            "each configured "
            "--pause-every-requests interval. "
            "The shorter alias is --pause."
        ),
    )

    parser.add_argument(
        "--max-jobs",
        type=_integer_in_range(
            minimum=1,
        ),
        default=None,
        metavar="COUNT",
        help=("Stop after generating this many model-city jobs. Useful for testing."),
    )

    parser.add_argument(
        "--resume-run-id",
        type=_non_empty_string,
        default=None,
        metavar="RUN_ID",
        help=(
            "Resume an existing Cardekho "
            "city-price run using its saved "
            "run ID and settings."
        ),
    )

    parser.add_argument(
        "--failed-only",
        action="store_true",
        help=("Retry only unresolved failures stored for --resume-run-id."),
    )

    parser.add_argument(
        "--retry-terminal-failures",
        action="store_true",
        help=(
            "Include terminal failures such "
            "as invalid responses or HTTP 404 "
            "in a failed-only retry."
        ),
    )

    parser.set_defaults(
        handler=(_handle_cardekho_city_prices),
    )
