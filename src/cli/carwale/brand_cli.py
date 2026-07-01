from __future__ import annotations

import argparse
from typing import Any

from src.commands.carwale_brands import (
    run_carwale_brands,
)


def add_carwale_brands_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "carwale-brands",
        help=("Fetch CarWale brands and save them to brands.json"),
        description=(
            "Fetch the makeList from CarWale and save "
            "the latest data to "
            "data/raw/carwale/brands.json."
        ),
    )

    parser.add_argument(
        "--page-id",
        type=int,
        default=2,
        help="CarWale page ID. Default: 2",
    )

    parser.add_argument(
        "--platform-id",
        type=int,
        default=1,
        help="CarWale platform ID. Default: 1",
    )

    parser.add_argument(
        "--show-request",
        action="store_true",
        help=("Print the prepared HTTP request before sending it"),
    )

    parser.add_argument(
        "--save-request",
        action="store_true",
        help=(
            "Save request information to data/raw/carwale/requests/brands_request.json"
        ),
    )

    parser.add_argument(
        "--include-sensitive-request-data",
        action="store_true",
        help=(
            "Include cookies, authorization headers, "
            "and other sensitive values in the request "
            "debugging output"
        ),
    )

    parser.set_defaults(
        handler=handle_carwale_brands,
    )


def handle_carwale_brands(
    args: argparse.Namespace,
) -> int:
    validate_carwale_brands_arguments(
        args=args,
    )

    result = run_carwale_brands(
        page_id=args.page_id,
        platform_id=args.platform_id,
        show_request=args.show_request,
        save_request=args.save_request,
        include_sensitive_request_data=(args.include_sensitive_request_data),
    )

    print_carwale_brands_result(
        result=result,
        page_id=args.page_id,
        platform_id=args.platform_id,
    )

    return 0


def validate_carwale_brands_arguments(
    *,
    args: argparse.Namespace,
) -> None:
    if args.page_id < 1:
        raise ValueError("--page-id must be greater than zero")

    if args.platform_id < 1:
        raise ValueError("--platform-id must be greater than zero")

    if (
        args.include_sensitive_request_data
        and not args.show_request
        and not args.save_request
    ):
        raise ValueError(
            "--include-sensitive-request-data requires --show-request or --save-request"
        )


def print_carwale_brands_result(
    *,
    result: dict[str, Any],
    page_id: int,
    platform_id: int,
) -> None:
    print()
    print(f"Command: {result['command']}")
    print(f"Page ID: {page_id}")
    print(f"Platform ID: {platform_id}")
    print(f"Brands: {result['brands_count']}")
    print(f"Latest file: {result['output_file']}")

    archive_file = result.get("archive_file")

    if archive_file:
        print(f"Archive file: {archive_file}")

    request_file = result.get("request_file")

    if request_file:
        print(f"Request file: {request_file}")

    print("Status: completed")
