from __future__ import annotations

from collections.abc import AsyncIterator, Mapping
from typing import Any

from src.databases.mongodb import (
    mongo_connection,
)
from src.models.scraper_job import ScraperJob

SOURCE_NAME = "bikedekho"

RESOURCE_NAME = "trim-specs-features"

JOB_TYPE = "fetch-trim-specs-features"

SOURCE_COLLECTION = "bikedekho_bikes"

TARGET_COLLECTION = "bikedekho_trim_specs_features"

COMMAND_NAME = "bikedekho-trim-specs-features"


def _validate_non_empty_string(
    value: Any,
    *,
    field_name: str,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")

    return value.strip()


def _validate_positive_integer(
    value: Any,
    *,
    field_name: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")

    return value


def _normalize_optional_slug(
    value: str | None,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    normalized_value = value.strip().lower()

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

    return _validate_positive_integer(
        value,
        field_name=field_name,
    )


def _validate_variant_record(
    value: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("variant_record must be a mapping")

    brand_slug = _validate_non_empty_string(
        value.get("brandSlug"),
        field_name="variant_record.brandSlug",
    )

    model_slug = _validate_non_empty_string(
        value.get("modelSlug"),
        field_name="variant_record.modelSlug",
    )

    variant = value.get("variant")

    if not isinstance(variant, Mapping):
        raise ValueError("variant_record.variant must be an object")

    variant_id = _validate_positive_integer(
        variant.get("variantId"),
        field_name="variant.variantId",
    )

    variant_slug = _validate_non_empty_string(
        variant.get("variantSlug"),
        field_name="variant.variantSlug",
    )

    variant_name = (
        variant.get("variantName")
        or variant.get("displayName")
        or variant.get("title")
        or variant.get("text")
    )

    variant_name = _validate_non_empty_string(
        variant_name,
        field_name="variant.variantName",
    )

    model_id = _validate_positive_integer(
        value.get("modelId"),
        field_name="variant_record.modelId",
    )

    model_name = _validate_non_empty_string(
        value.get("modelName"),
        field_name="variant_record.modelName",
    )

    brand_name = _validate_non_empty_string(
        value.get("brandName"),
        field_name="variant_record.brandName",
    )

    model_status = _validate_non_empty_string(
        value.get("modelStatus"),
        field_name="variant_record.modelStatus",
    )

    return {
        "bikeDocumentId": value.get("bikeDocumentId") or value.get("carDocumentId"),
        "sourceBikeRunId": value.get("sourceBikeRunId") or value.get("sourceCarRunId"),
        "brandId": value.get("brandId"),
        "brandName": brand_name,
        "brandSlug": brand_slug,
        "modelId": model_id,
        "modelName": model_name,
        "modelSlug": model_slug,
        "bikeSlug": value.get("bikeSlug") or value.get("carSlug"),
        "modelStatus": model_status,
        "variant": dict(variant),
        "variantId": variant_id,
        "variantName": variant_name,
        "variantSlug": variant_slug,
    }


async def iter_bikedekho_trim_specs_features_variants(
    *,
    selected_brand: str | None = None,
    selected_model: str | None = None,
    selected_model_id: int | None = None,
    selected_variant: str | None = None,
    selected_variant_id: int | None = None,
    model_status: str | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """
    Yield variants stored inside the bikedekho_bikes collection.

    One yielded record represents one BikeDekho variant and is later
    converted into one scraper job.
    """

    brand_slug = _normalize_optional_slug(
        selected_brand,
        field_name="brand",
    )

    model_slug = _normalize_optional_slug(
        selected_model,
        field_name="model",
    )

    model_id = _normalize_optional_positive_integer(
        selected_model_id,
        field_name="model_id",
    )

    variant_slug = _normalize_optional_slug(
        selected_variant,
        field_name="variant",
    )

    variant_id = _normalize_optional_positive_integer(
        selected_variant_id,
        field_name="variant_id",
    )

    normalized_model_status = None

    if model_status is not None:
        normalized_model_status = model_status.strip().upper()

        if normalized_model_status not in {
            "CURRENT",
            "UPCOMING",
            "DISCONTINUED",
        }:
            raise ValueError("model_status must be CURRENT, UPCOMING, or DISCONTINUED")

    query: dict[str, Any] = {
        "variantSpecsExist": True,
    }

    if brand_slug is not None:
        query["brandSlug"] = brand_slug

    if model_slug is not None:
        query["slug"] = model_slug

    if model_id is not None:
        query["id"] = model_id

    if normalized_model_status is not None:
        query["modelStatus"] = normalized_model_status

    await mongo_connection.connect()

    collection = mongo_connection.collection(
        SOURCE_COLLECTION,
    )

    projection = {
        "_id": 1,
        "id": 1,
        "brandId": 1,
        "brandName": 1,
        "brandSlug": 1,
        "name": 1,
        "slug": 1,
        "bikeSlug": 1,
        "modelName": 1,
        "modelStatus": 1,
        "lastRunId": 1,
        "variants": 1,
    }

    cursor = collection.find(
        query,
        projection,
    ).sort(
        [
            ("brandName", 1),
            ("modelName", 1),
            ("id", 1),
        ]
    )

    async for document in cursor:
        variants = document.get("variants")

        if not isinstance(variants, list):
            continue

        for variant in variants:
            if not isinstance(variant, Mapping):
                continue

            raw_variant_id = variant.get("variantId")

            if (
                isinstance(raw_variant_id, bool)
                or not isinstance(raw_variant_id, int)
                or raw_variant_id <= 0
            ):
                continue

            raw_variant_slug = variant.get("variantSlug")

            if not isinstance(raw_variant_slug, str) or not raw_variant_slug.strip():
                continue

            record = {
                "bikeDocumentId": document.get("_id"),
                "modelId": document.get("id"),
                "brandId": document.get("brandId"),
                "brandName": document.get("brandName"),
                "brandSlug": document.get("brandSlug"),
                "modelName": document.get("modelName"),
                "modelSlug": document.get("slug"),
                "bikeSlug": document.get("bikeSlug"),
                "modelStatus": document.get("modelStatus"),
                "sourceBikeRunId": document.get("lastRunId"),
                "variant": dict(variant),
            }

            normalized_record = _validate_variant_record(
                record,
            )

            if variant_id is not None:
                if normalized_record["variantId"] != variant_id:
                    continue

            if variant_slug is not None:
                if normalized_record["variantSlug"] != variant_slug:
                    continue

            if model_slug is not None:
                if normalized_record["modelSlug"] != model_slug:
                    continue

            yield normalized_record


async def load_bikedekho_trim_specs_features_variants(
    *,
    selected_brand: str | None = None,
    selected_model: str | None = None,
    selected_model_id: int | None = None,
    selected_variant: str | None = None,
    selected_variant_id: int | None = None,
    model_status: str | None = None,
) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []

    async for variant_record in iter_bikedekho_trim_specs_features_variants(
        selected_brand=selected_brand,
        selected_model=selected_model,
        selected_model_id=selected_model_id,
        selected_variant=selected_variant,
        selected_variant_id=selected_variant_id,
        model_status=model_status,
    ):
        variants.append(variant_record)

    if not variants:
        raise LookupError(
            "No BikeDekho variants matched the provided " "trim specs/features filters."
        )

    return variants


def build_bikedekho_trim_specs_features_job(
    *,
    run_id: str,
    variant_record: Mapping[str, Any],
) -> ScraperJob:
    normalized_run_id = _validate_non_empty_string(
        run_id,
        field_name="run_id",
    )

    normalized_variant_record = _validate_variant_record(
        variant_record,
    )

    variant_id = normalized_variant_record["variantId"]

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
            "sourceCollection": SOURCE_COLLECTION,
            "targetCollection": TARGET_COLLECTION,
            "sourceBikeDocumentId": (normalized_variant_record.get("bikeDocumentId")),
            "sourceBikeRunId": (normalized_variant_record.get("sourceBikeRunId")),
            "modelId": normalized_variant_record["modelId"],
            "modelStatus": normalized_variant_record["modelStatus"],
            "variantId": variant_id,
            "variantStatus": (
                normalized_variant_record["variant"].get("variantStatus")
                or normalized_variant_record["variant"].get("status")
            ),
        },
        priority=100,
        max_attempts=3,
    )


def build_bikedekho_trim_specs_features_jobs(
    *,
    run_id: str,
    variant_records: list[dict[str, Any]],
) -> list[ScraperJob]:
    jobs: list[ScraperJob] = []

    seen_job_ids: set[str] = set()

    for variant_record in variant_records:
        job = build_bikedekho_trim_specs_features_job(
            run_id=run_id,
            variant_record=variant_record,
        )

        if job.job_id in seen_job_ids:
            continue

        seen_job_ids.add(job.job_id)
        jobs.append(job)

    return jobs
