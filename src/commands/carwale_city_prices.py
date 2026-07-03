from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from src.databases.mongodb import mongo_connection
from src.external.executors.carwale.async_client_factory import (
    create_carwale_async_client,
)
from src.external.executors.carwale.city_price import (
    CarWaleCityPriceExecutor,
)
from src.external.executors.carwale.city_price_jobs import (
    iter_carwale_city_price_jobs,
)
from src.logger.logger import logger_service
from src.models.carwale_city_price_run import (
    CarWaleCityPriceRun,
)
from src.pipelines.carwale_city_price_pipeline import (
    CarWaleCityPricePipeline,
)
from src.repositories.carwale_city_price_failure_repository import (
    carwale_city_price_failure_repository,
)
from src.repositories.carwale_city_price_repository import (
    carwale_city_price_repository,
)
from src.repositories.carwale_city_price_run_repository import (
    carwale_city_price_run_repository,
)

DEFAULT_CARS_DIRECTORY = Path("data/raw/carwale/car")

DEFAULT_CITIES_FILE = Path("data/raw/carwale/cities.json")


def _build_interruption_error(
    *,
    stop_reason: str | None,
    stop_http_status: int | None,
) -> RuntimeError:
    message = "CarWale city-price pipeline stopped early"

    if stop_reason:
        message += f": reason={stop_reason}"

    if stop_http_status is not None:
        message += f", http_status={stop_http_status}"

    return RuntimeError(message)


