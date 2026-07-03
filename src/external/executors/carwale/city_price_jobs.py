from __future__ import annotations

from collections.abc import AsyncIterator, Mapping
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from src.models.carwale_city_price_job import (
    CarWaleCityPriceJob,
)
from src.repositories.carwale_car_repository import (
    carwale_car_repository,
)
from src.repositories.carwale_city_repository import (
    carwale_city_repository,
)

INDIA_TIMEZONE = ZoneInfo("Asia/Kolkata")
CARWALE_DATE_FORMAT = "%m/%d/%Y %H:%M:%S"


class CarWaleCityPriceJobSourceError(ValueError):
    """Raised when MongoDB city-price input data is invalid."""


def _normalize_optional_slug(
    value: str | None,
) -> str | None:
    if value is None:
        return None

    if not isinstance(
        value,
        str,
    ):
        raise ValueError("Slug filter must be a string or null")

    normalized_value = value.strip().lower()

    return normalized_value or None


def _is_launched_by_date(
    value: Any,
) -> bool:
    """
    Return True only when the CarWale launch date is
    today or in the past.

    Expected format:
        MM/DD/YYYY HH:MM:SS
    """

    if not isinstance(
        value,
        str,
    ):
        return False

    normalized_value = value.strip()

    if not normalized_value:
        return False

    try:
        launched_at = datetime.strptime(
            normalized_value,
            CARWALE_DATE_FORMAT,
        )
    except ValueError:
        return False

    current_date = datetime.now(
        INDIA_TIMEZONE,
    ).date()

    return launched_at.date() <= current_date


async def _load_carwale_cities(
    *,
    selected_city: str | None,
) -> list[tuple[int, str]]:
    normalized_selected_city = _normalize_optional_slug(
        selected_city,
    )

    cities: list[tuple[int, str]] = []
    seen_city_ids: set[int] = set()

    async for city in carwale_city_repository.iter_all(
        include_deleted=False,
    ):
        city_id = city.city_id
        city_masking_name = city.city_masking_name.strip().lower()

        if (
            normalized_selected_city is not None
            and city_masking_name != normalized_selected_city
        ):
            continue

        if city_id in seen_city_ids:
            continue

        seen_city_ids.add(city_id)

        cities.append(
            (
                city_id,
                city_masking_name,
            )
        )

    if not cities:
        if normalized_selected_city is not None:
            raise CarWaleCityPriceJobSourceError(
                "No active CarWale city was found in "
                "MongoDB for filter: "
                f"city={normalized_selected_city!r}"
            )

        raise CarWaleCityPriceJobSourceError(
            "No active CarWale cities were found in "
            "MongoDB. Run carwale-cities first."
        )

    return cities


async def iter_carwale_city_price_jobs(
    *,
    selected_brand: str | None = None,
    selected_model: str | None = None,
    selected_city: str | None = None,
    max_jobs: int | None = None,
) -> AsyncIterator[CarWaleCityPriceJob]:
    """
    Generate launched version-city jobs from MongoDB.

    Input collections:
        carwale_cars
        carwale_cities

    The pipeline, result storage, failures, run tracking,
    resume checks, batching, and logs remain unchanged.
    """

    if max_jobs is not None and (
        isinstance(max_jobs, bool) or not isinstance(max_jobs, int) or max_jobs < 1
    ):
        raise ValueError("max_jobs must be greater than zero")

    normalized_brand = _normalize_optional_slug(
        selected_brand,
    )

    normalized_model = _normalize_optional_slug(
        selected_model,
    )

    if normalized_model is not None and normalized_brand is None:
        raise ValueError("selected_model requires selected_brand")

    cities = await _load_carwale_cities(
        selected_city=selected_city,
    )

    seen_version_ids: set[int] = set()
    generated_jobs = 0
    matched_car_records = 0

    async for version_record in carwale_car_repository.iter_versions():
        make_masking_name = version_record.get("makeMaskingName")

        model_masking_name = version_record.get("modelMaskingName")

        if not isinstance(
            make_masking_name,
            str,
        ):
            continue

        if not isinstance(
            model_masking_name,
            str,
        ):
            continue

        normalized_make_masking_name = make_masking_name.strip().lower()

        normalized_model_masking_name = model_masking_name.strip().lower()

        if not normalized_make_masking_name or not normalized_model_masking_name:
            continue

        if (
            normalized_brand is not None
            and normalized_make_masking_name != normalized_brand
        ):
            continue

        if (
            normalized_model is not None
            and normalized_model_masking_name != normalized_model
        ):
            continue

        version = version_record.get("version")

        if not isinstance(
            version,
            Mapping,
        ):
            continue

        launched_on = version.get("launchedOn")

        if not _is_launched_by_date(launched_on):
            continue

        version_id = version.get("versionId")

        if (
            isinstance(version_id, bool)
            or not isinstance(version_id, int)
            or version_id <= 0
        ):
            continue

        if version_id in seen_version_ids:
            continue

        seen_version_ids.add(version_id)
        matched_car_records += 1

        for (
            city_id,
            city_masking_name,
        ) in cities:
            yield CarWaleCityPriceJob(
                version_id=version_id,
                city_id=city_id,
                make_masking_name=(normalized_make_masking_name),
                model_masking_name=(normalized_model_masking_name),
                city_masking_name=(city_masking_name),
            )

            generated_jobs += 1

            if max_jobs is not None and generated_jobs >= max_jobs:
                return

    if matched_car_records == 0:
        filters: list[str] = []

        if normalized_brand is not None:
            filters.append(f"brand={normalized_brand!r}")

        if normalized_model is not None:
            filters.append(f"model={normalized_model!r}")

        filter_text = f" for {', '.join(filters)}" if filters else ""

        raise CarWaleCityPriceJobSourceError(
            "No launched CarWale versions were found "
            f"in MongoDB{filter_text}. "
            "Run carwale-cars first."
        )
