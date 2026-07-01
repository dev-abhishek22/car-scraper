from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.clients.client import (
    ExternalHttpClient,
    ExternalResponseError,
)
from src.external.constants.carwale import (
    CARWALE_BASE_URL,
    CARWALE_MODEL_PAGE_DATA,
)
from src.logger.logger import logger_service

MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

EXCLUDED_VERSION_FIELDS = frozenset(
    {
        "specsSummary",
        "featureSpecs",
    }
)


def _validate_slug(
    value: Any,
    *,
    field_name: str,
) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")

    normalized_value = value.strip().lower()

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    if not MASKING_NAME_PATTERN.fullmatch(normalized_value):
        raise ValueError(
            f"{field_name} contains invalid " f"characters: {normalized_value!r}"
        )

    return normalized_value


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


def _validate_positive_integer(
    value: Any,
    *,
    field_name: str,
) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")

    return value


def _validate_non_negative_integer(
    value: Any,
    *,
    field_name: str,
) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative " "integer")

    return value


def _validate_model_identity(
    *,
    make: Mapping[str, Any],
    model: Mapping[str, Any],
) -> tuple[
    int,
    str,
    str,
    int,
    str,
    str,
]:
    make_id = _validate_positive_integer(
        make.get("makeId"),
        field_name="makeId",
    )

    make_name = _validate_non_empty_string(
        make.get("makeName"),
        field_name="makeName",
    )

    make_masking_name = _validate_slug(
        make.get("maskingName"),
        field_name="maskingName",
    )

    model_id = _validate_positive_integer(
        model.get("modelId"),
        field_name="modelId",
    )

    model_name = _validate_non_empty_string(
        model.get("modelName"),
        field_name="modelName",
    )

    model_masking_name = _validate_slug(
        model.get("modelMaskingName"),
        field_name="modelMaskingName",
    )

    model_make_id = model.get("makeId")

    if (
        isinstance(model_make_id, int)
        and not isinstance(model_make_id, bool)
        and model_make_id != make_id
    ):
        raise ValueError(
            "Model makeId does not match the "
            "parent make: "
            f"expected={make_id}, "
            f"found={model_make_id}"
        )

    model_make_masking_name = model.get("makeMaskingName")

    if isinstance(model_make_masking_name, str):
        normalized_model_make_masking_name = _validate_slug(
            model_make_masking_name,
            field_name=("model.makeMaskingName"),
        )

        if normalized_model_make_masking_name != make_masking_name:
            raise ValueError(
                "Model makeMaskingName does not "
                "match the parent make: "
                f"expected={make_masking_name!r}, "
                "found="
                f"{normalized_model_make_masking_name!r}"
            )

    return (
        make_id,
        make_name,
        make_masking_name,
        model_id,
        model_name,
        model_masking_name,
    )


def _validate_page_validation(
    response_data: Mapping[str, Any],
    *,
    make_masking_name: str,
    model_masking_name: str,
) -> None:
    page_validation = response_data.get("pageValidation")

    if not isinstance(page_validation, dict):
        raise ExternalResponseError(
            "CarWale model-page API response does "
            "not contain a valid pageValidation "
            "object: "
            f"make={make_masking_name!r}, "
            f"model={model_masking_name!r}"
        )

    redirect_path = page_validation.get("redirectPath")

    if isinstance(redirect_path, str) and redirect_path.strip():
        raise ExternalResponseError(
            "CarWale model-page API returned a "
            "redirect path: "
            f"make={make_masking_name!r}, "
            f"model={model_masking_name!r}, "
            f"redirect_path={redirect_path!r}"
        )

    if page_validation.get("isDeleted") is True:
        raise ExternalResponseError(
            "CarWale model-page API marked the "
            "model as deleted: "
            f"make={make_masking_name!r}, "
            f"model={model_masking_name!r}"
        )

    if page_validation.get("isInvalidInput") is True:
        raise ExternalResponseError(
            "CarWale model-page API rejected the "
            "make or model input: "
            f"make={make_masking_name!r}, "
            f"model={model_masking_name!r}"
        )

    if page_validation.get("isValid") is not True:
        raise ExternalResponseError(
            "CarWale model-page API returned an "
            "invalid page: "
            f"make={make_masking_name!r}, "
            f"model={model_masking_name!r}"
        )


