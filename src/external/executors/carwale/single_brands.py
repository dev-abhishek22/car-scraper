from __future__ import annotations

import json
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
    CARWALE_MAKE_PAGE_DATA,
)
from src.logger.logger import logger_service
from src.storage.scraper_status import ScrapeStatusStore
from src.storage.json_storage import JsonStorage

STATUS_RESOURCE_NAME = "carwale_models"

MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _validate_brand(
    brand: Mapping[str, Any],
) -> tuple[int, str, str]:
    """
    Validate and normalize one CarWale brand.

    Returns:
        make_id, make_name, masking_name
    """
    make_id = brand.get("makeId")
    make_name = brand.get("makeName")
    masking_name = brand.get("maskingName")

    if not isinstance(make_id, int):
        raise ValueError("Brand makeId must be an integer")

    if not isinstance(make_name, str):
        raise ValueError("Brand makeName must be a string")

    if not isinstance(masking_name, str):
        raise ValueError("Brand maskingName must be a string")

    normalized_make_name = make_name.strip()

    normalized_masking_name = masking_name.strip().lower()

    if not normalized_make_name:
        raise ValueError("Brand makeName cannot be empty")

    if not normalized_masking_name:
        raise ValueError("Brand maskingName cannot be empty")

    if not MASKING_NAME_PATTERN.fullmatch(normalized_masking_name):
        raise ValueError(
            "Brand maskingName contains invalid "
            "characters: "
            f"{normalized_masking_name!r}"
        )

    return (
        make_id,
        normalized_make_name,
        normalized_masking_name,
    )


def _validate_models_response(
    response_data: dict[str, Any] | list[Any],
    *,
    masking_name: str,
) -> list[dict[str, Any]]:
    """
    Validate the CarWale make-page API response and
    return only the models list.
    """
    if not isinstance(response_data, dict):
        raise ExternalResponseError(
            "CarWale make-page API returned an invalid "
            f"response for {masking_name!r}. "
            "Expected a JSON object."
        )

    models = response_data.get("models")

    if not isinstance(models, list):
        raise ExternalResponseError(
            "CarWale make-page API response does not "
            "contain a valid models list for "
            f"{masking_name!r}."
        )

    validated_models: list[dict[str, Any]] = []

    for index, model in enumerate(models):
        if not isinstance(model, dict):
            raise ExternalResponseError(
                "CarWale make-page API returned an "
                f"invalid model at index {index} for "
                f"{masking_name!r}."
            )

        validated_models.append(model)

    return validated_models


def _read_existing_total_models(
    output_file: Path,
) -> int:
    """
    Read totalModels from an existing output file.

    Returns zero when the existing file cannot be read
    or does not contain a valid totalModels value.
    """
    try:
        existing_data = json.loads(
            output_file.read_text(
                encoding="utf-8",
            )
        )

        if not isinstance(existing_data, dict):
            return 0

        total_models = existing_data.get(
            "totalModels",
            0,
        )

        if isinstance(total_models, int):
            return total_models

    except (
        OSError,
        json.JSONDecodeError,
    ):
        pass

    return 0


def scrape_carwale_model(
    *,
    client: ExternalHttpClient,
    brand: Mapping[str, Any],
    output_dir: str | Path,
    force: bool = False,
    show_request: bool = False,
    save_request: bool = False,
    request_dir: str | Path | None = None,
) -> dict[str, Any]:
    """
    Scrape and save models for one CarWale brand.

    This is the reusable core operation.

    It does not start or complete a status run because
    the caller may be:

    - The single-brand runner
    - The all-brands runner
    - A future scheduled scraper

    Retry handling, Retry-After handling, HTTP 429
    handling, and network retries are performed by
    ExternalHttpClient.
    """
    (
        make_id,
        make_name,
        masking_name,
    ) = _validate_brand(brand)

    models_directory = Path(output_dir)

    output_file = models_directory / f"{masking_name}.json"

    if output_file.exists() and not force:
        total_models = _read_existing_total_models(output_file)

        logger_service.info(
            (
                "CarWale model file already exists; "
                f"skipping brand={make_name}, "
                f"masking_name={masking_name}, "
                f"file={output_file}"
            ),
            context="CarWaleModelExecutor",
        )

        return {
            "status": "skipped",
            "make_id": make_id,
            "make_name": make_name,
            "masking_name": masking_name,
            "total_models": total_models,
            "output_file": str(output_file),
        }

    endpoint = CARWALE_MAKE_PAGE_DATA

    params: dict[str, Any] = {
        **endpoint.default_params,
        "maskingName": masking_name,
    }

    headers: dict[str, str] = {
        **endpoint.default_headers,
        "Referer": (f"{CARWALE_BASE_URL}/{masking_name}-cars/"),
    }

    request_log_file: Path | None = None

    if save_request:
        requests_directory = (
            Path(request_dir)
            if request_dir is not None
            else (models_directory.parent / "requests" / "models")
        )

        request_log_file = requests_directory / f"{masking_name}.json"

    logger_service.info(
        (f"Scraping CarWale models: brand={make_name}, masking_name={masking_name}"),
        context="CarWaleModelExecutor",
    )

    response_data = client.get_json(
        endpoint=endpoint.path,
        params=params,
        headers=headers,
        show_request=show_request,
        request_log_file=request_log_file,
    )

    models = _validate_models_response(
        response_data,
        masking_name=masking_name,
    )

    scraped_at = datetime.now(timezone.utc).isoformat()

    payload: dict[str, Any] = {
        "makeId": make_id,
        "makeName": make_name,
        "maskingName": masking_name,
        "totalModels": len(models),
        "scrapedAt": scraped_at,
        "models": models,
    }

    files = JsonStorage.save(
        directory=output_dir,
        file_name=masking_name,
        data=payload,
        create_archive=True,
        archive_directory="data/raw/carwale/archive/models",
    )

    logger_service.info(
        (
            "CarWale models saved: "
            f"brand={make_name}, "
            f"masking_name={masking_name}, "
            f"total_models={len(models)}, "
            f"file={output_file}"
        ),
        context="CarWaleModelExecutor",
    )

    return {
        "status": "success",
        "make_id": make_id,
        "make_name": make_name,
        "masking_name": masking_name,
        "total_models": len(models),
        "scraped_at": scraped_at,
        "output_file": str(files["latest_file"]),
        "archive_file": (str(files["archive_file"]) if files["archive_file"] else None),
    }


