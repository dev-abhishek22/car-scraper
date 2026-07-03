from __future__ import annotations

import asyncio
import math
import random
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import httpx

from src.clients.client import (
    ExternalAccessDeniedError,
    ExternalClientError,
    ExternalJsonDecodeError,
    ExternalRateLimitError,
    ExternalResponseError,
)
from src.logger.logger import logger_service


@dataclass(slots=True)
class AsyncClientMetrics:
    """In-memory metrics for one async client session."""

    started_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    cancelled_requests: int = 0
    total_attempts: int = 0
    retries: int = 0
    rate_limited_responses: int = 0
    access_denied_responses: int = 0
    access_denied_circuit_trips: int = 0
    access_denied_circuit_rejections: int = 0
    access_denied_cooldowns: int = 0
    access_denied_cooldown_seconds: float = 0.0
    scheduled_pauses: int = 0
    scheduled_pause_seconds: float = 0.0
    scheduled_connection_resets: int = 0
    network_errors: int = 0
    json_decode_errors: int = 0
    total_attempt_duration_seconds: float = 0.0
    status_counts: dict[int, int] = field(default_factory=dict)

    def record_status(self, status_code: int) -> None:
        self.status_counts[status_code] = self.status_counts.get(status_code, 0) + 1

    def snapshot(self) -> dict[str, Any]:
        average_attempt_duration = 0.0

        if self.total_attempts:
            average_attempt_duration = (
                self.total_attempt_duration_seconds / self.total_attempts
            )

        return {
            "started_requests": self.started_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "cancelled_requests": self.cancelled_requests,
            "total_attempts": self.total_attempts,
            "retries": self.retries,
            "rate_limited_responses": self.rate_limited_responses,
            "access_denied_responses": self.access_denied_responses,
            "access_denied_circuit_trips": (self.access_denied_circuit_trips),
            "access_denied_circuit_rejections": (self.access_denied_circuit_rejections),
            "access_denied_cooldowns": self.access_denied_cooldowns,
            "access_denied_cooldown_seconds": round(
                self.access_denied_cooldown_seconds,
                2,
            ),
            "scheduled_pauses": self.scheduled_pauses,
            "scheduled_pause_seconds": round(
                self.scheduled_pause_seconds,
                2,
            ),
            "scheduled_connection_resets": (self.scheduled_connection_resets),
            "network_errors": self.network_errors,
            "json_decode_errors": self.json_decode_errors,
            "average_attempt_duration_seconds": round(
                average_attempt_duration,
                4,
            ),
            "status_counts": dict(sorted(self.status_counts.items())),
        }


