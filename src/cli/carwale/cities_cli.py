from __future__ import annotations

import argparse
import json
from typing import Any

from src.commands.carwale_cities import (
    DEFAULT_ARCHIVE_DIRECTORY,
    DEFAULT_CITIES_DIRECTORY,
    DEFAULT_REQUEST_DIRECTORY,
    run_carwale_cities,
)


def _handle_carwale_cities(
    args: argparse.Namespace,
) -> int:
    result = run_carwale_cities(
        output_dir=args.output_dir,
        request_dir=args.request_dir,
        archive_dir=args.archive_dir,
        min_request_interval=(args.min_request_interval),
        show_request=args.show_request,
        save_request=args.save_request,
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )

    return 0


def add_carwale_cities_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "carwale-cities",
        help=("Fetch all CarWale cities and save them to cities.json"),
        description=(
            "Fetch all cities from the CarWale "
            "cities API in a single request and "
            "save them to a JSON file."
        ),
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(DEFAULT_CITIES_DIRECTORY),
        help=(
            "Directory where cities.json will "
            "be saved. "
            f"Default: {DEFAULT_CITIES_DIRECTORY}"
        ),
    )

    parser.add_argument(
        "--request-dir",
        type=str,
        default=str(DEFAULT_REQUEST_DIRECTORY),
        help=(
            "Directory where the prepared request "
            "snapshot will be saved when "
            "--save-request is used. "
            f"Default: {DEFAULT_REQUEST_DIRECTORY}"
        ),
    )

    parser.add_argument(
        "--archive-dir",
        type=str,
        default=str(DEFAULT_ARCHIVE_DIRECTORY),
        help=(
            "Directory where timestamped cities "
            "archives will be saved. "
            f"Default: {DEFAULT_ARCHIVE_DIRECTORY}"
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
        help=("Print the prepared HTTP request before sending it."),
    )

    parser.add_argument(
        "--save-request",
        action="store_true",
        help=("Save the prepared HTTP request snapshot."),
    )

    parser.set_defaults(
        handler=_handle_carwale_cities,
    )
