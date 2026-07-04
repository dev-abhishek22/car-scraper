from __future__ import annotations

from typing import Final

from src.external.constants.base import (
    ApiEndpoint,
)

CARDEKHO_BASE_URL: Final[str] = "https://www.cardekho.com"

CARDEKHO_DEFAULT_HEADERS: Final[dict[str, str]] = {
    "Accept": "application/json, text/plain, */*",
    "Source": "WEB",
}

CARDEKHO_CITIES_BUNDLE_URL: Final[str] = (
    "https://staticcont.cardekho.com/pwa/js/bundle/" "cities.7731e9424bd84181d23f.cjs"
)


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


CARDEKHO_MODEL_OVERVIEW: Final[ApiEndpoint] = ApiEndpoint(
    name="cardekho_model_overview",
    method="GET",
    path="/api/v1/model/pwamodeloverview",
    default_params={
        "otherinfo": "all",
    },
)


CARDEKHO_MODEL_SPECS: Final[ApiEndpoint] = ApiEndpoint(
    name="cardekho_model_specs",
    method="GET",
    path="/api/v3/model/pwamodelspecs",
    default_params={
        "otherinfo": "all",
    },
)


CARDEKHO_CITIES_BUNDLE: Final[ApiEndpoint] = ApiEndpoint(
    name="cardekho_cities_bundle",
    method="GET",
    path=CARDEKHO_CITIES_BUNDLE_URL,
    default_headers={
        "Accept": "*/*",
        "Referer": "https://www.cardekho.com/",
    },
    expected_response="bytes",
)


CARDEKHO_MODEL_PRICE: Final[ApiEndpoint] = ApiEndpoint(
    name="cardekho_model_price",
    method="GET",
    path="/api/v3/model/modelprice",
    default_params={
        "otherinfo": "all",
        "source": "web",
    },
)


CARDEKHO_APIS: Final[dict[str, ApiEndpoint]] = {
    CARDEKHO_NEW_CARS.name: CARDEKHO_NEW_CARS,
    CARDEKHO_BRAND_MODELS.name: CARDEKHO_BRAND_MODELS,
    CARDEKHO_MODEL_OVERVIEW.name: CARDEKHO_MODEL_OVERVIEW,
    CARDEKHO_MODEL_SPECS.name: CARDEKHO_MODEL_SPECS,
    CARDEKHO_CITIES_BUNDLE.name: CARDEKHO_CITIES_BUNDLE,
    CARDEKHO_MODEL_PRICE.name: CARDEKHO_MODEL_PRICE,
}
