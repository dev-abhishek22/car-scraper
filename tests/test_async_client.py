from __future__ import annotations

import asyncio

import httpx
import pytest

from src.clients.async_client import AsyncExternalHttpClient


@pytest.mark.asyncio
async def test_retries_temporary_response_and_returns_json() -> None:
    attempt = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempt
        attempt += 1

        if attempt == 1:
            return httpx.Response(
                503,
                json={"error": "temporary"},
            )

        return httpx.Response(
            200,
            json={"ok": True},
        )

    client = AsyncExternalHttpClient(
        base_url="https://example.com",
        concurrency=2,
        requests_per_second=100,
        max_retries=1,
        max_connections=2,
        max_keepalive_connections=2,
        transport=httpx.MockTransport(handler),
    )

    try:
        result = await client.get_json("/resource")
    finally:
        await client.aclose()

    assert result == {"ok": True}
    assert attempt == 2
    assert client.metrics_snapshot()["retries"] == 1


@pytest.mark.asyncio
async def test_never_exceeds_configured_concurrency() -> None:
    active_requests = 0
    maximum_active_requests = 0
    counter_lock = asyncio.Lock()

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal active_requests
        nonlocal maximum_active_requests

        async with counter_lock:
            active_requests += 1
            maximum_active_requests = max(
                maximum_active_requests,
                active_requests,
            )

        await asyncio.sleep(0.03)

        async with counter_lock:
            active_requests -= 1

        return httpx.Response(
            200,
            json={"ok": True},
        )

    client = AsyncExternalHttpClient(
        base_url="https://example.com",
        concurrency=3,
        requests_per_second=0,
        max_retries=0,
        max_connections=3,
        max_keepalive_connections=3,
        transport=httpx.MockTransport(handler),
    )

    try:
        await asyncio.gather(*(client.get_json("/resource") for _ in range(12)))
    finally:
        await client.aclose()

    assert maximum_active_requests == 3
