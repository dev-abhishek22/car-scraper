from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.clients.async_client import (
    AsyncExternalHttpClient,
)
from src.clients.client import (
    ExternalResponseError,
)
from src.external.constants.carwale import (
    CARWALE_NEW_CARS,
)


class CarWaleBrandsExecutor:
    """
    Fetch and validate the CarWale brand list.

    This executor performs no file writes, archive creation,
    status tracking, or MongoDB operations.
    """

    def __init__(
        self,
        client: AsyncExternalHttpClient,
    ) -> None:
        self._client = client

    @staticmethod
    def _validate_positive_integer(
        value: int,
        *,
        field_name: str,
    ) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field_name} must be a positive integer")

        return value

    @staticmethod
    def _parse_make_list(
        response: Mapping[str, Any],
    ) -> list[dict[str, Any]]:
        raw_make_list = response.get("makeList")

        if not isinstance(
            raw_make_list,
            list,
        ):
            raise ExternalResponseError(
                "CarWale response does not contain a valid makeList array"
            )

        make_list: list[dict[str, Any]] = []

        for index, raw_brand in enumerate(raw_make_list):
            if not isinstance(
                raw_brand,
                Mapping,
            ):
                raise ExternalResponseError(
                    "CarWale makeList contains an invalid "
                    f"brand at index {index}. "
                    "Expected an object"
                )

            make_list.append(dict(raw_brand))

        if not make_list:
            raise ExternalResponseError("CarWale makeList is empty")

        return make_list

    async def execute(
        self,
        *,
        page_id: int,
        platform_id: int = 1,
    ) -> list[dict[str, Any]]:
        normalized_page_id = self._validate_positive_integer(
            page_id,
            field_name="page_id",
        )

        normalized_platform_id = self._validate_positive_integer(
            platform_id,
            field_name="platform_id",
        )

        endpoint = CARWALE_NEW_CARS

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for the CarWale brands API"
            )

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params={
                **endpoint.default_params,
                "pageId": normalized_page_id,
                "platformId": normalized_platform_id,
            },
            headers=endpoint.default_headers,
        )

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarWale brands API returned an invalid response. Expected an object"
            )

        return self._parse_make_list(response_data)
