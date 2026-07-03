from __future__ import annotations

from typing import Final

from pymongo import (
    ASCENDING,
    DESCENDING,
    IndexModel,
)

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.logger.logger import logger_service

SCRAPER_RUNS_COLLECTION: Final[str] = "scraper_runs"

SCRAPER_JOBS_COLLECTION: Final[str] = "scraper_jobs"

CARWALE_BRANDS_COLLECTION: Final[str] = "carwale_brands"

CARWALE_MODELS_COLLECTION: Final[str] = "carwale_models"

CARWALE_CARS_COLLECTION: Final[str] = "carwale_cars"

CARWALE_CITIES_COLLECTION: Final[str] = "carwale_cities"

CARWALE_CITY_PRICES_COLLECTION: Final[str] = "carwale_city_prices"

CARWALE_CITY_PRICE_RUNS_COLLECTION: Final[str] = "carwale_city_price_runs"

CARWALE_CITY_PRICE_FAILURES_COLLECTION: Final[str] = "carwale_city_price_failures"


async def _create_scraper_run_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(SCRAPER_RUNS_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("source", ASCENDING),
                    ("resource", ASCENDING),
                    ("createdAt", DESCENDING),
                ],
                name="idx_source_resource_created_at",
            ),
            IndexModel(
                [
                    ("resource", ASCENDING),
                    ("status", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_resource_status_updated_at",
            ),
            IndexModel(
                [
                    ("status", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_status_updated_at",
            ),
            IndexModel(
                [
                    ("command", ASCENDING),
                    ("createdAt", DESCENDING),
                ],
                name="idx_command_created_at",
            ),
            IndexModel(
                [
                    ("source", ASCENDING),
                    ("command", ASCENDING),
                    ("status", ASCENDING),
                    ("createdAt", DESCENDING),
                ],
                name="idx_source_command_status",
            ),
        ]
    )


async def _create_scraper_job_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(SCRAPER_JOBS_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("runId", ASCENDING),
                    ("jobId", ASCENDING),
                ],
                name="uniq_run_job",
                unique=True,
            ),
            IndexModel(
                [
                    ("runId", ASCENDING),
                    ("status", ASCENDING),
                    ("priority", DESCENDING),
                    ("queuedAt", ASCENDING),
                    ("_id", ASCENDING),
                ],
                name="idx_claim_pending_job",
            ),
            IndexModel(
                [
                    ("runId", ASCENDING),
                    ("status", ASCENDING),
                    ("resource", ASCENDING),
                    ("jobType", ASCENDING),
                    ("priority", DESCENDING),
                    ("queuedAt", ASCENDING),
                ],
                name="idx_claim_pending_job_by_type",
            ),
            IndexModel(
                [
                    ("runId", ASCENDING),
                    ("status", ASCENDING),
                ],
                name="idx_run_status",
            ),
            IndexModel(
                [
                    ("runId", ASCENDING),
                    ("status", ASCENDING),
                    ("retryable", ASCENDING),
                    ("updatedAt", ASCENDING),
                ],
                name="idx_failed_retry",
            ),
            IndexModel(
                [
                    ("runId", ASCENDING),
                    ("status", ASCENDING),
                    ("lastHeartbeatAt", ASCENDING),
                ],
                name="idx_stale_running_jobs",
            ),
            IndexModel(
                [
                    ("workerId", ASCENDING),
                    ("status", ASCENDING),
                    ("lastHeartbeatAt", ASCENDING),
                ],
                name="idx_worker_running_jobs",
            ),
            IndexModel(
                [
                    ("source", ASCENDING),
                    ("resource", ASCENDING),
                    ("itemKey", ASCENDING),
                    ("createdAt", DESCENDING),
                ],
                name="idx_item_history",
            ),
        ]
    )


async def _create_carwale_brand_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(CARWALE_BRANDS_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("makeId", ASCENDING),
                ],
                name="uniq_make_id",
                unique=True,
            ),
            IndexModel(
                [
                    ("maskingName", ASCENDING),
                ],
                name="uniq_masking_name",
                unique=True,
            ),
            IndexModel(
                [
                    ("makeName", ASCENDING),
                    ("makeId", ASCENDING),
                ],
                name="idx_make_name_make_id",
            ),
            IndexModel(
                [
                    ("lastRunId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_last_run_updated_at",
            ),
            IndexModel(
                [
                    ("scrapedAt", DESCENDING),
                ],
                name="idx_scraped_at",
            ),
        ]
    )


