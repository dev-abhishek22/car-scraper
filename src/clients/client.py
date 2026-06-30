from __future__ import annotations

import json as json_lib
import random
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

    Features:
    - Persistent HTTP connection pooling
    - Stable user-agent for one client session
    - Default and request-specific headers
    - Cookie persistence
    - Minimum interval between requests
    - Configurable timeouts
    - Retry handling
    - Retry-After support
    - Prepared-request display
    - Prepared-request JSON logging
    - Sensitive-data redaction
    - JSON response parsing
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
        self._validate_configuration(
            base_url=base_url,
            user_agent=user_agent,
            user_agents=user_agents,
            min_request_interval=min_request_interval,
            max_retries=max_retries,
        )

        self.base_url = base_url.rstrip("/")
        self.min_request_interval = min_request_interval
        self.max_retries = max_retries

        self._request_lock = threading.Lock()
        self._last_request_started_at: float | None = None

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

        transport = httpx.HTTPTransport(
            retries=1,
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
                f"user_agent={selected_user_agent}"
            ),
            context=self.__class__.__name__,
        )

    @staticmethod
    def _validate_configuration(
        *,
        base_url: str,
        user_agent: str | None,
        user_agents: Sequence[str] | None,
        min_request_interval: float,
        max_retries: int,
    ) -> None:
        if not base_url.startswith(("http://", "https://")):
            raise ValueError("base_url must begin with http:// or https://")

        if user_agent and user_agents:
            raise ValueError("Provide either user_agent or user_agents, not both")

        if isinstance(user_agents, str):
            raise ValueError(
                "user_agents must be a sequence of strings, " "not a single string"
            )

        if min_request_interval < 0:
            raise ValueError("min_request_interval cannot be negative")

        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")

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
            valid_user_agents = [
                cls._validate_user_agent(value)
                for value in user_agents
                if value and value.strip()
            ]

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

    def _wait_for_request_slot(self) -> None:
        """
        Enforce the configured minimum interval between
        the starting time of requests.
        """
        with self._request_lock:
            if self._last_request_started_at is not None:
                elapsed = time.monotonic() - self._last_request_started_at

                remaining = self.min_request_interval - elapsed

                if remaining > 0:
                    time.sleep(remaining)

            self._last_request_started_at = time.monotonic()

    @staticmethod
    def _calculate_backoff(
        attempt: int,
    ) -> float:
        base_delay = min(2**attempt, 30)
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
        """
        Return a URL without query parameters for normal logs.
        """
        port = f":{url.port}" if url.port else ""

        return f"{url.scheme}://" f"{url.host}" f"{port}" f"{url.path}"

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
            return f"<binary body: " f"{len(content)} bytes>"

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
                return decoded_content

        if "application/x-www-form-urlencoded" in content_type:
            form_items = parse_qsl(
                decoded_content,
                keep_blank_values=True,
            )

            return urlencode(
                [
                    (
                        key,
                        "<redacted>" if cls._is_sensitive_field(key) else value,
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
                include_sensitive_data=(include_sensitive_data),
            ),
        }

    @staticmethod
    def _save_request_snapshots(
        file_path: str | Path,
        snapshots: list[dict[str, Any]],
    ) -> None:
        output_file = Path(file_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file.write_text(
            json_lib.dumps(
                {
                    "requests": snapshots,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

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
                "External website rate limit was exceeded: " f"url={safe_url}"
            )

        if not 200 <= status_code < 300:
            raise ExternalResponseError(
                "External website returned an "
                "unsuccessful response: "
                f"status={status_code}, "
                f"url={safe_url}, "
                f"preview="
                f"{self._response_preview(response)!r}"
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
        method = method.upper()

        total_attempts = self.max_retries + 1
        last_exception: Exception | None = None

        request_snapshots: list[dict[str, Any]] = []

        for attempt in range(
            1,
            total_attempts + 1,
        ):
            self._wait_for_request_slot()

            started_at = time.monotonic()

            request = self.client.build_request(
                method=method,
                url=endpoint,
                params=params,
                headers=dict(headers or {}),
                json=json,
                data=data,
                content=content,
                files=files,
            )

            snapshot = self._create_request_snapshot(
                request,
                attempt=attempt,
                include_sensitive_data=(include_sensitive_request_data),
            )

            request_snapshots.append(snapshot)

            if show_request:
                print("\nPrepared external request:")

                print(
                    json_lib.dumps(
                        snapshot,
                        indent=2,
                        ensure_ascii=False,
                    )
                )

            if request_log_file is not None:
                self._save_request_snapshots(
                    request_log_file,
                    request_snapshots,
                )

            try:
                response = self.client.send(request)

                duration = time.monotonic() - started_at

                snapshot["response_status"] = response.status_code

                snapshot["duration_seconds"] = round(duration, 4)

                if request_log_file is not None:
                    self._save_request_snapshots(
                        request_log_file,
                        request_snapshots,
                    )

                safe_url = self._safe_url(response.request.url)

                logger_service.info(
                    (
                        "External request completed: "
                        f"method={method}, "
                        f"url={safe_url}, "
                        f"status="
                        f"{response.status_code}, "
                        f"duration={duration:.2f}s, "
                        f"attempt="
                        f"{attempt}/{total_attempts}"
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

                logger_service.info(
                    (
                        "Retryable response received: "
                        f"method={method}, "
                        f"url={safe_url}, "
                        f"status="
                        f"{response.status_code}, "
                        f"retry_in="
                        f"{retry_delay:.2f}s"
                    ),
                    context=self.__class__.__name__,
                )

                time.sleep(retry_delay)

            except (
                ExternalAccessDeniedError,
                ExternalRateLimitError,
                ExternalResponseError,
            ):
                raise

            except httpx.RequestError as error:
                duration = time.monotonic() - started_at

                last_exception = error

                snapshot["duration_seconds"] = round(duration, 4)

                snapshot["error"] = str(error)

                if request_log_file is not None:
                    self._save_request_snapshots(
                        request_log_file,
                        request_snapshots,
                    )

                logger_service.error(
                    (
                        "External network request failed: "
                        f"method={method}, "
                        f"endpoint={endpoint}, "
                        f"duration={duration:.2f}s, "
                        f"attempt="
                        f"{attempt}/{total_attempts}"
                    ),
                    exception=error,
                    context=self.__class__.__name__,
                )

                if attempt >= total_attempts:
                    break

                retry_delay = self._calculate_backoff(attempt)

                time.sleep(retry_delay)

        raise ExternalClientError(
            "External request failed after all "
            "retry attempts: "
            f"method={method}, "
            f"endpoint={endpoint}"
        ) from last_exception

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
            include_sensitive_request_data=(include_sensitive_request_data),
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
            include_sensitive_request_data=(include_sensitive_request_data),
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
            include_sensitive_request_data=(include_sensitive_request_data),
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
            include_sensitive_request_data=(include_sensitive_request_data),
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
            include_sensitive_request_data=(include_sensitive_request_data),
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
            include_sensitive_request_data=(include_sensitive_request_data),
        )

        try:
            result = response.json()

        except ValueError as error:
            raise ExternalJsonDecodeError(
                "External website did not return "
                "valid JSON: "
                f"status={response.status_code}, "
                f"content_type="
                f"{response.headers.get('Content-Type')!r}, "
                f"preview="
                f"{self._response_preview(response)!r}"
            ) from error

        if not isinstance(
            result,
            (dict, list),
        ):
            raise ExternalJsonDecodeError(
                "Expected a JSON object or array, "
                f"but received "
                f"{type(result).__name__}"
            )

        return result

    def update_headers(
        self,
        headers: Mapping[str, str],
    ) -> None:
        self.client.headers.update(dict(headers))

    def update_cookies(
        self,
        cookies: Mapping[str, str],
    ) -> None:
        self.client.cookies.update(dict(cookies))

    def clear_cookies(self) -> None:
        self.client.cookies.clear()

    def close(self) -> None:
        self.client.close()

        logger_service.info(
            "External HTTP client closed",
            context=self.__class__.__name__,
        )

    def __enter__(
        self,
    ) -> ExternalHttpClient:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: Any,
    ) -> None:
        self.close()
