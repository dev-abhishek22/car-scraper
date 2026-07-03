from __future__ import annotations

from collections.abc import AsyncIterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from pymongo import UpdateOne
from pymongo.results import BulkWriteResult

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.carwale_brand import (
    CarWaleBrand,
)

CARWALE_BRANDS_COLLECTION = "carwale_brands"


@dataclass(frozen=True, slots=True)
class BrandBulkUpsertResult:
    received: int
    processed: int
    matched: int
    modified: int
    inserted: int

    def to_dict(self) -> dict[str, int]:
        return {
            "received": self.received,
            "processed": self.processed,
            "matched": self.matched,
            "modified": self.modified,
            "inserted": self.inserted,
        }


class CarWaleBrandRepository:
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
    def _normalize_masking_name(
        masking_name: str,
    ) -> str:
        normalized_masking_name = masking_name.strip().lower()

        if not normalized_masking_name:
            raise ValueError("masking_name cannot be empty")

        return normalized_masking_name

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

        collection = self._connection.collection(CARWALE_BRANDS_COLLECTION)

        deduplicated_brands: dict[
            str,
            CarWaleBrand,
        ] = {}

        for brand_data in brands:
            brand = CarWaleBrand.create(
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
    ) -> CarWaleBrand:
        normalized_run_id = self._normalize_run_id(run_id)

        brand = CarWaleBrand.create(
            brand=brand_data,
            run_id=normalized_run_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_BRANDS_COLLECTION)

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
                    "createdAt": brand.created_at,
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
                "CarWale brand was upserted but "
                "could not be read back: "
                f"_id={brand.document_id}"
            )

        return CarWaleBrand.model_validate(stored_document)

    async def get_by_make_id(
        self,
        make_id: int,
    ) -> CarWaleBrand | None:
        document_id = CarWaleBrand.build_document_id(make_id)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_BRANDS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return CarWaleBrand.model_validate(document)

    async def get_by_masking_name(
        self,
        masking_name: str,
    ) -> CarWaleBrand | None:
        normalized_masking_name = self._normalize_masking_name(masking_name)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_BRANDS_COLLECTION)

        document = await collection.find_one(
            {
                "maskingName": normalized_masking_name,
            }
        )

        if document is None:
            return None

        return CarWaleBrand.model_validate(document)

    async def require_by_masking_name(
        self,
        masking_name: str,
    ) -> CarWaleBrand:
        brand = await self.get_by_masking_name(masking_name)

        if brand is None:
            raise LookupError(
                f"CarWale brand was not found: masking_name={masking_name!r}"
            )

        return brand

    async def count(
        self,
    ) -> int:
        await self._connection.connect()

        collection = self._connection.collection(CARWALE_BRANDS_COLLECTION)

        return await collection.count_documents({})

    async def iter_all(
        self,
    ) -> AsyncIterator[CarWaleBrand]:
        await self._connection.connect()

        collection = self._connection.collection(CARWALE_BRANDS_COLLECTION)

        cursor = collection.find({}).sort(
            [
                (
                    "makeName",
                    1,
                ),
                (
                    "makeId",
                    1,
                ),
            ]
        )

        async for document in cursor:
            yield CarWaleBrand.model_validate(document)

    async def list_all(
        self,
    ) -> list[CarWaleBrand]:
        brands: list[CarWaleBrand] = []

        async for brand in self.iter_all():
            brands.append(brand)

        return brands

    async def get_make_ids(
        self,
    ) -> set[int]:
        await self._connection.connect()

        collection = self._connection.collection(CARWALE_BRANDS_COLLECTION)

        cursor = collection.find(
            {},
            {
                "_id": 0,
                "makeId": 1,
            },
        )

        make_ids: set[int] = set()

        async for document in cursor:
            make_id = document.get("makeId")

            if (
                isinstance(make_id, int)
                and not isinstance(make_id, bool)
                and make_id > 0
            ):
                make_ids.add(make_id)

        return make_ids

    async def delete_not_seen_in_run(
        self,
        *,
        run_id: str,
    ) -> int:
        """
        Remove brands that were not present in the specified run.

        Do not call this automatically. It should only be used when
        a complete, successful all-brands response is guaranteed.
        """
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_BRANDS_COLLECTION)

        result = await collection.delete_many(
            {
                "lastRunId": {
                    "$ne": normalized_run_id,
                }
            }
        )

        return result.deleted_count


carwale_brand_repository = CarWaleBrandRepository()
