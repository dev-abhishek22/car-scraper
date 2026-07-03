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
from src.models.carwale_city import (
    CarWaleCity,
)

CARWALE_CITIES_COLLECTION = "carwale_cities"


@dataclass(frozen=True, slots=True)
class CityBulkUpsertResult:
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


class CarWaleCityRepository:
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
    def _validate_positive_integer(
        value: int,
        *,
        field_name: str,
    ) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field_name} must be a positive integer")

        return value

    @staticmethod
    def _normalize_masking_name(
        value: str,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError("city_masking_name must be a string")

        normalized_value = value.strip().lower()

        if not normalized_value:
            raise ValueError("city_masking_name cannot be empty")

        return normalized_value

    async def bulk_upsert(
        self,
        *,
        cities: Sequence[Mapping[str, Any]],
        run_id: str,
    ) -> CityBulkUpsertResult:
        if not cities:
            return CityBulkUpsertResult(
                received=0,
                processed=0,
                matched=0,
                modified=0,
                inserted=0,
            )

        normalized_run_id = self._normalize_run_id(run_id)

        deduplicated_cities: dict[
            str,
            CarWaleCity,
        ] = {}

        for city_data in cities:
            city = CarWaleCity.create(
                city=city_data,
                run_id=normalized_run_id,
            )

            deduplicated_cities[city.document_id] = city

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITIES_COLLECTION)

        operations: list[UpdateOne] = []

        for city in deduplicated_cities.values():
            document = city.to_mongo_document()

            document.pop(
                "_id",
                None,
            )

            created_at = document.pop(
                "createdAt",
                datetime.now(timezone.utc),
            )

            operations.append(
                UpdateOne(
                    {
                        "_id": city.document_id,
                    },
                    {
                        "$set": document,
                        "$setOnInsert": {
                            "createdAt": created_at,
                        },
                    },
                    upsert=True,
                )
            )

        result: BulkWriteResult = await collection.bulk_write(
            operations,
            ordered=False,
        )

        return CityBulkUpsertResult(
            received=len(cities),
            processed=len(operations),
            matched=result.matched_count,
            modified=result.modified_count,
            inserted=result.upserted_count,
        )

    async def get_by_city_id(
        self,
        city_id: int,
    ) -> CarWaleCity | None:
        normalized_city_id = self._validate_positive_integer(
            city_id,
            field_name="city_id",
        )

        document_id = CarWaleCity.build_document_id(
            city_id=normalized_city_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITIES_COLLECTION)

        document = await collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return CarWaleCity.model_validate(document)

    async def get_by_masking_name(
        self,
        city_masking_name: str,
    ) -> CarWaleCity | None:
        normalized_masking_name = self._normalize_masking_name(city_masking_name)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITIES_COLLECTION)

        document = await collection.find_one(
            {
                "cityMaskingName": (normalized_masking_name),
            }
        )

        if document is None:
            return None

        return CarWaleCity.model_validate(document)

    async def count(
        self,
        *,
        include_deleted: bool = True,
    ) -> int:
        query: dict[str, Any] = {}

        if not include_deleted:
            query["isDeleted"] = False

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITIES_COLLECTION)

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        include_deleted: bool = True,
    ) -> AsyncIterator[CarWaleCity]:
        query: dict[str, Any] = {}

        if not include_deleted:
            query["isDeleted"] = False

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CITIES_COLLECTION)

        cursor = collection.find(query).sort(
            [
                (
                    "isPopular",
                    -1,
                ),
                (
                    "cityName",
                    1,
                ),
                (
                    "cityId",
                    1,
                ),
            ]
        )

        async for document in cursor:
            yield CarWaleCity.model_validate(document)

    async def list_all(
        self,
        *,
        include_deleted: bool = True,
    ) -> list[CarWaleCity]:
        cities: list[CarWaleCity] = []

        async for city in self.iter_all(
            include_deleted=include_deleted,
        ):
            cities.append(city)

        return cities


carwale_city_repository = CarWaleCityRepository()
