from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence

from src.cli.cardekho.brand_cli import (
    add_cardekho_brands_command,
)
from src.cli.cardekho.car_cli import (
    add_cardekho_cars_command,
)
from src.cli.cardekho.cities_cli import (
    add_cardekho_cities_command,
)
from src.cli.cardekho.city_price_cli import (
    add_cardekho_city_prices_command,
)
from src.cli.cardekho.model_cli import (
    add_cardekho_models_command,
)
from src.cli.cardekho.trim_specs_features_cli import (
    add_cardekho_trim_specs_features_command,
)
from src.cli.bikedekho.brand_cli import (
    add_bikedekho_brands_command,
)
from src.cli.bikedekho.model_cli import (
    add_bikedekho_models_command,
)
from src.cli.bikedekho.bike_cli import (
    add_bikedekho_bikes_command,
)
from src.cli.bikedekho.trim_specs_features_cli import (
    add_bikedekho_trim_specs_features_command,
)
from src.cli.bikedekho.scooter_brand_cli import (
    add_bikedekho_scooter_brands_command,
)
from src.cli.bikedekho.scooter_model_cli import (
    add_bikedekho_scooter_models_command,
)
from src.cli.bikedekho.scooters_cli import (
    add_bikedekho_scooters_command,
)
from src.cli.carwale.brand_cli import (
    add_carwale_brands_command,
)
from src.cli.carwale.car_cli import (
    add_carwale_cars_command,
)
from src.cli.carwale.cities_cli import (
    add_carwale_cities_command,
)
from src.cli.carwale.city_price_cli import (
    add_carwale_city_prices_command,
)
from src.cli.carwale.model_cli import (
    add_carwale_models_command,
)
from src.cli.carwale.trim_specs_features_cli import (
    add_carwale_trim_specs_features_command,
)
from src.cli.cleanup_cli import (
    add_cleanup_command,
)
from src.cli.mongodb_cli import (
    add_mongodb_indexes_command,
)
from src.cli.goodreturns.fuel_graph_cli import (
    add_goodreturns_fuel_graph_prices_command,
)

CommandHandler = Callable[
    [argparse.Namespace],
    int,
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="car-scraper",
        description="Car website scraping CLI",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="available commands",
        metavar="COMMAND",
    )

    add_cleanup_command(
        subparsers=subparsers,
    )

    add_mongodb_indexes_command(
        subparsers=subparsers,
    )

    add_carwale_brands_command(
        subparsers=subparsers,
    )

    add_carwale_models_command(
        subparsers=subparsers,
    )

    add_carwale_cars_command(
        subparsers=subparsers,
    )

    add_carwale_cities_command(
        subparsers=subparsers,
    )

    add_carwale_city_prices_command(
        subparsers=subparsers,
    )

    add_carwale_trim_specs_features_command(
        subparsers=subparsers,
    )

    add_cardekho_brands_command(
        subparsers=subparsers,
    )

    add_bikedekho_brands_command(
        subparsers=subparsers,
    )

    add_bikedekho_scooter_brands_command(
        subparsers=subparsers,
    )

    add_bikedekho_scooter_models_command(
        subparsers=subparsers,
    )

    add_bikedekho_scooters_command(
        subparsers=subparsers,
    )

    add_bikedekho_models_command(
        subparsers=subparsers,
    )

    add_bikedekho_bikes_command(
        subparsers=subparsers,
    )

    add_bikedekho_trim_specs_features_command(
        subparsers=subparsers,
    )

    add_cardekho_models_command(
        subparsers=subparsers,
    )

    add_cardekho_cars_command(
        subparsers=subparsers,
    )

    add_cardekho_cities_command(
        subparsers=subparsers,
    )

    add_cardekho_city_prices_command(
        subparsers=subparsers,
    )

    add_cardekho_trim_specs_features_command(
        subparsers=subparsers,
    )

    add_goodreturns_fuel_graph_prices_command(
        subparsers=subparsers,
    )

    return parser


def main(
    argv: Sequence[str] | None = None,
) -> int:
    parser = build_parser()

    arguments = list(argv if argv is not None else sys.argv[1:])

    if not arguments:
        parser.print_help()
        return 0

    args = parser.parse_args(arguments)

    handler: CommandHandler | None = getattr(
        args,
        "handler",
        None,
    )

    if handler is None:
        parser.print_help()
        return 0

    try:
        return handler(args)

    except KeyboardInterrupt:
        print(
            "\nCommand interrupted.",
            file=sys.stderr,
        )

        return 130

    except Exception as error:
        print(
            f"Command failed: {error}",
            file=sys.stderr,
        )

        return 1