class AsyncExternalHttpClient:
    """
    Reusable asynchronous HTTP client for high-volume external requests.

    The same instance is intended to be shared by many asyncio tasks.

    Concurrency limits the number of in-flight attempts. Request-rate pacing
    limits how frequently attempts may begin across all tasks sharing this
    client. Retries do not bypass either limit.
    """

    RETRYABLE_STATUS_CODES = {
        408,
        425,
        429,
        500,
        502,
        503,
        504,
    }

    ACCESS_DENIED_STATUS_CODES = {
        401,
        403,
    }

    RETRYABLE_REQUEST_EXCEPTIONS = (
        httpx.TimeoutException,
        httpx.NetworkError,
        httpx.RemoteProtocolError,
    )

    def __init__(
        self,
        *,
        base_url: str,
        default_headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        user_agent: str | None = None,
        user_agents: Sequence[str] | None = None,
        concurrency: int = 20,
        requests_per_second: float = 10.0,
        pause_every_requests: int = 0,
        pause_seconds: float = 0.0,
        access_denied_cooldown_seconds: float = 300.0,
        max_retries: int = 3,
        connect_timeout: float = 10.0,
        read_timeout: float = 30.0,
        write_timeout: float = 30.0,
        pool_timeout: float = 10.0,
        max_connections: int = 40,
        max_keepalive_connections: int = 40,
        keepalive_expiry: float = 30.0,
        follow_redirects: bool = True,
        verify_ssl: bool = True,
        trust_environment: bool = False,
        http2: bool = False,
        log_successful_requests: bool = False,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        normalized_base_url = self._normalize_base_url(base_url)

        self._validate_configuration(
            user_agent=user_agent,
            user_agents=user_agents,
            concurrency=concurrency,
            requests_per_second=requests_per_second,
            pause_every_requests=pause_every_requests,
            pause_seconds=pause_seconds,
            access_denied_cooldown_seconds=access_denied_cooldown_seconds,
            max_retries=max_retries,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            write_timeout=write_timeout,
            pool_timeout=pool_timeout,
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=keepalive_expiry,
        )

        self.base_url = normalized_base_url
        self.concurrency = concurrency
        self.requests_per_second = float(requests_per_second)
        self.pause_every_requests = pause_every_requests
        self.pause_seconds = float(pause_seconds)
        self.access_denied_cooldown_seconds = float(access_denied_cooldown_seconds)
        self.max_retries = max_retries
        self.log_successful_requests = log_successful_requests

        self._concurrency_semaphore = asyncio.Semaphore(concurrency)

        # Coordinates global request-start pacing and Retry-After cooldowns.
        self._rate_condition = asyncio.Condition()
        self._last_request_started_at: float | None = None
        self._blocked_until = 0.0
        self._request_starts_since_pause = 0
        self._scheduled_pause_in_progress = False
        self._in_flight_attempts = 0

        # A 401/403 starts one shared cooldown for every worker. The Python
        # process, pipeline, MongoDB connection, and HTTP pool remain alive.
        # After the cooldown, all affected logical requests retry automatically.
        self._access_denied_event = asyncio.Event()
        self._access_denied_status: int | None = None
        self._access_denied_url: str | None = None
        self._access_denied_cooldown_task: asyncio.Task[None] | None = None

        # Protects header/cookie mutations and request preparation.
        self._client_configuration_lock = asyncio.Lock()

        # Tracks lifecycle so aclose() can wait for active logical requests.
        self._lifecycle_condition = asyncio.Condition()
        self._close_lock = asyncio.Lock()
        self._close_event = asyncio.Event()
        self._active_requests = 0
        self._closed = False
        self._client_closed = False

        self._metrics = AsyncClientMetrics()

        selected_user_agent = self._select_user_agent(
            user_agent=user_agent,
            user_agents=user_agents,
        )

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-IN,en;q=0.9",
            "User-Agent": selected_user_agent,
        }

        if default_headers:
            headers.update(dict(default_headers))

        # Store the HTTP-client configuration so the connection pool can be
        # completely closed during a scheduled pause and rebuilt afterward.
        # Only explicitly configured cookies are restored; cookies learned
        # from responses in the previous HTTP session are intentionally reset.
        self._configured_headers = headers
        self._configured_cookies = dict(cookies or {})
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._write_timeout = write_timeout
        self._pool_timeout = pool_timeout
        self._max_connections = max_connections
        self._max_keepalive_connections = max_keepalive_connections
        self._keepalive_expiry = keepalive_expiry
        self._follow_redirects = follow_redirects
        self._verify_ssl = verify_ssl
        self._trust_environment = trust_environment
        self._http2 = http2
        self._provided_transport = transport
        self._http_client_generation = 0

        self.client = self._create_http_client()

        logger_service.info(
            (
                "Async external HTTP client initialized: "
                f"base_url={self.base_url}, "
                f"user_agent={selected_user_agent}, "
                f"concurrency={self.concurrency}, "
                "requests_per_second="
                f"{self.requests_per_second:.2f}, "
                "pause_every_requests="
                f"{self.pause_every_requests}, "
                "pause_seconds="
                f"{self.pause_seconds:.2f}, "
                "access_denied_cooldown_seconds="
                f"{self.access_denied_cooldown_seconds:.2f}, "
                f"max_connections={max_connections}, "
                "max_keepalive_connections="
                f"{max_keepalive_connections}, "
                f"http2={http2}"
            ),
            context=self.__class__.__name__,
        )

    def _create_http_transport(self) -> httpx.AsyncBaseTransport:
        # A caller-supplied transport is used only for the initial client.
        # Reconnected production sessions need a new transport because closing
        # an AsyncClient also closes its transport and connection pool.
        if self._provided_transport is not None and self._http_client_generation == 0:
            return self._provided_transport

        limits = httpx.Limits(
            max_connections=self._max_connections,
            max_keepalive_connections=(self._max_keepalive_connections),
            keepalive_expiry=self._keepalive_expiry,
        )

        # Retry ownership stays in this class. Transport retries remain
        # disabled so attempts and metrics are never hidden from us.
        return httpx.AsyncHTTPTransport(
            retries=0,
            verify=self._verify_ssl,
            trust_env=self._trust_environment,
            http1=True,
            http2=self._http2,
            limits=limits,
        )

    def _create_http_client(self) -> httpx.AsyncClient:
        timeout = httpx.Timeout(
            connect=self._connect_timeout,
            read=self._read_timeout,
            write=self._write_timeout,
            pool=self._pool_timeout,
        )

        client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=dict(self._configured_headers),
            cookies=dict(self._configured_cookies),
            timeout=timeout,
            transport=self._create_http_transport(),
            follow_redirects=self._follow_redirects,
            trust_env=self._trust_environment,
        )

        self._http_client_generation += 1
        return client

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        if not isinstance(base_url, str):
            raise ValueError("base_url must be a string")

        normalized_base_url = base_url.strip().rstrip("/")

        if not normalized_base_url:
            raise ValueError("base_url cannot be empty")

        try:
            parsed_url = httpx.URL(normalized_base_url)
        except Exception as error:
            raise ValueError("base_url is not a valid URL") from error

        if parsed_url.scheme not in {"http", "https"}:
            raise ValueError("base_url must begin with http:// or https://")

        if not parsed_url.host:
            raise ValueError("base_url must include a host")

        return normalized_base_url

    @staticmethod
    def _validate_positive_number(
        *,
        name: str,
        value: float,
        allow_zero: bool = False,
    ) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number")

        numeric_value = float(value)

        if not math.isfinite(numeric_value):
            raise ValueError(f"{name} must be finite")

        if allow_zero:
            if numeric_value < 0:
                raise ValueError(f"{name} cannot be negative")
        elif numeric_value <= 0:
            raise ValueError(f"{name} must be greater than zero")

    @classmethod
    def _validate_configuration(
        cls,
        *,
        user_agent: str | None,
        user_agents: Sequence[str] | None,
        concurrency: int,
        requests_per_second: float,
        pause_every_requests: int,
        pause_seconds: float,
        access_denied_cooldown_seconds: float,
        max_retries: int,
        connect_timeout: float,
        read_timeout: float,
        write_timeout: float,
        pool_timeout: float,
        max_connections: int,
        max_keepalive_connections: int,
        keepalive_expiry: float,
    ) -> None:
        if user_agent and user_agents:
            raise ValueError("Provide either user_agent or user_agents, not both")

        if isinstance(user_agents, str):
            raise ValueError(
                "user_agents must be a sequence of strings, not one string"
            )

        if isinstance(concurrency, bool) or not isinstance(concurrency, int):
            raise ValueError("concurrency must be an integer")

        if concurrency < 1:
            raise ValueError("concurrency must be at least 1")

        cls._validate_positive_number(
            name="requests_per_second",
            value=requests_per_second,
            allow_zero=True,
        )

        if isinstance(pause_every_requests, bool) or not isinstance(
            pause_every_requests, int
        ):
            raise ValueError("pause_every_requests must be an integer")

        if pause_every_requests < 0:
            raise ValueError("pause_every_requests cannot be negative")

        cls._validate_positive_number(
            name="pause_seconds",
            value=pause_seconds,
            allow_zero=True,
        )

        if (pause_every_requests > 0) != (pause_seconds > 0):
            raise ValueError(
                "pause_every_requests and pause_seconds must "
                "both be greater than zero or both be zero"
            )

        cls._validate_positive_number(
            name="access_denied_cooldown_seconds",
            value=access_denied_cooldown_seconds,
        )

        if isinstance(max_retries, bool) or not isinstance(max_retries, int):
            raise ValueError("max_retries must be an integer")

        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")

        for timeout_name, timeout_value in (
            ("connect_timeout", connect_timeout),
            ("read_timeout", read_timeout),
            ("write_timeout", write_timeout),
            ("pool_timeout", pool_timeout),
        ):
            cls._validate_positive_number(
                name=timeout_name,
                value=timeout_value,
            )

        if isinstance(max_connections, bool) or not isinstance(
            max_connections,
            int,
        ):
            raise ValueError("max_connections must be an integer")

        if max_connections < concurrency:
            raise ValueError("max_connections cannot be lower than concurrency")

        if isinstance(max_keepalive_connections, bool) or not isinstance(
            max_keepalive_connections,
            int,
        ):
            raise ValueError("max_keepalive_connections must be an integer")

        if max_keepalive_connections < 0:
            raise ValueError("max_keepalive_connections cannot be negative")

        if max_keepalive_connections > max_connections:
            raise ValueError("max_keepalive_connections cannot exceed max_connections")

        cls._validate_positive_number(
            name="keepalive_expiry",
            value=keepalive_expiry,
        )

    @classmethod
    def _select_user_agent(
        cls,
        *,
        user_agent: str | None,
        user_agents: Sequence[str] | None,
    ) -> str:
        if user_agent:
            return cls._validate_user_agent(user_agent)

        if user_agents:
            valid_user_agents: list[str] = []

            for value in user_agents:
                if not isinstance(value, str):
                    raise ValueError("Every user_agents item must be a string")

                if not value.strip():
                    continue

                valid_user_agents.append(cls._validate_user_agent(value))

            if not valid_user_agents:
                raise ValueError("user_agents does not contain a valid value")

            return random.SystemRandom().choice(valid_user_agents)

        return "AsyncExternalDataClient/1.0"

    @staticmethod
    def _validate_user_agent(user_agent: str) -> str:
        normalized_user_agent = user_agent.strip()

        if not normalized_user_agent:
            raise ValueError("User-Agent cannot be empty")

        if "\r" in normalized_user_agent or "\n" in normalized_user_agent:
            raise ValueError("User-Agent cannot contain line breaks")

        return normalized_user_agent

    async def _begin_request(self) -> None:
        async with self._lifecycle_condition:
            if self._closed:
                raise ExternalClientError("Async HTTP client is already closed")

            self._active_requests += 1

    async def _end_request(self) -> None:
        async with self._lifecycle_condition:
            self._active_requests -= 1
            self._lifecycle_condition.notify_all()

    async def _wait_for_access_denied_cooldown(self) -> None:
        """Wait for the currently active shared 401/403 cooldown."""

        while True:
            async with self._rate_condition:
                if self._closed:
                    raise ExternalClientError(
                        "Async HTTP client was closed during access-denied cooldown"
                    )

                if not self._access_denied_event.is_set():
                    return

                cooldown_task = self._access_denied_cooldown_task

                if cooldown_task is None:
                    await self._rate_condition.wait()
                    continue

            # Shielding prevents one cancelled worker from cancelling the
            # single global cooldown task used by every other worker.
            await asyncio.shield(cooldown_task)

    async def _run_access_denied_cooldown(
        self,
        *,
        cooldown_number: int,
        status_code: int,
        safe_url: str,
    ) -> None:
        logger_service.warning(
            (
                "External access denied; global HTTP cooldown started: "
                f"cooldown_number={cooldown_number}, "
                f"status={status_code}, url={safe_url}, "
                "duration_seconds="
                f"{self.access_denied_cooldown_seconds:.2f}, "
                "http_connections_closed=False, "
                "pipeline_and_mongodb_remain_active=True"
            ),
            context=self.__class__.__name__,
        )

        try:
            try:
                await asyncio.wait_for(
                    self._close_event.wait(),
                    timeout=self.access_denied_cooldown_seconds,
                )
            except TimeoutError:
                pass

            if not self._closed:
                logger_service.info(
                    (
                        "External access-denied cooldown completed: "
                        f"cooldown_number={cooldown_number}, "
                        "scraping_resumed_automatically=True"
                    ),
                    context=self.__class__.__name__,
                )

        finally:
            async with self._rate_condition:
                current_task = asyncio.current_task()

                if self._access_denied_cooldown_task is current_task:
                    self._access_denied_cooldown_task = None

                self._access_denied_event.clear()
                self._access_denied_status = None
                self._access_denied_url = None
                self._last_request_started_at = None
                self._rate_condition.notify_all()

    async def _start_access_denied_cooldown(
        self,
        response: httpx.Response,
    ) -> asyncio.Task[None]:
        status_code = response.status_code
        safe_url = self._safe_url(response.request.url)

        async with self._rate_condition:
            existing_task = self._access_denied_cooldown_task

            if existing_task is not None and not existing_task.done():
                return existing_task

            self._access_denied_status = status_code
            self._access_denied_url = safe_url
            self._access_denied_event.set()
            self._request_starts_since_pause = 0
            self._metrics.access_denied_circuit_trips += 1
            self._metrics.access_denied_cooldowns += 1
            self._metrics.access_denied_cooldown_seconds += (
                self.access_denied_cooldown_seconds
            )
            cooldown_number = self._metrics.access_denied_cooldowns

            cooldown_task = asyncio.create_task(
                self._run_access_denied_cooldown(
                    cooldown_number=cooldown_number,
                    status_code=status_code,
                    safe_url=safe_url,
                ),
                name=(f"external-access-denied-cooldown-{cooldown_number}"),
            )
            self._access_denied_cooldown_task = cooldown_task
            self._rate_condition.notify_all()
            return cooldown_task

    async def _perform_scheduled_connection_pause(
        self,
        *,
        pause_number: int,
    ) -> None:
        """Close the HTTP pool, wait, rebuild it, and continue automatically."""

        old_client_closed = False

        try:
            # No new attempts can start while the pause flag is set. Wait for
            # attempts that already own a request slot to finish before closing
            # the underlying connection pool.
            async with self._rate_condition:
                while self._in_flight_attempts > 0 and not self._closed:
                    await self._rate_condition.wait()

            if self._closed:
                raise ExternalClientError(
                    "Async HTTP client was closed before scheduled pause"
                )

            if self._access_denied_event.is_set():
                logger_service.info(
                    (
                        "Scheduled HTTP connection reset skipped because "
                        "an access-denied cooldown is already active: "
                        f"pause_number={pause_number}"
                    ),
                    context=self.__class__.__name__,
                )
                return

            async with self._client_configuration_lock:
                if not self.client.is_closed:
                    await self.client.aclose()
                old_client_closed = True

            logger_service.info(
                (
                    "Scheduled external HTTP connections closed: "
                    f"pause_number={pause_number}, "
                    f"duration_seconds={self.pause_seconds:.2f}, "
                    "pipeline_and_mongodb_remain_active=True"
                ),
                context=self.__class__.__name__,
            )

            try:
                await asyncio.wait_for(
                    self._close_event.wait(),
                    timeout=self.pause_seconds,
                )
            except TimeoutError:
                pass
            else:
                raise ExternalClientError(
                    "Async HTTP client was closed during scheduled pause"
                )

            async with self._client_configuration_lock:
                if self._closed:
                    raise ExternalClientError(
                        "Async HTTP client was closed during scheduled pause"
                    )

                self.client = self._create_http_client()
                self._metrics.scheduled_connection_resets += 1
                old_client_closed = False

            logger_service.info(
                (
                    "Scheduled external HTTP pause completed: "
                    f"pause_number={pause_number}, "
                    "new_connection_pool=True, "
                    "scraping_resumed_automatically=True"
                ),
                context=self.__class__.__name__,
            )

        except asyncio.CancelledError:
            # Avoid leaving other workers blocked forever if the worker that
            # initiated the pause is cancelled while the process is still live.
            if old_client_closed and not self._closed:
                async with self._client_configuration_lock:
                    if self.client.is_closed:
                        self.client = self._create_http_client()
                        self._metrics.scheduled_connection_resets += 1
            raise

        finally:
            async with self._rate_condition:
                self._scheduled_pause_in_progress = False
                self._blocked_until = 0.0
                self._last_request_started_at = None
                self._rate_condition.notify_all()

    async def _wait_for_request_slot(self) -> None:
        """Reserve one paced request slot, respecting every global pause."""

        while True:
            pause_number: int | None = None
            cooldown_task: asyncio.Task[None] | None = None

            async with self._rate_condition:
                if self._closed:
                    raise ExternalClientError(
                        "Async HTTP client was closed while waiting for a request slot"
                    )

                if self._access_denied_event.is_set():
                    cooldown_task = self._access_denied_cooldown_task

                    if cooldown_task is None:
                        await self._rate_condition.wait()
                        continue

                elif self._scheduled_pause_in_progress:
                    await self._rate_condition.wait()
                    continue

                else:
                    should_start_scheduled_pause = (
                        self.pause_every_requests > 0
                        and self._request_starts_since_pause
                        >= self.pause_every_requests
                    )

                    if should_start_scheduled_pause:
                        self._scheduled_pause_in_progress = True
                        self._request_starts_since_pause = 0
                        self._metrics.scheduled_pauses += 1
                        self._metrics.scheduled_pause_seconds += self.pause_seconds
                        pause_number = self._metrics.scheduled_pauses
                        self._rate_condition.notify_all()

                        logger_service.info(
                            (
                                "Scheduled external HTTP pause started: "
                                f"pause_number={pause_number}, "
                                "after_requests="
                                f"{self.pause_every_requests}, "
                                "duration_seconds="
                                f"{self.pause_seconds:.2f}, "
                                "close_connections=True"
                            ),
                            context=self.__class__.__name__,
                        )

                    else:
                        current_time = time.monotonic()
                        interval_ready_at = current_time

                        if (
                            self.requests_per_second > 0
                            and self._last_request_started_at is not None
                        ):
                            interval_ready_at = self._last_request_started_at + (
                                1.0 / self.requests_per_second
                            )

                        next_request_at = max(
                            current_time,
                            interval_ready_at,
                            self._blocked_until,
                        )
                        remaining = next_request_at - current_time

                        if remaining <= 0:
                            self._last_request_started_at = current_time
                            self._request_starts_since_pause += 1
                            self._in_flight_attempts += 1
                            return

                        try:
                            await asyncio.wait_for(
                                self._rate_condition.wait(),
                                timeout=remaining,
                            )
                        except TimeoutError:
                            pass

            if cooldown_task is not None:
                await asyncio.shield(cooldown_task)
                continue

            if pause_number is not None:
                await self._perform_scheduled_connection_pause(
                    pause_number=pause_number,
                )

    async def _finish_request_attempt(self) -> None:
        async with self._rate_condition:
            if self._in_flight_attempts > 0:
                self._in_flight_attempts -= 1
            self._rate_condition.notify_all()

    async def _set_global_cooldown(self, delay: float) -> None:
        if delay <= 0:
            return

        async with self._rate_condition:
            self._blocked_until = max(
                self._blocked_until,
                time.monotonic() + delay,
            )
            self._rate_condition.notify_all()

    async def set_requests_per_second(self, value: float) -> None:
        """Change request pacing for future attempts without rebuilding."""

        self._validate_positive_number(
            name="requests_per_second",
            value=value,
            allow_zero=True,
        )

        async with self._rate_condition:
            self.requests_per_second = float(value)
            self._rate_condition.notify_all()

    async def _sleep_before_retry(self, delay: float) -> None:
        if delay <= 0:
            return

        try:
            await asyncio.wait_for(
                self._close_event.wait(),
                timeout=delay,
            )
        except TimeoutError:
            return

        raise ExternalClientError("Async HTTP client was closed during retry backoff")

    @staticmethod
    def _calculate_backoff(attempt: int) -> float:
        base_delay = min(2 ** (attempt - 1), 30)
        jitter = random.uniform(0.1, 0.8)
        return base_delay + jitter

    @staticmethod
    def _parse_retry_after(response: httpx.Response) -> float | None:
        retry_after = response.headers.get("Retry-After")

        if not retry_after:
            return None

        try:
            return max(float(retry_after), 0.0)
        except ValueError:
            pass

        try:
            retry_datetime = parsedate_to_datetime(retry_after)

            if retry_datetime.tzinfo is None:
                retry_datetime = retry_datetime.replace(tzinfo=timezone.utc)

            return max(
                (retry_datetime - datetime.now(timezone.utc)).total_seconds(),
                0.0,
            )
        except (TypeError, ValueError, OverflowError):
            return None

    @staticmethod
    def _safe_url(url: httpx.URL) -> str:
        port = f":{url.port}" if url.port else ""
        return f"{url.scheme}://{url.host}{port}{url.path}"

    @staticmethod
    def _response_preview(
        response: httpx.Response,
        max_length: int = 300,
    ) -> str:
        content_type = response.headers.get("Content-Type", "").lower()

        if any(
            value in content_type
            for value in (
                "application/octet-stream",
                "image/",
                "audio/",
                "video/",
            )
        ):
            return "<binary response>"

        return response.text[:max_length].replace("\n", " ")

    def _raise_for_response(self, response: httpx.Response) -> None:
        status_code = response.status_code
        safe_url = self._safe_url(response.request.url)

        if status_code in self.ACCESS_DENIED_STATUS_CODES:
            raise ExternalAccessDeniedError(
                "External website denied the request: "
                f"status={status_code}, url={safe_url}"
            )

        if status_code == 429:
            raise ExternalRateLimitError(
                f"External website rate limit was exceeded: url={safe_url}"
            )

        if not 200 <= status_code < 300:
            raise ExternalResponseError(
                "External website returned an unsuccessful response: "
                f"status={status_code}, "
                f"url={safe_url}, "
                f"preview={self._response_preview(response)!r}"
            )

    async def _build_request(
        self,
        *,
        method: str,
        endpoint: str,
        params: Mapping[str, Any] | None,
        headers: Mapping[str, str] | None,
        json: Any,
        data: Any,
        content: bytes | str | None,
        files: Mapping[str, Any] | None,
    ) -> httpx.Request:
        if not endpoint:
            raise ValueError("endpoint cannot be empty")

        async with self._client_configuration_lock:
            if self._closed:
                raise ExternalClientError("Async HTTP client is already closed")

            try:
                return self.client.build_request(
                    method=method,
                    url=endpoint,
                    params=params,
                    headers=dict(headers or {}),
                    json=json,
                    data=data,
                    content=content,
                    files=files,
                )
            except httpx.InvalidURL as error:
                raise ExternalClientError(
                    "Cannot prepare async external request because the URL "
                    f"is invalid: endpoint={endpoint!r}"
                ) from error

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any = None,
        data: Any = None,
        content: bytes | str | None = None,
        files: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        normalized_method = method.strip().upper()

        if not normalized_method:
            raise ValueError("method cannot be empty")

        total_attempts = self.max_retries + 1
        attempt = 1
        last_exception: Exception | None = None

        await self._begin_request()
        self._metrics.started_requests += 1

        try:
            while attempt <= total_attempts:
                try:
                    async with self._concurrency_semaphore:
                        await self._wait_for_request_slot()

                        started_at = time.monotonic()
                        self._metrics.total_attempts += 1

                        try:
                            request = await self._build_request(
                                method=normalized_method,
                                endpoint=endpoint,
                                params=params,
                                headers=headers,
                                json=json,
                                data=data,
                                content=content,
                                files=files,
                            )
                            response = await self.client.send(request)
                        finally:
                            duration = time.monotonic() - started_at
                            self._metrics.total_attempt_duration_seconds += duration
                            await self._finish_request_attempt()

                except self.RETRYABLE_REQUEST_EXCEPTIONS as error:
                    last_exception = error
                    self._metrics.network_errors += 1

                    if attempt >= total_attempts:
                        raise ExternalClientError(
                            "Async external request failed after all retry "
                            "attempts: "
                            f"method={normalized_method}, endpoint={endpoint}"
                        ) from error

                    retry_delay = self._calculate_backoff(attempt)
                    self._metrics.retries += 1

                    logger_service.warning(
                        (
                            "Retrying async external request after network "
                            "failure: "
                            f"method={normalized_method}, "
                            f"endpoint={endpoint}, "
                            f"error_type={type(error).__name__}, "
                            f"attempt={attempt}/{total_attempts}, "
                            f"retry_in={retry_delay:.2f}s"
                        ),
                        context=self.__class__.__name__,
                    )

                    await self._sleep_before_retry(retry_delay)
                    attempt += 1
                    continue

                except httpx.RequestError as error:
                    raise ExternalClientError(
                        "Async external request failed because of a "
                        "non-retryable HTTP client error: "
                        f"method={normalized_method}, "
                        f"endpoint={endpoint}, "
                        f"error_type={type(error).__name__}"
                    ) from error

                self._metrics.record_status(response.status_code)

                if response.status_code in self.ACCESS_DENIED_STATUS_CODES:
                    self._metrics.access_denied_responses += 1
                    self._metrics.retries += 1
                    cooldown_task = await self._start_access_denied_cooldown(response)
                    await asyncio.shield(cooldown_task)

                    # A 401/403 retry does not consume max_retries. If the
                    # upstream still denies access, one new shared cooldown
                    # begins and the same logical request remains pending.
                    continue

                if response.status_code == 429:
                    self._metrics.rate_limited_responses += 1

                if response.status_code not in self.RETRYABLE_STATUS_CODES:
                    self._raise_for_response(response)
                    self._metrics.successful_requests += 1

                    if self.log_successful_requests:
                        logger_service.info(
                            (
                                "Async external request completed: "
                                f"method={normalized_method}, "
                                f"url={self._safe_url(response.request.url)}, "
                                f"status={response.status_code}, "
                                f"attempt={attempt}/{total_attempts}"
                            ),
                            context=self.__class__.__name__,
                        )

                    return response

                if attempt >= total_attempts:
                    self._raise_for_response(response)

                retry_after = self._parse_retry_after(response)
                retry_delay = (
                    retry_after
                    if retry_after is not None
                    else self._calculate_backoff(attempt)
                )

                self._metrics.retries += 1

                logger_service.warning(
                    (
                        "Retryable async response received: "
                        f"method={normalized_method}, "
                        f"url={self._safe_url(response.request.url)}, "
                        f"status={response.status_code}, "
                        f"attempt={attempt}/{total_attempts}, "
                        f"retry_in={retry_delay:.2f}s"
                    ),
                    context=self.__class__.__name__,
                )

                if response.status_code == 429:
                    await self._set_global_cooldown(retry_delay)
                else:
                    await self._sleep_before_retry(retry_delay)

                attempt += 1

            raise ExternalClientError(
                "Async external request failed after all retry attempts: "
                f"method={normalized_method}, endpoint={endpoint}"
            ) from last_exception

        except asyncio.CancelledError:
            self._metrics.cancelled_requests += 1
            raise

        except Exception:
            self._metrics.failed_requests += 1
            raise

        finally:
            await self._end_request()

    async def get(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> httpx.Response:
        return await self.request(
            method="GET",
            endpoint=endpoint,
            params=params,
            headers=headers,
        )

    async def post(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any = None,
        data: Any = None,
    ) -> httpx.Response:
        return await self.request(
            method="POST",
            endpoint=endpoint,
            params=params,
            headers=headers,
            json=json,
            data=data,
        )

    async def put(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any = None,
        data: Any = None,
    ) -> httpx.Response:
        return await self.request(
            method="PUT",
            endpoint=endpoint,
            params=params,
            headers=headers,
            json=json,
            data=data,
        )

    async def patch(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any = None,
        data: Any = None,
    ) -> httpx.Response:
        return await self.request(
            method="PATCH",
            endpoint=endpoint,
            params=params,
            headers=headers,
            json=json,
            data=data,
        )

    async def delete(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> httpx.Response:
        return await self.request(
            method="DELETE",
            endpoint=endpoint,
            params=params,
            headers=headers,
        )

    async def get_json(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any] | list[Any]:
        response = await self.get(
            endpoint=endpoint,
            params=params,
            headers=headers,
        )

        try:
            result = response.json()
        except ValueError as error:
            self._metrics.json_decode_errors += 1

            raise ExternalJsonDecodeError(
                "External website did not return valid JSON: "
                f"status={response.status_code}, "
                "content_type="
                f"{response.headers.get('Content-Type')!r}, "
                f"preview={self._response_preview(response)!r}"
            ) from error

        if not isinstance(result, (dict, list)):
            self._metrics.json_decode_errors += 1

            raise ExternalJsonDecodeError(
                f"Expected a JSON object or array, but received {type(result).__name__}"
            )

        return result

    async def update_headers(self, headers: Mapping[str, str]) -> None:
        async with self._client_configuration_lock:
            if self._closed:
                raise ExternalClientError(
                    "Cannot update headers because the async client is closed"
                )

            normalized_headers = dict(headers)
            self._configured_headers.update(normalized_headers)
            self.client.headers.update(normalized_headers)

    async def update_cookies(self, cookies: Mapping[str, str]) -> None:
        async with self._client_configuration_lock:
            if self._closed:
                raise ExternalClientError(
                    "Cannot update cookies because the async client is closed"
                )

            normalized_cookies = dict(cookies)
            self._configured_cookies.update(normalized_cookies)
            self.client.cookies.update(normalized_cookies)

    async def clear_cookies(self) -> None:
        async with self._client_configuration_lock:
            if self._closed:
                raise ExternalClientError(
                    "Cannot clear cookies because the async client is closed"
                )

            self._configured_cookies.clear()
            self.client.cookies.clear()

    @property
    def is_closed(self) -> bool:
        return self._closed

    @property
    def active_requests(self) -> int:
        return self._active_requests

    def metrics_snapshot(self) -> dict[str, Any]:
        snapshot = self._metrics.snapshot()
        snapshot["access_denied_circuit_open"] = self._access_denied_event.is_set()
        snapshot["access_denied_status"] = self._access_denied_status
        snapshot["access_denied_url"] = self._access_denied_url
        snapshot["access_denied_cooldown_seconds_configured"] = (
            self.access_denied_cooldown_seconds
        )
        snapshot["http_client_generation"] = self._http_client_generation
        snapshot["scheduled_pause_in_progress"] = self._scheduled_pause_in_progress
        snapshot["in_flight_attempts"] = self._in_flight_attempts
        return snapshot

    @property
    def access_denied_circuit_open(self) -> bool:
        return self._access_denied_event.is_set()

    async def aclose(self) -> None:
        async with self._close_lock:
            if self._client_closed:
                return

            async with self._lifecycle_condition:
                self._closed = True
                self._close_event.set()

            async with self._rate_condition:
                self._rate_condition.notify_all()

            async with self._lifecycle_condition:
                while self._active_requests > 0:
                    await self._lifecycle_condition.wait()

            async with self._client_configuration_lock:
                if not self.client.is_closed:
                    await self.client.aclose()
                self._client_closed = True

            logger_service.info(
                (
                    "Async external HTTP client closed: "
                    f"metrics={self.metrics_snapshot()}"
                ),
                context=self.__class__.__name__,
            )

    async def close(self) -> None:
        await self.aclose()

    async def __aenter__(self) -> AsyncExternalHttpClient:
        if self._closed:
            raise ExternalClientError(
                "Cannot enter context because the async client is closed"
            )

        return self

    async def __aexit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: Any,
    ) -> None:
        await self.aclose()
