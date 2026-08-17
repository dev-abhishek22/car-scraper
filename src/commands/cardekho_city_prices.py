from __future__ import annotations

import asyncio
from typing import Any

from src.databases.mongodb import mongo_connection
from src.external.executors.cardekho.async_client_factory import (
    create_cardekho_async_client,
)
from src.external.executors.cardekho.city_price import (
    CardekhoCityPriceExecutor,
)
from src.external.executors.cardekho.city_price_jobs import (
    iter_cardekho_city_price_jobs,
)
from src.logger.logger import logger_service
from src.models.cardekho_city_price_run import (
    CardekhoCityPriceRun,
)
from src.pipelines.cardekho_city_price_pipeline import (
    CardekhoCityPricePipeline,
)
from src.repositories.cardekho_city_price_failure_repository import (
    cardekho_city_price_failure_repository,
)
from src.repositories.cardekho_city_price_repository import (
    cardekho_city_price_repository,
)
from src.repositories.cardekho_city_price_run_repository import (
    cardekho_city_price_run_repository,
)


def _build_interruption_error(
    *,
    stop_reason: str | None,
    stop_http_status: int | None,
) -> RuntimeError:
    message = "Cardekho city-price pipeline stopped early"

    if stop_reason:
        message += f": reason={stop_reason}"

    if stop_http_status is not None:
        message += f", http_status={stop_http_status}"

    return RuntimeError(message)


def _normalize_optional_slug(
    value: str | None,
    *,
    field_name: str,
) -> str | None:
    if value is None:
        return None

    if not isinstance(
        value,
        str,
    ):
        raise ValueError(f"{field_name} must be a string or null")

    normalized_value = value.strip().lower().replace("_", "-").replace(" ", "-")

    while "--" in normalized_value:
        normalized_value = normalized_value.replace(
            "--",
            "-",
        )

    normalized_value = normalized_value.strip("-")

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

    if (
        isinstance(
            value,
            bool,
        )
        or not isinstance(
            value,
            int,
        )
        or value <= 0
    ):
        raise ValueError(f"{field_name} must be a positive integer")

    return value


def _validate_workers(
    workers: int,
) -> int:
    if (
        isinstance(
            workers,
            bool,
        )
        or not isinstance(
            workers,
            int,
        )
        or workers < 1
    ):
        raise ValueError("workers must be at least 1")

    if workers > 1000:
        raise ValueError("workers cannot exceed 1000")

    return workers


def _validate_requests_per_second(
    requests_per_second: float,
) -> float:
    if (
        isinstance(
            requests_per_second,
            bool,
        )
        or not isinstance(
            requests_per_second,
            (
                int,
                float,
            ),
        )
        or requests_per_second <= 0
    ):
        raise ValueError("requests_per_second must be greater than zero")

    return float(requests_per_second)


def _validate_mongo_batch_size(
    mongo_batch_size: int,
) -> int:
    if (
        isinstance(
            mongo_batch_size,
            bool,
        )
        or not isinstance(
            mongo_batch_size,
            int,
        )
        or mongo_batch_size < 1
    ):
        raise ValueError("mongo_batch_size must be at least 1")

    return mongo_batch_size


def _validate_max_jobs(
    max_jobs: int | None,
) -> int | None:
    if max_jobs is None:
        return None

    if (
        isinstance(
            max_jobs,
            bool,
        )
        or not isinstance(
            max_jobs,
            int,
        )
        or max_jobs < 1
    ):
        raise ValueError("max_jobs must be at least 1")

    return max_jobs


