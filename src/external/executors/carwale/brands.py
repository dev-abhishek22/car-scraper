from __future__ import annotations

from pathlib import Path
from typing import Any

from src.clients.client import (
    ExternalHttpClient,
    ExternalResponseError,
)
from src.external.constants.carwale import (
    CARWALE_NEW_CARS,
)
from src.external.executors.base import BaseApiExecutor


class CarWaleBrandsExecutor(BaseApiExecutor):
    def __init__(
        self,
        client: ExternalHttpClient,
    ) -> None:
        self.client = client

    def execute(
        self,
        *,
        page_id: int,
        platform_id: int = 1,
        show_request: bool = False,
        request_log_file: str | Path | None = None,
        include_sensitive_request_data: bool = False,
    ) -> list[Any]:
        if page_id < 1:
            raise ValueError("page_id must be greater than zero")

        if platform_id < 1:
            raise ValueError("platform_id must be greater than zero")

        params = {
            **CARWALE_NEW_CARS.default_params,
            "pageId": page_id,
            "platformId": platform_id,
        }

        if CARWALE_NEW_CARS.method != "GET":
            raise RuntimeError("Unexpected method configured for CarWale brands API")

        response = self.client.get_json(
            endpoint=CARWALE_NEW_CARS.path,
            params=params,
            headers=CARWALE_NEW_CARS.default_headers,
            show_request=show_request,
            request_log_file=request_log_file,
            include_sensitive_request_data=(include_sensitive_request_data),
        )

        if not isinstance(response, dict):
            raise ExternalResponseError("Expected CarWale response to be a JSON object")

        make_list = response.get("makeList")

        if not isinstance(make_list, list):
            raise ExternalResponseError(
                "CarWale response does not contain a valid 'makeList' array"
            )

        return make_list
