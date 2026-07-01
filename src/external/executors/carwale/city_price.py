from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.clients.async_client import AsyncExternalHttpClient
from src.clients.client import ExternalResponseError
from src.external.constants.carwale import (
    CARWALE_BASE_URL,
    CARWALE_PIC_PAGE_DATA,
)
from src.models.carwale_city_price import (
    CarWaleCityPrice,
)
from src.models.carwale_city_price_job import (
    CarWaleCityPriceJob,
)


class CarWaleCityPriceExecutor:
    def __init__(
        self,
        client: AsyncExternalHttpClient,
    ) -> None:
        self._client = client

    @staticmethod
    def _build_referer(
        job: CarWaleCityPriceJob,
    ) -> str:
        return (
            f"{CARWALE_BASE_URL}/"
            f"{job.make_masking_name}-cars/"
            f"{job.model_masking_name}/"
            f"price-in-{job.city_masking_name}/"
        )

    @staticmethod
    def _parse_version_details(
        response: Mapping[str, Any],
        *,
        requested_version_id: int,
    ) -> dict[str, Any]:
        raw_version_details = response.get("versionDetails")

        if not isinstance(
            raw_version_details,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarWale PIC-page response does not contain valid versionDetails"
            )

        version_details = dict(raw_version_details)

        returned_version_id = version_details.get("versionId")

        if not isinstance(
            returned_version_id,
            int,
        ):
            raise ExternalResponseError(
                "CarWale versionDetails.versionId must be an integer"
            )

        if returned_version_id != requested_version_id:
            raise ExternalResponseError(
                "CarWale returned a different version: "
                f"requested={requested_version_id}, "
                f"returned={returned_version_id}"
            )

        return version_details

    @staticmethod
    def _parse_price_breakup(
        response: Mapping[str, Any],
    ) -> list[dict[str, Any]]:
        raw_price_breakup = response.get("priceBreakup")

        if not isinstance(
            raw_price_breakup,
            list,
        ):
            raise ExternalResponseError(
                "CarWale PIC-page response does not contain a valid priceBreakup array"
            )

        price_breakup: list[dict[str, Any]] = []

        for index, price_item in enumerate(raw_price_breakup):
            if not isinstance(
                price_item,
                Mapping,
            ):
                raise ExternalResponseError(
                    f"CarWale priceBreakup item must be an object: index={index}"
                )

            price_breakup.append(dict(price_item))

        return price_breakup

    async def execute(
        self,
        job: CarWaleCityPriceJob,
    ) -> CarWaleCityPrice:
        endpoint = CARWALE_PIC_PAGE_DATA

        if endpoint.method != "GET":
            raise RuntimeError(
                "Unexpected HTTP method configured for CarWale PIC-page API"
            )

        response_data = await self._client.get_json(
            endpoint=endpoint.path,
            params={
                **endpoint.default_params,
                "makeMaskingName": (job.make_masking_name),
                "modelMaskingName": (job.model_masking_name),
                "cityMaskingName": (job.city_masking_name),
                "versionId": job.version_id,
            },
            headers={
                **endpoint.default_headers,
                "Referer": self._build_referer(job),
            },
        )

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ExternalResponseError(
                "CarWale PIC-page API returned an invalid response. Expected an object"
            )

        version_details = self._parse_version_details(
            response_data,
            requested_version_id=(job.version_id),
        )

        price_breakup = self._parse_price_breakup(response_data)

        return CarWaleCityPrice(
            versionId=job.version_id,
            cityId=job.city_id,
            makeMaskingName=(job.make_masking_name),
            modelMaskingName=(job.model_masking_name),
            cityMaskingName=(job.city_masking_name),
            versionDetails=version_details,
            priceBreakup=price_breakup,
        )
