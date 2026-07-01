from __future__ import annotations

import json
import random
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from src.clients.client import (
    ExternalClientError,
    ExternalHttpClient,
)
from src.external.executors.carwale.single_brands import (
    scrape_carwale_model,
)
from src.logger.logger import logger_service
from src.storage.scraper_status import ScrapeStatusStore

STATUS_RESOURCE_NAME = "carwale_models"


def _load_brands(
    brands_file: str | Path,
) -> list[dict[str, Any]]:
    """
    Load brands from the CarWale brands JSON file.

    Supported structures:

    [
        {...},
        {...},
    ]

    {
        "brands": [
            {...},
            {...},
        ]
    }

    {
        "makeList": [
            {...},
            {...},
        ]
    }
    """
    input_file = Path(brands_file)

    if not input_file.exists():
        raise FileNotFoundError(f"CarWale brands file was not found: {input_file}")

    if not input_file.is_file():
        raise ValueError(f"CarWale brands path is not a file: {input_file}")

    try:
        payload = json.loads(
            input_file.read_text(
                encoding="utf-8",
            )
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"CarWale brands file contains invalid JSON: {input_file}"
        ) from error

    brands_data: Any = payload

    if isinstance(payload, dict):
        if isinstance(
            payload.get("brands"),
            list,
        ):
            brands_data = payload["brands"]

        elif isinstance(
            payload.get("makeList"),
            list,
        ):
            brands_data = payload["makeList"]

        else:
            raise ValueError(
                "CarWale brands file does not contain a brands or makeList array"
            )

    if not isinstance(brands_data, list):
        raise ValueError("CarWale brands file must contain a JSON array")

    brands: list[dict[str, Any]] = []

    for index, brand in enumerate(brands_data):
        if not isinstance(brand, dict):
            logger_service.error(
                (
                    "Ignoring invalid brand entry: "
                    f"index={index}, "
                    f"type={type(brand).__name__}"
                ),
                context="CarWaleModelsExecutor",
            )
            continue

        brands.append(brand)

    if not brands:
        raise ValueError("CarWale brands file does not contain any valid brand objects")

    return brands


def _get_brand_identity(
    brand: Mapping[str, Any],
) -> tuple[int | None, str, str]:
    """
    Read and normalize the basic brand identity.

    Full validation remains the responsibility of the
    single-brand executor.
    """
    make_id = brand.get("makeId")
    make_name = brand.get("makeName")
    masking_name = brand.get("maskingName")

    normalized_make_id = make_id if isinstance(make_id, int) else None

    normalized_make_name = make_name.strip() if isinstance(make_name, str) else ""

    normalized_masking_name = (
        masking_name.strip().lower() if isinstance(masking_name, str) else ""
    )

    return (
        normalized_make_id,
        normalized_make_name,
        normalized_masking_name,
    )


def _build_status_item_key(
    *,
    make_id: int | None,
    masking_name: str,
    index: int,
) -> str:
    """
    Build a non-empty key for the generic status store.

    Normally maskingName is used. Fallback keys allow an
    invalid brand entry to still be recorded as failed.
    """
    if masking_name:
        return masking_name

    if make_id is not None:
        return f"make-id-{make_id}"

    return f"invalid-brand-{index}"


def _build_brand_metadata(
    *,
    make_id: int | None,
    make_name: str,
    masking_name: str,
    position: int,
    total: int,
) -> dict[str, Any]:
    return {
        "makeId": make_id,
        "makeName": make_name,
        "maskingName": masking_name,
        "position": position,
        "totalSelected": total,
    }


def _select_failed_brands(
    *,
    brands: list[dict[str, Any]],
    status_store: ScrapeStatusStore,
) -> list[dict[str, Any]]:
    """
    Select brands whose maskingName is currently marked
    as failed in the generic status store.
    """
    failed_keys = status_store.get_failed_keys()

    if not failed_keys:
        return []

    selected_brands: list[dict[str, Any]] = []

    for brand in brands:
        masking_name = brand.get("maskingName")

        if not isinstance(
            masking_name,
            str,
        ):
            continue

        normalized_masking_name = masking_name.strip().lower()

        if normalized_masking_name and normalized_masking_name in failed_keys:
            selected_brands.append(brand)

    return selected_brands


