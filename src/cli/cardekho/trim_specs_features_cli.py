from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.cardekho_trim_specs_features import (
    run_cardekho_trim_specs_features,
)


def _handle_cardekho_trim_specs_features(
    args: argparse.Namespace,
) -> int:
    result = asyncio.run(
        run_cardekho_trim_specs_features(
            brand=args.brand,
            model=args.model,
            model_id=args.model_id,
            variant=args.variant,
            variant_id=args.variant_id,
            workers=args.workers,
            requests_per_second=(args.requests_per_second),
            max_jobs=args.max_jobs,
            pause_every_requests=(args.pause_every_requests),
            pause_seconds=args.pause_seconds,
            refresh_existing=(args.refresh_existing),
            resume_run_id=(args.resume_run_id),
            failed_only=args.failed_only,
            retry_terminal_failures=(args.retry_terminal_failures),
            stale_after_seconds=(args.stale_after_seconds),
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

    failed_variants = result.get(
        "failedVariants",
        0,
    )

    if (
        isinstance(
            failed_variants,
            int,
        )
        and not isinstance(
            failed_variants,
            bool,
        )
        and failed_variants > 0
    ):
        return 1

    return 0


def add_cardekho_trim_specs_features_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "cardekho-trim-specs-features",
        help=(
            "Fetch Cardekho specifications and features for variants stored in MongoDB"
        ),
        description=(
            "Read variants from the "
            "cardekho_cars MongoDB collection, "
            "fetch Cardekho model-specs data "
            "asynchronously, store featured "
            "specifications and full "
            "specification sections in "
            "cardekho_trim_specs_features, "
            "and track execution through "
            "scraper_runs and scraper_jobs."
        ),
    )

    parser.add_argument(
        "--brand",
        type=str,
        default=None,
        metavar="BRAND_SLUG",
        help=(
            "Process one brand, for example "
            "'maruti'. By default, variants "
            "from all brands are processed."
        ),
    )

    parser.add_argument(
        "--model",
        type=str,
        default=None,
        metavar="MODEL_SLUG",
        help=("Process one model, for example 'brezza'. This option requires --brand."),
    )

    parser.add_argument(
        "--model-id",
        type=int,
        default=None,
        metavar="MODEL_ID",
        help=("Process one Cardekho model ID, for example 3289."),
    )

    parser.add_argument(
        "--variant",
        type=str,
        default=None,
        metavar="VARIANT_SLUG",
        help=(
            "Process one variant slug, for "
            "example 'maruti-brezza-lxi'. "
            "This option requires --brand "
            "and --model."
        ),
    )

    parser.add_argument(
        "--variant-id",
        type=int,
        default=None,
        metavar="VARIANT_ID",
        help=("Process one Cardekho variant ID, for example 10387."),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        metavar="COUNT",
        help=("Number of concurrent variant workers. Default: 5"),
    )

    parser.add_argument(
        "--requests-per-second",
        type=float,
        default=2.0,
        metavar="RPS",
        help=(
            "Maximum global HTTP request starts "
            "per second across all workers. "
            "Default: 2"
        ),
    )

    parser.add_argument(
        "--max-jobs",
        type=int,
        default=None,
        metavar="COUNT",
        help=("Optional maximum number of variants to process."),
    )

    parser.add_argument(
        "--pause-every-requests",
        type=int,
        default=0,
        metavar="COUNT",
        help=(
            "Pause and reset HTTP connections "
            "after this many request starts. "
            "Use 0 to disable. Must be used "
            "with --pause-seconds. Default: 0"
        ),
    )

    parser.add_argument(
        "--pause-seconds",
        type=float,
        default=0.0,
        metavar="SECONDS",
        help=(
            "Scheduled pause duration in "
            "seconds. Use 0 to disable. Must "
            "be used with "
            "--pause-every-requests. Default: 0"
        ),
    )

    parser.add_argument(
        "--refresh-existing",
        action="store_true",
        help=(
            "Fetch and update variants that "
            "already exist in "
            "cardekho_trim_specs_features. "
            "By default, existing variants "
            "are skipped."
        ),
    )

    parser.add_argument(
        "--resume-run-id",
        type=str,
        default=None,
        metavar="RUN_ID",
        help=("Resume an existing Cardekho trim specs/features scraper run."),
    )

    parser.add_argument(
        "--failed-only",
        action="store_true",
        help=("When resuming, process only failed jobs. Requires --resume-run-id."),
    )

    parser.add_argument(
        "--retry-terminal-failures",
        action="store_true",
        help=(
            "When resuming, retry failed jobs "
            "even when they are non-retryable "
            "or have reached max attempts. "
            "Requires --resume-run-id."
        ),
    )

    parser.add_argument(
        "--stale-after-seconds",
        type=float,
        default=300.0,
        metavar="SECONDS",
        help=(
            "When resuming, requeue running jobs "
            "whose heartbeat is older than this "
            "value. Default: 300"
        ),
    )

    parser.set_defaults(
        handler=(_handle_cardekho_trim_specs_features),
    )