async def _create_carwale_model_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(CARWALE_MODELS_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("makeId", ASCENDING),
                    ("modelId", ASCENDING),
                ],
                name="uniq_make_model_id",
                unique=True,
            ),
            IndexModel(
                [
                    ("makeMaskingName", ASCENDING),
                    ("modelMaskingName", ASCENDING),
                ],
                name="uniq_make_model_masking_name",
                unique=True,
            ),
            IndexModel(
                [
                    ("makeId", ASCENDING),
                    ("modelName", ASCENDING),
                    ("modelId", ASCENDING),
                ],
                name="idx_make_model_name",
            ),
            IndexModel(
                [
                    ("makeName", ASCENDING),
                    ("modelName", ASCENDING),
                ],
                name="idx_make_name_model_name",
            ),
            IndexModel(
                [
                    ("lastRunId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_last_run_updated_at",
            ),
            IndexModel(
                [
                    ("sourceBrandRunId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_source_brand_run",
            ),
            IndexModel(
                [
                    ("scrapedAt", DESCENDING),
                ],
                name="idx_scraped_at",
            ),
        ]
    )


async def _create_carwale_car_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(CARWALE_CARS_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("makeId", ASCENDING),
                    ("modelId", ASCENDING),
                ],
                name="uniq_make_model_id",
                unique=True,
            ),
            IndexModel(
                [
                    ("makeMaskingName", ASCENDING),
                    ("modelMaskingName", ASCENDING),
                ],
                name="uniq_make_model_masking_name",
                unique=True,
            ),
            IndexModel(
                [
                    ("data.versions.versionId", ASCENDING),
                ],
                name="idx_version_id",
            ),
            IndexModel(
                [
                    ("makeId", ASCENDING),
                    ("modelName", ASCENDING),
                    ("modelId", ASCENDING),
                ],
                name="idx_make_model_name",
            ),
            IndexModel(
                [
                    ("makeName", ASCENDING),
                    ("modelName", ASCENDING),
                ],
                name="idx_make_name_model_name",
            ),
            IndexModel(
                [
                    ("totalVersions", DESCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_total_versions_updated_at",
            ),
            IndexModel(
                [
                    ("lastRunId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_last_run_updated_at",
            ),
            IndexModel(
                [
                    ("sourceModelRunId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_source_model_run",
            ),
            IndexModel(
                [
                    ("requestContext.cityId", ASCENDING),
                    ("requestContext.areaId", ASCENDING),
                ],
                name="idx_request_city_area",
            ),
            IndexModel(
                [
                    ("scrapedAt", DESCENDING),
                ],
                name="idx_scraped_at",
            ),
        ]
    )


async def _create_carwale_city_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(CARWALE_CITIES_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("cityId", ASCENDING),
                ],
                name="uniq_city_id",
                unique=True,
            ),
            IndexModel(
                [
                    ("cityMaskingName", ASCENDING),
                ],
                name="idx_city_masking_name",
            ),
            IndexModel(
                [
                    ("stateId", ASCENDING),
                    ("cityName", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_state_city_name",
            ),
            IndexModel(
                [
                    ("isPopular", DESCENDING),
                    ("cityName", ASCENDING),
                ],
                name="idx_popular_city_name",
            ),
            IndexModel(
                [
                    ("isDeleted", ASCENDING),
                    ("cityName", ASCENDING),
                ],
                name="idx_deleted_city_name",
            ),
            IndexModel(
                [
                    ("lastRunId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_last_run_updated_at",
            ),
            IndexModel(
                [
                    ("scrapedAt", DESCENDING),
                ],
                name="idx_scraped_at",
            ),
        ]
    )


async def _create_city_price_indexes(
    connection: MongoConnection,
) -> dict[str, list[str]]:
    city_prices_collection = connection.collection(CARWALE_CITY_PRICES_COLLECTION)

    city_price_runs_collection = connection.collection(
        CARWALE_CITY_PRICE_RUNS_COLLECTION
    )

    city_price_failures_collection = connection.collection(
        CARWALE_CITY_PRICE_FAILURES_COLLECTION
    )

    city_price_indexes = await city_prices_collection.create_indexes(
        [
            IndexModel(
                [
                    ("versionId", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_version_city",
            ),
            IndexModel(
                [
                    ("lastRunId", ASCENDING),
                    ("_id", ASCENDING),
                ],
                name="idx_last_run_job",
            ),
            IndexModel(
                [
                    (
                        "makeMaskingName",
                        ASCENDING,
                    ),
                    (
                        "modelMaskingName",
                        ASCENDING,
                    ),
                    (
                        "cityMaskingName",
                        ASCENDING,
                    ),
                ],
                name="idx_make_model_city",
            ),
            IndexModel(
                [
                    ("versionId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_version_updated_at",
            ),
            IndexModel(
                [
                    ("cityId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_city_updated_at",
            ),
        ]
    )

    city_price_run_indexes = await city_price_runs_collection.create_indexes(
        [
            IndexModel(
                [
                    ("status", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_status_updated_at",
            ),
            IndexModel(
                [
                    ("filters.brand", ASCENDING),
                    ("filters.model", ASCENDING),
                    ("filters.city", ASCENDING),
                    ("startedAt", DESCENDING),
                ],
                name="idx_filters_started_at",
            ),
            IndexModel(
                [
                    ("startedAt", DESCENDING),
                ],
                name="idx_started_at",
            ),
        ]
    )

    city_price_failure_indexes = await city_price_failures_collection.create_indexes(
        [
            IndexModel(
                [
                    ("runId", ASCENDING),
                    ("jobId", ASCENDING),
                ],
                name="idx_run_job",
            ),
            IndexModel(
                [
                    ("runId", ASCENDING),
                    ("status", ASCENDING),
                    ("retryable", ASCENDING),
                    ("lastFailedAt", ASCENDING),
                ],
                name="idx_unresolved_failures",
            ),
            IndexModel(
                [
                    ("runId", ASCENDING),
                    ("versionId", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_run_version_city",
            ),
            IndexModel(
                [
                    ("status", ASCENDING),
                    ("retryable", ASCENDING),
                    ("lastFailedAt", DESCENDING),
                ],
                name="idx_status_retryable_failed_at",
            ),
        ]
    )

    return {
        CARWALE_CITY_PRICES_COLLECTION: (city_price_indexes),
        CARWALE_CITY_PRICE_RUNS_COLLECTION: (city_price_run_indexes),
        CARWALE_CITY_PRICE_FAILURES_COLLECTION: (city_price_failure_indexes),
    }


async def ensure_mongodb_indexes(
    connection: MongoConnection = mongo_connection,
) -> dict[str, list[str]]:
    """
    Create all required MongoDB indexes.

    This operation is non-destructive:

    - It does not delete documents.
    - It does not drop collections.
    - It does not drop existing indexes.
    - It does not create TTL indexes.
    """
    await connection.connect()

    scraper_run_indexes = await _create_scraper_run_indexes(connection)

    scraper_job_indexes = await _create_scraper_job_indexes(connection)

    carwale_brand_indexes = await _create_carwale_brand_indexes(connection)

    carwale_model_indexes = await _create_carwale_model_indexes(connection)

    carwale_car_indexes = await _create_carwale_car_indexes(connection)

    carwale_city_indexes = await _create_carwale_city_indexes(connection)

    city_price_indexes = await _create_city_price_indexes(connection)

    created_indexes = {
        SCRAPER_RUNS_COLLECTION: (scraper_run_indexes),
        SCRAPER_JOBS_COLLECTION: (scraper_job_indexes),
        CARWALE_BRANDS_COLLECTION: (carwale_brand_indexes),
        CARWALE_MODELS_COLLECTION: (carwale_model_indexes),
        CARWALE_CARS_COLLECTION: (carwale_car_indexes),
        CARWALE_CITIES_COLLECTION: (carwale_city_indexes),
        **city_price_indexes,
    }

    logger_service.info(
        (f"MongoDB indexes initialized: collections={list(created_indexes)}"),
        context="MongoDBIndexes",
    )

    return created_indexes
