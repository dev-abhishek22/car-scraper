from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from src.clients.client import (
    ExternalHttpClient,
    ExternalResponseError,
)
from src.external.constants.carwale import (
    CARWALE_CITIES,
)
from src.logger.logger import logger_service


def scrape_carwale_cities(
    *,
    client: ExternalHttpClient,
    show_request: bool = False,
    request_log_file: str | Path | None = None,
) -> list[dict[str, Any]]:
    """
    Fetch and validate all cities from CarWale.

    This executor only handles:

    - Calling the CarWale cities API
    - Validating the response
    - Returning the raw city records

    Saving files and creating the final payload
    belong to the command layer.
    """

    endpoint = CARWALE_CITIES

    logger_service.info(
        "Scraping CarWale cities",
        context="CarWaleCitiesExecutor",
    )

    response_data = client.get_json(
        endpoint=endpoint.path,
        params={
            **endpoint.default_params,
        },
        headers={
            **endpoint.default_headers,
        },
        show_request=show_request,
        request_log_file=(
            Path(request_log_file) if request_log_file is not None else None
        ),
    )

    if not isinstance(response_data, list):
        raise ExternalResponseError(
            "CarWale cities API returned an invalid response. Expected a JSON array."
        )

    cities: list[dict[str, Any]] = []

    for index, city in enumerate(response_data):
        if not isinstance(city, Mapping):
            raise ExternalResponseError(
                "CarWale cities API returned an invalid "
                "city record. Expected a JSON object: "
                f"index={index}"
            )

        cities.append(dict(city))

    logger_service.info(
        (f"CarWale cities scraped successfully: total_cities={len(cities)}"),
        context="CarWaleCitiesExecutor",
    )

    return cities
