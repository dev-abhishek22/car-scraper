from __future__ import annotations

import argparse
import json
from typing import Any

from src.commands.carwale_cars import (
    DEFAULT_ARCHIVE_DIRECTORY,
    DEFAULT_CARS_DIRECTORY,
    DEFAULT_MODELS_DIRECTORY,
    DEFAULT_REQUEST_DIRECTORY,
    DEFAULT_STATUS_FILE,
    run_carwale_cars,
)


def _handle_carwale_cars(
    args: argparse.Namespace,
) -> int:
    result = run_carwale_cars(
        brand=args.brand,
        model=args.model,
        models_dir=args.models_dir,
        output_dir=args.output_dir,
        status_file=args.status_file,
        request_dir=args.request_dir,
        archive_dir=args.archive_dir,
        workers=args.workers,
        min_request_interval=(args.min_request_interval),
        city_id=args.city_id,
        area_id=args.area_id,
        platform_id=args.platform_id,
        show_offer_upfront=(args.show_offer_upfront),
        force=args.force,
        failed_only=args.failed_only,
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

    return 1 if result.get("failed_cars", 0) > 0 else 0


def add_carwale_cars_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "carwale-cars",
        help=("Fetch detailed CarWale data for saved car models"),
        description=(
            "Read previously saved CarWale model "
            "files and fetch model-page details "
            "for each car. This command does not "
            "fetch brands or model lists again."
        ),
    )

    selection_group = parser.add_mutually_exclusive_group()

    selection_group.add_argument(
        "--brand",
        type=str,
        default=None,
        metavar="MAKE_MASKING_NAME",
        help=("Scrape all saved models for one brand, for example 'tata'."),
    )

    selection_group.add_argument(
        "--failed-only",
        action="store_true",
        help=("Retry only cars currently marked as failed in the cars status file."),
    )

    parser.add_argument(
        "--model",
        type=str,
        default=None,
        metavar="MODEL_MASKING_NAME",
        help=(
            "Scrape one model from the selected "
            "brand, for example 'punch'. "
            "Requires --brand."
        ),
    )

    parser.add_argument(
        "--models-dir",
        type=str,
        default=str(DEFAULT_MODELS_DIRECTORY),
        help=(
            "Directory containing previously "
            "saved CarWale model JSON files. "
            f"Default: {DEFAULT_MODELS_DIRECTORY}"
        ),
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(DEFAULT_CARS_DIRECTORY),
        help=(
            "Directory where detailed car files "
            "will be saved. "
            f"Default: {DEFAULT_CARS_DIRECTORY}"
        ),
    )

    parser.add_argument(
        "--status-file",
        type=str,
        default=str(DEFAULT_STATUS_FILE),
        help=(f"Path to the cars scraping status file. Default: {DEFAULT_STATUS_FILE}"),
    )

    parser.add_argument(
        "--request-dir",
        type=str,
        default=str(DEFAULT_REQUEST_DIRECTORY),
        help=(
            "Directory where prepared request "
            "snapshots are saved when "
            "--save-request is used. "
            f"Default: {DEFAULT_REQUEST_DIRECTORY}"
        ),
    )

    parser.add_argument(
        "--archive-dir",
        type=str,
        default=str(DEFAULT_ARCHIVE_DIRECTORY),
        help=(
            "Directory where timestamped car "
            "archives will be saved. "
            f"Default: {DEFAULT_ARCHIVE_DIRECTORY}"
        ),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=3,
        choices=range(1, 9),
        metavar="[1-8]",
        help=("Number of concurrent car workers. Allowed: 1-8. Default: 3"),
    )

    parser.add_argument(
        "--min-request-interval",
        type=float,
        default=2.0,
        metavar="SECONDS",
        help=(
            "Minimum global interval between "
            "request starts across all workers. "
            "Default: 2"
        ),
    )

    parser.add_argument(
        "--city-id",
        type=int,
        default=10,
        help=("CarWale city ID used for model-page data. Default: 10"),
    )

    parser.add_argument(
        "--area-id",
        type=int,
        default=3657,
        help=("CarWale area ID used for model-page data. Default: 3657"),
    )

    parser.add_argument(
        "--platform-id",
        type=int,
        default=1,
        help=("CarWale platform ID. Default: 1"),
    )

    parser.add_argument(
        "--show-offer-upfront",
        action="store_true",
        help=("Send showOfferUpfront=true to the CarWale model-page API."),
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help=("Scrape again and overwrite existing valid car files."),
    )

    parser.add_argument(
        "--show-request",
        action="store_true",
        help=("Print prepared HTTP requests before sending them."),
    )

    parser.add_argument(
        "--save-request",
        action="store_true",
        help=("Save prepared HTTP request snapshots for each car."),
    )

    parser.set_defaults(
        handler=_handle_carwale_cars,
    )