def _validate_required_mapping_section(
    response_data: Mapping[str, Any],
    *,
    field_name: str,
    make_masking_name: str,
    model_masking_name: str,
) -> dict[str, Any]:
    section = response_data.get(field_name)

    if not isinstance(section, dict):
        raise ExternalResponseError(
            "CarWale model-page API response "
            f"contains an invalid {field_name} "
            "section: "
            f"make={make_masking_name!r}, "
            f"model={model_masking_name!r}, "
            f"type={type(section).__name__}"
        )

    return dict(section)


def _get_optional_json_section(
    response_data: Mapping[str, Any],
    *,
    field_name: str,
) -> Any:
    """
    Return an optional API section without forcing a
    specific JSON type.

    CarWale may return an object, an empty array, or null
    for optional sections depending on the model.
    """
    return response_data.get(field_name)


def _clean_versions(
    response_data: Mapping[str, Any],
    *,
    make_masking_name: str,
    model_masking_name: str,
) -> list[dict[str, Any]]:
    versions = response_data.get("versions")

    if not isinstance(versions, list):
        raise ExternalResponseError(
            "CarWale model-page API response does "
            "not contain a valid versions list: "
            f"make={make_masking_name!r}, "
            f"model={model_masking_name!r}"
        )

    cleaned_versions: list[dict[str, Any]] = []

    for index, version in enumerate(versions):
        if not isinstance(version, dict):
            raise ExternalResponseError(
                "CarWale model-page API returned "
                "an invalid version record: "
                f"make={make_masking_name!r}, "
                f"model={model_masking_name!r}, "
                f"index={index}, "
                f"type={type(version).__name__}"
            )

        cleaned_version = {
            key: value
            for key, value in version.items()
            if key not in EXCLUDED_VERSION_FIELDS
        }

        cleaned_versions.append(cleaned_version)

    return cleaned_versions


def _validate_response_identity(
    *,
    model_details: Mapping[str, Any],
    expected_make_masking_name: str,
    expected_model_id: int,
    expected_model_masking_name: str,
) -> None:
    response_model_id = model_details.get("modelId")

    if (
        isinstance(response_model_id, int)
        and not isinstance(response_model_id, bool)
        and response_model_id != expected_model_id
    ):
        raise ExternalResponseError(
            "CarWale model-page API returned a "
            "different modelId: "
            f"expected={expected_model_id}, "
            f"found={response_model_id}"
        )

    response_make_masking_name = model_details.get("makeMaskingName")

    if isinstance(
        response_make_masking_name,
        str,
    ):
        normalized_make_masking_name = response_make_masking_name.strip().lower()

        if (
            normalized_make_masking_name
            and normalized_make_masking_name != expected_make_masking_name
        ):
            raise ExternalResponseError(
                "CarWale model-page API returned a "
                "different makeMaskingName: "
                "expected="
                f"{expected_make_masking_name!r}, "
                "found="
                f"{normalized_make_masking_name!r}"
            )

    response_model_masking_name = model_details.get("modelMaskingName")

    if isinstance(
        response_model_masking_name,
        str,
    ):
        normalized_model_masking_name = response_model_masking_name.strip().lower()

        if (
            normalized_model_masking_name
            and normalized_model_masking_name != expected_model_masking_name
        ):
            raise ExternalResponseError(
                "CarWale model-page API returned a "
                "different modelMaskingName: "
                "expected="
                f"{expected_model_masking_name!r}, "
                "found="
                f"{normalized_model_masking_name!r}"
            )


def _build_request_log_file(
    *,
    request_dir: str | Path | None,
    make_masking_name: str,
    model_masking_name: str,
) -> Path:
    base_directory = (
        Path(request_dir)
        if request_dir is not None
        else Path("data/raw/carwale/requests/cars")
    )

    return base_directory / make_masking_name / f"{model_masking_name}.json"


