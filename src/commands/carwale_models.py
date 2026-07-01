from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.external.executors.carwale.client_factory import (
    create_carwale_client,
)
from src.external.executors.carwale.all_brands import (
    scrape_carwale_models,
)
from src.external.executors.carwale.single_brands import (
    run_carwale_single_model,
)

DEFAULT_BRANDS_FILE = Path("data/raw/carwale/brands.json")

DEFAULT_MODELS_DIRECTORY = Path("data/raw/carwale/models")

DEFAULT_STATUS_FILE = Path("data/raw/carwale/scraping/models_status.json")

DEFAULT_REQUEST_DIRECTORY = Path("data/raw/carwale/requests/models")


def _load_brand_records(
    brands_file: str | Path,
) -> list[dict[str, Any]]:
    """
    Load brand records for single-brand selection.

    Supported JSON structures:

    [
        {...},
        {...},
    ]

    {
        "brands": [...]
    }

    {
        "makeList": [...]
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

    for brand in brands_data:
        if isinstance(brand, dict):
            brands.append(brand)

    if not brands:
        raise ValueError("CarWale brands file does not contain any valid brand records")

    return brands


def _find_brand_by_masking_name(
    *,
    brands_file: str | Path,
    masking_name: str,
) -> dict[str, Any]:
    normalized_masking_name = masking_name.strip().lower()

    if not normalized_masking_name:
        raise ValueError("brand cannot be empty")

    brands = _load_brand_records(brands_file)

    for brand in brands:
        brand_masking_name = brand.get("maskingName")

        if not isinstance(
            brand_masking_name,
            str,
        ):
            continue

        if brand_masking_name.strip().lower() == normalized_masking_name:
            return brand

    raise ValueError(
        "CarWale brand was not found in brands file: "
        f"masking_name={normalized_masking_name!r}, "
        f"file={Path(brands_file)}"
    )


def run_carwale_models(
    *,
    brand: str | None = None,
    brands_file: str | Path = DEFAULT_BRANDS_FILE,
    output_dir: str | Path = DEFAULT_MODELS_DIRECTORY,
    status_file: str | Path = DEFAULT_STATUS_FILE,
    request_dir: str | Path = DEFAULT_REQUEST_DIRECTORY,
    force: bool = False,
    failed_only: bool = False,
    show_request: bool = False,
    save_request: bool = False,
    delay_min: float = 2.0,
    delay_max: float = 4.0,
) -> dict[str, Any]:
    """
    Run the CarWale models scraper.

    Modes:

    - brand provided:
      Scrape one brand.

    - failed_only=True:
      Scrape brands previously marked as failed.

    - otherwise:
      Scrape all brands.
    """
    if brand is not None and failed_only:
        raise ValueError("--brand and --failed-only cannot be used together")

    if delay_min < 0:
        raise ValueError("delay_min cannot be negative")

    if delay_max < 0:
        raise ValueError("delay_max cannot be negative")

    if delay_max < delay_min:
        raise ValueError("delay_max cannot be less than delay_min")

    normalized_brand = brand.strip().lower() if isinstance(brand, str) else None

    if brand is not None and not normalized_brand:
        raise ValueError("brand cannot be empty")

    with create_carwale_client() as client:
        if normalized_brand is not None:
            selected_brand = _find_brand_by_masking_name(
                brands_file=brands_file,
                masking_name=normalized_brand,
            )

            result = run_carwale_single_model(
                client=client,
                brand=selected_brand,
                output_dir=output_dir,
                status_file=status_file,
                force=force,
                show_request=show_request,
                save_request=save_request,
                request_dir=request_dir,
            )

            return {
                "command": "carwale-models",
                "mode": "single",
                "brand": normalized_brand,
                "status": result["status"],
                "models_count": result.get(
                    "total_models",
                    0,
                ),
                "output_file": result.get("output_file"),
                "status_file": str(Path(status_file)),
                "request_file": (
                    str(Path(request_dir) / f"{normalized_brand}.json")
                    if save_request
                    else None
                ),
            }

        summary = scrape_carwale_models(
            client=client,
            brands_file=brands_file,
            output_dir=output_dir,
            status_file=status_file,
            request_dir=request_dir,
            force=force,
            failed_only=failed_only,
            show_request=show_request,
            save_request=save_request,
            delay_min=delay_min,
            delay_max=delay_max,
        )

    return {
        "command": "carwale-models",
        **summary,
        "brands_file": str(Path(brands_file)),
        "output_directory": str(Path(output_dir)),
        "status_file": str(Path(status_file)),
        "request_directory": (str(Path(request_dir)) if save_request else None),
    }