def run_carwale_single_model(
    *,
    client: ExternalHttpClient,
    brand: Mapping[str, Any],
    output_dir: str | Path,
    status_file: str | Path,
    force: bool = False,
    show_request: bool = False,
    save_request: bool = False,
    request_dir: str | Path | None = None,
) -> dict[str, Any]:
    """
    Run the complete standalone single-brand scraper.

    This function manages the generic status lifecycle:

    - Start run
    - Mark item started
    - Scrape one brand
    - Mark success, skipped, or failed
    - Complete run
    """
    (
        make_id,
        make_name,
        masking_name,
    ) = _validate_brand(brand)

    item_key = masking_name

    item_metadata: dict[str, Any] = {
        "makeId": make_id,
        "makeName": make_name,
        "maskingName": masking_name,
    }

    status_store = ScrapeStatusStore(
        status_file=status_file,
        resource_name=STATUS_RESOURCE_NAME,
    )

    status_store.start_run(
        mode="single",
        selected_items=1,
        total_available_items=1,
        metadata={
            "outputDirectory": str(Path(output_dir)),
            "force": force,
        },
    )

    status_store.mark_started(
        item_key=item_key,
        metadata=item_metadata,
    )

    try:
        result = scrape_carwale_model(
            client=client,
            brand=brand,
            output_dir=output_dir,
            force=force,
            show_request=show_request,
            save_request=save_request,
            request_dir=request_dir,
        )

        result_status = result.get("status")

        if result_status == "success":
            status_store.mark_success(
                item_key=item_key,
                metadata=item_metadata,
                result={
                    "totalModels": result["total_models"],
                    "outputFile": result["output_file"],
                    "scrapedAt": result["scraped_at"],
                },
            )

            summary = {
                "selectedBrands": 1,
                "successfulBrands": 1,
                "failedBrands": 0,
                "skippedBrands": 0,
                "totalModels": result["total_models"],
            }

        elif result_status == "skipped":
            status_store.mark_skipped(
                item_key=item_key,
                metadata=item_metadata,
                result={
                    "totalModels": result["total_models"],
                    "outputFile": result["output_file"],
                },
                reason=("Model file already exists"),
            )

            summary = {
                "selectedBrands": 1,
                "successfulBrands": 0,
                "failedBrands": 0,
                "skippedBrands": 1,
                "totalModels": 0,
            }

        else:
            raise ValueError(
                "Single-brand scraper returned an "
                "unsupported status: "
                f"{result_status!r}"
            )

    except Exception as error:
        status_store.mark_failed(
            item_key=item_key,
            metadata=item_metadata,
            error_type=(error.__class__.__name__),
            error_message=str(error),
        )

        status_store.complete_run(
            metadata={
                "summary": {
                    "selectedBrands": 1,
                    "successfulBrands": 0,
                    "failedBrands": 1,
                    "skippedBrands": 0,
                    "totalModels": 0,
                }
            }
        )

        logger_service.error(
            (
                "Standalone CarWale model scraping "
                "failed: "
                f"brand={make_name}, "
                f"masking_name={masking_name}"
            ),
            exception=error,
            context="CarWaleModelExecutor",
        )

        raise

    status_store.complete_run(
        metadata={
            "summary": summary,
        }
    )

    return result
