from __future__ import annotations

from src.clients.client import ExternalHttpClient
from src.external.constants.carwale import (
    CARWALE_BASE_URL,
    CARWALE_DEFAULT_HEADERS,
)
from user_agents import choose_user_agent


def create_carwale_client(
    *,
    workers: int = 1,
    min_request_interval: float = 2.0,
) -> ExternalHttpClient:
    if workers < 1:
        raise ValueError("workers must be at least 1")

    if workers > 8:
        raise ValueError("workers cannot exceed 8")

    user_agent = choose_user_agent(
        category="CHROME_USER_AGENTS",
    )

    max_connections = max(
        workers,
        4,
    )

    return ExternalHttpClient(
        base_url=CARWALE_BASE_URL,
        user_agent=user_agent,
        default_headers=CARWALE_DEFAULT_HEADERS,
        cookies={
            "CurrentLanguage": "en",
        },
        min_request_interval=min_request_interval,
        max_retries=3,
        connect_timeout=10.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=10.0,
        max_connections=max_connections,
        max_keepalive_connections=max_connections,
        keepalive_expiry=30.0,
        follow_redirects=True,
        verify_ssl=True,
        trust_environment=False,
    )
