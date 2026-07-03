from __future__ import annotations

from collections.abc import (
    AsyncIterator,
    Mapping,
)
from typing import Any

from src.models.scraper_job import ScraperJob
from src.repositories.carwale_car_repository import (
    carwale_car_repository,
)

SOURCE_NAME = "carwale"

RESOURCE_NAME = "trim-specs-features"

JOB_TYPE = "fetch-trim-specs-features"

SOURCE_COLLECTION = "carwale_cars"

TARGET_COLLECTION = "carwale_trim_specs_features"

COMMAND_NAME = "carwale-trim-specs-features"

SOURCE_NAME = "carwale"

RESOURCE_NAME = "trim-specs-features"

JOB_TYPE = "fetch-trim-specs-features"


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


def _normalize_optional_slug(
    value: str | None,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    return _validate_non_empty_string(
        value,
        field_name=field_name,
    ).lower()


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


def _validate_version_record(
    version_record: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(version_record, Mapping):
        raise ValueError("version_record must be an object")

    version = version_record.get("version")

    if not isinstance(version, Mapping):
        raise ValueError("version_record.version must be an object")

    make_id = _validate_positive_integer(
        version_record.get("makeId"),
        field_name="version_record.makeId",
    )

    make_name = _validate_non_empty_string(
        version_record.get("makeName"),
        field_name="version_record.makeName",
    )

    make_masking_name = _validate_non_empty_string(
        version_record.get("makeMaskingName"),
        field_name=("version_record.makeMaskingName"),
    ).lower()

    model_id = _validate_positive_integer(
        version_record.get("modelId"),
        field_name="version_record.modelId",
    )

    model_name = _validate_non_empty_string(
        version_record.get("modelName"),
        field_name="version_record.modelName",
    )

    model_masking_name = _validate_non_empty_string(
        version_record.get("modelMaskingName"),
        field_name=("version_record.modelMaskingName"),
    ).lower()

    version_id = _validate_positive_integer(
        version.get("versionId"),
        field_name="version.versionId",
    )

    version_name = _validate_non_empty_string(
        version.get("versionName"),
        field_name="version.versionName",
    )

    version_masking_name = _validate_non_empty_string(
        version.get("versionMaskingName"),
        field_name=("version.versionMaskingName"),
    ).lower()

    trim_id = _validate_positive_integer(
        version.get("trimId"),
        field_name="version.trimId",
    )

    trim_name = _validate_non_empty_string(
        version.get("trimName"),
        field_name="version.trimName",
    )

    trim_masking_name = _validate_non_empty_string(
        version.get("trimMaskingName"),
        field_name=("version.trimMaskingName"),
    ).lower()

    source_car_document_id = version_record.get("carDocumentId")

    if source_car_document_id is not None:
        source_car_document_id = _validate_non_empty_string(
            source_car_document_id,
            field_name=("version_record.carDocumentId"),
        )

    source_car_run_id = version_record.get("sourceCarRunId")

    if source_car_run_id is not None:
        source_car_run_id = _validate_non_empty_string(
            source_car_run_id,
            field_name=("version_record.sourceCarRunId"),
        )

    normalized_version = dict(version)

    normalized_version.update(
        {
            "versionId": version_id,
            "versionName": version_name,
            "versionMaskingName": (version_masking_name),
            "trimId": trim_id,
            "trimName": trim_name,
            "trimMaskingName": (trim_masking_name),
        }
    )

    return {
        "carDocumentId": (source_car_document_id),
        "sourceCarRunId": source_car_run_id,
        "makeId": make_id,
        "makeName": make_name,
        "makeMaskingName": (make_masking_name),
        "modelId": model_id,
        "modelName": model_name,
        "modelMaskingName": (model_masking_name),
        "version": normalized_version,
    }


async def iter_carwale_trim_specs_features_versions(
    *,
    selected_brand: str | None = None,
    selected_model: str | None = None,
    selected_trim: str | None = None,
    selected_version_id: int | None = None,
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

    normalized_trim = _normalize_optional_slug(
        selected_trim,
        field_name="selected_trim",
    )

    normalized_version_id = _normalize_optional_positive_integer(
        selected_version_id,
        field_name="selected_version_id",
    )

    normalized_max_jobs = _normalize_optional_positive_integer(
        max_jobs,
        field_name="max_jobs",
    )

    if normalized_model is not None and normalized_brand is None:
        raise ValueError("selected_model requires selected_brand")

    if normalized_trim is not None and (
        normalized_brand is None or normalized_model is None
    ):
        raise ValueError("selected_trim requires selected_brand and selected_model")

    make_id: int | None = None
    model_id: int | None = None

    if normalized_brand is not None and normalized_model is not None:
        selected_car = await carwale_car_repository.get_by_masking_names(
            make_masking_name=(normalized_brand),
            model_masking_name=(normalized_model),
        )

        if selected_car is None:
            raise LookupError(
                "CarWale car was not found in "
                "MongoDB: "
                f"brand={normalized_brand!r}, "
                f"model={normalized_model!r}. "
                "Run carwale-cars first."
            )

        make_id = selected_car.make_id
        model_id = selected_car.model_id

    seen_version_ids: set[int] = set()

    yielded_jobs = 0

    async for raw_version_record in carwale_car_repository.iter_versions(
        make_id=make_id,
        model_id=model_id,
    ):
        version_record = _validate_version_record(raw_version_record)

        make_masking_name = version_record["makeMaskingName"]

        model_masking_name = version_record["modelMaskingName"]

        version = version_record["version"]

        trim_masking_name = version["trimMaskingName"]

        version_id = version["versionId"]

        if normalized_brand is not None and make_masking_name != normalized_brand:
            continue

        if normalized_model is not None and model_masking_name != normalized_model:
            continue

        if normalized_trim is not None and trim_masking_name != normalized_trim:
            continue

        if normalized_version_id is not None and version_id != normalized_version_id:
            continue

        if version_id in seen_version_ids:
            continue

        seen_version_ids.add(version_id)

        yield version_record

        yielded_jobs += 1

        if normalized_max_jobs is not None and yielded_jobs >= normalized_max_jobs:
            return


async def load_carwale_trim_specs_features_versions(
    *,
    selected_brand: str | None = None,
    selected_model: str | None = None,
    selected_trim: str | None = None,
    selected_version_id: int | None = None,
    max_jobs: int | None = None,
) -> list[dict[str, Any]]:
    version_records: list[dict[str, Any]] = []

    async for version_record in iter_carwale_trim_specs_features_versions(
        selected_brand=selected_brand,
        selected_model=selected_model,
        selected_trim=selected_trim,
        selected_version_id=(selected_version_id),
        max_jobs=max_jobs,
    ):
        version_records.append(version_record)

    if not version_records:
        raise LookupError(
            "No CarWale versions matched the provided trim specs/features filters."
        )

    return version_records


def build_carwale_trim_specs_features_job(
    *,
    run_id: str,
    version_record: Mapping[str, Any],
) -> ScraperJob:
    normalized_run_id = _validate_non_empty_string(
        run_id,
        field_name="run_id",
    )

    normalized_version_record = _validate_version_record(version_record)

    version = normalized_version_record["version"]

    version_id = version["versionId"]

    job_id = f"version:{version_id}"

    return ScraperJob.create(
        run_id=normalized_run_id,
        job_id=job_id,
        source=SOURCE_NAME,
        resource=RESOURCE_NAME,
        job_type=JOB_TYPE,
        item_key=job_id,
        payload=normalized_version_record,
        metadata={
            "sourceCollection": (SOURCE_COLLECTION),
            "targetCollection": (TARGET_COLLECTION),
            "sourceCarDocumentId": (normalized_version_record.get("carDocumentId")),
            "sourceCarRunId": (normalized_version_record.get("sourceCarRunId")),
        },
        priority=100,
        max_attempts=3,
    )


def build_carwale_trim_specs_features_jobs(
    *,
    run_id: str,
    version_records: list[dict[str, Any]],
) -> list[ScraperJob]:
    jobs: list[ScraperJob] = []

    seen_job_ids: set[str] = set()

    for version_record in version_records:
        job = build_carwale_trim_specs_features_job(
            run_id=run_id,
            version_record=version_record,
        )

        if job.job_id in seen_job_ids:
            continue

        seen_job_ids.add(job.job_id)

        jobs.append(job)

    return jobs
