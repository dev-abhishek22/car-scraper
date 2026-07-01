from __future__ import annotations

from pathlib import Path
from typing import Any

from src.clients.client import ExternalClientError
from src.external.executors.carwale.cities import (
    scrape_carwale_cities,
)
from src.external.executors.carwale.client_factory import (
    create_carwale_client,
)
from src.logger.logger import logger_service
from src.storage.json_storage import JsonStorage

DEFAULT_CITIES_DIRECTORY = Path("data/raw/carwale")

DEFAULT_REQUEST_DIRECTORY = Path("data/raw/carwale/requests/cities")

DEFAULT_ARCHIVE_DIRECTORY = Path("data/raw/carwale/archive/cities")

DEFAULT_REQUEST_FILE_NAME = "cities_request.json"


def _build_request_log_file(
    *,
    request_dir: str | Path,
) -> Path:
    return Path(request_dir) / DEFAULT_REQUEST_FILE_NAME


def _save_cities(
    *,
    cities: list[dict[str, Any]],
    output_dir: str | Path,
    archive_dir: str | Path,
) -> dict[str, str | None]:
    files = JsonStorage.save(
        directory=Path(output_dir),
        file_name="cities",
        data=cities,
        create_archive=True,
        archive_directory=Path(archive_dir),
    )

    return {
        "output_file": str(files["latest_file"]),
        "archive_file": (
            str(files["archive_file"]) if files["archive_file"] is not None else None
        ),
    }


def run_carwale_cities(
    *,
    output_dir: str | Path = (DEFAULT_CITIES_DIRECTORY),
    request_dir: str | Path = (DEFAULT_REQUEST_DIRECTORY),
    archive_dir: str | Path = (DEFAULT_ARCHIVE_DIRECTORY),
    min_request_interval: float = 2.0,
    show_request: bool = False,
    save_request: bool = False,
) -> dict[str, Any]:
    """
    Scrape all cities from the CarWale cities API.

    This command is responsible for:

    - Creating the CarWale HTTP client
    - Calling the cities executor
    - Saving the latest cities file
    - Creating an archived copy
    - Returning the command summary

    The cities API returns every city in one
    request, so workers and status tracking are
    not required.
    """

    if isinstance(
        min_request_interval,
        bool,
    ) or not isinstance(
        min_request_interval,
        (
            int,
            float,
        ),
    ):
        raise TypeError("min_request_interval must be " "a number")

    if min_request_interval < 0:
        raise ValueError("min_request_interval cannot be " "negative")

    request_log_file: Path | None = None

    if save_request:
        request_log_file = _build_request_log_file(
            request_dir=request_dir,
        )

    logger_service.info(
        (
            "Starting CarWale cities scraping: "
            "mode=single-request, "
            "minimum_request_interval="
            f"{min_request_interval:.2f}s"
        ),
        context="CarWaleCitiesCommand",
    )

    try:
        with create_carwale_client(
            workers=1,
            min_request_interval=(float(min_request_interval)),
        ) as client:
            cities = scrape_carwale_cities(
                client=client,
                show_request=show_request,
                request_log_file=(request_log_file),
            )

        saved_files = _save_cities(
            cities=cities,
            output_dir=output_dir,
            archive_dir=archive_dir,
        )

    except (
        ExternalClientError,
        OSError,
        ValueError,
    ) as error:
        logger_service.error(
            "CarWale cities scraping failed",
            exception=error,
            context="CarWaleCitiesCommand",
        )

        raise

    logger_service.info(
        (
            "CarWale cities scraping completed: "
            f"total_cities={len(cities)}, "
            "file="
            f"{saved_files['output_file']}"
        ),
        context="CarWaleCitiesCommand",
    )

    return {
        "command": "carwale-cities",
        "total_cities": len(cities),
        "output_file": (saved_files["output_file"]),
        "archive_file": (saved_files["archive_file"]),
        "request_file": (
            str(request_log_file) if request_log_file is not None else None
        ),
        "output_directory": str(Path(output_dir)),
        "request_directory": (str(Path(request_dir)) if save_request else None),
        "archive_directory": str(Path(archive_dir)),
        "min_request_interval": float(min_request_interval),
    }
