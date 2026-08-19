from __future__ import annotations

from typing import Final

from src.external.constants.base import ApiEndpoint

BIKEDEKHO_API_BASE_URL: Final[str] = "https://api.bikedekho.com"

BIKEDEKHO_DEFAULT_HEADERS: Final[dict[str, str]] = {
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.bikedekho.com",
    "Referer": "https://www.bikedekho.com/",
}

BIKEDEKHO_NEW_BIKES: Final[ApiEndpoint] = ApiEndpoint(
    name="bikedekho_new_bikes",
    method="GET",
    path="/v1/pwa/newBikeLandingPages",
    default_params={
        "_format": "json",
        "lang_code": "en",
        "url": "/new-bikes",
        "source": "web",
    },
)

BIKEDEKHO_SCOOTERS: Final[ApiEndpoint] = ApiEndpoint(
    name="bikedekho_scooters",
    method="GET",
    path="/v1/pwa/newBikeLandingPages",
    default_params={
        "_format": "json",
        "url": "/scooters",
    },
)

BIKEDEKHO_BRAND_PAGE: Final[ApiEndpoint] = ApiEndpoint(
    name="bikedekho_brand_page",
    method="GET",
    path="/v1/pwa/brandPage",
    default_params={
        "_format": "json",
        "devicePlatform": "web",
    },
)

BIKEDEKHO_MODEL_OVERVIEW: Final[ApiEndpoint] = ApiEndpoint(
    name="bikedekho_model_overview",
    method="GET",
    path="/v1/pwa/modelOverview",
    default_params={
        "_format": "json",
        "devicePlatform": "web",
    },
)

BIKEDEKHO_TRIM_SPECS_FEATURES: Final[ApiEndpoint] = ApiEndpoint(
    name="bikedekho_trim_specs_features",
    method="GET",
    path="/v1/pwa/modelSpec",
    default_params={
        "_format": "json",
        "otherinfo": "all",
    },
)

BIKEDEKHO_APIS: Final[dict[str, ApiEndpoint]] = {
    BIKEDEKHO_NEW_BIKES.name: BIKEDEKHO_NEW_BIKES,
    BIKEDEKHO_SCOOTERS.name: BIKEDEKHO_SCOOTERS,
    BIKEDEKHO_BRAND_PAGE.name: BIKEDEKHO_BRAND_PAGE,
    BIKEDEKHO_MODEL_OVERVIEW.name: BIKEDEKHO_MODEL_OVERVIEW,
    BIKEDEKHO_TRIM_SPECS_FEATURES.name: BIKEDEKHO_TRIM_SPECS_FEATURES,
}
