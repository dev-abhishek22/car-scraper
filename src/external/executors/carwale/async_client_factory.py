from __future__ import annotations

from src.clients.async_client import AsyncExternalHttpClient
from src.external.constants.carwale import (
    CARWALE_BASE_URL,
    CARWALE_DEFAULT_HEADERS,
)
from user_agents import choose_user_agent


def create_carwale_async_client(
    *,
    concurrency: int = 20,
    requests_per_second: float = 10.0,
) -> AsyncExternalHttpClient:
    if concurrency < 1:
        raise ValueError("concurrency must be at least 1")

    if concurrency > 1000:
        raise ValueError("concurrency cannot exceed 1000")

    if requests_per_second <= 0:
        raise ValueError("requests_per_second must be greater than zero")

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

    return AsyncExternalHttpClient(
        base_url=CARWALE_BASE_URL,
        user_agent=user_agent,
        default_headers=CARWALE_DEFAULT_HEADERS,
        concurrency=concurrency,
        requests_per_second=requests_per_second,
        max_retries=3,
        connect_timeout=10.0,
        read_timeout=45.0,
        write_timeout=30.0,
        pool_timeout=10.0,
        max_connections=max_connections,
        max_keepalive_connections=(max_keepalive_connections),
        keepalive_expiry=30.0,
        follow_redirects=True,
        verify_ssl=True,
        trust_environment=False,
        http2=False,
        log_successful_requests=False,
    )
