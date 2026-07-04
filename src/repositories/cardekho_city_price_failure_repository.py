from __future__ import annotations

from collections.abc import (
    AsyncIterator,
    Mapping,
    Sequence,
)
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from pymongo import UpdateOne
from pymongo.results import BulkWriteResult

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.logger.logger import logger_service
from src.models.cardekho_city_price_failure import (
    CardekhoCityPriceFailure,
)
from src.models.cardekho_city_price_job import (
    CardekhoCityPriceJob,
    CardekhoCityPriceSourceTrim,
)

CARDEKHO_CITY_PRICE_FAILURES_COLLECTION = "cardekho_city_price_failures"

CARDEKHO_CARS_COLLECTION = "cardekho_cars"

ACCESS_DENIED_HTTP_STATUS_CODES = {
    401,
    403,
}


@dataclass(
    frozen=True,
    slots=True,
)
class BulkFailureUpsertResult:
    received: int
    processed: int
    matched: int
    modified: int
    inserted: int


@dataclass(
    frozen=True,
    slots=True,
)
class FailureResolutionResult:
    requested: int
    matched: int
    modified: int


class CardekhoCityPriceFailureRepository:
    def __init__(
        self,
        connection: MongoConnection = mongo_connection,
    ) -> None:
        self._connection = connection

    @staticmethod
    def _normalize_run_id(
        run_id: str,
    ) -> str:
        if not isinstance(
            run_id,
            str,
        ):
            raise ValueError("run_id must be a string")

        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        return normalized_run_id

    @staticmethod
    def _normalize_job_ids(
        job_ids: Sequence[str],
    ) -> list[str]:
        normalized_job_ids: list[str] = []
        seen_job_ids: set[str] = set()

        for job_id in job_ids:
            if not isinstance(
                job_id,
                str,
            ):
                continue

            normalized_job_id = job_id.strip()

            if not normalized_job_id:
                continue

            if normalized_job_id in seen_job_ids:
                continue

            seen_job_ids.add(normalized_job_id)

            normalized_job_ids.append(normalized_job_id)

        return normalized_job_ids

    @staticmethod
    def _is_retryable_failure(
        failure: CardekhoCityPriceFailure,
    ) -> bool:
        """
        Access-denied failures are not retried immediately
        by the HTTP client, but remain eligible for a later
        failed-only resume.
        """

        if failure.http_status in ACCESS_DENIED_HTTP_STATUS_CODES:
            return True

        return failure.retryable

    @staticmethod
    def _normalize_optional_string(
        value: Any,
    ) -> str | None:
        if not isinstance(
            value,
            str,
        ):
            return None

        normalized_value = value.strip()

        return normalized_value or None

    @staticmethod
    def _normalize_slug(
        value: Any,
    ) -> str | None:
        if not isinstance(
            value,
            str,
        ):
            return None

        normalized_value = value.strip().lower().replace("_", "-").replace(" ", "-")

        while "--" in normalized_value:
            normalized_value = normalized_value.replace(
                "--",
                "-",
            )

        normalized_value = normalized_value.strip("-")

        return normalized_value or None

    @staticmethod
    def _normalize_url(
        value: Any,
    ) -> str | None:
        if not isinstance(
            value,
            str,
        ):
            return None

        normalized_value = value.strip()

        if not normalized_value:
            return None

        if not normalized_value.startswith("/"):
            normalized_value = f"/{normalized_value}"

        return normalized_value

    @staticmethod
    def _validate_positive_integer(
        value: Any,
    ) -> int | None:
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
            return None

        return value

    @classmethod
    def _parse_source_trim(
        cls,
        raw_trim: Mapping[str, Any],
    ) -> CardekhoCityPriceSourceTrim | None:
        status = cls._normalize_optional_string(raw_trim.get("status"))

        if status is None:
            status = cls._normalize_optional_string(raw_trim.get("modelStatus"))

        if status is None or status.upper() != "CURRENT":
            return None

        trim_id = cls._validate_positive_integer(raw_trim.get("id"))

        if trim_id is None:
            trim_id = cls._validate_positive_integer(raw_trim.get("variantId"))

        name = cls._normalize_optional_string(raw_trim.get("name"))

        if name is None:
            name = cls._normalize_optional_string(raw_trim.get("variantName"))

        if name is None:
            name = cls._normalize_optional_string(raw_trim.get("displayName"))

        short_name = cls._normalize_optional_string(raw_trim.get("shortName"))

        if short_name is None:
            short_name = cls._normalize_optional_string(
                raw_trim.get("variantShortName")
            )

        if short_name is None:
            short_name = name

        slug = cls._normalize_slug(raw_trim.get("slug"))

        if slug is None:
            slug = cls._normalize_slug(raw_trim.get("variantSlug"))

        url = cls._normalize_url(raw_trim.get("url"))

        if url is None:
            url = cls._normalize_url(raw_trim.get("variantUrl"))

        if (
            trim_id is None
            or name is None
            or short_name is None
            or slug is None
            or url is None
        ):
            return None

        try:
            return CardekhoCityPriceSourceTrim(
                trim_id=trim_id,
                name=name,
                short_name=short_name,
                slug=slug,
                url=url,
                status="CURRENT",
            )

        except (
            TypeError,
            ValueError,
        ):
            return None

    async def _load_source_trims(
        self,
        *,
        source_car_document_id: str,
        model_id: int,
    ) -> tuple[
        CardekhoCityPriceSourceTrim,
        ...,
    ]:
        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CARS_COLLECTION)

        car_document = await collection.find_one(
            {
                "$or": [
                    {
                        "_id": (source_car_document_id),
                    },
                    {
                        "id": model_id,
                    },
                    {
                        "modelId": model_id,
                    },
                ]
            },
            {
                "_id": 1,
                "id": 1,
                "modelId": 1,
                "variants": 1,
            },
        )

        if car_document is None:
            logger_service.error(
                (
                    "Unable to rebuild Cardekho "
                    "city-price retry job because "
                    "the source car was not found: "
                    "source_car_document_id="
                    f"{source_car_document_id!r}, "
                    f"model_id={model_id}"
                ),
                context=self.__class__.__name__,
            )

            return ()

        raw_variants = car_document.get("variants")

        if not isinstance(
            raw_variants,
            list,
        ):
            logger_service.error(
                (
                    "Unable to rebuild Cardekho "
                    "city-price retry job because "
                    "source car variants are invalid: "
                    "source_car_document_id="
                    f"{source_car_document_id!r}, "
                    f"model_id={model_id}"
                ),
                context=self.__class__.__name__,
            )

            return ()

        source_trims: list[CardekhoCityPriceSourceTrim] = []

        seen_trim_ids: set[int] = set()
        seen_trim_slugs: set[str] = set()

        for raw_trim in raw_variants:
            if not isinstance(
                raw_trim,
                Mapping,
            ):
                continue

            source_trim = self._parse_source_trim(raw_trim)

            if source_trim is None:
                continue

            if source_trim.trim_id in seen_trim_ids:
                continue

            if source_trim.slug in seen_trim_slugs:
                continue

            seen_trim_ids.add(source_trim.trim_id)

            seen_trim_slugs.add(source_trim.slug)

            source_trims.append(source_trim)

        source_trims.sort(
            key=lambda trim: (
                trim.trim_id,
                trim.slug,
            )
        )

        return tuple(source_trims)

    async def bulk_upsert(
        self,
        failures: Sequence[CardekhoCityPriceFailure],
    ) -> BulkFailureUpsertResult:
        if not failures:
            return BulkFailureUpsertResult(
                received=0,
                processed=0,
                matched=0,
                modified=0,
                inserted=0,
            )

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_CITY_PRICE_FAILURES_COLLECTION
        )

        deduplicated_failures: dict[
            str,
            CardekhoCityPriceFailure,
        ] = {}

        for failure in failures:
            deduplicated_failures[failure.failure_id] = failure

        operations: list[UpdateOne] = []

        for failure in deduplicated_failures.values():
            retryable = self._is_retryable_failure(failure)

            operations.append(
                UpdateOne(
                    {
                        "_id": (failure.failure_id),
                    },
                    {
                        "$set": {
                            "runId": (failure.run_id),
                            "jobId": (failure.job_id),
                            "modelId": (failure.model_id),
                            "modelName": (failure.model_name),
                            "modelSlug": (failure.model_slug),
                            "modelStatus": (failure.model_status),
                            "brandId": (failure.brand_id),
                            "brandName": (failure.brand_name),
                            "brandSlug": (failure.brand_slug),
                            "carSlug": (failure.car_slug),
                            "cityId": (failure.city_id),
                            "cityName": (failure.city_name),
                            "cityDisplayName": (failure.city_display_name),
                            "citySlug": (failure.city_slug),
                            "isPopularCity": (failure.is_popular_city),
                            "sourceCarDocumentId": (failure.source_car_document_id),
                            "sourceCarRunId": (failure.source_car_run_id),
                            "sourceCityDocumentId": (failure.source_city_document_id),
                            "sourceCityRunId": (failure.source_city_run_id),
                            "requestUrl": (failure.request_url),
                            "errorType": (failure.error_type),
                            "errorMessage": (failure.error_message),
                            "httpStatus": (failure.http_status),
                            "retryable": retryable,
                            "status": "failed",
                            "lastFailedAt": (failure.last_failed_at),
                            "resolvedAt": None,
                            "updatedAt": (failure.updated_at),
                        },
                        "$setOnInsert": {
                            "firstFailedAt": (failure.first_failed_at),
                        },
                        "$inc": {
                            "attempts": 1,
                        },
                    },
                    upsert=True,
                )
            )

        result: BulkWriteResult = await collection.bulk_write(
            operations,
            ordered=False,
        )

        return BulkFailureUpsertResult(
            received=len(failures),
            processed=len(operations),
            matched=(result.matched_count),
            modified=(result.modified_count),
            inserted=(result.upserted_count),
        )

    async def get_terminal_job_ids(
        self,
        *,
        run_id: str,
        job_ids: Sequence[str],
    ) -> set[str]:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_job_ids = self._normalize_job_ids(job_ids)

        if not normalized_job_ids:
            return set()

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_CITY_PRICE_FAILURES_COLLECTION
        )

        cursor = collection.find(
            {
                "runId": (normalized_run_id),
                "jobId": {
                    "$in": (normalized_job_ids),
                },
                "status": "failed",
                "retryable": False,
            },
            {
                "_id": 0,
                "jobId": 1,
            },
        )

        terminal_job_ids: set[str] = set()

        async for document in cursor:
            job_id = document.get("jobId")

            if isinstance(
                job_id,
                str,
            ):
                terminal_job_ids.add(job_id)

        return terminal_job_ids

    async def iter_unresolved_jobs(
        self,
        *,
        run_id: str,
        retryable_only: bool = False,
    ) -> AsyncIterator[CardekhoCityPriceJob]:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_CITY_PRICE_FAILURES_COLLECTION
        )

        query: dict[str, Any] = {
            "runId": normalized_run_id,
            "status": "failed",
        }

        if retryable_only:
            query["retryable"] = True

        cursor = collection.find(
            query,
            {
                "_id": 0,
                "jobId": 1,
                "modelId": 1,
                "modelName": 1,
                "modelSlug": 1,
                "modelStatus": 1,
                "brandId": 1,
                "brandName": 1,
                "brandSlug": 1,
                "carSlug": 1,
                "cityId": 1,
                "cityName": 1,
                "cityDisplayName": 1,
                "citySlug": 1,
                "isPopularCity": 1,
                "sourceCarDocumentId": 1,
                "sourceCarRunId": 1,
                "sourceCityDocumentId": 1,
                "sourceCityRunId": 1,
            },
        ).sort(
            [
                (
                    "modelId",
                    1,
                ),
                (
                    "cityId",
                    1,
                ),
            ]
        )

        source_trim_cache: dict[
            str,
            tuple[
                CardekhoCityPriceSourceTrim,
                ...,
            ],
        ] = {}

        async for document in cursor:
            try:
                source_car_document_id = document["sourceCarDocumentId"]

                model_id = document["modelId"]

                if not isinstance(
                    source_car_document_id,
                    str,
                ):
                    raise ValueError("sourceCarDocumentId must be a string")

                normalized_source_car_id = source_car_document_id.strip()

                if not normalized_source_car_id:
                    raise ValueError("sourceCarDocumentId cannot be empty")

                source_trims = source_trim_cache.get(normalized_source_car_id)

                if source_trims is None:
                    source_trims = await self._load_source_trims(
                        source_car_document_id=(normalized_source_car_id),
                        model_id=model_id,
                    )

                    source_trim_cache[normalized_source_car_id] = source_trims

                yield CardekhoCityPriceJob(
                    model_id=model_id,
                    model_name=document["modelName"],
                    model_slug=document["modelSlug"],
                    model_status=document["modelStatus"],
                    brand_id=document["brandId"],
                    brand_name=document["brandName"],
                    brand_slug=document["brandSlug"],
                    car_slug=document["carSlug"],
                    city_id=document["cityId"],
                    city_name=document["cityName"],
                    city_display_name=document["cityDisplayName"],
                    city_slug=document["citySlug"],
                    is_popular_city=bool(
                        document.get(
                            "isPopularCity",
                            False,
                        )
                    ),
                    source_car_document_id=(normalized_source_car_id),
                    source_car_run_id=(document.get("sourceCarRunId")),
                    source_city_document_id=(document["sourceCityDocumentId"]),
                    source_city_run_id=(document.get("sourceCityRunId")),
                    source_trims=source_trims,
                )

            except (
                KeyError,
                TypeError,
                ValueError,
            ) as error:
                logger_service.error(
                    (
                        "Skipping malformed Cardekho "
                        "city-price failure document: "
                        f"run_id={normalized_run_id}, "
                        "job_id="
                        f"{document.get('jobId')!r}"
                    ),
                    exception=error,
                    context=(self.__class__.__name__),
                )

    async def count_unresolved(
        self,
        *,
        run_id: str,
        retryable_only: bool = False,
    ) -> int:
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_CITY_PRICE_FAILURES_COLLECTION
        )

        query: dict[str, Any] = {
            "runId": normalized_run_id,
            "status": "failed",
        }

        if retryable_only:
            query["retryable"] = True

        return await collection.count_documents(query)

    async def mark_resolved(
        self,
        *,
        run_id: str,
        job_ids: Sequence[str],
    ) -> FailureResolutionResult:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_job_ids = self._normalize_job_ids(job_ids)

        if not normalized_job_ids:
            return FailureResolutionResult(
                requested=0,
                matched=0,
                modified=0,
            )

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_CITY_PRICE_FAILURES_COLLECTION
        )

        current_time = datetime.now(timezone.utc)

        result = await collection.update_many(
            {
                "runId": (normalized_run_id),
                "jobId": {
                    "$in": (normalized_job_ids),
                },
                "status": "failed",
            },
            {
                "$set": {
                    "status": "resolved",
                    "resolvedAt": (current_time),
                    "updatedAt": (current_time),
                }
            },
        )

        return FailureResolutionResult(
            requested=len(normalized_job_ids),
            matched=(result.matched_count),
            modified=(result.modified_count),
        )


cardekho_city_price_failure_repository = CardekhoCityPriceFailureRepository()
