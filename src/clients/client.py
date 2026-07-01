from __future__ import annotations

import json as json_lib
import math
import os
import random
import tempfile
import threading
import time
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import httpx

from src.logger.logger import logger_service


class ExternalClientError(Exception):
    """Base exception for external website requests."""


class ExternalAccessDeniedError(ExternalClientError):
    """Raised when an external website denies access."""


class ExternalRateLimitError(ExternalClientError):
    """Raised when an external website rate limit is exceeded."""


class ExternalResponseError(ExternalClientError):
    """Raised when an external website returns an invalid response."""


class ExternalJsonDecodeError(ExternalClientError):
    """Raised when a response cannot be decoded as JSON."""


class ExternalHttpClient:
    """
    Reusable synchronous HTTP client for external websites.

    The same instance can be shared by multiple worker threads.

    Features:
    - Persistent HTTP connection pooling
    - Stable user-agent for one client session
    - Default and request-specific headers
    - Cookie persistence
    - Global minimum interval between request starts
    - Global Retry-After cooldown for rate limiting
    - Configurable timeouts and connection limits
    - Retry handling for temporary HTTP and network failures
    - Prepared-request display
    - Atomic prepared-request JSON logging
    - Sensitive-data redaction
    - JSON response parsing
    - Graceful and idempotent shutdown
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

    SENSITIVE_REQUEST_HEADERS = {
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "x-api-key",
        "api-key",
        "x-auth-token",
        "x-csrf-token",
        "x-xsrf-token",
    }

    SENSITIVE_FIELD_NAMES = {
        "authorization",
        "password",
        "passwd",
        "secret",
        "client_secret",
        "token",
        "access_token",
        "refresh_token",
        "api_key",
        "apikey",
        "x_api_key",
        "session",
        "session_id",
        "sessionid",
        "csrf_token",
        "xsrf_token",
    }

    def __init__(
        self,
        *,
        base_url: str,
        default_headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        user_agent: str | None = None,
        user_agents: Sequence[str] | None = None,
        min_request_interval: float = 1.5,
        max_retries: int = 3,
        connect_timeout: float = 10.0,
        read_timeout: float = 30.0,
        write_timeout: float = 30.0,
        pool_timeout: float = 10.0,
        max_connections: int = 10,
        max_keepalive_connections: int = 5,
        keepalive_expiry: float = 30.0,
        follow_redirects: bool = True,
        verify_ssl: bool = True,
        trust_environment: bool = False,
    ) -> None:
        normalized_base_url = self._normalize_base_url(base_url)

        self._validate_configuration(
            user_agent=user_agent,
            user_agents=user_agents,
            min_request_interval=min_request_interval,
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
        self.min_request_interval = float(min_request_interval)
        self.max_retries = max_retries

        # Coordinates request-start spacing and global rate-limit cooldowns.
        self._rate_condition = threading.Condition()
        self._last_request_started_at: float | None = None
        self._blocked_until = 0.0

        # Protects header/cookie mutations and request preparation.
        self._client_configuration_lock = threading.RLock()

        # Keeps console output from multiple workers readable.
        self._console_lock = threading.Lock()

        # Protects request snapshot files when multiple workers accidentally
        # use the same path.
        self._snapshot_locks_guard = threading.Lock()
        self._snapshot_locks: dict[Path, threading.Lock] = {}

        # Tracks lifecycle so close() can wait for active logical requests.
        self._lifecycle_condition = threading.Condition()
        self._close_lock = threading.Lock()
        self._close_event = threading.Event()
        self._active_requests = 0
        self._closed = False
        self._client_closed = False

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

        timeout = httpx.Timeout(
            connect=connect_timeout,
            read=read_timeout,
            write=write_timeout,
            pool=pool_timeout,
        )

        limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=keepalive_expiry,
        )

        # Retry ownership stays in this class. Keeping transport retries at
        # zero avoids hidden duplicate connection attempts.
        transport = httpx.HTTPTransport(
            retries=0,
            verify=verify_ssl,
        )

        self.client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            cookies=dict(cookies or {}),
            timeout=timeout,
            limits=limits,
            transport=transport,
            follow_redirects=follow_redirects,
            trust_env=trust_environment,
        )

        logger_service.info(
            (
                "External HTTP client initialized: "
                f"base_url={self.base_url}, "
                f"user_agent={selected_user_agent}, "
                f"max_connections={max_connections}, "
                "max_keepalive_connections="
                f"{max_keepalive_connections}, "
                "min_request_interval="
                f"{self.min_request_interval:.2f}s"
            ),
            context=self.__class__.__name__,
        )

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
        min_request_interval: float,
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
                "user_agents must be a sequence of strings, not a single string"
            )

        cls._validate_positive_number(
            name="min_request_interval",
            value=min_request_interval,
            allow_zero=True,
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

        if max_connections < 1:
            raise ValueError("max_connections must be at least 1")

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

        return "ExternalDataClient/1.0"

    @staticmethod
    def _validate_user_agent(
        user_agent: str,
    ) -> str:
        normalized_user_agent = user_agent.strip()

        if not normalized_user_agent:
            raise ValueError("User-Agent cannot be empty")

        if "\r" in normalized_user_agent or "\n" in normalized_user_agent:
            raise ValueError("User-Agent cannot contain line breaks")

        return normalized_user_agent

    def _begin_request(self) -> None:
        with self._lifecycle_condition:
            if self._closed:
                raise ExternalClientError("External HTTP client is already closed")

            self._active_requests += 1

    def _end_request(self) -> None:
        with self._lifecycle_condition:
            self._active_requests -= 1
            self._lifecycle_condition.notify_all()

    def _wait_for_request_slot(self) -> None:
        """
        Enforce one global minimum interval between request start times.

        All worker threads sharing this client also share this limiter and
        any active rate-limit cooldown.
        """
        with self._rate_condition:
            while True:
                if self._closed:
                    raise ExternalClientError(
                        "External HTTP client was closed while waiting "
                        "for a request slot"
                    )

                current_time = time.monotonic()

                interval_ready_at = current_time

                if self._last_request_started_at is not None:
                    interval_ready_at = (
                        self._last_request_started_at + self.min_request_interval
                    )

                next_request_at = max(
                    current_time,
                    interval_ready_at,
                    self._blocked_until,
                )

                remaining = next_request_at - current_time

                if remaining <= 0:
                    self._last_request_started_at = current_time
                    return

                self._rate_condition.wait(timeout=remaining)

    def _set_global_cooldown(
        self,
        delay: float,
    ) -> None:
        if delay <= 0:
            return

        with self._rate_condition:
            self._blocked_until = max(
                self._blocked_until,
                time.monotonic() + delay,
            )

            # Wake waiting workers so they recalculate against the new,
            # possibly later cooldown deadline.
            self._rate_condition.notify_all()

    def _sleep_before_retry(
        self,
        delay: float,
    ) -> None:
        if delay <= 0:
            return

        if self._close_event.wait(timeout=delay):
            raise ExternalClientError(
                "External HTTP client was closed during retry backoff"
            )

    @staticmethod
    def _calculate_backoff(
        attempt: int,
    ) -> float:
        # attempt starts at 1, producing approximately 1s, 2s, 4s, 8s...
        base_delay = min(2 ** (attempt - 1), 30)
        jitter = random.uniform(0.1, 0.8)

        return base_delay + jitter

    @staticmethod
    def _parse_retry_after(
        response: httpx.Response,
    ) -> float | None:
        retry_after = response.headers.get("Retry-After")

        if not retry_after:
            return None

        try:
            return max(
                float(retry_after),
                0.0,
            )
        except ValueError:
            pass

        try:
            retry_datetime = parsedate_to_datetime(retry_after)

            if retry_datetime.tzinfo is None:
                retry_datetime = retry_datetime.replace(tzinfo=timezone.utc)

            current_datetime = datetime.now(timezone.utc)

            return max(
                (retry_datetime - current_datetime).total_seconds(),
                0.0,
            )

        except (
            TypeError,
            ValueError,
            OverflowError,
        ):
            return None

    @staticmethod
    def _safe_url(
        url: httpx.URL,
    ) -> str:
        """Return a URL without query parameters for normal logs."""
        port = f":{url.port}" if url.port else ""

        return f"{url.scheme}://{url.host}{port}{url.path}"

    @classmethod
    def _is_sensitive_field(
        cls,
        name: str,
    ) -> bool:
        normalized_name = name.strip().lower().replace("-", "_")

        return normalized_name in cls.SENSITIVE_FIELD_NAMES

    @classmethod
    def _redact_url(
        cls,
        url: str,
    ) -> str:
        parts = urlsplit(url)

        query_items = parse_qsl(
            parts.query,
            keep_blank_values=True,
        )

        redacted_query = urlencode(
            [
                (
                    key,
                    "<redacted>" if cls._is_sensitive_field(key) else value,
                )
                for key, value in query_items
            ],
            doseq=True,
        )

        return urlunsplit(
            (
                parts.scheme,
                parts.netloc,
                parts.path,
                redacted_query,
                parts.fragment,
            )
        )

    @classmethod
    def _redact_json_value(
        cls,
        value: Any,
    ) -> Any:
        if isinstance(value, dict):
            return {
                key: (
                    "<redacted>"
                    if cls._is_sensitive_field(str(key))
                    else cls._redact_json_value(item)
                )
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [cls._redact_json_value(item) for item in value]

        return value

    @classmethod
    def _request_body_for_snapshot(
        cls,
        request: httpx.Request,
        *,
        include_sensitive_data: bool,
    ) -> str | None:
        try:
            content = request.content
        except httpx.RequestNotRead:
            return "<streaming request body>"

        if not content:
            return None

        try:
            decoded_content = content.decode("utf-8")
        except UnicodeDecodeError:
            return f"<binary body: {len(content)} bytes>"

        if include_sensitive_data:
            return decoded_content

        content_type = request.headers.get(
            "Content-Type",
            "",
        ).lower()

        if "application/json" in content_type:
            try:
                parsed_body = json_lib.loads(decoded_content)

                redacted_body = cls._redact_json_value(parsed_body)

                return json_lib.dumps(
                    redacted_body,
                    ensure_ascii=False,
                )

            except json_lib.JSONDecodeError:
                return "<unparseable JSON body omitted>"

        if "application/x-www-form-urlencoded" in content_type:
            form_items = parse_qsl(
                decoded_content,
                keep_blank_values=True,
            )

            return urlencode(
                [
                    (
                        key,
                        ("<redacted>" if cls._is_sensitive_field(key) else value),
                    )
                    for key, value in form_items
                ],
                doseq=True,
            )

        return decoded_content

    @classmethod
    def _create_request_snapshot(
        cls,
        request: httpx.Request,
        *,
        attempt: int,
        include_sensitive_data: bool,
    ) -> dict[str, Any]:
        request_headers: dict[str, str] = {}

        for name, value in request.headers.items():
            if (
                not include_sensitive_data
                and name.lower() in cls.SENSITIVE_REQUEST_HEADERS
            ):
                request_headers[name] = "<redacted>"
            else:
                request_headers[name] = value

        request_url = str(request.url)

        if not include_sensitive_data:
            request_url = cls._redact_url(request_url)

        return {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "attempt": attempt,
            "method": request.method,
            "url": request_url,
            "headers": request_headers,
            "body": cls._request_body_for_snapshot(
                request,
                include_sensitive_data=include_sensitive_data,
            ),
        }

    def _get_snapshot_lock(
        self,
        file_path: Path,
    ) -> threading.Lock:
        normalized_path = file_path.expanduser().resolve()

        with self._snapshot_locks_guard:
            lock = self._snapshot_locks.get(normalized_path)

            if lock is None:
                lock = threading.Lock()
                self._snapshot_locks[normalized_path] = lock

            return lock

    def _save_request_snapshots(
        self,
        file_path: str | Path,
        snapshots: list[dict[str, Any]],
    ) -> None:
        output_file = Path(file_path)
        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        serialized_data = json_lib.dumps(
            {
                "requests": snapshots,
            },
            indent=2,
            ensure_ascii=False,
        )

        file_lock = self._get_snapshot_lock(output_file)

        temporary_path: Path | None = None

        with file_lock:
            try:
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    dir=output_file.parent,
                    prefix=f".{output_file.name}.",
                    suffix=".tmp",
                    delete=False,
                ) as temporary_file:
                    temporary_path = Path(temporary_file.name)

                    temporary_file.write(serialized_data)
                    temporary_file.flush()
                    os.fsync(temporary_file.fileno())

                temporary_path.replace(output_file)

            except Exception:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)

                raise

    @staticmethod
    def _response_preview(
        response: httpx.Response,
        max_length: int = 300,
    ) -> str:
        content_type = response.headers.get(
            "Content-Type",
            "",
        ).lower()

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

        return response.text[:max_length].replace(
            "\n",
            " ",
        )

    def _raise_for_response(
        self,
        response: httpx.Response,
    ) -> None:
        status_code = response.status_code
        safe_url = self._safe_url(response.request.url)

        if status_code in self.ACCESS_DENIED_STATUS_CODES:
            raise ExternalAccessDeniedError(
                "External website denied the request: "
                f"status={status_code}, "
                f"url={safe_url}"
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

    def _build_request(
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

        with self._client_configuration_lock:
            if self._closed:
                raise ExternalClientError("External HTTP client is already closed")

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
                    "Cannot prepare external request because the URL "
                    f"is invalid: endpoint={endpoint!r}"
                ) from error

    def _print_request_snapshot(
        self,
        snapshot: dict[str, Any],
    ) -> None:
        with self._console_lock:
            print("\nPrepared external request:")
            print(
                json_lib.dumps(
                    snapshot,
                    indent=2,
                    ensure_ascii=False,
                )
            )

    def request(
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
        show_request: bool = False,
        request_log_file: str | Path | None = None,
        include_sensitive_request_data: bool = False,
    ) -> httpx.Response:
        normalized_method = method.strip().upper()

        if not normalized_method:
            raise ValueError("method cannot be empty")

        total_attempts = self.max_retries + 1
        last_exception: Exception | None = None
        request_snapshots: list[dict[str, Any]] = []

        self._begin_request()

        try:
            for attempt in range(
                1,
                total_attempts + 1,
            ):
                self._wait_for_request_slot()

                started_at = time.monotonic()

                request = self._build_request(
                    method=normalized_method,
                    endpoint=endpoint,
                    params=params,
                    headers=headers,
                    json=json,
                    data=data,
                    content=content,
                    files=files,
                )

                snapshot = self._create_request_snapshot(
                    request,
                    attempt=attempt,
                    include_sensitive_data=include_sensitive_request_data,
                )

                request_snapshots.append(snapshot)

                if show_request:
                    self._print_request_snapshot(snapshot)

                if request_log_file is not None:
                    self._save_request_snapshots(
                        request_log_file,
                        request_snapshots,
                    )

                try:
                    response = self.client.send(request)

                    duration = time.monotonic() - started_at
                    safe_url = self._safe_url(response.request.url)

                    snapshot["response_status"] = response.status_code
                    snapshot["duration_seconds"] = round(duration, 4)

                    if request_log_file is not None:
                        self._save_request_snapshots(
                            request_log_file,
                            request_snapshots,
                        )

                    logger_service.info(
                        (
                            "External request completed: "
                            f"method={normalized_method}, "
                            f"url={safe_url}, "
                            f"status={response.status_code}, "
                            f"duration={duration:.2f}s, "
                            f"attempt={attempt}/{total_attempts}"
                        ),
                        context=self.__class__.__name__,
                    )

                    if response.status_code not in self.RETRYABLE_STATUS_CODES:
                        self._raise_for_response(response)
                        return response

                    if attempt >= total_attempts:
                        self._raise_for_response(response)

                    retry_after = self._parse_retry_after(response)
                    retry_delay = (
                        retry_after
                        if retry_after is not None
                        else self._calculate_backoff(attempt)
                    )

                    snapshot["retry_delay_seconds"] = round(
                        retry_delay,
                        4,
                    )

                    if request_log_file is not None:
                        self._save_request_snapshots(
                            request_log_file,
                            request_snapshots,
                        )

                    logger_service.info(
                        (
                            "Retryable response received: "
                            f"method={normalized_method}, "
                            f"url={safe_url}, "
                            f"status={response.status_code}, "
                            f"retry_in={retry_delay:.2f}s"
                        ),
                        context=self.__class__.__name__,
                    )

                    if response.status_code == 429:
                        # All workers using this client must pause before
                        # starting another request.
                        self._set_global_cooldown(retry_delay)
                    else:
                        self._sleep_before_retry(retry_delay)

                except (
                    ExternalAccessDeniedError,
                    ExternalRateLimitError,
                    ExternalResponseError,
                ):
                    raise

                except self.RETRYABLE_REQUEST_EXCEPTIONS as error:
                    duration = time.monotonic() - started_at
                    last_exception = error

                    snapshot["duration_seconds"] = round(duration, 4)
                    snapshot["error_type"] = type(error).__name__
                    snapshot["error"] = str(error)

                    if request_log_file is not None:
                        self._save_request_snapshots(
                            request_log_file,
                            request_snapshots,
                        )

                    logger_service.error(
                        (
                            "External network request failed: "
                            f"method={normalized_method}, "
                            f"endpoint={endpoint}, "
                            f"duration={duration:.2f}s, "
                            f"attempt={attempt}/{total_attempts}"
                        ),
                        exception=error,
                        context=self.__class__.__name__,
                    )

                    if attempt >= total_attempts:
                        break

                    retry_delay = self._calculate_backoff(attempt)
                    snapshot["retry_delay_seconds"] = round(
                        retry_delay,
                        4,
                    )

                    if request_log_file is not None:
                        self._save_request_snapshots(
                            request_log_file,
                            request_snapshots,
                        )

                    self._sleep_before_retry(retry_delay)

                except httpx.RequestError as error:
                    duration = time.monotonic() - started_at

                    snapshot["duration_seconds"] = round(duration, 4)
                    snapshot["error_type"] = type(error).__name__
                    snapshot["error"] = str(error)

                    if request_log_file is not None:
                        self._save_request_snapshots(
                            request_log_file,
                            request_snapshots,
                        )

                    raise ExternalClientError(
                        "External request failed because of a "
                        "non-retryable HTTP client error: "
                        f"method={normalized_method}, "
                        f"endpoint={endpoint}, "
                        f"error_type={type(error).__name__}"
                    ) from error

            raise ExternalClientError(
                "External request failed after all retry attempts: "
                f"method={normalized_method}, "
                f"endpoint={endpoint}"
            ) from last_exception

        finally:
            self._end_request()

    def get(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        show_request: bool = False,
        request_log_file: str | Path | None = None,
        include_sensitive_request_data: bool = False,
    ) -> httpx.Response:
        return self.request(
            method="GET",
            endpoint=endpoint,
            params=params,
            headers=headers,
            show_request=show_request,
            request_log_file=request_log_file,
            include_sensitive_request_data=include_sensitive_request_data,
        )

    def post(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any = None,
        data: Any = None,
        show_request: bool = False,
        request_log_file: str | Path | None = None,
        include_sensitive_request_data: bool = False,
    ) -> httpx.Response:
        return self.request(
            method="POST",
            endpoint=endpoint,
            params=params,
            headers=headers,
            json=json,
            data=data,
            show_request=show_request,
            request_log_file=request_log_file,
            include_sensitive_request_data=include_sensitive_request_data,
        )

    def put(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any = None,
        data: Any = None,
        show_request: bool = False,
        request_log_file: str | Path | None = None,
        include_sensitive_request_data: bool = False,
    ) -> httpx.Response:
        return self.request(
            method="PUT",
            endpoint=endpoint,
            params=params,
            headers=headers,
            json=json,
            data=data,
            show_request=show_request,
            request_log_file=request_log_file,
            include_sensitive_request_data=include_sensitive_request_data,
        )

    def patch(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any = None,
        data: Any = None,
        show_request: bool = False,
        request_log_file: str | Path | None = None,
        include_sensitive_request_data: bool = False,
    ) -> httpx.Response:
        return self.request(
            method="PATCH",
            endpoint=endpoint,
            params=params,
            headers=headers,
            json=json,
            data=data,
            show_request=show_request,
            request_log_file=request_log_file,
            include_sensitive_request_data=include_sensitive_request_data,
        )

    def delete(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        show_request: bool = False,
        request_log_file: str | Path | None = None,
        include_sensitive_request_data: bool = False,
    ) -> httpx.Response:
        return self.request(
            method="DELETE",
            endpoint=endpoint,
            params=params,
            headers=headers,
            show_request=show_request,
            request_log_file=request_log_file,
            include_sensitive_request_data=include_sensitive_request_data,
        )

    def get_json(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        show_request: bool = False,
        request_log_file: str | Path | None = None,
        include_sensitive_request_data: bool = False,
    ) -> dict[str, Any] | list[Any]:
        response = self.get(
            endpoint=endpoint,
            params=params,
            headers=headers,
            show_request=show_request,
            request_log_file=request_log_file,
            include_sensitive_request_data=include_sensitive_request_data,
        )

        try:
            result = response.json()

        except ValueError as error:
            raise ExternalJsonDecodeError(
                "External website did not return valid JSON: "
                f"status={response.status_code}, "
                "content_type="
                f"{response.headers.get('Content-Type')!r}, "
                f"preview={self._response_preview(response)!r}"
            ) from error

        if not isinstance(
            result,
            (dict, list),
        ):
            raise ExternalJsonDecodeError(
                f"Expected a JSON object or array, but received {type(result).__name__}"
            )

        return result

    def update_headers(
        self,
        headers: Mapping[str, str],
    ) -> None:
        with self._client_configuration_lock:
            if self._closed:
                raise ExternalClientError(
                    "Cannot update headers because the client is closed"
                )

            self.client.headers.update(dict(headers))

    def update_cookies(
        self,
        cookies: Mapping[str, str],
    ) -> None:
        with self._client_configuration_lock:
            if self._closed:
                raise ExternalClientError(
                    "Cannot update cookies because the client is closed"
                )

            self.client.cookies.update(dict(cookies))

    def clear_cookies(self) -> None:
        with self._client_configuration_lock:
            if self._closed:
                raise ExternalClientError(
                    "Cannot clear cookies because the client is closed"
                )

            self.client.cookies.clear()

    @property
    def is_closed(self) -> bool:
        return self._closed

    def close(self) -> None:
        with self._close_lock:
            if self._client_closed:
                return

            with self._lifecycle_condition:
                self._closed = True
                self._close_event.set()

            with self._rate_condition:
                self._rate_condition.notify_all()

            with self._lifecycle_condition:
                while self._active_requests > 0:
                    self._lifecycle_condition.wait()

            with self._client_configuration_lock:
                self.client.close()
                self._client_closed = True

            logger_service.info(
                "External HTTP client closed",
                context=self.__class__.__name__,
            )

    def __enter__(
        self,
    ) -> ExternalHttpClient:
        if self._closed:
            raise ExternalClientError(
                "Cannot enter context because the client is closed"
            )

        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: Any,
    ) -> None:
        self.close()
