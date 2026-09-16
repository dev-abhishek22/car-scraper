from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.cardekho_model_images import (
    run_cardekho_model_images,
)


def _handle_cardekho_model_images(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_cardekho_model_images(
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

    failed_models = result.get(
        "failedModels",
        0,
    )

    if (
        isinstance(failed_models, int)
        and not isinstance(
            failed_models,
            bool,
        )
        and failed_models > 0
    ):
        return 1

    return 0


def add_cardekho_model_images_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "cardekho-model-images",
        help=("Fetch CarDekho model gallery images"),
        description=(
            "Read models from the cardekho_models "
            "MongoDB collection, fetch model gallery "
            "images from CarDekho asynchronously, store "
            "the complete data.images structure in "
            "cardekho_model_images, and track the run "
            "through scraper_runs and scraper_jobs."
        ),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        metavar="COUNT",
        help=("Number of concurrent model workers. Default: 5"),
    )

    parser.add_argument(
        "--requests-per-second",
        type=float,
        default=5.0,
        metavar="RPS",
        help=(
            "Maximum global request starts per second "
            "across all workers. Default: 5"
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
        handler=_handle_cardekho_model_images,
    )