async def run_carwale_city_prices(
    *,
    cars_directory: str | Path = DEFAULT_CARS_DIRECTORY,
    cities_file: str | Path = DEFAULT_CITIES_FILE,
    brand: str | None = None,
    model: str | None = None,
    city: str | None = None,
    workers: int = 5,
    requests_per_second: float = 2.0,
    mongo_batch_size: int = 100,
    pause_every_requests: int | None = None,
    pause_seconds: float | None = None,
    max_jobs: int | None = None,
    resume_run_id: str | None = None,
    failed_only: bool = False,
    retry_terminal_failures: bool = False,
) -> dict[str, Any]:
    if failed_only and resume_run_id is None:
        raise ValueError("--failed-only requires --resume-run-id")

    if model is not None and brand is None:
        raise ValueError("model requires brand")

    if workers < 1:
        raise ValueError("workers must be at least 1")

    if requests_per_second <= 0:
        raise ValueError("requests_per_second must be greater than zero")

    if mongo_batch_size < 1:
        raise ValueError("mongo_batch_size must be at least 1")

    pause_override_requested = (
        pause_every_requests is not None or pause_seconds is not None
    )

    if pause_override_requested and (
        pause_every_requests is None or pause_seconds is None
    ):
        raise ValueError(
            "--pause-every-requests and --pause-seconds must be provided together"
        )

    if pause_every_requests is not None and (
        isinstance(pause_every_requests, bool) or pause_every_requests < 0
    ):
        raise ValueError("pause_every_requests must be a non-negative integer")

    if pause_seconds is not None and (
        isinstance(pause_seconds, bool) or pause_seconds < 0
    ):
        raise ValueError("pause_seconds must be a non-negative number")

    if pause_override_requested:
        pause_count_enabled = (
            pause_every_requests is not None and pause_every_requests > 0
        )
        pause_duration_enabled = pause_seconds is not None and pause_seconds > 0

        if pause_count_enabled != pause_duration_enabled:
            raise ValueError(
                "pause_every_requests and pause_seconds must "
                "both be greater than zero or both be zero"
            )

    if max_jobs is not None and max_jobs < 1:
        raise ValueError("max_jobs must be at least 1")

    normalized_resume_run_id = (
        resume_run_id.strip() if resume_run_id is not None else None
    )

    if resume_run_id is not None and not normalized_resume_run_id:
        raise ValueError("resume_run_id cannot be empty")

    run_id: str | None = None
    pipeline: CarWaleCityPricePipeline | None = None
    client_metrics: dict[str, Any] = {}

    await mongo_connection.connect()

    try:
        if normalized_resume_run_id is None:
            active_cars_directory = Path(cars_directory)
            active_cities_file = Path(cities_file)

            active_brand = brand
            active_model = model
            active_city = city
            active_max_jobs = max_jobs

            active_workers = workers
            active_requests_per_second = requests_per_second
            active_mongo_batch_size = mongo_batch_size
            active_pause_every_requests = (
                pause_every_requests if pause_every_requests is not None else 0
            )
            active_pause_seconds = pause_seconds if pause_seconds is not None else 0.0

            run = CarWaleCityPriceRun.create(
                cars_directory=str(active_cars_directory),
                cities_file=str(active_cities_file),
                brand=active_brand,
                model=active_model,
                city=active_city,
                max_jobs=active_max_jobs,
                workers=active_workers,
                requests_per_second=(active_requests_per_second),
                mongo_batch_size=(active_mongo_batch_size),
                pause_every_requests=(active_pause_every_requests),
                pause_seconds=active_pause_seconds,
            )

            await carwale_city_price_run_repository.create(run)

            run_id = run.run_id
            resumed = False

        else:
            existing_run = await carwale_city_price_run_repository.require(
                normalized_resume_run_id
            )

            if pause_override_requested:
                existing_run = (
                    await carwale_city_price_run_repository.update_pause_settings(
                        normalized_resume_run_id,
                        pause_every_requests=(
                            pause_every_requests
                            if pause_every_requests is not None
                            else 0
                        ),
                        pause_seconds=(
                            pause_seconds if pause_seconds is not None else 0.0
                        ),
                    )
                )

            resumed_run = await carwale_city_price_run_repository.mark_resumed(
                normalized_resume_run_id
            )

            run_id = resumed_run.run_id
            resumed = True

            active_cars_directory = Path(existing_run.settings.cars_directory)
            active_cities_file = Path(existing_run.settings.cities_file)

            active_brand = existing_run.filters.brand
            active_model = existing_run.filters.model
            active_city = existing_run.filters.city
            active_max_jobs = existing_run.filters.max_jobs

            active_workers = existing_run.settings.workers
            active_requests_per_second = existing_run.settings.requests_per_second
            active_mongo_batch_size = existing_run.settings.mongo_batch_size
            active_pause_every_requests = existing_run.settings.pause_every_requests
            active_pause_seconds = existing_run.settings.pause_seconds

        logger_service.info(
            (
                "Starting CarWale city-price "
                "scraping: "
                f"run_id={run_id}, "
                f"resumed={resumed}, "
                f"failed_only={failed_only}, "
                f"brand={active_brand}, "
                f"model={active_model}, "
                f"city={active_city}, "
                f"workers={active_workers}, "
                "requests_per_second="
                f"{active_requests_per_second:.2f}, "
                "mongo_batch_size="
                f"{active_mongo_batch_size}, "
                "pause_every_requests="
                f"{active_pause_every_requests}, "
                "pause_seconds="
                f"{active_pause_seconds:.2f}"
            ),
            context="CarWaleCityPricesCommand",
        )

        if failed_only:
            jobs = carwale_city_price_failure_repository.iter_unresolved_jobs(
                run_id=run_id,
                retryable_only=(not retry_terminal_failures),
            )
        else:
            jobs = iter_carwale_city_price_jobs(
                cars_directory=(active_cars_directory),
                cities_file=active_cities_file,
                selected_brand=active_brand,
                selected_model=active_model,
                selected_city=active_city,
                max_jobs=active_max_jobs,
            )

        async with create_carwale_async_client(
            concurrency=active_workers,
            requests_per_second=(active_requests_per_second),
            pause_every_requests=(active_pause_every_requests),
            pause_seconds=active_pause_seconds,
        ) as client:
            executor = CarWaleCityPriceExecutor(client)

            pipeline = CarWaleCityPricePipeline(
                executor=executor,
                repository=(carwale_city_price_repository),
                failure_repository=(carwale_city_price_failure_repository),
                run_repository=(carwale_city_price_run_repository),
                workers=active_workers,
                job_queue_size=max(
                    active_workers * 20,
                    500,
                ),
                result_queue_size=max(
                    active_workers * 20,
                    100,
                ),
                failure_queue_size=max(
                    active_workers * 20,
                    100,
                ),
                mongo_batch_size=(active_mongo_batch_size),
                failure_batch_size=min(
                    active_mongo_batch_size,
                    50,
                ),
                resume_check_batch_size=1_000,
                progress_interval=10.0,
                retry_terminal_failures=(retry_terminal_failures),
            )

            summary = await pipeline.run(
                jobs,
                run_id=run_id,
            )

            client_metrics = client.metrics_snapshot()

        unresolved_failures = await (
            carwale_city_price_failure_repository.count_unresolved(
                run_id=run_id,
                retryable_only=False,
            )
        )

        stopped_early = bool(summary.get("stoppedEarly", False))

        stop_reason_value = summary.get("stopReason")
        stop_reason = (
            stop_reason_value
            if isinstance(stop_reason_value, str) and stop_reason_value.strip()
            else None
        )

        stop_http_status_value = summary.get("stopHttpStatus")
        stop_http_status = (
            stop_http_status_value
            if isinstance(
                stop_http_status_value,
                int,
            )
            and not isinstance(
                stop_http_status_value,
                bool,
            )
            else None
        )

        if stopped_early:
            interruption_error = _build_interruption_error(
                stop_reason=stop_reason,
                stop_http_status=(stop_http_status),
            )

            finished_run = await carwale_city_price_run_repository.mark_interrupted(
                run_id,
                progress=(pipeline.progress_snapshot()),
                error=interruption_error,
                stop_reason=stop_reason,
                stop_http_status=(stop_http_status),
            )
        else:
            finished_run = await carwale_city_price_run_repository.mark_completed(
                run_id,
                progress=(pipeline.progress_snapshot()),
            )

        return {
            "command": "carwale-city-prices",
            "runId": run_id,
            "status": finished_run.status,
            "resumed": resumed,
            "failedOnly": failed_only,
            "retryTerminalFailures": (retry_terminal_failures),
            "brand": active_brand,
            "model": active_model,
            "city": active_city,
            "workers": active_workers,
            "requestsPerSecond": (active_requests_per_second),
            "mongoBatchSize": (active_mongo_batch_size),
            "pauseEveryRequests": (active_pause_every_requests),
            "pauseSeconds": active_pause_seconds,
            "maxJobs": active_max_jobs,
            "carsDirectory": str(active_cars_directory),
            "citiesFile": str(active_cities_file),
            "unresolvedFailures": (unresolved_failures),
            "httpMetrics": client_metrics,
            **summary,
        }

    except asyncio.CancelledError as error:
        if run_id is not None:
            progress = pipeline.progress_snapshot() if pipeline is not None else {}

            try:
                await asyncio.shield(
                    carwale_city_price_run_repository.mark_interrupted(
                        run_id,
                        progress=progress,
                        error=error,
                        stop_reason=("keyboard_interrupt"),
                    )
                )
            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarWale "
                        "city-price run as "
                        "interrupted: "
                        f"run_id={run_id}"
                    ),
                    exception=tracking_error,
                    context=("CarWaleCityPricesCommand"),
                )

        raise

    except KeyboardInterrupt as error:
        if run_id is not None:
            progress = pipeline.progress_snapshot() if pipeline is not None else {}

            try:
                await carwale_city_price_run_repository.mark_interrupted(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("keyboard_interrupt"),
                )
            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarWale "
                        "city-price run as "
                        "interrupted: "
                        f"run_id={run_id}"
                    ),
                    exception=tracking_error,
                    context=("CarWaleCityPricesCommand"),
                )

        raise

    except Exception as error:
        if run_id is not None:
            progress = pipeline.progress_snapshot() if pipeline is not None else {}

            try:
                await carwale_city_price_run_repository.mark_failed(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("pipeline_error"),
                )
            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark CarWale "
                        "city-price run as failed: "
                        f"run_id={run_id}"
                    ),
                    exception=tracking_error,
                    context=("CarWaleCityPricesCommand"),
                )

        raise

    finally:
        await mongo_connection.close()
