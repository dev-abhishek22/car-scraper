from __future__ import annotations

import json
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

from src.logger.logger import logger_service
from src.models.carwale_city_price_job import (
    CarWaleCityPriceJob,
)


class CarWaleCityPriceJobSourceError(ValueError):
    """Raised when saved CarWale input data is invalid."""


def _read_json_file(
    file_path: Path,
) -> Any:
    try:
        return json.loads(
            file_path.read_text(
                encoding="utf-8",
            )
        )

    except json.JSONDecodeError as error:
        raise CarWaleCityPriceJobSourceError(
            f"Invalid JSON file: {file_path}"
        ) from error

    except OSError as error:
        raise CarWaleCityPriceJobSourceError(
            f"Unable to read file: {file_path}"
        ) from error


def _normalize_optional_slug(
    value: str | None,
) -> str | None:
    if value is None:
        return None

    normalized_value = value.strip().lower()

    if not normalized_value:
        return None

    return normalized_value


def load_carwale_cities(
    cities_file: str | Path,
    *,
    selected_city: str | None = None,
) -> list[tuple[int, str]]:
    file_path = Path(cities_file)

    payload = _read_json_file(file_path)

    if not isinstance(payload, list):
        raise CarWaleCityPriceJobSourceError(
            "CarWale cities file must contain a JSON array"
        )

    normalized_selected_city = _normalize_optional_slug(selected_city)

    cities: list[tuple[int, str]] = []
    seen_city_ids: set[int] = set()

    for index, city in enumerate(payload):
        if not isinstance(city, Mapping):
            logger_service.warning(
                (f"Skipping invalid CarWale city: index={index}"),
                context="CarWaleCityPriceJobs",
            )
            continue

        city_id = city.get("CityId")
        city_masking_name = city.get("CityMaskingName")
        is_deleted = city.get(
            "IsDeleted",
            False,
        )

        if is_deleted is True:
            continue

        if isinstance(city_id, bool) or not isinstance(city_id, int) or city_id <= 0:
            logger_service.warning(
                (f"Skipping CarWale city with invalid CityId: index={index}"),
                context="CarWaleCityPriceJobs",
            )
            continue

        if not isinstance(
            city_masking_name,
            str,
        ):
            continue

        normalized_city_masking_name = city_masking_name.strip().lower()

        if not normalized_city_masking_name:
            continue

        if (
            normalized_selected_city is not None
            and normalized_city_masking_name != normalized_selected_city
        ):
            continue

        if city_id in seen_city_ids:
            continue

        seen_city_ids.add(city_id)

        cities.append(
            (
                city_id,
                normalized_city_masking_name,
            )
        )

    if not cities:
        raise CarWaleCityPriceJobSourceError("No valid CarWale cities were found")

    return cities


def iter_carwale_city_price_jobs(
    *,
    cars_directory: str | Path,
    cities_file: str | Path,
    selected_brand: str | None = None,
    selected_model: str | None = None,
    selected_city: str | None = None,
    max_jobs: int | None = None,
) -> Iterator[CarWaleCityPriceJob]:
    cars_path = Path(cars_directory)

    if not cars_path.exists():
        raise CarWaleCityPriceJobSourceError(
            (f"CarWale cars directory does not exist: {cars_path}")
        )

    if max_jobs is not None and max_jobs < 1:
        raise ValueError("max_jobs must be greater than zero")

    normalized_brand = _normalize_optional_slug(selected_brand)
    normalized_model = _normalize_optional_slug(selected_model)

    if normalized_model is not None and normalized_brand is None:
        raise ValueError("selected_model requires selected_brand")

    cities = load_carwale_cities(
        cities_file,
        selected_city=selected_city,
    )

    seen_version_ids: set[int] = set()
    generated_jobs = 0

    car_files = sorted(cars_path.rglob("*.json"))

    for car_file in car_files:
        payload = _read_json_file(car_file)

        if not isinstance(payload, Mapping):
            logger_service.warning(
                (f"Skipping invalid CarWale car file: file={car_file}"),
                context="CarWaleCityPriceJobs",
            )
            continue

        make_masking_name = payload.get("makeMaskingName")
        model_masking_name = payload.get("modelMaskingName")

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

        make_masking_name = make_masking_name.strip().lower()
        model_masking_name = model_masking_name.strip().lower()

        if normalized_brand is not None and make_masking_name != normalized_brand:
            continue

        if normalized_model is not None and model_masking_name != normalized_model:
            continue

        data = payload.get("data")

        if not isinstance(data, Mapping):
            continue

        versions = data.get("versions")

        if not isinstance(versions, list):
            continue

        for version in versions:
            if not isinstance(
                version,
                Mapping,
            ):
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

            for (
                city_id,
                city_masking_name,
            ) in cities:
                yield CarWaleCityPriceJob(
                    version_id=version_id,
                    city_id=city_id,
                    make_masking_name=(make_masking_name),
                    model_masking_name=(model_masking_name),
                    city_masking_name=(city_masking_name),
                )

                generated_jobs += 1

                if max_jobs is not None and generated_jobs >= max_jobs:
                    return
