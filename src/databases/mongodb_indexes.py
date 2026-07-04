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

CARDEKHO_BRANDS_COLLECTION: Final[str] = "cardekho_brands"

CARWALE_MODELS_COLLECTION: Final[str] = "carwale_models"

CARDEKHO_MODELS_COLLECTION: Final[str] = "cardekho_models"

CARWALE_CARS_COLLECTION: Final[str] = "carwale_cars"

CARDEKHO_CARS_COLLECTION: Final[str] = "cardekho_cars"

CARWALE_TRIM_SPECS_FEATURES_COLLECTION: Final[str] = "carwale_trim_specs_features"

CARWALE_CITIES_COLLECTION: Final[str] = "carwale_cities"

CARDEKHO_CITIES_COLLECTION: Final[str] = "cardekho_cities"

CARWALE_CITY_PRICES_COLLECTION: Final[str] = "carwale_city_prices"

CARWALE_CITY_PRICE_RUNS_COLLECTION: Final[str] = "carwale_city_price_runs"

CARWALE_CITY_PRICE_FAILURES_COLLECTION: Final[str] = "carwale_city_price_failures"

CARDEKHO_CITY_PRICES_COLLECTION: Final[str] = "cardekho_city_prices"

CARDEKHO_CITY_PRICE_RUNS_COLLECTION: Final[str] = "cardekho_city_price_runs"

CARDEKHO_CITY_PRICE_FAILURES_COLLECTION: Final[str] = "cardekho_city_price_failures"


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
                    ("_id", ASCENDING),
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


