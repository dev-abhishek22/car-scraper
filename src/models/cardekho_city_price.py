from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CardekhoCityPriceRange(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )

    display: str | None = None

    minimum_ex_showroom: int | None = Field(
        default=None,
        alias="minimumExShowroom",
        ge=0,
    )

    maximum_ex_showroom: int | None = Field(
        default=None,
        alias="maximumExShowroom",
        ge=0,
    )

    @model_validator(mode="after")
    def validate_range(
        self,
    ) -> Self:
        if (
            self.minimum_ex_showroom is not None
            and self.maximum_ex_showroom is not None
            and self.minimum_ex_showroom > self.maximum_ex_showroom
        ):
            raise ValueError(
                "minimumExShowroom cannot be greater than maximumExShowroom"
            )

        return self


class CardekhoCityPriceAccessoryItem(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    key: str | None = None

    name: str = Field(
        min_length=1,
    )

    amount: int = Field(
        ge=0,
    )

    display: str | None = None


class CardekhoCityPriceOptionalAccessories(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    total: int = Field(
        default=0,
        ge=0,
    )

    total_display: str | None = Field(
        default=None,
        alias="totalDisplay",
    )

    items: list[CardekhoCityPriceAccessoryItem] = Field(
        default_factory=list,
    )


class CardekhoCityPriceOtherChargeItem(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    key: str | None = None

    name: str = Field(
        min_length=1,
    )

    amount: int = Field(
        ge=0,
    )

    display: str | None = None


class CardekhoCityPriceOtherCharges(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    total: int = Field(
        default=0,
        ge=0,
    )

    total_display: str | None = Field(
        default=None,
        alias="totalDisplay",
    )

    items: list[CardekhoCityPriceOtherChargeItem] = Field(
        default_factory=list,
    )


class CardekhoCityPriceDifference(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    amount: int | None = Field(
        default=None,
        ge=0,
    )

    display: str | None = None


class CardekhoCityPriceAmounts(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )

    ex_showroom: int | None = Field(
        default=None,
        alias="exShowroom",
        ge=0,
    )

    rto: int | None = Field(
        default=None,
        ge=0,
    )

    insurance: int | None = Field(
        default=None,
        ge=0,
    )

    optional_accessories: CardekhoCityPriceOptionalAccessories | None = Field(
        default=None,
        alias="optionalAccessories",
    )

    other_charges: CardekhoCityPriceOtherCharges | None = Field(
        default=None,
        alias="otherCharges",
    )

    on_road_without_optional_accessories: int | None = Field(
        default=None,
        alias=("onRoadWithoutOptionalAccessories"),
        ge=0,
    )

    on_road: int | None = Field(
        default=None,
        alias="onRoad",
        ge=0,
    )

    difference_to_next_variant: CardekhoCityPriceDifference | None = Field(
        default=None,
        alias="differenceToNextVariant",
    )

    additional_price_data: dict[
        str,
        Any,
    ] = Field(
        default_factory=dict,
        alias="additionalPriceData",
    )


class CardekhoCityPriceEmi(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )

    monthly_amount: int | None = Field(
        default=None,
        alias="monthlyAmount",
        ge=0,
    )

    low_emi_applicable: bool | None = Field(
        default=None,
        alias="lowEmiApplicable",
    )

    low_monthly_amount: int | None = Field(
        default=None,
        alias="lowMonthlyAmount",
        ge=0,
    )

    interest_rate: float | None = Field(
        default=None,
        alias="interestRate",
        ge=0,
    )

    tenure_months: int | None = Field(
        default=None,
        alias="tenureMonths",
        ge=0,
    )

    down_payment: int | None = Field(
        default=None,
        alias="downPayment",
        ge=0,
    )

    loan_amount: int | None = Field(
        default=None,
        alias="loanAmount",
        ge=0,
    )

    interest_amount: int | None = Field(
        default=None,
        alias="interestAmount",
        ge=0,
    )

    payable_amount: int | None = Field(
        default=None,
        alias="payableAmount",
        ge=0,
    )


class CardekhoCityPriceDisplayPrices(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    ex_showroom: str | None = Field(
        default=None,
        alias="exShowroom",
    )

    on_road: str | None = Field(
        default=None,
        alias="onRoad",
    )

    on_road_without_optional_accessories: str | None = Field(
        default=None,
        alias=("onRoadWithoutOptionalAccessories"),
    )


class CardekhoCityPriceVariant(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    trim_id: int | None = Field(
        default=None,
        alias="trimId",
        gt=0,
    )

    trim_name: str | None = Field(
        default=None,
        alias="trimName",
    )

    trim_short_name: str | None = Field(
        default=None,
        alias="trimShortName",
    )

    trim_slug: str | None = Field(
        default=None,
        alias="trimSlug",
    )

    trim_status: str | None = Field(
        default=None,
        alias="trimStatus",
    )

    trim_url: str | None = Field(
        default=None,
        alias="trimUrl",
    )

    api_variant_name: str = Field(
        alias="apiVariantName",
        min_length=1,
    )

    api_variant_slug: str | None = Field(
        default=None,
        alias="apiVariantSlug",
    )

    variant_display_name: str | None = Field(
        default=None,
        alias="variantDisplayName",
    )

    variant_display_id: str | None = Field(
        default=None,
        alias="variantDisplayId",
    )

    fuel_type: str | None = Field(
        default=None,
        alias="fuelType",
    )

    price_type: str | None = Field(
        default=None,
        alias="priceType",
    )

    prices: CardekhoCityPriceAmounts

    emi: CardekhoCityPriceEmi | None = None

    display_prices: CardekhoCityPriceDisplayPrices | None = Field(
        default=None,
        alias="displayPrices",
    )

    variant_slug: str | None = Field(
        default=None,
        alias="variantSlug",
    )

    variant_url: str | None = Field(
        default=None,
        alias="variantUrl",
    )

    price_url: str | None = Field(
        default=None,
        alias="priceUrl",
    )

    tag: str | None = None

    top_selling: bool = Field(
        default=False,
        alias="topSelling",
    )

    is_recent_launch: bool = Field(
        default=False,
        alias="isRecentLaunch",
    )


class CardekhoCityPriceVariantStats(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )

    api_variants: int = Field(
        alias="apiVariants",
        ge=0,
    )

    stored_variants: int = Field(
        alias="storedVariants",
        ge=0,
    )

    matched_with_source_trims: int = Field(
        alias="matchedWithSourceTrims",
        ge=0,
    )

    unmatched_source_trims: int = Field(
        alias="unmatchedSourceTrims",
        ge=0,
    )

    unmatched_api_variants: int = Field(
        alias="unmatchedApiVariants",
        ge=0,
    )


class CardekhoCityPriceSource(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    car_document_id: str = Field(
        alias="carDocumentId",
        min_length=1,
    )

    car_run_id: str | None = Field(
        default=None,
        alias="carRunId",
    )

    city_document_id: str = Field(
        alias="cityDocumentId",
        min_length=1,
    )

    city_run_id: str | None = Field(
        default=None,
        alias="cityRunId",
    )


class CardekhoCityPriceRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    model_slug: str = Field(
        alias="modelSlug",
        min_length=1,
    )

    city_id: int = Field(
        alias="cityId",
        gt=0,
    )

    url: str = Field(
        min_length=1,
    )


class CardekhoCityPrice(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    model_id: int = Field(
        alias="modelId",
        gt=0,
    )

    model_name: str = Field(
        alias="modelName",
        min_length=1,
    )

    model_slug: str = Field(
        alias="modelSlug",
        min_length=1,
    )

    model_status: str = Field(
        alias="modelStatus",
        min_length=1,
    )

    brand_id: int = Field(
        alias="brandId",
        gt=0,
    )

    brand_name: str = Field(
        alias="brandName",
        min_length=1,
    )

    brand_slug: str = Field(
        alias="brandSlug",
        min_length=1,
    )

    car_slug: str = Field(
        alias="carSlug",
        min_length=1,
    )

    city_id: int = Field(
        alias="cityId",
        gt=0,
    )

    city_name: str = Field(
        alias="cityName",
        min_length=1,
    )

    city_display_name: str = Field(
        alias="cityDisplayName",
        min_length=1,
    )

    city_slug: str = Field(
        alias="citySlug",
        min_length=1,
    )

    is_popular_city: bool = Field(
        default=False,
        alias="isPopularCity",
    )

    price_available: bool = Field(
        alias="priceAvailable",
    )

    price_range: CardekhoCityPriceRange | None = Field(
        default=None,
        alias="priceRange",
    )

    price_detail_title: str | None = Field(
        default=None,
        alias="priceDetailTitle",
    )

    model_url: str | None = Field(
        default=None,
        alias="modelUrl",
    )

    price_url: str | None = Field(
        default=None,
        alias="priceUrl",
    )

    estimated_text: str | None = Field(
        default=None,
        alias="estimatedText",
    )

    fuel_types: list[str] = Field(
        default_factory=list,
        alias="fuelTypes",
    )

    transmission_types: list[str] = Field(
        default_factory=list,
        alias="transmissionTypes",
    )

    total_variants: int = Field(
        alias="totalVariants",
        ge=0,
    )

    variants: list[CardekhoCityPriceVariant] = Field(
        default_factory=list,
    )

    variant_stats: CardekhoCityPriceVariantStats = Field(
        alias="variantStats",
    )

    source: CardekhoCityPriceSource

    request: CardekhoCityPriceRequest

    scraped_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        alias="scrapedAt",
    )

    @property
    def document_id(
        self,
    ) -> str:
        return f"m:{self.model_id}:c:{self.city_id}"

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
