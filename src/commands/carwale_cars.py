from __future__ import annotations

import json
import re
from concurrent.futures import (
    Future,
    ThreadPoolExecutor,
    as_completed,
)
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.clients.client import ExternalClientError
from src.external.executors.carwale.client_factory import (
    create_carwale_client,
)
from src.external.executors.carwale.model_page import (
    scrape_carwale_model_page,
)
from src.logger.logger import logger_service
from src.storage.json_storage import JsonStorage
from src.storage.scraper_status import ScrapeStatusStore

DEFAULT_MODELS_DIRECTORY = Path("data/raw/carwale/models")

DEFAULT_CARS_DIRECTORY = Path("data/raw/carwale/car")

DEFAULT_STATUS_FILE = Path("data/raw/carwale/scraping/cars_status.json")

DEFAULT_REQUEST_DIRECTORY = Path("data/raw/carwale/requests/cars")

DEFAULT_ARCHIVE_DIRECTORY = Path("data/raw/carwale/archive/cars")

STATUS_RESOURCE_NAME = "carwale_cars"

MASKING_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(
    frozen=True,
    slots=True,
)
class CarScrapingJob:
    make: dict[str, Any]
    model: dict[str, Any]
    make_id: int | None
    make_name: str
    make_masking_name: str
    model_id: int | None
    model_name: str
    model_masking_name: str
    item_key: str
    position: int
    total_selected: int

    def metadata(self) -> dict[str, Any]:
        return {
            "makeId": self.make_id,
            "makeName": self.make_name,
            "makeMaskingName": (self.make_masking_name),
            "modelId": self.model_id,
            "modelName": self.model_name,
            "modelMaskingName": (self.model_masking_name),
            "position": self.position,
            "totalSelected": self.total_selected,
        }