def _validate_pause_configuration(
    *,
    pause_every_requests: int | None,
    pause_seconds: float | None,
) -> tuple[
    bool,
    int | None,
    float | None,
]:
    override_requested = pause_every_requests is not None or pause_seconds is not None

    if not override_requested:
        return (
            False,
            None,
            None,
        )

    if pause_every_requests is None or pause_seconds is None:
        raise ValueError(
            "pause_every_requests and pause_seconds must be provided together"
        )

    if (
        isinstance(
            pause_every_requests,
            bool,
        )
        or not isinstance(
            pause_every_requests,
            int,
        )
        or pause_every_requests < 0
    ):
        raise ValueError("pause_every_requests must be a non-negative integer")

    if (
        isinstance(
            pause_seconds,
            bool,
        )
        or not isinstance(
            pause_seconds,
            (
                int,
                float,
            ),
        )
        or pause_seconds < 0
    ):
        raise ValueError("pause_seconds must be a non-negative number")

    normalized_pause_seconds = float(pause_seconds)

    pause_count_enabled = pause_every_requests > 0

    pause_duration_enabled = normalized_pause_seconds > 0

    if pause_count_enabled != pause_duration_enabled:
        raise ValueError(
            "pause_every_requests and "
            "pause_seconds must both be "
            "greater than zero or both "
            "be zero"
        )

    return (
        True,
        pause_every_requests,
        normalized_pause_seconds,
    )


