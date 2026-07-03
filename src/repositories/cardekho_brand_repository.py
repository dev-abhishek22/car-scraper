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
from src.models.cardekho_brand import (
    CarDekhoBrand,
)

CARDEKHO_BRANDS_COLLECTION = "cardekho_brands"


@dataclass(
    frozen=True,
    slots=True,
)
class BrandBulkUpsertResult:
    received: int
    processed: int
    matched: int
    modified: int
    inserted: int

    def to_dict(
        self,
    ) -> dict[str, int]:
        return {
            "received": self.received,
            "processed": self.processed,
            "matched": self.matched,
            "modified": self.modified,
            "inserted": self.inserted,
        }


class CarDekhoBrandRepository:
    def __init__(
        self,
        connection: MongoConnection = mongo_connection,
    ) -> None:
        self._connection = connection

    @staticmethod
    def _normalize_run_id(
        run_id: str,
    ) -> str:
        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        return normalized_run_id

    @staticmethod
    def _normalize_slug(
        slug: str,
    ) -> str:
        if not isinstance(
            slug,
            str,
        ):
            raise ValueError("slug must be a string")

        normalized_slug = slug.strip().lower().replace("_", "-").replace(" ", "-")

        while "--" in normalized_slug:
            normalized_slug = normalized_slug.replace(
                "--",
                "-",
            )

        normalized_slug = normalized_slug.strip("-")

        if not normalized_slug:
            raise ValueError("slug cannot be empty")

        return normalized_slug

    @staticmethod
    def _validate_brand_id(
        brand_id: int,
    ) -> int:
        if isinstance(brand_id, bool) or not isinstance(brand_id, int) or brand_id <= 0:
            raise ValueError("brand_id must be a positive integer")

        return brand_id

    async def bulk_upsert(
        self,
        brands: Sequence[Mapping[str, Any]],
        *,
        run_id: str,
    ) -> BrandBulkUpsertResult:
        if not brands:
            return BrandBulkUpsertResult(
                received=0,
                processed=0,
                matched=0,
                modified=0,
                inserted=0,
            )

        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        deduplicated_brands: dict[
            str,
            CarDekhoBrand,
        ] = {}

        for brand_data in brands:
            brand = CarDekhoBrand.create(
                brand=brand_data,
                run_id=normalized_run_id,
            )

            deduplicated_brands[brand.document_id] = brand

        current_time = datetime.now(timezone.utc)

        operations: list[UpdateOne] = []

        for brand in deduplicated_brands.values():
            document = brand.to_mongo_document()

            document.pop(
                "_id",
                None,
            )

            document.pop(
                "createdAt",
                None,
            )

            operations.append(
                UpdateOne(
                    {
                        "_id": brand.document_id,
                    },
                    {
                        "$set": document,
                        "$setOnInsert": {
                            "createdAt": current_time,
                        },
                    },
                    upsert=True,
                )
            )

        result: BulkWriteResult = await collection.bulk_write(
            operations,
            ordered=False,
        )

        return BrandBulkUpsertResult(
            received=len(brands),
            processed=len(operations),
            matched=result.matched_count,
            modified=result.modified_count,
            inserted=result.upserted_count,
        )

    async def upsert_one(
        self,
        brand_data: Mapping[str, Any],
        *,
        run_id: str,
    ) -> CarDekhoBrand:
        normalized_run_id = self._normalize_run_id(run_id)

        brand = CarDekhoBrand.create(
            brand=brand_data,
            run_id=normalized_run_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        document = brand.to_mongo_document()

        document.pop(
            "_id",
            None,
        )

        document.pop(
            "createdAt",
            None,
        )

        await collection.update_one(
            {
                "_id": brand.document_id,
            },
            {
                "$set": document,
                "$setOnInsert": {
                    "createdAt": (brand.created_at),
                },
            },
            upsert=True,
        )

        stored_document = await collection.find_one(
            {
                "_id": brand.document_id,
            }
        )

        if stored_document is None:
            raise RuntimeError(
                "CarDekho brand was upserted but "
                "could not be read back: "
                f"_id={brand.document_id}"
            )

        return CarDekhoBrand.model_validate(stored_document)

    async def get_by_slug(
        self,
        slug: str,
    ) -> CarDekhoBrand | None:
        normalized_slug = self._normalize_slug(slug)

        document_id = CarDekhoBrand.build_document_id(normalized_slug)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return CarDekhoBrand.model_validate(document)

    async def require_by_slug(
        self,
        slug: str,
    ) -> CarDekhoBrand:
        brand = await self.get_by_slug(slug)

        if brand is None:
            raise LookupError("CarDekho brand was not found: " f"slug={slug!r}")

        return brand

    async def get_by_brand_id(
        self,
        brand_id: int,
    ) -> CarDekhoBrand | None:
        normalized_brand_id = self._validate_brand_id(brand_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        document = await collection.find_one(
            {
                "id": normalized_brand_id,
            }
        )

        if document is None:
            return None

        return CarDekhoBrand.model_validate(document)

    async def get_by_model_request_slug(
        self,
        model_request_slug: str,
    ) -> CarDekhoBrand | None:
        normalized_model_request_slug = self._normalize_slug(model_request_slug)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        document = await collection.find_one(
            {
                "modelRequestSlug": (normalized_model_request_slug),
            }
        )

        if document is None:
            return None

        return CarDekhoBrand.model_validate(document)

    async def count(
        self,
        *,
        brand_status: str | None = None,
    ) -> int:
        query: dict[str, Any] = {}

        if brand_status is not None:
            normalized_status = brand_status.strip().upper()

            if normalized_status not in {
                "CURRENT",
                "UPCOMING",
                "EXPIRED",
            }:
                raise ValueError(
                    "brand_status must be one of: " "CURRENT, UPCOMING, EXPIRED"
                )

            query["brandStatus"] = normalized_status

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        brand_status: str | None = None,
    ) -> AsyncIterator[CarDekhoBrand]:
        query: dict[str, Any] = {}

        if brand_status is not None:
            normalized_status = brand_status.strip().upper()

            if normalized_status not in {
                "CURRENT",
                "UPCOMING",
                "EXPIRED",
            }:
                raise ValueError(
                    "brand_status must be one of: " "CURRENT, UPCOMING, EXPIRED"
                )

            query["brandStatus"] = normalized_status

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        cursor = collection.find(query).sort(
            [
                (
                    "isCurrent",
                    -1,
                ),
                (
                    "isUpcoming",
                    -1,
                ),
                (
                    "isExpired",
                    1,
                ),
                (
                    "isPopular",
                    -1,
                ),
                (
                    "popularity",
                    -1,
                ),
                (
                    "brandName",
                    1,
                ),
                (
                    "slug",
                    1,
                ),
            ]
        )

        async for document in cursor:
            yield CarDekhoBrand.model_validate(document)

    async def list_all(
        self,
        *,
        brand_status: str | None = None,
    ) -> list[CarDekhoBrand]:
        brands: list[CarDekhoBrand] = []

        async for brand in self.iter_all(
            brand_status=brand_status,
        ):
            brands.append(brand)

        return brands

    async def get_slugs(
        self,
        *,
        brand_status: str | None = None,
    ) -> set[str]:
        query: dict[str, Any] = {}

        if brand_status is not None:
            normalized_status = brand_status.strip().upper()

            if normalized_status not in {
                "CURRENT",
                "UPCOMING",
                "EXPIRED",
            }:
                raise ValueError(
                    "brand_status must be one of: " "CURRENT, UPCOMING, EXPIRED"
                )

            query["brandStatus"] = normalized_status

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        cursor = collection.find(
            query,
            {
                "_id": 0,
                "slug": 1,
            },
        )

        slugs: set[str] = set()

        async for document in cursor:
            slug = document.get("slug")

            if isinstance(slug, str) and slug.strip():
                slugs.add(slug.strip().lower())

        return slugs

    async def get_model_request_slugs(
        self,
        *,
        include_current: bool = True,
        include_upcoming: bool = True,
        include_expired: bool = False,
    ) -> set[str]:
        selected_statuses: list[str] = []

        if include_current:
            selected_statuses.append("CURRENT")

        if include_upcoming:
            selected_statuses.append("UPCOMING")

        if include_expired:
            selected_statuses.append("EXPIRED")

        if not selected_statuses:
            return set()

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        cursor = collection.find(
            {
                "brandStatus": {
                    "$in": selected_statuses,
                },
            },
            {
                "_id": 0,
                "modelRequestSlug": 1,
            },
        )

        request_slugs: set[str] = set()

        async for document in cursor:
            request_slug = document.get("modelRequestSlug")

            if isinstance(request_slug, str) and request_slug.strip():
                request_slugs.add(request_slug.strip().lower())

        return request_slugs

    async def delete_not_seen_in_run(
        self,
        *,
        run_id: str,
    ) -> int:
        """
        Remove brands that were not present in the
        specified successful full catalogue run.

        Do not call this automatically unless the API
        returned Current, Upcoming and Expired groups
        successfully.
        """
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_BRANDS_COLLECTION)

        result = await collection.delete_many(
            {
                "lastRunId": {
                    "$ne": normalized_run_id,
                },
            }
        )

        return result.deleted_count


cardekho_brand_repository = CarDekhoBrandRepository()
