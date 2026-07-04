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
from src.models.cardekho_city import (
    CarDekhoCity,
)

CARDEKHO_CITIES_COLLECTION = "cardekho_cities"


@dataclass(
    frozen=True,
    slots=True,
)
class CityBulkUpsertResult:
    received: int
    processed: int
    matched: int
    modified: int
    inserted: int
    total_aliases: int
    total_regions: int

    def to_dict(
        self,
    ) -> dict[str, int]:
        return {
            "received": self.received,
            "processed": self.processed,
            "matched": self.matched,
            "modified": self.modified,
            "inserted": self.inserted,
            "totalAliases": self.total_aliases,
            "totalRegions": self.total_regions,
        }


class CarDekhoCityRepository:
    def __init__(
        self,
        connection: MongoConnection = mongo_connection,
    ) -> None:
        self._connection = connection

    @staticmethod
    def _normalize_run_id(
        run_id: str,
    ) -> str:
        if not isinstance(run_id, str):
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
    def _normalize_non_empty_string(
        value: str,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        return normalized_value

    @staticmethod
    def _validate_optional_boolean(
        value: bool | None,
        *,
        field_name: str,
    ) -> bool | None:
        if value is None:
            return None

        if not isinstance(value, bool):
            raise ValueError(f"{field_name} must be a boolean")

        return value

    async def bulk_upsert(
        self,
        *,
        cities: Sequence[Mapping[str, Any]],
        run_id: str,
    ) -> CityBulkUpsertResult:
        """
        Upsert all normalized CarDekho cities.

        Existing documents are updated in place. New
        documents are inserted. Cities missing from a
        later bundle are not deleted automatically.
        """
        normalized_run_id = self._normalize_run_id(run_id)

        if not cities:
            return CityBulkUpsertResult(
                received=0,
                processed=0,
                matched=0,
                modified=0,
                inserted=0,
                total_aliases=0,
                total_regions=0,
            )

        deduplicated_cities: dict[
            str,
            CarDekhoCity,
        ] = {}

        for city_data in cities:
            city = CarDekhoCity.create(
                city_data=city_data,
                run_id=normalized_run_id,
            )

            deduplicated_cities[city.document_id] = city

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITIES_COLLECTION)

        operations: list[UpdateOne] = []

        total_aliases = 0
        total_regions = 0

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

            total_aliases += len(city.aliases)

            total_regions += len(city.regions)

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
            total_aliases=total_aliases,
            total_regions=total_regions,
        )

    async def upsert_one(
        self,
        *,
        city_data: Mapping[str, Any],
        run_id: str,
    ) -> CarDekhoCity:
        normalized_run_id = self._normalize_run_id(run_id)

        city = CarDekhoCity.create(
            city_data=city_data,
            run_id=normalized_run_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITIES_COLLECTION)

        document = city.to_mongo_document()

        document.pop(
            "_id",
            None,
        )

        created_at = document.pop(
            "createdAt",
            city.created_at,
        )

        await collection.update_one(
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

        stored_document = await collection.find_one(
            {
                "_id": city.document_id,
            }
        )

        if stored_document is None:
            raise RuntimeError(
                "CarDekho city was upserted but "
                "could not be read back: "
                f"_id={city.document_id}"
            )

        return CarDekhoCity.model_validate(stored_document)

    async def get_by_city_id(
        self,
        city_id: int,
    ) -> CarDekhoCity | None:
        normalized_city_id = self._validate_positive_integer(
            city_id,
            field_name="city_id",
        )

        document_id = CarDekhoCity.build_document_id(normalized_city_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITIES_COLLECTION)

        document = await collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return CarDekhoCity.model_validate(document)

    async def require_by_city_id(
        self,
        city_id: int,
    ) -> CarDekhoCity:
        city = await self.get_by_city_id(city_id)

        if city is None:
            raise LookupError(f"CarDekho city was not found: city_id={city_id}")

        return city

    async def find_by_name(
        self,
        name: str,
    ) -> list[CarDekhoCity]:
        """
        Find cities using cityName, displayName, or aliases.

        Multiple documents may be returned because different
        city IDs can share the same source name.
        """
        normalized_name = self._normalize_non_empty_string(
            name,
            field_name="name",
        )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITIES_COLLECTION)

        cursor = collection.find(
            {
                "$or": [
                    {
                        "cityName": normalized_name,
                    },
                    {
                        "displayName": normalized_name,
                    },
                    {
                        "aliases": normalized_name,
                    },
                ]
            }
        ).sort(
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

        cities: list[CarDekhoCity] = []

        async for document in cursor:
            cities.append(CarDekhoCity.model_validate(document))

        return cities

    async def count(
        self,
        *,
        is_popular: bool | None = None,
        is_prime: bool | None = None,
        has_regions: bool | None = None,
    ) -> int:
        query: dict[str, Any] = {}

        normalized_is_popular = self._validate_optional_boolean(
            is_popular,
            field_name="is_popular",
        )

        normalized_is_prime = self._validate_optional_boolean(
            is_prime,
            field_name="is_prime",
        )

        normalized_has_regions = self._validate_optional_boolean(
            has_regions,
            field_name="has_regions",
        )

        if normalized_is_popular is not None:
            query["isPopular"] = normalized_is_popular

        if normalized_is_prime is not None:
            query["isPrime"] = normalized_is_prime

        if normalized_has_regions is True:
            query["regions.0"] = {
                "$exists": True,
            }

        elif normalized_has_regions is False:
            query["regions.0"] = {
                "$exists": False,
            }

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITIES_COLLECTION)

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        is_popular: bool | None = None,
        is_prime: bool | None = None,
        has_regions: bool | None = None,
    ) -> AsyncIterator[CarDekhoCity]:
        query: dict[str, Any] = {}

        normalized_is_popular = self._validate_optional_boolean(
            is_popular,
            field_name="is_popular",
        )

        normalized_is_prime = self._validate_optional_boolean(
            is_prime,
            field_name="is_prime",
        )

        normalized_has_regions = self._validate_optional_boolean(
            has_regions,
            field_name="has_regions",
        )

        if normalized_is_popular is not None:
            query["isPopular"] = normalized_is_popular

        if normalized_is_prime is not None:
            query["isPrime"] = normalized_is_prime

        if normalized_has_regions is True:
            query["regions.0"] = {
                "$exists": True,
            }

        elif normalized_has_regions is False:
            query["regions.0"] = {
                "$exists": False,
            }

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITIES_COLLECTION)

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
            yield CarDekhoCity.model_validate(document)

    async def list_all(
        self,
        *,
        is_popular: bool | None = None,
        is_prime: bool | None = None,
        has_regions: bool | None = None,
    ) -> list[CarDekhoCity]:
        cities: list[CarDekhoCity] = []

        async for city in self.iter_all(
            is_popular=is_popular,
            is_prime=is_prime,
            has_regions=has_regions,
        ):
            cities.append(city)

        return cities

    async def get_city_ids(
        self,
        *,
        is_popular: bool | None = None,
        is_prime: bool | None = None,
        has_regions: bool | None = None,
    ) -> set[int]:
        city_ids: set[int] = set()

        async for city in self.iter_all(
            is_popular=is_popular,
            is_prime=is_prime,
            has_regions=has_regions,
        ):
            city_ids.add(city.city_id)

        return city_ids

    async def delete_not_seen_in_run(
        self,
        *,
        run_id: str,
    ) -> int:
        """
        Delete city documents not seen in a completed run.

        Do not call this automatically. It is safe only when
        the complete bundle was downloaded, parsed, validated,
        and stored successfully.
        """
        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CITIES_COLLECTION)

        result = await collection.delete_many(
            {
                "lastRunId": {
                    "$ne": normalized_run_id,
                }
            }
        )

        return result.deleted_count


cardekho_city_repository = CarDekhoCityRepository()