def scrape_carwale_model_page(
    *,
    client: ExternalHttpClient,
    make: Mapping[str, Any],
    model: Mapping[str, Any],
    city_id: int = 10,
    area_id: int = 3657,
    platform_id: int = 1,
    show_offer_upfront: bool = False,
    show_request: bool = False,
    save_request: bool = False,
    request_dir: str | Path | None = None,
) -> dict[str, Any]:
    """
    Fetch, validate, and transform one CarWale
    model-page API response.

    This function intentionally does not:

    - Start worker threads
    - Update the shared status store
    - Save the final car output file

    Those responsibilities belong to the command
    layer so this function remains safe to execute
    inside ThreadPoolExecutor workers.
    """
    (
        make_id,
        make_name,
        make_masking_name,
        model_id,
        model_name,
        model_masking_name,
    ) = _validate_model_identity(
        make=make,
        model=model,
    )

    normalized_city_id = _validate_positive_integer(
        city_id,
        field_name="city_id",
    )

    normalized_area_id = _validate_non_negative_integer(
        area_id,
        field_name="area_id",
    )

    normalized_platform_id = _validate_positive_integer(
        platform_id,
        field_name="platform_id",
    )

    endpoint = CARWALE_MODEL_PAGE_DATA

    params: dict[str, Any] = {
        **endpoint.default_params,
        "makeMaskingName": make_masking_name,
        "modelMaskingName": (model_masking_name),
        "cityId": normalized_city_id,
        "areaId": normalized_area_id,
        "showOfferUpfront": ("true" if show_offer_upfront else "false"),
        "platformId": normalized_platform_id,
    }

    headers: dict[str, str] = {
        **endpoint.default_headers,
        "Referer": (
            f"{CARWALE_BASE_URL}/" f"{make_masking_name}-cars/" f"{model_masking_name}/"
        ),
    }

    request_log_file: Path | None = None

    if save_request:
        request_log_file = _build_request_log_file(
            request_dir=request_dir,
            make_masking_name=(make_masking_name),
            model_masking_name=(model_masking_name),
        )

    logger_service.info(
        (
            "Scraping CarWale model page: "
            f"make={make_name}, "
            f"make_masking_name="
            f"{make_masking_name}, "
            f"model={model_name}, "
            f"model_masking_name="
            f"{model_masking_name}"
        ),
        context="CarWaleModelPageExecutor",
    )

    response_data = client.get_json(
        endpoint=endpoint.path,
        params=params,
        headers=headers,
        show_request=show_request,
        request_log_file=request_log_file,
    )

    if not isinstance(response_data, dict):
        raise ExternalResponseError(
            "CarWale model-page API returned an "
            "invalid response. Expected a JSON "
            "object: "
            f"make={make_masking_name!r}, "
            f"model={model_masking_name!r}"
        )

    _validate_page_validation(
        response_data,
        make_masking_name=make_masking_name,
        model_masking_name=(model_masking_name),
    )

    model_details = _validate_required_mapping_section(
        response_data,
        field_name="modelDetails",
        make_masking_name=make_masking_name,
        model_masking_name=(model_masking_name),
    )

    replaced_model_details = _get_optional_json_section(
        response_data,
        field_name="replacedModelDetails",
    )

    similar_cars = _get_optional_json_section(
        response_data,
        field_name="similarCars",
    )

    versions = _clean_versions(
        response_data,
        make_masking_name=make_masking_name,
        model_masking_name=(model_masking_name),
    )

    _validate_response_identity(
        model_details=model_details,
        expected_make_masking_name=(make_masking_name),
        expected_model_id=model_id,
        expected_model_masking_name=(model_masking_name),
    )

    scraped_at = datetime.now(timezone.utc).isoformat()

    payload: dict[str, Any] = {
        "makeId": make_id,
        "makeName": make_name,
        "makeMaskingName": (make_masking_name),
        "modelId": model_id,
        "modelName": model_name,
        "modelMaskingName": (model_masking_name),
        "totalVersions": len(versions),
        "scrapedAt": scraped_at,
        "data": {
            "modelDetails": model_details,
            "replacedModelDetails": (replaced_model_details),
            "similarCars": similar_cars,
            "versions": versions,
        },
    }

    logger_service.info(
        (
            "CarWale model page scraped: "
            f"make={make_name}, "
            f"model={model_name}, "
            f"total_versions={len(versions)}"
        ),
        context="CarWaleModelPageExecutor",
    )

    return {
        "status": "success",
        "make_id": make_id,
        "make_name": make_name,
        "make_masking_name": (make_masking_name),
        "model_id": model_id,
        "model_name": model_name,
        "model_masking_name": (model_masking_name),
        "total_versions": len(versions),
        "scraped_at": scraped_at,
        "request_file": (
            str(request_log_file) if request_log_file is not None else None
        ),
        "payload": payload,
    }