def _normalize_optional_slug(
    value: str | None,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized_value = value.strip().lower()

    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty")

    if not MASKING_NAME_PATTERN.fullmatch(normalized_value):
        raise ValueError(
            f"{field_name} contains invalid characters: {normalized_value!r}"
        )

    return normalized_value


def _normalize_required_slug(
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
            f"{field_name} contains invalid characters: {normalized_value!r}"
        )

    return normalized_value


def _read_model_file(
    input_file: Path,
) -> dict[str, Any]:
    if not input_file.exists():
        raise FileNotFoundError(f"CarWale model file was not found: {input_file}")

    if not input_file.is_file():
        raise ValueError(f"CarWale model path is not a file: {input_file}")

    try:
        payload = json.loads(
            input_file.read_text(
                encoding="utf-8",
            )
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"CarWale model file contains invalid JSON: {input_file}"
        ) from error

    if not isinstance(payload, dict):
        raise ValueError(f"CarWale model file must contain a JSON object: {input_file}")

    return payload


def _discover_model_files(
    models_dir: str | Path,
) -> list[Path]:
    input_directory = Path(models_dir)

    if not input_directory.exists():
        raise FileNotFoundError(
            f"CarWale models directory was not found: {input_directory}"
        )

    if not input_directory.is_dir():
        raise ValueError(f"CarWale models path is not a directory: {input_directory}")

    model_files = sorted(
        file_path for file_path in input_directory.glob("*.json") if file_path.is_file()
    )

    if not model_files:
        raise ValueError(
            "CarWale models directory does not "
            f"contain any JSON files: "
            f"{input_directory}"
        )

    return model_files


def _extract_jobs(
    *,
    models_dir: str | Path,
    selected_brand: str | None,
    selected_model: str | None,
) -> tuple[
    list[
        tuple[
            dict[str, Any],
            dict[str, Any],
            int | None,
            str,
            str,
            int | None,
            str,
            str,
        ]
    ],
    list[dict[str, Any]],
]:
    model_files = _discover_model_files(models_dir)

    raw_jobs: list[
        tuple[
            dict[str, Any],
            dict[str, Any],
            int | None,
            str,
            str,
            int | None,
            str,
            str,
        ]
    ] = []

    input_errors: list[dict[str, Any]] = []

    seen_keys: set[str] = set()
    matching_brand_found = False
    matching_model_found = False

    for input_file in model_files:
        try:
            payload = _read_model_file(input_file)

            make_masking_name = _normalize_required_slug(
                payload.get("maskingName"),
                field_name=(f"{input_file}.maskingName"),
            )

            if selected_brand is not None and make_masking_name != selected_brand:
                continue

            matching_brand_found = True

            make_id_value = payload.get("makeId")

            make_id = (
                make_id_value
                if isinstance(
                    make_id_value,
                    int,
                )
                and not isinstance(
                    make_id_value,
                    bool,
                )
                else None
            )

            make_name_value = payload.get("makeName")

            make_name = (
                make_name_value.strip()
                if isinstance(
                    make_name_value,
                    str,
                )
                else ""
            )

            models = payload.get("models")

            if not isinstance(models, list):
                raise ValueError(
                    "CarWale model file does not "
                    "contain a valid models list: "
                    f"{input_file}"
                )

            make_data: dict[str, Any] = {
                "makeId": payload.get("makeId"),
                "makeName": payload.get("makeName"),
                "maskingName": (make_masking_name),
            }

            for model_index, model in enumerate(models):
                if not isinstance(model, dict):
                    input_errors.append(
                        {
                            "file": str(input_file),
                            "modelIndex": (model_index),
                            "errorType": ("ValueError"),
                            "errorMessage": ("Model entry is not a JSON object"),
                        }
                    )
                    continue

                try:
                    model_masking_name = _normalize_required_slug(
                        model.get("modelMaskingName"),
                        field_name=("modelMaskingName"),
                    )

                except ValueError as error:
                    input_errors.append(
                        {
                            "file": str(input_file),
                            "modelIndex": (model_index),
                            "errorType": (type(error).__name__),
                            "errorMessage": str(error),
                        }
                    )
                    continue

                if selected_model is not None and model_masking_name != selected_model:
                    continue

                matching_model_found = True

                item_key = f"{make_masking_name}/{model_masking_name}"

                if item_key in seen_keys:
                    logger_service.info(
                        (f"Ignoring duplicate CarWale car job: key={item_key}"),
                        context=("CarWaleCarsCommand"),
                    )
                    continue

                seen_keys.add(item_key)

                model_id_value = model.get("modelId")

                model_id = (
                    model_id_value
                    if isinstance(
                        model_id_value,
                        int,
                    )
                    and not isinstance(
                        model_id_value,
                        bool,
                    )
                    else None
                )

                model_name_value = model.get("modelName")

                model_name = (
                    model_name_value.strip()
                    if isinstance(
                        model_name_value,
                        str,
                    )
                    else ""
                )

                raw_jobs.append(
                    (
                        make_data,
                        dict(model),
                        make_id,
                        make_name,
                        make_masking_name,
                        model_id,
                        model_name,
                        model_masking_name,
                    )
                )

        except (
            OSError,
            ValueError,
        ) as error:
            input_errors.append(
                {
                    "file": str(input_file),
                    "errorType": (error.__class__.__name__),
                    "errorMessage": str(error),
                }
            )

            logger_service.error(
                (f"Ignoring invalid CarWale model input file: file={input_file}"),
                exception=error,
                context="CarWaleCarsCommand",
            )

    if selected_brand is not None and not matching_brand_found:
        raise ValueError(
            f"CarWale brand was not found in the models directory: {selected_brand!r}"
        )

    if selected_model is not None and not matching_model_found:
        raise ValueError(
            "CarWale model was not found for "
            f"brand={selected_brand!r}: "
            f"model={selected_model!r}"
        )

    return (
        raw_jobs,
        input_errors,
    )


def _build_jobs(
    *,
    models_dir: str | Path,
    selected_brand: str | None,
    selected_model: str | None,
) -> tuple[
    list[CarScrapingJob],
    list[dict[str, Any]],
]:
    (
        raw_jobs,
        input_errors,
    ) = _extract_jobs(
        models_dir=models_dir,
        selected_brand=selected_brand,
        selected_model=selected_model,
    )

    total_selected = len(raw_jobs)

    jobs: list[CarScrapingJob] = []

    for position, raw_job in enumerate(
        raw_jobs,
        start=1,
    ):
        (
            make,
            model,
            make_id,
            make_name,
            make_masking_name,
            model_id,
            model_name,
            model_masking_name,
        ) = raw_job

        jobs.append(
            CarScrapingJob(
                make=make,
                model=model,
                make_id=make_id,
                make_name=make_name,
                make_masking_name=(make_masking_name),
                model_id=model_id,
                model_name=model_name,
                model_masking_name=(model_masking_name),
                item_key=(f"{make_masking_name}/{model_masking_name}"),
                position=position,
                total_selected=(total_selected),
            )
        )

    return (
        jobs,
        input_errors,
    )


def _output_file_for_job(
    *,
    output_dir: str | Path,
    job: CarScrapingJob,
) -> Path:
    return Path(output_dir) / job.make_masking_name / f"{job.model_masking_name}.json"


def _existing_output_is_valid(
    *,
    output_file: Path,
    job: CarScrapingJob,
) -> bool:
    if not output_file.exists():
        return False

    if not output_file.is_file():
        return False

    try:
        payload = json.loads(
            output_file.read_text(
                encoding="utf-8",
            )
        )

    except (
        OSError,
        json.JSONDecodeError,
    ):
        return False

    if not isinstance(payload, dict):
        return False

    if payload.get("makeMaskingName") != job.make_masking_name:
        return False

    if payload.get("modelMaskingName") != job.model_masking_name:
        return False

    data = payload.get("data")

    if not isinstance(data, dict):
        return False

    if not isinstance(
        data.get("modelDetails"),
        dict,
    ):
        return False

    optional_section_types = (
        dict,
        list,
        type(None),
    )

    if not isinstance(
        data.get("replacedModelDetails"),
        optional_section_types,
    ):
        return False

    if not isinstance(
        data.get("similarCars"),
        optional_section_types,
    ):
        return False

    versions = data.get("versions")

    if not isinstance(versions, list):
        return False

    for version in versions:
        if not isinstance(version, dict):
            return False

        if "specsSummary" in version:
            return False

        if "featureSpecs" in version:
            return False

    return True


def _select_failed_jobs(
    *,
    jobs: list[CarScrapingJob],
    status_store: ScrapeStatusStore,
) -> list[CarScrapingJob]:
    failed_keys = status_store.get_failed_keys()

    if not failed_keys:
        return []

    return [job for job in jobs if job.item_key in failed_keys]


def _save_car_payload(
    *,
    job: CarScrapingJob,
    payload: dict[str, Any],
    output_dir: str | Path,
    archive_dir: str | Path,
) -> dict[str, str | None]:
    files = JsonStorage.save(
        directory=(Path(output_dir) / job.make_masking_name),
        file_name=(job.model_masking_name),
        data=payload,
        create_archive=True,
        archive_directory=(Path(archive_dir) / job.make_masking_name),
    )

    return {
        "output_file": str(files["latest_file"]),
        "archive_file": (
            str(files["archive_file"]) if files["archive_file"] is not None else None
        ),
    }


def _run_single_job(
    *,
    client: Any,
    job: CarScrapingJob,
    city_id: int,
    area_id: int,
    platform_id: int,
    show_offer_upfront: bool,
    show_request: bool,
    save_request: bool,
    request_dir: str | Path,
) -> dict[str, Any]:
    return scrape_carwale_model_page(
        client=client,
        make=job.make,
        model=job.model,
        city_id=city_id,
        area_id=area_id,
        platform_id=platform_id,
        show_offer_upfront=(show_offer_upfront),
        show_request=show_request,
        save_request=save_request,
        request_dir=request_dir,
    )


def run_carwale_cars(
    *,
    brand: str | None = None,
    model: str | None = None,
    models_dir: str | Path = (DEFAULT_MODELS_DIRECTORY),
    output_dir: str | Path = (DEFAULT_CARS_DIRECTORY),
    status_file: str | Path = (DEFAULT_STATUS_FILE),
    request_dir: str | Path = (DEFAULT_REQUEST_DIRECTORY),
    archive_dir: str | Path = (DEFAULT_ARCHIVE_DIRECTORY),
    workers: int = 3,
    min_request_interval: float = 2.0,
    city_id: int = 10,
    area_id: int = 3657,
    platform_id: int = 1,
    show_offer_upfront: bool = False,
    force: bool = False,
    failed_only: bool = False,
    show_request: bool = False,
    save_request: bool = False,
) -> dict[str, Any]:
    """
    Scrape CarWale model-page data for one or many
    car models.

    Worker threads only perform HTTP fetching and
    response transformation.

    The main thread performs:

    - Status-store updates
    - Existing-file checks
    - Final JSON writes
    - Summary collection

    This keeps ScrapeStatusStore safe even though it
    is not designed for concurrent writes.
    """
    normalized_brand = _normalize_optional_slug(
        brand,
        field_name="brand",
    )

    normalized_model = _normalize_optional_slug(
        model,
        field_name="model",
    )

    if normalized_model is not None and normalized_brand is None:
        raise ValueError("--model requires --brand")

    if failed_only and (normalized_brand is not None or normalized_model is not None):
        raise ValueError("--failed-only cannot be combined with --brand or --model")

    if (
        not isinstance(workers, int)
        or isinstance(workers, bool)
        or workers < 1
        or workers > 8
    ):
        raise ValueError("workers must be an integer between 1 and 8")

    if min_request_interval < 0:
        raise ValueError("min_request_interval cannot be negative")

    if city_id <= 0:
        raise ValueError("city_id must be greater than zero")

    if area_id < 0:
        raise ValueError("area_id cannot be negative")

    if platform_id <= 0:
        raise ValueError("platform_id must be greater than zero")

    (
        all_jobs,
        input_errors,
    ) = _build_jobs(
        models_dir=models_dir,
        selected_brand=normalized_brand,
        selected_model=normalized_model,
    )

    status_store = ScrapeStatusStore(
        status_file=status_file,
        resource_name=STATUS_RESOURCE_NAME,
    )

    mode = "all"

    if failed_only:
        mode = "failed-only"

        selected_jobs = _select_failed_jobs(
            jobs=all_jobs,
            status_store=status_store,
        )

    elif normalized_model is not None:
        mode = "single-model"
        selected_jobs = all_jobs

    elif normalized_brand is not None:
        mode = "single-brand"
        selected_jobs = all_jobs

    else:
        selected_jobs = all_jobs

    summary: dict[str, Any] = {
        "mode": mode,
        "total_available_cars": len(all_jobs),
        "selected_cars": len(selected_jobs),
        "successful_cars": 0,
        "failed_cars": 0,
        "skipped_cars": 0,
        "total_versions": 0,
        "workers": workers,
        "min_request_interval": (min_request_interval),
        "input_errors": input_errors,
        "failures": [],
    }

    status_store.start_run(
        mode=mode,
        selected_items=len(selected_jobs),
        total_available_items=len(all_jobs),
        metadata={
            "modelsDirectory": str(Path(models_dir)),
            "outputDirectory": str(Path(output_dir)),
            "requestDirectory": (str(Path(request_dir)) if save_request else None),
            "archiveDirectory": str(Path(archive_dir)),
            "brand": normalized_brand,
            "model": normalized_model,
            "workers": workers,
            "minimumRequestInterval": (min_request_interval),
            "cityId": city_id,
            "areaId": area_id,
            "platformId": platform_id,
            "showOfferUpfront": (show_offer_upfront),
            "force": force,
            "failedOnly": failed_only,
            "inputErrors": input_errors,
        },
    )

    logger_service.info(
        (
            "Starting CarWale cars scraping: "
            f"mode={mode}, "
            f"available={len(all_jobs)}, "
            f"selected={len(selected_jobs)}, "
            f"workers={workers}, "
            "minimum_request_interval="
            f"{min_request_interval:.2f}s"
        ),
        context="CarWaleCarsCommand",
    )

    if not selected_jobs:
        completed_run = status_store.complete_run(
            metadata={
                "summary": summary,
            }
        )

        return {
            "command": "carwale-cars",
            **summary,
            "status_file": str(Path(status_file)),
            "completed_run": completed_run,
        }

    pending_jobs: list[CarScrapingJob] = []

    for job in selected_jobs:
        metadata = job.metadata()

        status_store.mark_started(
            item_key=job.item_key,
            metadata=metadata,
        )

        output_file = _output_file_for_job(
            output_dir=output_dir,
            job=job,
        )

        should_skip_existing = (
            not force
            and not failed_only
            and _existing_output_is_valid(
                output_file=output_file,
                job=job,
            )
        )

        if should_skip_existing:
            summary["skipped_cars"] += 1

            status_store.mark_skipped(
                item_key=job.item_key,
                metadata=metadata,
                result={
                    "outputFile": str(output_file),
                },
                reason=("Valid car file already exists"),
            )

            logger_service.info(
                (
                    "Skipping existing CarWale "
                    "car file: "
                    f"key={job.item_key}, "
                    f"file={output_file}"
                ),
                context=("CarWaleCarsCommand"),
            )

            continue

        pending_jobs.append(job)

    if pending_jobs:
        with create_carwale_client(
            workers=workers,
            min_request_interval=(min_request_interval),
        ) as client:
            with ThreadPoolExecutor(
                max_workers=workers,
                thread_name_prefix=("carwale-car"),
            ) as executor:
                future_to_job: dict[
                    Future[dict[str, Any]],
                    CarScrapingJob,
                ] = {}

                for job in pending_jobs:
                    future = executor.submit(
                        _run_single_job,
                        client=client,
                        job=job,
                        city_id=city_id,
                        area_id=area_id,
                        platform_id=platform_id,
                        show_offer_upfront=(show_offer_upfront),
                        show_request=(show_request),
                        save_request=(save_request),
                        request_dir=request_dir,
                    )

                    future_to_job[future] = job

                for future in as_completed(future_to_job):
                    job = future_to_job[future]

                    metadata = job.metadata()

                    try:
                        result = future.result()

                        if result.get("status") != "success":
                            raise ValueError(
                                "Model-page executor "
                                "returned an "
                                "unsupported status: "
                                f"{result.get('status')!r}"
                            )

                        payload = result.get("payload")

                        if not isinstance(
                            payload,
                            dict,
                        ):
                            raise ValueError(
                                "Model-page executor did not return a valid payload"
                            )

                        saved_files = _save_car_payload(
                            job=job,
                            payload=payload,
                            output_dir=(output_dir),
                            archive_dir=(archive_dir),
                        )

                        total_versions = result.get(
                            "total_versions",
                            0,
                        )

                        if not isinstance(
                            total_versions,
                            int,
                        ):
                            total_versions = 0

                        summary["successful_cars"] += 1

                        summary["total_versions"] += total_versions

                        status_store.mark_success(
                            item_key=(job.item_key),
                            metadata=metadata,
                            result={
                                "totalVersions": (total_versions),
                                "outputFile": (saved_files["output_file"]),
                                "archiveFile": (saved_files["archive_file"]),
                                "requestFile": (result.get("request_file")),
                                "scrapedAt": (result.get("scraped_at")),
                            },
                        )

                        logger_service.info(
                            (
                                "CarWale car saved: "
                                f"key={job.item_key}, "
                                "total_versions="
                                f"{total_versions}, "
                                "file="
                                f"{saved_files['output_file']}"
                            ),
                            context=("CarWaleCarsCommand"),
                        )

                    except (
                        ExternalClientError,
                        OSError,
                        ValueError,
                    ) as error:
                        summary["failed_cars"] += 1

                        failure = {
                            **metadata,
                            "itemKey": (job.item_key),
                            "errorType": (type(error).__name__),
                            "errorMessage": str(error),
                        }

                        summary["failures"].append(failure)

                        status_store.mark_failed(
                            item_key=(job.item_key),
                            metadata=metadata,
                            error_type=(type(error).__name__),
                            error_message=str(error),
                        )

                        logger_service.error(
                            (f"CarWale car scraping failed: key={job.item_key}"),
                            exception=error,
                            context=("CarWaleCarsCommand"),
                        )

                    except Exception as error:
                        summary["failed_cars"] += 1

                        failure = {
                            **metadata,
                            "itemKey": (job.item_key),
                            "errorType": (type(error).__name__),
                            "errorMessage": str(error),
                        }

                        summary["failures"].append(failure)

                        status_store.mark_failed(
                            item_key=(job.item_key),
                            metadata=metadata,
                            error_type=(type(error).__name__),
                            error_message=str(error),
                        )

                        logger_service.error(
                            (
                                "Unexpected error "
                                "while processing "
                                "CarWale car: "
                                f"key={job.item_key}"
                            ),
                            exception=error,
                            context=("CarWaleCarsCommand"),
                        )

    completed_run = status_store.complete_run(
        metadata={
            "summary": summary,
        }
    )

    logger_service.info(
        (
            "CarWale cars scraping completed: "
            f"selected="
            f"{summary['selected_cars']}, "
            f"successful="
            f"{summary['successful_cars']}, "
            f"failed="
            f"{summary['failed_cars']}, "
            f"skipped="
            f"{summary['skipped_cars']}, "
            f"total_versions="
            f"{summary['total_versions']}"
        ),
        context="CarWaleCarsCommand",
    )

    return {
        "command": "carwale-cars",
        **summary,
        "models_directory": str(Path(models_dir)),
        "output_directory": str(Path(output_dir)),
        "status_file": str(Path(status_file)),
        "request_directory": (str(Path(request_dir)) if save_request else None),
        "archive_directory": str(Path(archive_dir)),
        "completed_run": completed_run,
    }
