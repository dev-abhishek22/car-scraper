from __future__ import annotations

from collections.abc import (
    AsyncIterator,
    Mapping,
)
from typing import Any

from src.logger.logger import logger_service
from src.models.scraper_job import ScraperJob
from src.repositories.cardekho_car_repository import (
    cardekho_car_repository,
)

SOURCE_NAME = "cardekho"

RESOURCE_NAME = "trim-specs-features"

JOB_TYPE = "fetch-trim-specs-features"

SOURCE_COLLECTION = "cardekho_cars"

TARGET_COLLECTION = "cardekho_trim_specs_features"

COMMAND_NAME = "cardekho-trim-specs-features"


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
    if not isinstance(
        value,
        str,
    ):
        raise ValueError(f"{field_name} must be a string")

    normalized_value = value.strip()

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    return normalized_value


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


def _normalize_optional_variant_slug(
    value: Any,
) -> str | None:
    if not isinstance(value, str):
        return None

    normalized_value = value.strip()

    return normalized_value or None


def _normalize_slug(
    value: Any,
    *,
    field_name: str,
) -> str:
    normalized_value = (
        _validate_non_empty_string(
            value,
            field_name=field_name,
        )
        .lower()
        .replace("_", "-")
        .replace(" ", "-")
    )

    while "--" in normalized_value:
        normalized_value = normalized_value.replace(
            "--",
            "-",
        )

    normalized_value = normalized_value.strip("-")

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    return normalized_value


def _normalize_status(
    value: Any,
    *,
    field_name: str,
) -> str:
    return _validate_non_empty_string(
        value,
        field_name=field_name,
    ).upper()


