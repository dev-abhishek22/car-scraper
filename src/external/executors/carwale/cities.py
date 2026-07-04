from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from src.clients.client import (
    ExternalHttpClient,
    ExternalResponseError,
)
from src.external.constants.carwale import (
    CARWALE_BASE_URL,
    CARWALE_CITIES,
    CARWALE_DEFAULT_HEADERS,
)
from src.logger.logger import logger_service

CITY_REQUEST_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/144.0.0.0 Safari/537.36"
)


def _city_request_headers() -> dict[str, str]:
    return {
        **CARWALE_DEFAULT_HEADERS,
        **CARWALE_CITIES.default_headers,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-IN,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": f"{CARWALE_BASE_URL}/",
        "ServerDomain": "CarWale",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": CITY_REQUEST_USER_AGENT,
    }


def _warm_up_carwale_session(
    *,
    client: ExternalHttpClient,
) -> None:
    """
    Open the CarWale home page once so the HTTP session can
    receive any cookies required by the cities API.
    """

    client.get(
        endpoint="/",
        headers={
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/avif,"
                "image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "en-IN,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": f"{CARWALE_BASE_URL}/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": CITY_REQUEST_USER_AGENT,
        },
    )


def scrape_carwale_cities(
    *,
    client: ExternalHttpClient,
    show_request: bool = False,
    request_log_file: str | Path | None = None,
) -> list[dict[str, Any]]:
    """
    Fetch and validate every city returned by CarWale.

    Duplicate city IDs are ignored after the first
    occurrence.
    """

    endpoint = CARWALE_CITIES

    if endpoint.method != "GET":
        raise RuntimeError(
            "Unexpected HTTP method configured for the CarWale cities API"
        )

    logger_service.info(
        "Scraping CarWale cities",
        context="CarWaleCitiesExecutor",
    )

    _warm_up_carwale_session(
        client=client,
    )

    response_data = client.get_json(
        endpoint=endpoint.path,
        params={
            **endpoint.default_params,
        },
        headers=_city_request_headers(),
        show_request=show_request,
        request_log_file=(
            Path(request_log_file) if request_log_file is not None else None
        ),
    )

    if not isinstance(
        response_data,
        list,
    ):
        raise ExternalResponseError(
            "CarWale cities API returned an invalid response. Expected a JSON array."
        )

    cities: list[dict[str, Any]] = []

    seen_city_ids: set[int] = set()

    duplicate_cities = 0

    for index, raw_city in enumerate(response_data):
        if not isinstance(
            raw_city,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarWale cities API returned an "
                "invalid city record: "
                f"index={index}, "
                f"type={type(raw_city).__name__}"
            )

        city_id = raw_city.get("CityId")

        if isinstance(city_id, bool) or not isinstance(city_id, int) or city_id <= 0:
            raise ExternalResponseError(
                "CarWale city contains an invalid "
                "CityId: "
                f"index={index}, "
                f"value={city_id!r}"
            )

        if city_id in seen_city_ids:
            duplicate_cities += 1
            continue

        seen_city_ids.add(city_id)

        cities.append(dict(raw_city))

    logger_service.info(
        (
            "CarWale cities scraped successfully: "
            f"total_cities={len(cities)}, "
            f"duplicates_ignored={duplicate_cities}"
        ),
        context="CarWaleCitiesExecutor",
    )

    return cities
