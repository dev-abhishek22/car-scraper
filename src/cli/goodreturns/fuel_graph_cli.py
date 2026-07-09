from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from src.commands.goodreturns_fuel_graph_prices import (
    run_goodreturns_fuel_graph_prices,
)


DEFAULT_GOODRETURNS_CITIES_JSON_PATH = "data/raw/goodreturns_fuel_cities.json"


def _handle_goodreturns_fuel_graph_prices(
    args: argparse.Namespace,
) -> int:
    fuel_types = tuple(
        fuel_type.strip().lower()
        for fuel_type in args.fuel_types.split(",")
        if fuel_type.strip()
    )

    result = asyncio.run(
        run_goodreturns_fuel_graph_prices(
            cities_json_path=args.cities_json,
            fuel_types=fuel_types,
            timeframe=args.timeframe,
            token=args.token,
            workers=args.workers,
            requests_per_second=args.requests_per_second,
            batch_size=args.batch_size,
            retries=args.retries,
            city=args.city,
            limit=args.limit,
            refresh_existing=args.refresh_existing,
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

    failed_prices = result.get(
        "failedPrices",
        0,
    )

    if (
        isinstance(failed_prices, int)
        and not isinstance(
            failed_prices,
            bool,
        )
        and failed_prices > 0
    ):
        return 1

    return 0


def add_goodreturns_fuel_graph_prices_command(
    *,
    subparsers: Any,
) -> None:
    parser = subparsers.add_parser(
        "goodreturns-fuel-graph-prices",
        help=("Fetch Goodreturns petrol, diesel and CNG graph prices"),
        description=(
            "Read Goodreturns city JSON from data/raw/goodreturns_fuel_cities.json "
            "by default, generate city slug based fuel graph API jobs, fetch fuel "
            "graph data for petrol, diesel and CNG, store successful responses in "
            "MongoDB, track jobs through scraper_runs and scraper_jobs, and resume "
            "by skipping already scraped city-fuel-timeframe records."
        ),
    )

    parser.add_argument(
        "--cities-json",
        type=str,
        default=DEFAULT_GOODRETURNS_CITIES_JSON_PATH,
        metavar="PATH",
        help=(
            "Path to Goodreturns cities JSON file. "
            f"Default: {DEFAULT_GOODRETURNS_CITIES_JSON_PATH}"
        ),
    )

    parser.add_argument(
        "--fuel-types",
        type=str,
        default="petrol,diesel,cng",
        metavar="TYPES",
        help=("Comma-separated fuel types. Default: petrol,diesel,cng"),
    )

    parser.add_argument(
        "--timeframe",
        type=str,
        default="1M",
        metavar="TIMEFRAME",
        help=("Graph timeframe. Allowed: 1M, 3M, 6M, 1Y. Default: 1M"),
    )

    parser.add_argument(
        "--token",
        type=str,
        default=None,
        metavar="TOKEN",
        help=("Goodreturns fuel API JWT token. Can also use GOODRETURNS_TOKEN env."),
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=3,
        metavar="COUNT",
        help=("Number of concurrent workers. Default: 3"),
    )

    parser.add_argument(
        "--requests-per-second",
        type=float,
        default=2.0,
        metavar="RPS",
        help=("Maximum global HTTP request starts per second. Default: 2"),
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        metavar="COUNT",
        help=("Mongo write batch size. Default: 50"),
    )

    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        metavar="COUNT",
        help=("Retry count per city-fuel job. Default: 2"),
    )

    parser.add_argument(
        "--city",
        type=str,
        default=None,
        metavar="CITY_SLUG",
        help=("Process one city slug, for example 'mumbai'."),
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="COUNT",
        help=("Limit number of generated city-fuel jobs."),
    )

    parser.add_argument(
        "--refresh-existing",
        action="store_true",
        help=(
            "Scrape records again even if they already exist in MongoDB. "
            "By default, existing records are skipped for safe resume."
        ),
    )

    parser.set_defaults(
        handler=_handle_goodreturns_fuel_graph_prices,
    )