def _normalize_optional_slug(
    value: str | None,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    return _normalize_slug(
        value,
        field_name=field_name,
    )


def _normalize_optional_positive_integer(
    value: int | None,
    *,
    field_name: str,
) -> int | None:
    if value is None:
        return None

    return _validate_positive_integer(
        value,
        field_name=field_name,
    )


def _validate_variant_record(
    variant_record: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(
        variant_record,
        Mapping,
    ):
        raise ValueError("variant_record must be an object")

    variant = variant_record.get("variant")

    if not isinstance(
        variant,
        Mapping,
    ):
        raise ValueError("variant_record.variant must be an object")

    car_document_id = _normalize_optional_string(variant_record.get("carDocumentId"))

    source_car_run_id = _normalize_optional_string(variant_record.get("sourceCarRunId"))

    brand_id = _validate_positive_integer(
        variant_record.get("brandId"),
        field_name="variant_record.brandId",
    )

    brand_name = _validate_non_empty_string(
        variant_record.get("brandName"),
        field_name="variant_record.brandName",
    )

    brand_slug = _normalize_slug(
        variant_record.get("brandSlug"),
        field_name="variant_record.brandSlug",
    )

    model_id = _validate_positive_integer(
        variant_record.get("modelId"),
        field_name="variant_record.modelId",
    )

    model_name = _validate_non_empty_string(
        variant_record.get("modelName"),
        field_name="variant_record.modelName",
    )

    model_slug = _normalize_slug(
        variant_record.get("modelSlug"),
        field_name="variant_record.modelSlug",
    )

    car_slug = _normalize_slug(
        variant_record.get("carSlug"),
        field_name="variant_record.carSlug",
    )

    model_status = _normalize_status(
        variant_record.get("modelStatus"),
        field_name="variant_record.modelStatus",
    )

    variant_id = _validate_positive_integer(
        variant.get("id"),
        field_name="variant.id",
    )

    variant_slug = _normalize_optional_variant_slug(
        variant.get("slug"),
    )

    if variant_slug is None:
        raise ValueError("variant.slug must be a non-empty string")

    variant_name = (
        _normalize_optional_string(variant.get("name"))
        or _normalize_optional_string(variant.get("shortName"))
        or variant_slug
    )

    variant_short_name = (
        _normalize_optional_string(variant.get("shortName")) or variant_name
    )

    variant_url = _normalize_optional_string(variant.get("url"))

    variant_status = _normalize_status(
        variant.get("status"),
        field_name="variant.status",
    )

    normalized_variant = dict(variant)

    normalized_variant.update(
        {
            "id": variant_id,
            "name": variant_name,
            "shortName": variant_short_name,
            "slug": variant_slug,
            "url": variant_url,
            "status": variant_status,
        }
    )

    return {
        "carDocumentId": car_document_id,
        "sourceCarRunId": source_car_run_id,
        "brandId": brand_id,
        "brandName": brand_name,
        "brandSlug": brand_slug,
        "modelId": model_id,
        "modelName": model_name,
        "modelSlug": model_slug,
        "carSlug": car_slug,
        "modelStatus": model_status,
        "variant": normalized_variant,
    }


async def iter_cardekho_trim_specs_features_variants(
    *,
    selected_brand: str | None = None,
    selected_model: str | None = None,
    selected_model_id: int | None = None,
    selected_variant: str | None = None,
    selected_variant_id: int | None = None,
    max_jobs: int | None = None,
) -> AsyncIterator[dict[str, Any]]:
    normalized_brand = _normalize_optional_slug(
        selected_brand,
        field_name="selected_brand",
    )

    normalized_model = _normalize_optional_slug(
        selected_model,
        field_name="selected_model",
    )

    normalized_model_id = _normalize_optional_positive_integer(
        selected_model_id,
        field_name="selected_model_id",
    )

    normalized_variant = _normalize_optional_variant_slug(
        selected_variant,
    )

    normalized_variant_id = _normalize_optional_positive_integer(
        selected_variant_id,
        field_name="selected_variant_id",
    )

    normalized_max_jobs = _normalize_optional_positive_integer(
        max_jobs,
        field_name="max_jobs",
    )

    if normalized_model is not None and normalized_brand is None:
        raise ValueError("selected_model requires selected_brand")

    if normalized_variant is not None and (
        normalized_brand is None or normalized_model is None
    ):
        raise ValueError(
            "selected_variant requires " "selected_brand and selected_model"
        )

    resolved_model_id = normalized_model_id

    if normalized_brand is not None and normalized_model is not None:
        selected_car = await cardekho_car_repository.get_by_slugs(
            brand_slug=normalized_brand,
            model_slug=normalized_model,
        )

        if selected_car is None:
            raise LookupError(
                "Cardekho car was not found "
                "in MongoDB: "
                f"brand={normalized_brand!r}, "
                f"model={normalized_model!r}. "
                "Run cardekho-cars first."
            )

        if (
            normalized_model_id is not None
            and selected_car.model_id != normalized_model_id
        ):
            raise ValueError(
                "selected_model_id does not "
                "match the selected brand and model: "
                f"expected={selected_car.model_id}, "
                f"found={normalized_model_id}"
            )

        resolved_model_id = selected_car.model_id

    elif normalized_model_id is not None:
        selected_car = await cardekho_car_repository.get_by_model_id(
            normalized_model_id
        )

        if selected_car is None:
            raise LookupError(
                "Cardekho car was not found "
                "in MongoDB: "
                f"model_id={normalized_model_id}. "
                "Run cardekho-cars first."
            )

        if normalized_brand is not None and selected_car.brand_slug != normalized_brand:
            raise ValueError(
                "selected_model_id does not "
                "belong to the selected brand: "
                f"model_id={normalized_model_id}, "
                f"expected_brand={normalized_brand!r}, "
                f"found_brand="
                f"{selected_car.brand_slug!r}"
            )

    seen_variant_ids: set[int] = set()

    yielded_jobs = 0

    async for raw_variant_record in cardekho_car_repository.iter_variants(
        brand_slug=normalized_brand,
        model_id=resolved_model_id,
    ):
        try:
            variant_record = _validate_variant_record(raw_variant_record)

        except (
            TypeError,
            ValueError,
        ) as error:
            raw_variant = (
                raw_variant_record.get("variant")
                if isinstance(
                    raw_variant_record,
                    Mapping,
                )
                else None
            )

            raw_variant_id = (
                raw_variant.get("id")
                if isinstance(
                    raw_variant,
                    Mapping,
                )
                else None
            )

            raw_variant_slug = (
                raw_variant.get("slug")
                if isinstance(
                    raw_variant,
                    Mapping,
                )
                else None
            )

            logger_service.warning(
                (
                    "Skipping invalid Cardekho "
                    "variant source record: "
                    "car_document_id="
                    f"{raw_variant_record.get('carDocumentId')!r}, "
                    f"variant_id={raw_variant_id!r}, "
                    f"variant_slug={raw_variant_slug!r}, "
                    "error="
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
                context=("CardekhoTrimSpecsFeaturesJobs"),
            )

            continue

        brand_slug = variant_record["brandSlug"]

        model_slug = variant_record["modelSlug"]

        model_id = variant_record["modelId"]

        variant = variant_record["variant"]

        variant_id = variant["id"]

        variant_slug = variant["slug"]

        if normalized_brand is not None and brand_slug != normalized_brand:
            continue

        if normalized_model is not None and model_slug != normalized_model:
            continue

        if normalized_model_id is not None and model_id != normalized_model_id:
            continue

        if normalized_variant is not None and variant_slug != normalized_variant:
            continue

        if normalized_variant_id is not None and variant_id != normalized_variant_id:
            continue

        if variant_id in seen_variant_ids:
            continue

        seen_variant_ids.add(variant_id)

        yield variant_record

        yielded_jobs += 1

        if normalized_max_jobs is not None and yielded_jobs >= normalized_max_jobs:
            return


async def load_cardekho_trim_specs_features_variants(
    *,
    selected_brand: str | None = None,
    selected_model: str | None = None,
    selected_model_id: int | None = None,
    selected_variant: str | None = None,
    selected_variant_id: int | None = None,
    max_jobs: int | None = None,
) -> list[dict[str, Any]]:
    variant_records: list[dict[str, Any]] = []

    async for variant_record in iter_cardekho_trim_specs_features_variants(
        selected_brand=selected_brand,
        selected_model=selected_model,
        selected_model_id=(selected_model_id),
        selected_variant=(selected_variant),
        selected_variant_id=(selected_variant_id),
        max_jobs=max_jobs,
    ):
        variant_records.append(variant_record)

    if not variant_records:
        raise LookupError(
            "No Cardekho variants matched "
            "the provided trim "
            "specs/features filters."
        )

    return variant_records


def build_cardekho_trim_specs_features_job(
    *,
    run_id: str,
    variant_record: Mapping[str, Any],
) -> ScraperJob:
    normalized_run_id = _validate_non_empty_string(
        run_id,
        field_name="run_id",
    )

    normalized_variant_record = _validate_variant_record(variant_record)

    variant = normalized_variant_record["variant"]

    variant_id = variant["id"]

    job_id = f"variant:{variant_id}"

    return ScraperJob.create(
        run_id=normalized_run_id,
        job_id=job_id,
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        job_type=JOB_TYPE,
        item_key=job_id,
        payload=normalized_variant_record,
        metadata={
            "sourceCollection": (SOURCE_COLLECTION),
            "targetCollection": (TARGET_COLLECTION),
            "sourceCarDocumentId": (normalized_variant_record.get("carDocumentId")),
            "sourceCarRunId": (normalized_variant_record.get("sourceCarRunId")),
            "modelId": (normalized_variant_record["modelId"]),
            "modelStatus": (normalized_variant_record["modelStatus"]),
            "variantId": variant_id,
            "variantStatus": (variant["status"]),
        },
        priority=100,
        max_attempts=3,
    )


def build_cardekho_trim_specs_features_jobs(
    *,
    run_id: str,
    variant_records: list[dict[str, Any]],
) -> list[ScraperJob]:
    jobs: list[ScraperJob] = []

    seen_job_ids: set[str] = set()

    for variant_record in variant_records:
        job = build_cardekho_trim_specs_features_job(
            run_id=run_id,
            variant_record=variant_record,
        )

        if job.job_id in seen_job_ids:
            continue

        seen_job_ids.add(job.job_id)

        jobs.append(job)

    return jobs
