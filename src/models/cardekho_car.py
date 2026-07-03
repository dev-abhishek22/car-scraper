from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

SLUG_PATTERN = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
)

CarDekhoModelStatus = Literal[
    "CURRENT",
    "UPCOMING",
    "DISCONTINUED",
]


def _validate_positive_integer(
    value: Any,
    *,
    field_name: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")

    return value


def _validate_non_empty_string(
    value: Any,
    *,
    field_name: str,
) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")

    normalized_value = value.strip()

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    return normalized_value


def _normalize_optional_string(
    value: Any,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string or null")

    normalized_value = value.strip()

    return normalized_value or None


def _normalize_slug(
    value: Any,
    *,
    field_name: str,
) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")

    normalized_value = value.strip().lower().replace("_", "-").replace(" ", "-")

    normalized_value = re.sub(
        r"-+",
        "-",
        normalized_value,
    ).strip("-")

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    if not SLUG_PATTERN.fullmatch(
        normalized_value,
    ):
        raise ValueError(
            f"{field_name} contains invalid " f"characters: {normalized_value!r}"
        )

    return normalized_value


def _normalize_optional_slug(
    value: Any,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    return _normalize_slug(
        value,
        field_name=field_name,
    )


def _normalize_model_status(
    value: Any,
    *,
    field_name: str,
) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")

    normalized_value = value.strip().upper()

    if normalized_value not in {
        "CURRENT",
        "UPCOMING",
        "DISCONTINUED",
    }:
        raise ValueError(f"{field_name} must be CURRENT, " "UPCOMING, or DISCONTINUED")

    return normalized_value


class CarDekhoCarOverview(BaseModel):
    """
    Minimal model-level overview data returned by
    the CarDekho model-overview endpoint.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    display_name: str | None = Field(
        default=None,
        alias="displayName",
    )

    short_name: str | None = Field(
        default=None,
        alias="shortName",
    )

    model_url: str | None = Field(
        default=None,
        alias="modelUrl",
    )

    review_url: str | None = Field(
        default=None,
        alias="reviewUrl",
    )

    image: str | None = None

    webp_image: str | None = Field(
        default=None,
        alias="webpImage",
    )

    brand_logo: str | None = Field(
        default=None,
        alias="brandLogo",
    )

    rating: float | None = Field(
        default=None,
        ge=0,
    )

    review_count: int | None = Field(
        default=None,
        alias="reviewCount",
        ge=0,
    )


class CarDekhoCarVariant(BaseModel):
    """
    Minimal identity and linking data for one variant.

    Detailed prices, specifications, fuel, transmission,
    mileage, and features belong to the trims scraper.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    variant_id: int | None = Field(
        default=None,
        alias="id",
        gt=0,
    )

    name: str | None = None

    short_name: str | None = Field(
        default=None,
        alias="shortName",
    )

    slug: str | None = None

    url: str | None = None

    status: CarDekhoModelStatus

    @field_validator(
        "slug",
        mode="before",
    )
    @classmethod
    def normalize_slug(
        cls,
        value: Any,
    ) -> str | None:
        return _normalize_optional_slug(
            value,
            field_name="variant.slug",
        )

    @field_validator(
        "status",
        mode="before",
    )
    @classmethod
    def normalize_status(
        cls,
        value: Any,
    ) -> str:
        return _normalize_model_status(
            value,
            field_name="variant.status",
        )

    @model_validator(
        mode="after",
    )
    def validate_identity(
        self,
    ) -> Self:
        if self.variant_id is None and self.slug is None:
            raise ValueError("Variant must contain an id or slug")

        return self


class CarDekhoRelatedCar(BaseModel):
    """
    Minimal related-car structure used by both:

    - compareWith
    - similarCars
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    brand_name: str | None = Field(
        default=None,
        alias="brandName",
    )

    brand_slug: str = Field(
        alias="brandSlug",
        min_length=1,
    )

    model_name: str | None = Field(
        default=None,
        alias="modelName",
    )

    short_name: str | None = Field(
        default=None,
        alias="shortName",
    )

    model_slug: str = Field(
        alias="modelSlug",
        min_length=1,
    )

    car_slug: str = Field(
        alias="carSlug",
        min_length=1,
    )

    model_url: str | None = Field(
        default=None,
        alias="modelUrl",
    )

    comparison_url: str | None = Field(
        default=None,
        alias="comparisonUrl",
    )

    compare_text: str | None = Field(
        default=None,
        alias="compareText",
    )

    image: str | None = None

    webp_image: str | None = Field(
        default=None,
        alias="webpImage",
    )

    @field_validator(
        "brand_slug",
        mode="before",
    )
    @classmethod
    def normalize_brand_slug(
        cls,
        value: Any,
    ) -> str:
        return _normalize_slug(
            value,
            field_name="related_car.brandSlug",
        )

    @field_validator(
        "model_slug",
        mode="before",
    )
    @classmethod
    def normalize_model_slug(
        cls,
        value: Any,
    ) -> str:
        return _normalize_slug(
            value,
            field_name="related_car.modelSlug",
        )

    @field_validator(
        "car_slug",
        mode="before",
    )
    @classmethod
    def normalize_car_slug(
        cls,
        value: Any,
    ) -> str:
        return _normalize_slug(
            value,
            field_name="related_car.carSlug",
        )

    @model_validator(
        mode="after",
    )
    def validate_car_slug(
        self,
    ) -> Self:
        expected_car_slug = f"{self.brand_slug}-" f"{self.model_slug}"

        if self.car_slug != expected_car_slug:
            raise ValueError(
                "Related car carSlug does not match "
                "brandSlug and modelSlug: "
                f"expected={expected_car_slug!r}, "
                f"found={self.car_slug!r}"
            )

        return self


class CarDekhoOldGenerationComparison(BaseModel):
    """
    Optional comparison with an older generation of
    the same model.

    Some API responses provide a complete object while
    others provide only an HTML comparison link.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    model_name: str | None = Field(
        default=None,
        alias="modelName",
    )

    brand_slug: str | None = Field(
        default=None,
        alias="brandSlug",
    )

    model_slug: str | None = Field(
        default=None,
        alias="modelSlug",
    )

    car_slug: str | None = Field(
        default=None,
        alias="carSlug",
    )

    compare_text: str | None = Field(
        default=None,
        alias="compareText",
    )

    badge_text: str | None = Field(
        default=None,
        alias="badgeText",
    )

    comparison_url: str | None = Field(
        default=None,
        alias="comparisonUrl",
    )

    image: str | None = None

    @field_validator(
        "brand_slug",
        mode="before",
    )
    @classmethod
    def normalize_brand_slug(
        cls,
        value: Any,
    ) -> str | None:
        return _normalize_optional_slug(
            value,
            field_name=("old_generation_comparison.brandSlug"),
        )

    @field_validator(
        "model_slug",
        mode="before",
    )
    @classmethod
    def normalize_model_slug(
        cls,
        value: Any,
    ) -> str | None:
        return _normalize_optional_slug(
            value,
            field_name=("old_generation_comparison.modelSlug"),
        )

    @field_validator(
        "car_slug",
        mode="before",
    )
    @classmethod
    def normalize_car_slug(
        cls,
        value: Any,
    ) -> str | None:
        return _normalize_optional_slug(
            value,
            field_name=("old_generation_comparison.carSlug"),
        )

    @model_validator(
        mode="after",
    )
    def validate_identity(
        self,
    ) -> Self:
        if not any(
            (
                self.model_name,
                self.car_slug,
                self.compare_text,
                self.badge_text,
                self.comparison_url,
                self.image,
            )
        ):
            raise ValueError("Old-generation comparison cannot " "be empty")

        if self.car_slug is not None:
            if self.brand_slug is None or self.model_slug is None:
                raise ValueError(
                    "Old-generation brandSlug and "
                    "modelSlug are required when "
                    "carSlug is present"
                )

            expected_car_slug = f"{self.brand_slug}-" f"{self.model_slug}"

            if self.car_slug != expected_car_slug:
                raise ValueError(
                    "Old-generation carSlug does not "
                    "match brandSlug and modelSlug: "
                    f"expected={expected_car_slug!r}, "
                    f"found={self.car_slug!r}"
                )

        return self


class CarDekhoCar(BaseModel):
    """
    MongoDB representation of one CarDekho model
    overview.

    One document represents one CarDekho model.

    Example document ID:

        model:3289
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    document_id: str = Field(
        alias="_id",
        min_length=1,
    )

    model_id: int = Field(
        alias="id",
        gt=0,
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

    name: str = Field(
        min_length=1,
    )

    slug: str = Field(
        min_length=1,
    )

    car_slug: str = Field(
        alias="carSlug",
        min_length=1,
    )

    model_name: str = Field(
        alias="modelName",
        min_length=1,
    )

    model_status: CarDekhoModelStatus = Field(
        alias="modelStatus",
    )

    is_upcoming: bool = Field(
        alias="isUpcoming",
    )

    expected_launch_date: str | None = Field(
        default=None,
        alias="expectedLaunchDate",
    )

    overview: CarDekhoCarOverview

    total_variants: int = Field(
        alias="totalVariants",
        ge=0,
    )

    variants: list[CarDekhoCarVariant] = Field(
        default_factory=list,
    )

    total_comparisons: int = Field(
        alias="totalComparisons",
        ge=0,
    )

    compare_with: list[CarDekhoRelatedCar] = Field(
        default_factory=list,
        alias="compareWith",
    )

    total_similar_cars: int = Field(
        alias="totalSimilarCars",
        ge=0,
    )

    similar_cars: list[CarDekhoRelatedCar] = Field(
        default_factory=list,
        alias="similarCars",
    )

    old_generation_comparison: CarDekhoOldGenerationComparison | None = Field(
        default=None,
        alias="oldGenerationComparison",
    )

    last_run_id: str = Field(
        alias="lastRunId",
        min_length=1,
    )

    source_model_run_id: str | None = Field(
        default=None,
        alias="sourceModelRunId",
    )

    source_model_document_id: str = Field(
        alias="sourceModelDocumentId",
        min_length=1,
    )

    scraped_at: datetime = Field(
        alias="scrapedAt",
    )

    created_at: datetime = Field(
        alias="createdAt",
    )

    updated_at: datetime = Field(
        alias="updatedAt",
    )

    @field_validator(
        "brand_slug",
        mode="before",
    )
    @classmethod
    def normalize_brand_slug(
        cls,
        value: Any,
    ) -> str:
        return _normalize_slug(
            value,
            field_name="brandSlug",
        )

    @field_validator(
        "slug",
        mode="before",
    )
    @classmethod
    def normalize_model_slug(
        cls,
        value: Any,
    ) -> str:
        return _normalize_slug(
            value,
            field_name="slug",
        )

    @field_validator(
        "car_slug",
        mode="before",
    )
    @classmethod
    def normalize_car_slug(
        cls,
        value: Any,
    ) -> str:
        return _normalize_slug(
            value,
            field_name="carSlug",
        )

    @field_validator(
        "model_status",
        mode="before",
    )
    @classmethod
    def normalize_status(
        cls,
        value: Any,
    ) -> str:
        return _normalize_model_status(
            value,
            field_name="modelStatus",
        )

    @field_validator(
        "expected_launch_date",
        mode="before",
    )
    @classmethod
    def normalize_expected_launch_date(
        cls,
        value: Any,
    ) -> str | None:
        return _normalize_optional_string(
            value,
            field_name="expectedLaunchDate",
        )

    @field_validator(
        "source_model_run_id",
        mode="before",
    )
    @classmethod
    def normalize_source_model_run_id(
        cls,
        value: Any,
    ) -> str | None:
        return _normalize_optional_string(
            value,
            field_name="sourceModelRunId",
        )

    @model_validator(
        mode="after",
    )
    def validate_document(
        self,
    ) -> Self:
        expected_document_id = self.build_document_id(
            self.model_id,
        )

        if self.document_id != expected_document_id:
            raise ValueError(
                "CarDekho car document ID does not "
                "match id: "
                f"expected={expected_document_id!r}, "
                f"found={self.document_id!r}"
            )

        expected_source_document_id = self.build_document_id(
            self.model_id,
        )

        if self.source_model_document_id != expected_source_document_id:
            raise ValueError(
                "sourceModelDocumentId does not "
                "match the model ID: "
                f"expected="
                f"{expected_source_document_id!r}, "
                f"found="
                f"{self.source_model_document_id!r}"
            )

        expected_car_slug = f"{self.brand_slug}-" f"{self.slug}"

        if self.car_slug != expected_car_slug:
            raise ValueError(
                "CarDekho car carSlug does not "
                "match brandSlug and slug: "
                f"expected={expected_car_slug!r}, "
                f"found={self.car_slug!r}"
            )

        expected_is_upcoming = self.model_status == "UPCOMING"

        if self.is_upcoming != expected_is_upcoming:
            raise ValueError(
                "isUpcoming does not match " f"modelStatus={self.model_status!r}"
            )

        if (
            self.model_status
            in {
                "CURRENT",
                "DISCONTINUED",
            }
            and self.expected_launch_date is not None
        ):
            raise ValueError(
                "Current and discontinued cars " "cannot have expectedLaunchDate"
            )

        if self.total_variants != len(self.variants):
            raise ValueError(
                "totalVariants does not match "
                "the variants array length: "
                f"expected={len(self.variants)}, "
                f"found={self.total_variants}"
            )

        if self.total_comparisons != len(self.compare_with):
            raise ValueError(
                "totalComparisons does not match "
                "the compareWith array length: "
                f"expected={len(self.compare_with)}, "
                f"found={self.total_comparisons}"
            )

        if self.total_similar_cars != len(self.similar_cars):
            raise ValueError(
                "totalSimilarCars does not match "
                "the similarCars array length: "
                f"expected={len(self.similar_cars)}, "
                f"found={self.total_similar_cars}"
            )

        self._validate_unique_variants()
        self._validate_unique_related_cars(
            cars=self.compare_with,
            field_name="compareWith",
        )
        self._validate_unique_related_cars(
            cars=self.similar_cars,
            field_name="similarCars",
        )

        return self

    def _validate_unique_variants(
        self,
    ) -> None:
        seen_ids: set[int] = set()
        seen_slugs: set[str] = set()

        for variant in self.variants:
            if variant.variant_id is not None:
                if variant.variant_id in seen_ids:
                    raise ValueError(
                        "variants contains duplicate " f"id={variant.variant_id}"
                    )

                seen_ids.add(
                    variant.variant_id,
                )

            if variant.slug is not None:
                if variant.slug in seen_slugs:
                    raise ValueError(
                        "variants contains duplicate " f"slug={variant.slug!r}"
                    )

                seen_slugs.add(
                    variant.slug,
                )

    @staticmethod
    def _validate_unique_related_cars(
        *,
        cars: list[CarDekhoRelatedCar],
        field_name: str,
    ) -> None:
        seen_car_slugs: set[str] = set()

        for car in cars:
            if car.car_slug in seen_car_slugs:
                raise ValueError(
                    f"{field_name} contains duplicate " f"carSlug={car.car_slug!r}"
                )

            seen_car_slugs.add(
                car.car_slug,
            )

    @staticmethod
    def build_document_id(
        model_id: int,
    ) -> str:
        normalized_model_id = _validate_positive_integer(
            model_id,
            field_name="model_id",
        )

        return f"model:{normalized_model_id}"

    @classmethod
    def create(
        cls,
        *,
        model: Mapping[str, Any],
        car_data: Mapping[str, Any],
        run_id: str,
        source_model_run_id: str | None = None,
        created_at: datetime | None = None,
    ) -> Self:
        if not isinstance(model, Mapping):
            raise ValueError("model must be an object")

        if not isinstance(car_data, Mapping):
            raise ValueError("car_data must be an object")

        normalized_run_id = _validate_non_empty_string(
            run_id,
            field_name="run_id",
        )

        model_id = _validate_positive_integer(
            model.get("id"),
            field_name="model.id",
        )

        brand_id = _validate_positive_integer(
            model.get("brandId"),
            field_name="model.brandId",
        )

        brand_name = _validate_non_empty_string(
            model.get("brandName"),
            field_name="model.brandName",
        )

        brand_slug = _normalize_slug(
            model.get("brandSlug"),
            field_name="model.brandSlug",
        )

        name = _validate_non_empty_string(
            model.get("name"),
            field_name="model.name",
        )

        slug = _normalize_slug(
            model.get("slug"),
            field_name="model.slug",
        )

        model_name = _validate_non_empty_string(
            model.get("modelName"),
            field_name="model.modelName",
        )

        model_status = _normalize_model_status(
            model.get("modelStatus"),
            field_name="model.modelStatus",
        )

        is_upcoming = model.get("isUpcoming")

        if not isinstance(is_upcoming, bool):
            raise ValueError("model.isUpcoming must be a boolean")

        expected_is_upcoming = model_status == "UPCOMING"

        if is_upcoming != expected_is_upcoming:
            raise ValueError(
                "model.isUpcoming does not match " f"modelStatus={model_status!r}"
            )

        expected_launch_date = _normalize_optional_string(
            model.get("expectedLaunchDate"),
            field_name=("model.expectedLaunchDate"),
        )

        if (
            model_status
            in {
                "CURRENT",
                "DISCONTINUED",
            }
            and expected_launch_date is not None
        ):
            raise ValueError(
                "Current and discontinued models " "cannot have expectedLaunchDate"
            )

        resolved_source_model_run_id = source_model_run_id

        if resolved_source_model_run_id is None:
            resolved_source_model_run_id = model.get("lastRunId")

        normalized_source_model_run_id = _normalize_optional_string(
            resolved_source_model_run_id,
            field_name=("source_model_run_id"),
        )

        source_model_document_id = model.get("_id")

        if source_model_document_id is None:
            source_model_document_id = cls.build_document_id(
                model_id,
            )

        normalized_source_model_document_id = _validate_non_empty_string(
            source_model_document_id,
            field_name=("model._id"),
        )

        overview = car_data.get("overview")

        if not isinstance(overview, Mapping):
            raise ValueError("car_data.overview must be an object")

        raw_variants = car_data.get(
            "variants",
            [],
        )

        raw_compare_with = car_data.get(
            "compareWith",
            [],
        )

        raw_similar_cars = car_data.get(
            "similarCars",
            [],
        )

        if not isinstance(raw_variants, list):
            raise ValueError("car_data.variants must be an array")

        if not isinstance(raw_compare_with, list):
            raise ValueError("car_data.compareWith must be an array")

        if not isinstance(raw_similar_cars, list):
            raise ValueError("car_data.similarCars must be an array")

        total_variants = car_data.get(
            "totalVariants",
            len(raw_variants),
        )

        total_comparisons = car_data.get(
            "totalComparisons",
            len(raw_compare_with),
        )

        total_similar_cars = car_data.get(
            "totalSimilarCars",
            len(raw_similar_cars),
        )

        current_time = datetime.now(
            timezone.utc,
        )

        initial_created_at = created_at if created_at is not None else current_time

        return cls(
            _id=cls.build_document_id(
                model_id,
            ),
            id=model_id,
            brandId=brand_id,
            brandName=brand_name,
            brandSlug=brand_slug,
            name=name,
            slug=slug,
            carSlug=f"{brand_slug}-{slug}",
            modelName=model_name,
            modelStatus=model_status,
            isUpcoming=is_upcoming,
            expectedLaunchDate=(expected_launch_date),
            overview=dict(overview),
            totalVariants=total_variants,
            variants=raw_variants,
            totalComparisons=total_comparisons,
            compareWith=raw_compare_with,
            totalSimilarCars=total_similar_cars,
            similarCars=raw_similar_cars,
            oldGenerationComparison=(
                car_data.get(
                    "oldGenerationComparison",
                )
            ),
            lastRunId=normalized_run_id,
            sourceModelRunId=(normalized_source_model_run_id),
            sourceModelDocumentId=(normalized_source_model_document_id),
            scrapedAt=current_time,
            createdAt=initial_created_at,
            updatedAt=current_time,
        )

    def to_mongo_document(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            mode="python",
        )