async def run_cardekho_city_prices(
    *,
    brand: str | None = None,
    model: str | None = None,
    model_id: int | None = None,
    city: str | None = None,
    city_id: int | None = None,
    popular_cities_only: bool = False,
    tier: int | None = None,
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
    normalized_brand = _normalize_optional_slug(
        brand,
        field_name="brand",
    )

    normalized_model = _normalize_optional_slug(
        model,
        field_name="model",
    )

    normalized_model_id = _normalize_optional_positive_integer(
        model_id,
        field_name="model_id",
    )

    normalized_city = _normalize_optional_slug(
        city,
        field_name="city",
    )

    normalized_city_id = _normalize_optional_positive_integer(
        city_id,
        field_name="city_id",
    )

    normalized_tier = _normalize_optional_positive_integer(
        tier,
        field_name="tier",
    )

    if normalized_tier is not None and normalized_tier > 3:
        raise ValueError("tier must be between 1 and 3")

    normalized_workers = _validate_workers(workers)

    normalized_requests_per_second = _validate_requests_per_second(requests_per_second)

    normalized_mongo_batch_size = _validate_mongo_batch_size(mongo_batch_size)

    normalized_max_jobs = _validate_max_jobs(max_jobs)

    (
        pause_override_requested,
        normalized_pause_every_requests,
        normalized_pause_seconds,
    ) = _validate_pause_configuration(
        pause_every_requests=(pause_every_requests),
        pause_seconds=pause_seconds,
    )

    if normalized_model is not None and normalized_brand is None:
        raise ValueError("model requires brand")

    if not isinstance(
        popular_cities_only,
        bool,
    ):
        raise ValueError("popular_cities_only must be a boolean")

    if not isinstance(
        failed_only,
        bool,
    ):
        raise ValueError("failed_only must be a boolean")

    if not isinstance(
        retry_terminal_failures,
        bool,
    ):
        raise ValueError("retry_terminal_failures must be a boolean")

    normalized_resume_run_id = (
        resume_run_id.strip()
        if isinstance(
            resume_run_id,
            str,
        )
        else None
    )

    if resume_run_id is not None and not normalized_resume_run_id:
        raise ValueError("resume_run_id cannot be empty")

    if failed_only and normalized_resume_run_id is None:
        raise ValueError("--failed-only requires --resume-run-id")

    run_id: str | None = None

    pipeline: CardekhoCityPricePipeline | None = None

    client_metrics: dict[
        str,
        Any,
    ] = {}

    await mongo_connection.connect()

    try:
        if normalized_resume_run_id is None:
            active_brand = normalized_brand

            active_model = normalized_model

            active_model_id = normalized_model_id

            active_city = normalized_city

            active_city_id = normalized_city_id

            active_popular_cities_only = popular_cities_only

            active_tier = normalized_tier

            active_max_jobs = normalized_max_jobs

            active_workers = normalized_workers

            active_requests_per_second = normalized_requests_per_second

            active_mongo_batch_size = normalized_mongo_batch_size

            active_pause_every_requests = (
                normalized_pause_every_requests
                if normalized_pause_every_requests is not None
                else 0
            )

            active_pause_seconds = (
                normalized_pause_seconds
                if normalized_pause_seconds is not None
                else 0.0
            )

            run = CardekhoCityPriceRun.create(
                brand=active_brand,
                model=active_model,
                model_id=(active_model_id),
                city=active_city,
                city_id=active_city_id,
                popular_cities_only=(active_popular_cities_only),
                tier=(active_tier),
                max_jobs=(active_max_jobs),
                workers=(active_workers),
                requests_per_second=(active_requests_per_second),
                mongo_batch_size=(active_mongo_batch_size),
                pause_every_requests=(active_pause_every_requests),
                pause_seconds=(active_pause_seconds),
            )

            await cardekho_city_price_run_repository.create(run)

            run_id = run.run_id
            resumed = False

        else:
            existing_run = await cardekho_city_price_run_repository.require(
                normalized_resume_run_id
            )

            if pause_override_requested:
                existing_run = await (
                    cardekho_city_price_run_repository.update_pause_settings(
                        normalized_resume_run_id,
                        pause_every_requests=(
                            normalized_pause_every_requests
                            if normalized_pause_every_requests is not None
                            else 0
                        ),
                        pause_seconds=(
                            normalized_pause_seconds
                            if normalized_pause_seconds is not None
                            else 0.0
                        ),
                    )
                )

            resumed_run = await cardekho_city_price_run_repository.mark_resumed(
                normalized_resume_run_id
            )

            run_id = resumed_run.run_id
            resumed = True

            active_brand = existing_run.filters.brand

            active_model = existing_run.filters.model

            active_model_id = existing_run.filters.model_id

            active_city = existing_run.filters.city

            active_city_id = existing_run.filters.city_id

            active_popular_cities_only = existing_run.filters.popular_cities_only

            active_tier = existing_run.filters.tier

            active_max_jobs = existing_run.filters.max_jobs

            active_workers = existing_run.settings.workers

            active_requests_per_second = existing_run.settings.requests_per_second

            active_mongo_batch_size = existing_run.settings.mongo_batch_size

            active_pause_every_requests = existing_run.settings.pause_every_requests

            active_pause_seconds = existing_run.settings.pause_seconds

        logger_service.info(
            (
                "Starting Cardekho "
                "city-price scraping: "
                f"run_id={run_id}, "
                f"resumed={resumed}, "
                "failed_only="
                f"{failed_only}, "
                f"brand={active_brand}, "
                f"model={active_model}, "
                "model_id="
                f"{active_model_id}, "
                f"city={active_city}, "
                f"city_id={active_city_id}, "
                "popular_cities_only="
                f"{active_popular_cities_only}, "
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
            context=("CardekhoCityPricesCommand"),
        )

        if failed_only:
            jobs = cardekho_city_price_failure_repository.iter_unresolved_jobs(
                run_id=run_id,
                retryable_only=(not retry_terminal_failures),
            )

        else:
            jobs = iter_cardekho_city_price_jobs(
                selected_brand=(active_brand),
                selected_model=(active_model),
                selected_model_id=(active_model_id),
                selected_city=(active_city),
                selected_city_id=(active_city_id),
                selected_tier=(active_tier),
                popular_cities_only=(active_popular_cities_only),
                max_jobs=(active_max_jobs),
            )

        async with create_cardekho_async_client(
            concurrency=(active_workers),
            requests_per_second=(active_requests_per_second),
            pause_every_requests=(active_pause_every_requests),
            pause_seconds=(active_pause_seconds),
        ) as client:
            executor = CardekhoCityPriceExecutor(client)

            pipeline = CardekhoCityPricePipeline(
                executor=executor,
                repository=(cardekho_city_price_repository),
                failure_repository=(cardekho_city_price_failure_repository),
                run_repository=(cardekho_city_price_run_repository),
                workers=(active_workers),
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
                resume_check_batch_size=(1_000),
                progress_interval=10.0,
                retry_terminal_failures=(retry_terminal_failures),
            )

            summary = await pipeline.run(
                jobs,
                run_id=run_id,
            )

            client_metrics = client.metrics_snapshot()

        unresolved_failures = (
            await (
                cardekho_city_price_failure_repository.count_unresolved(
                    run_id=run_id,
                    retryable_only=False,
                )
            )
        )

        stopped_early = bool(
            summary.get(
                "stoppedEarly",
                False,
            )
        )

        stop_reason_value = summary.get("stopReason")

        stop_reason = (
            stop_reason_value
            if isinstance(
                stop_reason_value,
                str,
            )
            and stop_reason_value.strip()
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
                stop_reason=(stop_reason),
                stop_http_status=(stop_http_status),
            )

            finished_run = await cardekho_city_price_run_repository.mark_interrupted(
                run_id,
                progress=(pipeline.progress_snapshot()),
                error=(interruption_error),
                stop_reason=(stop_reason),
                stop_http_status=(stop_http_status),
            )

        else:
            finished_run = await cardekho_city_price_run_repository.mark_completed(
                run_id,
                progress=(pipeline.progress_snapshot()),
            )

        return {
            "command": ("cardekho-city-prices"),
            "runId": run_id,
            "status": (finished_run.status),
            "resumed": resumed,
            "failedOnly": (failed_only),
            "retryTerminalFailures": (retry_terminal_failures),
            "brand": active_brand,
            "model": active_model,
            "modelId": (active_model_id),
            "city": active_city,
            "cityId": (active_city_id),
            "popularCitiesOnly": (active_popular_cities_only),
            "workers": (active_workers),
            "requestsPerSecond": (active_requests_per_second),
            "mongoBatchSize": (active_mongo_batch_size),
            "pauseEveryRequests": (active_pause_every_requests),
            "pauseSeconds": (active_pause_seconds),
            "maxJobs": (active_max_jobs),
            "unresolvedFailures": (unresolved_failures),
            "httpMetrics": (client_metrics),
            **summary,
        }

    except asyncio.CancelledError as error:
        if run_id is not None:
            progress = pipeline.progress_snapshot() if pipeline is not None else {}

            try:
                await asyncio.shield(
                    cardekho_city_price_run_repository.mark_interrupted(
                        run_id,
                        progress=progress,
                        error=error,
                        stop_reason=("keyboard_interrupt"),
                    )
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark "
                        "Cardekho city-price "
                        "run as interrupted: "
                        f"run_id={run_id}"
                    ),
                    exception=(tracking_error),
                    context=("CardekhoCityPricesCommand"),
                )

        raise

    except KeyboardInterrupt as error:
        if run_id is not None:
            progress = pipeline.progress_snapshot() if pipeline is not None else {}

            try:
                await cardekho_city_price_run_repository.mark_interrupted(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("keyboard_interrupt"),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark "
                        "Cardekho city-price "
                        "run as interrupted: "
                        f"run_id={run_id}"
                    ),
                    exception=(tracking_error),
                    context=("CardekhoCityPricesCommand"),
                )

        raise

    except Exception as error:
        if run_id is not None:
            progress = pipeline.progress_snapshot() if pipeline is not None else {}

            try:
                await cardekho_city_price_run_repository.mark_failed(
                    run_id,
                    progress=progress,
                    error=error,
                    stop_reason=("pipeline_error"),
                )

            except Exception as tracking_error:
                logger_service.error(
                    (
                        "Unable to mark "
                        "Cardekho city-price "
                        "run as failed: "
                        f"run_id={run_id}"
                    ),
                    exception=(tracking_error),
                    context=("CardekhoCityPricesCommand"),
                )

        raise

    finally:
        await mongo_connection.close()
