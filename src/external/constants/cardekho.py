from __future__ import annotations

from typing import Final

from src.external.constants.base import ApiEndpoint

CARDEKHO_BASE_URL: Final[str] = "https://www.cardekho.com"

CARDEKHO_DEFAULT_HEADERS: Final[dict[str, str]] = {
    "Accept": "application/json, text/plain, */*",
    "Source": "WEB",
}

CARDEKHO_NEW_CARS: Final[ApiEndpoint] = ApiEndpoint(
    name="cardekho_new_cars",
    method="GET",
    path="/api/v1/model/newcars",
    default_params={
        "url": "/newcars",
    },
    default_headers={
        "Referer": "https://www.cardekho.com/newcars",
    },
)

CARDEKHO_BRAND_MODELS: Final[ApiEndpoint] = ApiEndpoint(
    name="cardekho_brand_models",
    method="GET",
    path="/api/v1/brand/models",
    default_params={
        "withUpcoming": "true",
        "otherinfo": "all",
    },
)

CARDEKHO_APIS: Final[dict[str, ApiEndpoint]] = {
    CARDEKHO_NEW_CARS.name: CARDEKHO_NEW_CARS,
    CARDEKHO_BRAND_MODELS.name: CARDEKHO_BRAND_MODELS,
}