async def _create_cardekho_brand_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(CARDEKHO_BRANDS_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("slug", ASCENDING),
                ],
                name="uniq_brand_slug",
                unique=True,
            ),
            IndexModel(
                [
                    ("id", ASCENDING),
                ],
                name="uniq_numeric_brand_id",
                unique=True,
                partialFilterExpression={
                    "id": {
                        "$type": "number",
                    },
                },
            ),
            IndexModel(
                [
                    ("modelRequestSlug", ASCENDING),
                ],
                name="idx_model_request_slug",
            ),
            IndexModel(
                [
                    ("brandStatus", ASCENDING),
                    ("brandName", ASCENDING),
                    ("slug", ASCENDING),
                ],
                name="idx_status_brand_name",
            ),
            IndexModel(
                [
                    ("brandStatus", ASCENDING),
                    ("isPopular", DESCENDING),
                    ("popularity", DESCENDING),
                    ("brandName", ASCENDING),
                ],
                name="idx_status_popularity",
            ),
            IndexModel(
                [
                    ("hasOfferData", ASCENDING),
                    ("totalOfferCount", DESCENDING),
                ],
                name="idx_offer_data_count",
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


async def _create_cardekho_model_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(CARDEKHO_MODELS_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("id", ASCENDING),
                ],
                name="uniq_model_id",
                unique=True,
            ),
            IndexModel(
                [
                    ("brandSlug", ASCENDING),
                    ("slug", ASCENDING),
                ],
                name="uniq_brand_model_slug",
                unique=True,
            ),
            IndexModel(
                [
                    ("brandId", ASCENDING),
                    ("id", ASCENDING),
                ],
                name="idx_brand_model_id",
            ),
            IndexModel(
                [
                    ("brandSlug", ASCENDING),
                    ("modelStatus", ASCENDING),
                    ("modelName", ASCENDING),
                    ("id", ASCENDING),
                ],
                name="idx_brand_status_model_name",
            ),
            IndexModel(
                [
                    ("modelStatus", ASCENDING),
                    ("expectedLaunchDate", ASCENDING),
                    ("brandName", ASCENDING),
                ],
                name="idx_status_launch_date",
            ),
            IndexModel(
                [
                    ("sourceBrandDocumentId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_source_brand_document",
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


async def _create_cardekho_car_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(CARDEKHO_CARS_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("id", ASCENDING),
                ],
                name="uniq_model_id",
                unique=True,
            ),
            IndexModel(
                [
                    ("brandSlug", ASCENDING),
                    ("slug", ASCENDING),
                ],
                name="uniq_brand_model_slug",
                unique=True,
            ),
            IndexModel(
                [
                    ("carSlug", ASCENDING),
                ],
                name="uniq_car_slug",
                unique=True,
            ),
            IndexModel(
                [
                    ("brandId", ASCENDING),
                    ("id", ASCENDING),
                ],
                name="idx_brand_model_id",
            ),
            IndexModel(
                [
                    ("brandSlug", ASCENDING),
                    ("modelStatus", ASCENDING),
                    ("modelName", ASCENDING),
                    ("id", ASCENDING),
                ],
                name="idx_brand_status_model_name",
            ),
            IndexModel(
                [
                    ("variants.id", ASCENDING),
                ],
                name="idx_variant_id",
            ),
            IndexModel(
                [
                    ("variants.slug", ASCENDING),
                ],
                name="idx_variant_slug",
            ),
            IndexModel(
                [
                    ("compareWith.carSlug", ASCENDING),
                ],
                name="idx_compare_with_car_slug",
            ),
            IndexModel(
                [
                    ("similarCars.carSlug", ASCENDING),
                ],
                name="idx_similar_car_slug",
            ),
            IndexModel(
                [
                    (
                        "oldGenerationComparison.carSlug",
                        ASCENDING,
                    ),
                ],
                name="idx_old_generation_car_slug",
                partialFilterExpression={
                    ("oldGenerationComparison.carSlug"): {
                        "$type": "string",
                    },
                },
            ),
            IndexModel(
                [
                    ("sourceModelDocumentId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_source_model_document",
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


async def _create_carwale_trim_specs_features_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(CARWALE_TRIM_SPECS_FEATURES_COLLECTION)

    return await collection.create_indexes(
        [
            IndexModel(
                [
                    ("versionId", ASCENDING),
                ],
                name="uniq_version_id",
                unique=True,
            ),
            IndexModel(
                [
                    ("makeId", ASCENDING),
                    ("modelId", ASCENDING),
                    ("trimId", ASCENDING),
                    ("versionId", ASCENDING),
                ],
                name="idx_make_model_trim_version",
            ),
            IndexModel(
                [
                    ("makeMaskingName", ASCENDING),
                    ("modelMaskingName", ASCENDING),
                    ("trimMaskingName", ASCENDING),
                    ("versionId", ASCENDING),
                ],
                name="idx_make_model_trim_slug_version",
            ),
            IndexModel(
                [
                    ("trimId", ASCENDING),
                    ("versionId", ASCENDING),
                ],
                name="idx_trim_version",
            ),
            IndexModel(
                [
                    ("sourceCarDocumentId", ASCENDING),
                    ("versionId", ASCENDING),
                ],
                name="idx_source_car_document_version",
            ),
            IndexModel(
                [
                    ("sourceCarRunId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_source_car_run_updated_at",
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


async def _create_cardekho_city_indexes(
    connection: MongoConnection,
) -> list[str]:
    collection = connection.collection(CARDEKHO_CITIES_COLLECTION)

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
                    ("cityName", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_city_name_city_id",
            ),
            IndexModel(
                [
                    ("displayName", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_display_name_city_id",
            ),
            IndexModel(
                [
                    ("aliases", ASCENDING),
                ],
                name="idx_aliases",
            ),
            IndexModel(
                [
                    ("isPopular", DESCENDING),
                    ("cityName", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_popular_city_name",
            ),
            IndexModel(
                [
                    ("isPrime", DESCENDING),
                    ("cityName", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_prime_city_name",
            ),
            IndexModel(
                [
                    ("regions.regionId", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_region_id_city_id",
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


async def _create_carwale_city_price_indexes(
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
                name="uniq_version_city",
                unique=True,
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
                    ("makeMaskingName", ASCENDING),
                    ("modelMaskingName", ASCENDING),
                    ("cityMaskingName", ASCENDING),
                ],
                name="idx_make_model_city",
            ),
            IndexModel(
                [
                    ("versionId", ASCENDING),
                    ("scrapedAt", DESCENDING),
                ],
                name="idx_version_scraped_at",
            ),
            IndexModel(
                [
                    ("cityId", ASCENDING),
                    ("scrapedAt", DESCENDING),
                ],
                name="idx_city_scraped_at",
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


async def _create_cardekho_city_price_indexes(
    connection: MongoConnection,
) -> dict[str, list[str]]:
    city_prices_collection = connection.collection(CARDEKHO_CITY_PRICES_COLLECTION)

    city_price_runs_collection = connection.collection(
        CARDEKHO_CITY_PRICE_RUNS_COLLECTION
    )

    city_price_failures_collection = connection.collection(
        CARDEKHO_CITY_PRICE_FAILURES_COLLECTION
    )

    city_price_indexes = await city_prices_collection.create_indexes(
        [
            IndexModel(
                [
                    ("modelId", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="uniq_model_city",
                unique=True,
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
                    ("brandSlug", ASCENDING),
                    ("modelSlug", ASCENDING),
                    ("citySlug", ASCENDING),
                ],
                name="idx_brand_model_city",
            ),
            IndexModel(
                [
                    ("modelStatus", ASCENDING),
                    ("priceAvailable", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_status_price_available",
            ),
            IndexModel(
                [
                    ("modelId", ASCENDING),
                    ("scrapedAt", DESCENDING),
                ],
                name="idx_model_scraped_at",
            ),
            IndexModel(
                [
                    ("cityId", ASCENDING),
                    ("scrapedAt", DESCENDING),
                ],
                name="idx_city_scraped_at",
            ),
            IndexModel(
                [
                    ("variants.trimId", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_trim_city",
            ),
            IndexModel(
                [
                    ("variants.variantSlug", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_variant_slug_city",
            ),
            IndexModel(
                [
                    ("source.carDocumentId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_source_car_document",
            ),
            IndexModel(
                [
                    ("source.cityDocumentId", ASCENDING),
                    ("updatedAt", DESCENDING),
                ],
                name="idx_source_city_document",
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
                    ("filters.modelId", ASCENDING),
                    ("filters.city", ASCENDING),
                    ("filters.cityId", ASCENDING),
                    ("startedAt", DESCENDING),
                ],
                name="idx_filters_started_at",
            ),
            IndexModel(
                [
                    (
                        "filters.popularCitiesOnly",
                        ASCENDING,
                    ),
                    ("status", ASCENDING),
                    ("startedAt", DESCENDING),
                ],
                name="idx_popular_status_started_at",
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
                    ("modelId", ASCENDING),
                    ("cityId", ASCENDING),
                ],
                name="idx_run_model_city",
            ),
            IndexModel(
                [
                    ("status", ASCENDING),
                    ("retryable", ASCENDING),
                    ("lastFailedAt", DESCENDING),
                ],
                name="idx_status_retryable_failed_at",
            ),
            IndexModel(
                [
                    ("brandSlug", ASCENDING),
                    ("modelSlug", ASCENDING),
                    ("citySlug", ASCENDING),
                    ("status", ASCENDING),
                ],
                name="idx_brand_model_city_status",
            ),
        ]
    )

    return {
        CARDEKHO_CITY_PRICES_COLLECTION: (city_price_indexes),
        CARDEKHO_CITY_PRICE_RUNS_COLLECTION: (city_price_run_indexes),
        CARDEKHO_CITY_PRICE_FAILURES_COLLECTION: (city_price_failure_indexes),
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

    cardekho_brand_indexes = await _create_cardekho_brand_indexes(connection)

    carwale_model_indexes = await _create_carwale_model_indexes(connection)

    cardekho_model_indexes = await _create_cardekho_model_indexes(connection)

    carwale_car_indexes = await _create_carwale_car_indexes(connection)

    cardekho_car_indexes = await _create_cardekho_car_indexes(connection)

    carwale_trim_specs_features_indexes = (
        await _create_carwale_trim_specs_features_indexes(connection)
    )

    carwale_city_indexes = await _create_carwale_city_indexes(connection)

    cardekho_city_indexes = await _create_cardekho_city_indexes(connection)

    carwale_city_price_indexes = await _create_carwale_city_price_indexes(connection)

    cardekho_city_price_indexes = await _create_cardekho_city_price_indexes(connection)

    created_indexes = {
        SCRAPER_RUNS_COLLECTION: (scraper_run_indexes),
        SCRAPER_JOBS_COLLECTION: (scraper_job_indexes),
        CARWALE_BRANDS_COLLECTION: (carwale_brand_indexes),
        CARDEKHO_BRANDS_COLLECTION: (cardekho_brand_indexes),
        CARWALE_MODELS_COLLECTION: (carwale_model_indexes),
        CARDEKHO_MODELS_COLLECTION: (cardekho_model_indexes),
        CARWALE_CARS_COLLECTION: (carwale_car_indexes),
        CARDEKHO_CARS_COLLECTION: (cardekho_car_indexes),
        CARWALE_TRIM_SPECS_FEATURES_COLLECTION: (carwale_trim_specs_features_indexes),
        CARWALE_CITIES_COLLECTION: (carwale_city_indexes),
        CARDEKHO_CITIES_COLLECTION: (cardekho_city_indexes),
        **carwale_city_price_indexes,
        **cardekho_city_price_indexes,
    }

    logger_service.info(
        (f"MongoDB indexes initialized: collections={list(created_indexes)}"),
        context="MongoDBIndexes",
    )

    return created_indexes
