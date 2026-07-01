from __future__ import annotations

from typing import Final

from src.external.constants.base import ApiEndpoint

CARWALE_BASE_URL: Final[str] = "https://www.carwale.com"

CARWALE_DEFAULT_HEADERS: Final[dict[str, str]] = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-IN,en;q=0.9",
    "ServerDomain": "CarWale",
}

CARWALE_NEW_CARS: Final[ApiEndpoint] = ApiEndpoint(
    name="carwale_new_cars",
    method="GET",
    path="/api/newcarsdata/",
    default_params={
        "platformId": 1,
    },
    default_headers={
        "Referer": "https://www.carwale.com/new-cars/",
    },
)

CARWALE_MAKE_PAGE_DATA: Final[ApiEndpoint] = ApiEndpoint(
    name="carwale_make_page_data",
    method="GET",
    path="/api/makepagedata/",
    default_params={
        "cityId": 10,
        "areaId": 3657,
        "platformId": 1,
    },
    default_headers={
        "Accept": "*/*",
        "Referer": "https://www.carwale.com/",
    },
)

CARWALE_MODEL_PAGE_DATA: Final[ApiEndpoint] = ApiEndpoint(
    name="carwale_model_page_data",
    method="GET",
    path="/api/modelpagedata/",
    default_params={
        "cityId": 10,
        "areaId": 3657,
        "showOfferUpfront": "false",
        "platformId": 1,
    },
    default_headers={
        "Accept": "*/*",
        "Referer": "https://www.carwale.com/",
    },
)

CARWALE_CITIES: Final[ApiEndpoint] = ApiEndpoint(
    name="carwale_cities",
    method="GET",
    path="/api/cities",
    default_headers={
        "Referer": "https://www.carwale.com/",
    },
)

CARWALE_PIC_PAGE_DATA: Final[ApiEndpoint] = ApiEndpoint(
    name="carwale_pic_page_data",
    method="GET",
    path="/api/picpagedata/",
    default_headers={
        "Accept": "*/*",
    },
)

CARWALE_APIS: Final[dict[str, ApiEndpoint]] = {
    CARWALE_NEW_CARS.name: CARWALE_NEW_CARS,
    CARWALE_MAKE_PAGE_DATA.name: CARWALE_MAKE_PAGE_DATA,
    CARWALE_MODEL_PAGE_DATA.name: CARWALE_MODEL_PAGE_DATA,
    CARWALE_CITIES.name: CARWALE_CITIES,
    CARWALE_PIC_PAGE_DATA.name: CARWALE_PIC_PAGE_DATA,
}
