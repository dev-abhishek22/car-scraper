from __future__ import annotations

from enum import StrEnum


GOODRETURNS_BASE_URL = "https://www.goodreturns.in"
GOODRETURNS_FUEL_GRAPH_PATH = "/fuel-graph-data.html"


class GoodReturnsFuelType(StrEnum):
    PETROL = "petrol"
    DIESEL = "diesel"
    CNG = "cng"


class GoodReturnsTimeframe(StrEnum):
    ONE_MONTH = "1M"
    THREE_MONTHS = "3M"
    SIX_MONTHS = "6M"
    ONE_YEAR = "1Y"


GOODRETURNS_FUEL_TYPES = {
    GoodReturnsFuelType.PETROL.value,
    GoodReturnsFuelType.DIESEL.value,
    GoodReturnsFuelType.CNG.value,
}


GOODRETURNS_TIMEFRAMES = {
    GoodReturnsTimeframe.ONE_MONTH.value,
    GoodReturnsTimeframe.THREE_MONTHS.value,
    GoodReturnsTimeframe.SIX_MONTHS.value,
    GoodReturnsTimeframe.ONE_YEAR.value,
}


GOODRETURNS_DEFAULT_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en;q=0.8",
    "X-Oigt-Header": "GITPL",
    "X-Requested-With": "XMLHttpRequest",
}
