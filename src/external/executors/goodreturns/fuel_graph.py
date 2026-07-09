from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from src.clients.async_client import (
    AsyncExternalHttpClient,
)
from src.clients.client import (
    ExternalResponseError,
)
from src.external.constants.goodreturns import (
    GOODRETURNS_BASE_URL,
    GOODRETURNS_DEFAULT_HEADERS,
    GOODRETURNS_FUEL_GRAPH_PATH,
)
from user_agents import choose_user_agent


class GoodReturnsFuelGraphExecutor:
    def __init__(
        self,
        *,
        requests_per_second: float = 2.0,
    ) -> None:
        if (
            isinstance(requests_per_second, bool)
            or not isinstance(
                requests_per_second,
                (int, float),
            )
            or requests_per_second <= 0
        ):
            raise ValueError("requests_per_second must be greater than zero")

        self.requests_per_second = float(requests_per_second)

    def build_referer_url(
        self,
        *,
        fuel_type: str,
        city_slug: str,
    ) -> str:
        normalized_fuel_type = self._validate_non_empty_string(
            fuel_type,
            field_name="fuel_type",
        ).lower()

        normalized_city_slug = self._validate_non_empty_string(
            city_slug,
            field_name="city_slug",
        ).lower()

        return (
            f"{GOODRETURNS_BASE_URL}/"
            f"{normalized_fuel_type}-price-in-{normalized_city_slug}.html"
        )

    @staticmethod
    def _validate_non_empty_string(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError(f"{field_name} must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        return normalized_value

    @staticmethod
    def _validate_token(
        value: Any,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError("token must be a string")

        normalized_token = value.strip()

        if not normalized_token:
            raise ValueError("token cannot be empty")

        return normalized_token

    @asynccontextmanager
    async def create_client(
        self,
        *,
        concurrency: int,
    ) -> AsyncIterator[AsyncExternalHttpClient]:
        if (
            isinstance(concurrency, bool)
            or not isinstance(
                concurrency,
                int,
            )
            or concurrency < 1
        ):
            raise ValueError("concurrency must be at least 1")

        if concurrency > 1000:
            raise ValueError("concurrency cannot exceed 1000")

        user_agent = choose_user_agent(
            category="CHROME_USER_AGENTS",
        )

        max_connections = max(
            concurrency * 2,
            20,
        )

        max_keepalive_connections = max(
            concurrency,
            20,
        )

        async with AsyncExternalHttpClient(
            base_url=GOODRETURNS_BASE_URL,
            user_agent=user_agent,
            default_headers=GOODRETURNS_DEFAULT_HEADERS,
            concurrency=concurrency,
            requests_per_second=self.requests_per_second,
            pause_every_requests=0,
            pause_seconds=0.0,
            max_retries=0,
            connect_timeout=10.0,
            read_timeout=45.0,
            write_timeout=30.0,
            pool_timeout=10.0,
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=30.0,
            follow_redirects=True,
            verify_ssl=True,
            trust_environment=False,
            http2=False,
            log_successful_requests=False,
        ) as client:
            yield client

    async def fetch_graph_data(
        self,
        *,
        client: AsyncExternalHttpClient,
        token: str,
        city_slug: str,
        fuel_type: str,
        timeframe: str,
    ) -> tuple[int, Any]:
        normalized_token = self._validate_token(token)

        normalized_city_slug = self._validate_non_empty_string(
            city_slug,
            field_name="city_slug",
        ).lower()

        normalized_fuel_type = self._validate_non_empty_string(
            fuel_type,
            field_name="fuel_type",
        ).lower()

        normalized_timeframe = self._validate_non_empty_string(
            timeframe,
            field_name="timeframe",
        )

        response_data = await client.get_json(
            endpoint=GOODRETURNS_FUEL_GRAPH_PATH,
            params={
                "token": normalized_token,
                "city": normalized_city_slug,
                "fuel_type": normalized_fuel_type,
                "timeframe": normalized_timeframe,
            },
            headers={
                "authorization": f"Bearer {normalized_token}",
                "referer": self.build_referer_url(
                    fuel_type=normalized_fuel_type,
                    city_slug=normalized_city_slug,
                ),
            },
        )

        if not isinstance(
            response_data,
            (
                list,
                dict,
            ),
        ):
            raise ExternalResponseError(
                "Goodreturns fuel graph API returned an invalid response. "
                "Expected a JSON array or object: "
                f"city={normalized_city_slug!r}, "
                f"fuel_type={normalized_fuel_type!r}, "
                f"timeframe={normalized_timeframe!r}"
            )

        return 200, response_data
