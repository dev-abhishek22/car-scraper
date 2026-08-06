from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.bikedekho_scooter_models import run_bikedekho_scooter_models


def _handle_bikedekho_scooter_models(args: argparse.Namespace) -> int:
    result = asyncio.run(
        run_bikedekho_scooter_models(
            brand=args.brand,
            workers=args.workers,
            requests_per_second=args.requests_per_second,
            pause_every_requests=args.pause_every_requests,
            pause_seconds=args.pause_seconds,
        )
    )
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return int(result.get("failedBrands", 0) > 0)


def add_bikedekho_scooter_models_command(*, subparsers: Any) -> None:
    parser = subparsers.add_parser(
        "bikedekho-scooter-models",
        help="Fetch BikeDekho scooter models using stored scooter brands",
    )
    parser.add_argument("--brand", type=str, default=None, metavar="SLUG")
    parser.add_argument("--workers", type=int, default=1, metavar="COUNT")
    parser.add_argument("--requests-per-second", type=float, default=5.0, metavar="RPS")
    parser.add_argument("--pause-every-requests", type=int, default=0, metavar="COUNT")
    parser.add_argument("--pause-seconds", type=float, default=0.0, metavar="SECONDS")
    parser.set_defaults(handler=_handle_bikedekho_scooter_models)
