from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

STANDARD_SLUG_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"

CARDEKHO_CITY_URL_SLUG_PATTERN = (
    r"^[a-z0-9]+" r"(?:-[a-z0-9]+)*" r"(?:-\([a-z0-9]+(?:-[a-z0-9]+)*\))?$"
)

CARDEKHO_CURRENT_STATUS = "CURRENT"


class CardekhoCityPriceSourceTrim(BaseModel):
    """
    Compact source-trim snapshot used to
    enrich API price variants.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    trim_id: int = Field(
        gt=0,
    )

    name: str = Field(
        min_length=1,
    )

    short_name: str = Field(
        min_length=1,
    )

    slug: str = Field(
        min_length=1,
        pattern=STANDARD_SLUG_PATTERN,
    )

    url: str = Field(
        min_length=1,
    )

    status: Literal["CURRENT"] = CARDEKHO_CURRENT_STATUS


class CardekhoCityPriceJob(BaseModel):
    """
    One Cardekho model-city price request.

    Permanent job identity:
        m:{model_id}:c:{city_id}

    Cardekho city URLs sometimes preserve a
    parenthesized region suffix:

        Saharanpur (UP)
            -> saharanpur-(up)

        Hamirpur (HP)
            -> hamirpur-(hp)

        Mandvi (Kachchh)
            -> mandvi-(kachchh)
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    model_id: int = Field(
        gt=0,
    )

    model_name: str = Field(
        min_length=1,
    )

    model_slug: str = Field(
        min_length=1,
        pattern=STANDARD_SLUG_PATTERN,
    )

    model_status: Literal["CURRENT"] = CARDEKHO_CURRENT_STATUS

    brand_id: int = Field(
        gt=0,
    )

    brand_name: str = Field(
        min_length=1,
    )

    brand_slug: str = Field(
        min_length=1,
        pattern=STANDARD_SLUG_PATTERN,
    )

    car_slug: str = Field(
        min_length=1,
        pattern=STANDARD_SLUG_PATTERN,
    )

    city_id: int = Field(
        gt=0,
    )

    city_name: str = Field(
        min_length=1,
    )

    city_display_name: str = Field(
        min_length=1,
    )

    city_slug: str = Field(
        min_length=1,
        pattern=(CARDEKHO_CITY_URL_SLUG_PATTERN),
    )

    is_popular_city: bool = False

    source_car_document_id: str = Field(
        min_length=1,
    )

    source_car_run_id: str | None = None

    source_city_document_id: str = Field(
        min_length=1,
    )

    source_city_run_id: str | None = None

    source_trims: tuple[
        CardekhoCityPriceSourceTrim,
        ...,
    ] = Field(
        default_factory=tuple,
    )

    @property
    def item_key(
        self,
    ) -> str:
        return f"m:{self.model_id}:c:{self.city_id}"

    @property
    def request_url_value(
        self,
    ) -> str:
        return f"{self.brand_slug}/{self.model_slug}/price-in-{self.city_slug}"

    @property
    def source_trim_count(
        self,
    ) -> int:
        return len(self.source_trims)
