from __future__ import annotations

import re
import unicodedata
from collections.abc import AsyncIterator, Mapping
from dataclasses import dataclass
from typing import Any

from src.databases.mongodb import mongo_connection
from src.models.cardekho_city_price_job import (
    CardekhoCityPriceJob,
    CardekhoCityPriceSourceTrim,
)

CARDEKHO_CARS_COLLECTION = "cardekho_cars"
CARDEKHO_CITIES_COLLECTION = "cardekho_cities"

CURRENT_STATUS = "CURRENT"

MULTIPLE_HYPHENS_PATTERN = re.compile(r"-+")

CITY_REGION_SUFFIX_PATTERN = re.compile(r"^(.*?)\s*\(([^()]+)\)\s*$")


class CardekhoCityPriceJobSourceError(
    ValueError,
):
    """
    Raised when MongoDB city-price source
    data is unavailable or invalid.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class _CardekhoCitySource:
    city_id: int
    city_name: str
    city_display_name: str
    city_slug: str
    is_popular: bool
    tier: int | None
    source_document_id: str
    source_run_id: str | None


def _slugify(
    value: str,
) -> str:
    """
    Build a standard lowercase URL slug.

    This formatter removes parentheses and is
    used for brands, models, cars, trims, and
    city-filter comparisons.
    """

    normalized_unicode = unicodedata.normalize(
        "NFKD",
        value,
    )

    ascii_value = normalized_unicode.encode(
        "ascii",
        "ignore",
    ).decode("ascii")

    normalized_value = re.sub(
        r"[^a-zA-Z0-9]+",
        "-",
        ascii_value,
    ).lower()

    return MULTIPLE_HYPHENS_PATTERN.sub(
        "-",
        normalized_value,
    ).strip("-")


def _cardekho_city_url_slug(
    value: str,
) -> str:
    """
    Build the city value Cardekho expects inside
    model-price page URLs.

    Cardekho preserves a final parenthesized
    region suffix:

        Saharanpur (UP)
            -> saharanpur-(up)

        Hamirpur (HP)
            -> hamirpur-(hp)

        Mandvi (Kachchh)
            -> mandvi-(kachchh)

        New Delhi
            -> new-delhi
    """

    normalized_value = value.strip()

    if not normalized_value:
        return ""

    region_match = CITY_REGION_SUFFIX_PATTERN.fullmatch(normalized_value)

    if region_match is None:
        return _slugify(normalized_value)

    city_part = _slugify(region_match.group(1))

    region_part = _slugify(region_match.group(2))

    if not city_part or not region_part:
        return _slugify(normalized_value)

    return f"{city_part}-({region_part})"


def _normalize_optional_slug(
    value: str | None,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    if not isinstance(
        value,
        str,
    ):
        raise ValueError(f"{field_name} must be a string or null")

    normalized_value = _slugify(value)

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    return normalized_value


def _normalize_optional_positive_integer(
    value: int | None,
    *,
    field_name: str,
) -> int | None:
    if value is None:
        return None

    if (
        isinstance(
            value,
            bool,
        )
        or not isinstance(
            value,
            int,
        )
        or value <= 0
    ):
        raise ValueError(f"{field_name} must be a positive integer")

    return value


def _normalize_optional_string(
    value: Any,
) -> str | None:
    if not isinstance(
        value,
        str,
    ):
        return None

    normalized_value = value.strip()

    return normalized_value or None


def _positive_integer_or_none(
    value: Any,
) -> int | None:
    if (
        isinstance(
            value,
            bool,
        )
        or not isinstance(
            value,
            int,
        )
        or value <= 0
    ):
        return None

    return value


def _normalize_url(
    value: Any,
) -> str | None:
    normalized_value = _normalize_optional_string(value)

    if normalized_value is None:
        return None

    if not normalized_value.startswith("/"):
        normalized_value = f"/{normalized_value}"

    return normalized_value


def _extract_alias_values(
    value: Any,
) -> set[str]:
    """
    Build standard slugs for city-filter
    matching.

    These values are not used directly in the
    Cardekho request URL.
    """

    aliases: set[str] = set()

    if not isinstance(
        value,
        list,
    ):
        return aliases

    for item in value:
        if isinstance(
            item,
            str,
        ):
            normalized_alias = _slugify(item)

            if normalized_alias:
                aliases.add(normalized_alias)

            continue

        if not isinstance(
            item,
            Mapping,
        ):
            continue

        for field_name in (
            "name",
            "displayName",
            "value",
            "label",
            "slug",
            "cityName",
        ):
            raw_alias = item.get(field_name)

            if not isinstance(
                raw_alias,
                str,
            ):
                continue

            normalized_alias = _slugify(raw_alias)

            if normalized_alias:
                aliases.add(normalized_alias)

    return aliases


def _resolve_city_slug(
    document: Mapping[
        str,
        Any,
    ],
    *,
    city_name: str,
    city_display_name: str,
) -> str | None:
    """
    Resolve the exact city value used in the
    Cardekho page/API URL.

    Prefer an explicitly stored URL field. When
    one is unavailable, derive the value from
    displayName or cityName while preserving a
    final parenthesized region suffix.
    """

    for field_name in (
        "citySlug",
        "slug",
        "cityMaskingName",
    ):
        value = document.get(field_name)

        if not isinstance(
            value,
            str,
        ):
            continue

        normalized_slug = _cardekho_city_url_slug(value)

        if normalized_slug:
            return normalized_slug

    for value in (
        city_display_name,
        city_name,
    ):
        normalized_slug = _cardekho_city_url_slug(value)

        if normalized_slug:
            return normalized_slug

    aliases = document.get("aliases")

    if isinstance(
        aliases,
        list,
    ):
        for alias in aliases:
            if not isinstance(
                alias,
                str,
            ):
                continue

            normalized_slug = _cardekho_city_url_slug(alias)

            if normalized_slug:
                return normalized_slug

    return None


def _city_matches_filter(
    document: Mapping[
        str,
        Any,
    ],
    *,
    selected_city: str | None,
    resolved_city_slug: str,
    city_name: str,
    city_display_name: str,
) -> bool:
    if selected_city is None:
        return True

    candidate_slugs = {
        _slugify(resolved_city_slug),
        _slugify(city_name),
        _slugify(city_display_name),
    }

    candidate_slugs.update(_extract_alias_values(document.get("aliases")))

    candidate_slugs.discard("")

    return selected_city in candidate_slugs


def _parse_city_document(
    document: Mapping[
        str,
        Any,
    ],
    *,
    selected_city: str | None,
) -> _CardekhoCitySource | None:
    city_id = _positive_integer_or_none(document.get("cityId"))

    if city_id is None:
        return None

    city_name = _normalize_optional_string(document.get("cityName"))

    city_display_name = _normalize_optional_string(document.get("displayName"))

    if city_name is None:
        city_name = city_display_name

    if city_display_name is None:
        city_display_name = city_name

    if city_name is None or city_display_name is None:
        return None

    city_slug = _resolve_city_slug(
        document,
        city_name=city_name,
        city_display_name=(city_display_name),
    )

    if city_slug is None:
        return None

    if not _city_matches_filter(
        document,
        selected_city=(selected_city),
        resolved_city_slug=(city_slug),
        city_name=city_name,
        city_display_name=(city_display_name),
    ):
        return None

    source_document_id = (
        _normalize_optional_string(document.get("_id")) or f"city:{city_id}"
    )

    is_popular_value = document.get(
        "isPopular",
        False,
    )

    is_popular = is_popular_value is True or is_popular_value == 1

    tier_value = document.get("tier")

    tier = (
        tier_value
        if isinstance(tier_value, int) and not isinstance(tier_value, bool)
        else None
    )

    return _CardekhoCitySource(
        city_id=city_id,
        city_name=city_name,
        city_display_name=(city_display_name),
        city_slug=city_slug,
        is_popular=is_popular,
        tier=tier,
        source_document_id=(source_document_id),
        source_run_id=(_normalize_optional_string(document.get("lastRunId"))),
    )


async def _load_cardekho_cities(
    *,
    selected_city: str | None,
    selected_city_id: int | None,
    selected_tier: int | None,
    popular_cities_only: bool,
) -> list[_CardekhoCitySource]:
    await mongo_connection.connect()

    collection = mongo_connection.collection(CARDEKHO_CITIES_COLLECTION)

    query: dict[
        str,
        Any,
    ] = {
        "isDeleted": {
            "$ne": True,
        },
    }

    if selected_city_id is not None:
        query["cityId"] = selected_city_id

    if popular_cities_only:
        query["isPopular"] = {
            "$in": [
                True,
                1,
            ],
        }

    if selected_tier is not None:
        query["tier"] = selected_tier

    cursor = collection.find(
        query,
        {
            "_id": 1,
            "cityId": 1,
            "cityName": 1,
            "displayName": 1,
            "citySlug": 1,
            "slug": 1,
            "cityMaskingName": 1,
            "aliases": 1,
            "tier": 1,
            "isPopular": 1,
            "lastRunId": 1,
        },
    ).sort(
        "cityId",
        1,
    )

    cities: list[_CardekhoCitySource] = []

    seen_city_ids: set[int] = set()

    async for document in cursor:
        city = _parse_city_document(
            document,
            selected_city=(selected_city),
        )

        if city is None:
            continue

        if city.city_id in seen_city_ids:
            continue

        seen_city_ids.add(city.city_id)

        cities.append(city)

    if cities:
        return cities

    filters: list[str] = []

    if selected_city is not None:
        filters.append(f"city={selected_city!r}")

    if selected_city_id is not None:
        filters.append(f"city_id={selected_city_id}")

    if popular_cities_only:
        filters.append("popular_cities_only=True")

    filter_text = f" for {', '.join(filters)}" if filters else ""

    raise CardekhoCityPriceJobSourceError(
        "No active Cardekho cities "
        "were found in MongoDB"
        f"{filter_text}. "
        "Run cardekho-cities first."
    )


def _parse_source_trim(
    raw_trim: Mapping[
        str,
        Any,
    ],
) -> CardekhoCityPriceSourceTrim | None:
    status = _normalize_optional_string(raw_trim.get("status"))

    if status is None or status.upper() != CURRENT_STATUS:
        return None

    trim_id = _positive_integer_or_none(raw_trim.get("id"))

    name = _normalize_optional_string(raw_trim.get("name"))

    short_name = _normalize_optional_string(raw_trim.get("shortName")) or name

    slug_value = _normalize_optional_string(raw_trim.get("slug"))

    slug = _slugify(slug_value) if slug_value is not None else ""

    url = _normalize_url(raw_trim.get("url"))

    if trim_id is None or name is None or short_name is None or not slug or url is None:
        return None

    try:
        return CardekhoCityPriceSourceTrim(
            trim_id=trim_id,
            name=name,
            short_name=(short_name),
            slug=slug,
            url=url,
            status=(CURRENT_STATUS),
        )

    except (
        TypeError,
        ValueError,
    ):
        return None


def _parse_source_trims(
    value: Any,
) -> tuple[
    CardekhoCityPriceSourceTrim,
    ...,
]:
    if not isinstance(
        value,
        list,
    ):
        return ()

    source_trims: list[CardekhoCityPriceSourceTrim] = []

    seen_trim_ids: set[int] = set()

    seen_trim_slugs: set[str] = set()

    for raw_trim in value:
        if not isinstance(
            raw_trim,
            Mapping,
        ):
            continue

        source_trim = _parse_source_trim(raw_trim)

        if source_trim is None:
            continue

        if source_trim.trim_id in seen_trim_ids:
            continue

        if source_trim.slug in seen_trim_slugs:
            continue

        seen_trim_ids.add(source_trim.trim_id)

        seen_trim_slugs.add(source_trim.slug)

        source_trims.append(source_trim)

    return tuple(source_trims)


def _build_car_query(
    *,
    selected_brand: str | None,
    selected_model: str | None,
    selected_model_id: int | None,
) -> dict[
    str,
    Any,
]:
    query: dict[
        str,
        Any,
    ] = {
        "modelStatus": (CURRENT_STATUS),
    }

    if selected_brand is not None:
        query["brandSlug"] = selected_brand

    if selected_model is not None:
        query["slug"] = selected_model

    if selected_model_id is not None:
        query["id"] = selected_model_id

    return query


async def iter_cardekho_city_price_jobs(
    *,
    selected_brand: str | None = None,
    selected_model: str | None = None,
    selected_model_id: int | None = None,
    selected_city: str | None = None,
    selected_city_id: int | None = None,
    selected_tier: int | None,
    popular_cities_only: bool = False,
    max_jobs: int | None = None,
) -> AsyncIterator[CardekhoCityPriceJob]:
    """
    Generate one job for every unique
    CURRENT model-city combination.

    Input collections:
        cardekho_cars
        cardekho_cities
    """

    normalized_brand = _normalize_optional_slug(
        selected_brand,
        field_name=("selected_brand"),
    )

    normalized_model = _normalize_optional_slug(
        selected_model,
        field_name=("selected_model"),
    )

    normalized_model_id = _normalize_optional_positive_integer(
        selected_model_id,
        field_name=("selected_model_id"),
    )

    normalized_city = _normalize_optional_slug(
        selected_city,
        field_name=("selected_city"),
    )

    normalized_city_id = _normalize_optional_positive_integer(
        selected_city_id,
        field_name=("selected_city_id"),
    )

    normalized_tier = _normalize_optional_positive_integer(
        selected_tier,
        field_name=("selected_tier"),
    )

    if normalized_tier is not None and normalized_tier > 3:
        raise ValueError("selected_tier must be between 1 and 3")

    if normalized_model is not None and normalized_brand is None:
        raise ValueError("selected_model requires selected_brand")

    if not isinstance(
        popular_cities_only,
        bool,
    ):
        raise ValueError("popular_cities_only must be a boolean")

    if max_jobs is not None and (
        isinstance(
            max_jobs,
            bool,
        )
        or not isinstance(
            max_jobs,
            int,
        )
        or max_jobs < 1
    ):
        raise ValueError("max_jobs must be greater than zero")

    cities = await _load_cardekho_cities(
        selected_city=(normalized_city),
        selected_city_id=(normalized_city_id),
        selected_tier=(normalized_tier),
        popular_cities_only=(popular_cities_only),
    )

    await mongo_connection.connect()

    collection = mongo_connection.collection(CARDEKHO_CARS_COLLECTION)

    cursor = collection.find(
        _build_car_query(
            selected_brand=(normalized_brand),
            selected_model=(normalized_model),
            selected_model_id=(normalized_model_id),
        ),
        {
            "_id": 1,
            "id": 1,
            "modelName": 1,
            "slug": 1,
            "modelStatus": 1,
            "brandId": 1,
            "brandName": 1,
            "brandSlug": 1,
            "carSlug": 1,
            "variants": 1,
            "lastRunId": 1,
        },
    ).sort(
        [
            (
                "brandSlug",
                1,
            ),
            (
                "slug",
                1,
            ),
            (
                "id",
                1,
            ),
        ]
    )

    generated_jobs = 0
    matched_car_records = 0

    seen_model_ids: set[int] = set()

    async for document in cursor:
        model_id = _positive_integer_or_none(document.get("id"))

        brand_id = _positive_integer_or_none(document.get("brandId"))

        model_name = _normalize_optional_string(document.get("modelName"))

        model_slug_value = _normalize_optional_string(document.get("slug"))

        brand_name = _normalize_optional_string(document.get("brandName"))

        brand_slug_value = _normalize_optional_string(document.get("brandSlug"))

        car_slug_value = _normalize_optional_string(document.get("carSlug"))

        model_status = _normalize_optional_string(document.get("modelStatus"))

        if (
            model_id is None
            or brand_id is None
            or model_name is None
            or model_slug_value is None
            or brand_name is None
            or brand_slug_value is None
            or car_slug_value is None
            or model_status is None
        ):
            continue

        if model_status.upper() != CURRENT_STATUS:
            continue

        model_slug = _slugify(model_slug_value)

        brand_slug = _slugify(brand_slug_value)

        car_slug = _slugify(car_slug_value)

        if not model_slug or not brand_slug or not car_slug:
            continue

        if model_id in seen_model_ids:
            continue

        seen_model_ids.add(model_id)

        source_car_document_id = (
            _normalize_optional_string(document.get("_id")) or f"car:{model_id}"
        )

        source_car_run_id = _normalize_optional_string(document.get("lastRunId"))

        source_trims = _parse_source_trims(document.get("variants"))

        matched_car_records += 1

        for city in cities:
            yield CardekhoCityPriceJob(
                model_id=model_id,
                model_name=model_name,
                model_slug=model_slug,
                model_status=(CURRENT_STATUS),
                brand_id=brand_id,
                brand_name=brand_name,
                brand_slug=brand_slug,
                car_slug=car_slug,
                city_id=city.city_id,
                city_name=(city.city_name),
                city_display_name=(city.city_display_name),
                city_slug=(city.city_slug),
                is_popular_city=(city.is_popular),
                source_car_document_id=(source_car_document_id),
                source_car_run_id=(source_car_run_id),
                source_city_document_id=(city.source_document_id),
                source_city_run_id=(city.source_run_id),
                source_trims=(source_trims),
            )

            generated_jobs += 1

            if max_jobs is not None and generated_jobs >= max_jobs:
                return

    if matched_car_records > 0:
        return

    filters: list[str] = [
        "model_status='CURRENT'",
    ]

    if normalized_brand is not None:
        filters.append(f"brand={normalized_brand!r}")

    if normalized_model is not None:
        filters.append(f"model={normalized_model!r}")

    if normalized_model_id is not None:
        filters.append(f"model_id={normalized_model_id}")

    raise CardekhoCityPriceJobSourceError(
        "No CURRENT Cardekho cars "
        "were found in MongoDB for "
        f"{', '.join(filters)}. "
        "Run cardekho-cars first."
    )
