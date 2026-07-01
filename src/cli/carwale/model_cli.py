from __future__ import annotations

import argparse
import json
from typing import Any

from src.commands.carwale_models import (
    DEFAULT_BRANDS_FILE,
    DEFAULT_MODELS_DIRECTORY,
    DEFAULT_REQUEST_DIRECTORY,
    DEFAULT_STATUS_FILE,
    run_carwale_models,
)


def _handle_carwale_models(
    args: argparse.Namespace,
) -> int:
    result = run_carwale_models(
        brand=args.brand,
        brands_file=args.brands_file,
        output_dir=args.output_dir,
        status_file=args.status_file,
        request_dir=args.request_dir,
        force=args.force,
        failed_only=args.failed_only,
        show_request=args.show_request,
        save_request=args.save_request,
        delay_min=args.delay_min,
        delay_max=args.delay_max,
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )

    return 0


def add_carwale_models_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "carwale-models",
        help=("Fetch CarWale models for one or multiple brands"),
        description=(
            "Read brands from the saved CarWale "
            "brands file and fetch only the models "
            "field from the make-page API."
        ),
    )

    selection_group = parser.add_mutually_exclusive_group()

    selection_group.add_argument(
        "--brand",
        type=str,
        default=None,
        metavar="MASKING_NAME",
        help=(
            "Scrape only one brand using its maskingName, for example 'maruti-suzuki'."
        ),
    )

    selection_group.add_argument(
        "--failed-only",
        action="store_true",
        help=("Scrape only brands currently marked as failed in the status file."),
    )

    parser.add_argument(
        "--brands-file",
        type=str,
        default=str(DEFAULT_BRANDS_FILE),
        help=(f"Path to the CarWale brands JSON file. Default: {DEFAULT_BRANDS_FILE}"),
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(DEFAULT_MODELS_DIRECTORY),
        help=(
            "Directory where brand model files "
            "will be saved. "
            f"Default: {DEFAULT_MODELS_DIRECTORY}"
        ),
    )

    parser.add_argument(
        "--status-file",
        type=str,
        default=str(DEFAULT_STATUS_FILE),
        help=(
            f"Path to the models scraping status file. Default: {DEFAULT_STATUS_FILE}"
        ),
    )

    parser.add_argument(
        "--request-dir",
        type=str,
        default=str(DEFAULT_REQUEST_DIRECTORY),
        help=(
            "Directory where prepared request "
            "snapshots will be saved when "
            "--save-request is used. "
            f"Default: {DEFAULT_REQUEST_DIRECTORY}"
        ),
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help=("Scrape again and overwrite existing model files."),
    )

    parser.add_argument(
        "--show-request",
        action="store_true",
        help=("Print each prepared HTTP request before sending it."),
    )

    parser.add_argument(
        "--save-request",
        action="store_true",
        help=("Save prepared HTTP request snapshots to the request directory."),
    )

    parser.add_argument(
        "--delay-min",
        type=float,
        default=2.0,
        metavar="SECONDS",
        help=("Minimum delay between brands when scraping multiple brands. Default: 2"),
    )

    parser.add_argument(
        "--delay-max",
        type=float,
        default=4.0,
        metavar="SECONDS",
        help=("Maximum delay between brands when scraping multiple brands. Default: 4"),
    )

    parser.set_defaults(
        handler=_handle_carwale_models,
    )