def scrape_carwale_models(
    *,
    client: ExternalHttpClient,
    brands_file: str | Path,
    output_dir: str | Path,
    status_file: str | Path,
    request_dir: str | Path | None = None,
    force: bool = False,
    failed_only: bool = False,
    show_request: bool = False,
    save_request: bool = False,
    delay_min: float = 2.0,
    delay_max: float = 4.0,
) -> dict[str, Any]:
    """
    Scrape models for multiple CarWale brands.

    Each brand is processed by scrape_carwale_model().

    Retry handling and HTTP 429 handling remain inside
    ExternalHttpClient.

    One brand failure does not stop the remaining brands.
    """
    if delay_min < 0:
        raise ValueError("delay_min cannot be negative")

    if delay_max < 0:
        raise ValueError("delay_max cannot be negative")

    if delay_max < delay_min:
        raise ValueError("delay_max cannot be less than delay_min")

    brands = _load_brands(brands_file)

    status_store = ScrapeStatusStore(
        status_file=status_file,
        resource_name=STATUS_RESOURCE_NAME,
    )

    mode = "all"
    selected_brands = brands

    if failed_only:
        mode = "failed-only"

        selected_brands = _select_failed_brands(
            brands=brands,
            status_store=status_store,
        )

    summary: dict[str, Any] = {
        "mode": mode,
        "total_available_brands": len(brands),
        "selected_brands": len(selected_brands),
        "successful_brands": 0,
        "failed_brands": 0,
        "skipped_brands": 0,
        "total_models": 0,
    }

    status_store.start_run(
        mode=mode,
        selected_items=len(selected_brands),
        total_available_items=len(brands),
        metadata={
            "brandsFile": str(Path(brands_file)),
            "outputDirectory": str(Path(output_dir)),
            "failedOnly": failed_only,
            "force": force,
        },
    )

    logger_service.info(
        (
            "Starting CarWale models scraping: "
            f"mode={mode}, "
            f"available_brands={len(brands)}, "
            f"selected_brands="
            f"{len(selected_brands)}"
        ),
        context="CarWaleModelsExecutor",
    )

    if not selected_brands:
        status_store.complete_run(
            metadata={
                "summary": summary,
            }
        )

        logger_service.info(
            (f"No CarWale brands were selected: mode={mode}"),
            context="CarWaleModelsExecutor",
        )

        return summary

    total_selected = len(selected_brands)

    for index, brand in enumerate(
        selected_brands,
        start=1,
    ):
        (
            make_id,
            make_name,
            masking_name,
        ) = _get_brand_identity(brand)

        item_key = _build_status_item_key(
            make_id=make_id,
            masking_name=masking_name,
            index=index,
        )

        display_name = make_name or masking_name or item_key

        metadata = _build_brand_metadata(
            make_id=make_id,
            make_name=make_name,
            masking_name=masking_name,
            position=index,
            total=total_selected,
        )

        logger_service.info(
            (
                "Processing CarWale brand: "
                f"position={index}/"
                f"{total_selected}, "
                f"brand={display_name}, "
                f"masking_name="
                f"{masking_name or '<missing>'}"
            ),
            context="CarWaleModelsExecutor",
        )

        status_store.mark_started(
            item_key=item_key,
            metadata=metadata,
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
                total_models = result.get(
                    "total_models",
                    0,
                )

                if not isinstance(
                    total_models,
                    int,
                ):
                    total_models = 0

                summary["successful_brands"] += 1

                summary["total_models"] += total_models

                status_store.mark_success(
                    item_key=item_key,
                    metadata=metadata,
                    result={
                        "totalModels": (total_models),
                        "outputFile": result.get("output_file"),
                        "scrapedAt": result.get("scraped_at"),
                    },
                )

            elif result_status == "skipped":
                total_models = result.get(
                    "total_models",
                    0,
                )

                if not isinstance(
                    total_models,
                    int,
                ):
                    total_models = 0

                summary["skipped_brands"] += 1

                status_store.mark_skipped(
                    item_key=item_key,
                    metadata=metadata,
                    result={
                        "totalModels": (total_models),
                        "outputFile": result.get("output_file"),
                    },
                    reason=("Model file already exists"),
                )

            else:
                raise ValueError(
                    "Single-brand executor returned "
                    "an unsupported status: "
                    f"{result_status!r}"
                )

        except (
            ExternalClientError,
            ValueError,
            OSError,
        ) as error:
            summary["failed_brands"] += 1

            status_store.mark_failed(
                item_key=item_key,
                metadata=metadata,
                error_type=(error.__class__.__name__),
                error_message=str(error),
            )

            logger_service.error(
                (
                    "CarWale brand model scraping "
                    "failed: "
                    f"position={index}/"
                    f"{total_selected}, "
                    f"brand={display_name}, "
                    f"masking_name="
                    f"{masking_name or '<missing>'}"
                ),
                exception=error,
                context=("CarWaleModelsExecutor"),
            )

        except Exception as error:
            summary["failed_brands"] += 1

            status_store.mark_failed(
                item_key=item_key,
                metadata=metadata,
                error_type=(error.__class__.__name__),
                error_message=str(error),
            )

            logger_service.error(
                (
                    "Unexpected error while scraping "
                    "CarWale brand models: "
                    f"position={index}/"
                    f"{total_selected}, "
                    f"brand={display_name}, "
                    f"masking_name="
                    f"{masking_name or '<missing>'}"
                ),
                exception=error,
                context=("CarWaleModelsExecutor"),
            )

        is_last_brand = index == total_selected

        if not is_last_brand:
            request_delay = random.uniform(
                delay_min,
                delay_max,
            )

            logger_service.info(
                (f"Waiting before next CarWale brand: delay={request_delay:.2f}s"),
                context=("CarWaleModelsExecutor"),
            )

            time.sleep(request_delay)

    status_store.complete_run(
        metadata={
            "summary": summary,
        }
    )

    logger_service.info(
        (
            "CarWale models scraping completed: "
            f"selected="
            f"{summary['selected_brands']}, "
            f"successful="
            f"{summary['successful_brands']}, "
            f"failed="
            f"{summary['failed_brands']}, "
            f"skipped="
            f"{summary['skipped_brands']}, "
            f"total_models="
            f"{summary['total_models']}"
        ),
        context="CarWaleModelsExecutor",
    )

    return summary
