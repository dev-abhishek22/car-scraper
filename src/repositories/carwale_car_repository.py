from __future__ import annotations

from collections.abc import (
    AsyncIterator,
    Mapping,
)
from dataclasses import dataclass
from typing import Any

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.carwale_car import (
    CarWaleCar,
)

CARWALE_CARS_COLLECTION = "carwale_cars"


@dataclass(frozen=True, slots=True)
class CarUpsertResult:
    car: CarWaleCar
    matched: int
    modified: int
    inserted: int
    total_versions: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "documentId": (self.car.document_id),
            "makeId": self.car.make_id,
            "modelId": self.car.model_id,
            "matched": self.matched,
            "modified": self.modified,
            "inserted": self.inserted,
            "totalVersions": (self.total_versions),
        }


class CarWaleCarRepository:
    def __init__(
        self,
        connection: MongoConnection = mongo_connection,
    ) -> None:
        self._connection = connection

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
        *,
        field_name: str,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
            raise ValueError(f"{field_name} must be a string")

        normalized_value = value.strip().lower()

        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        return normalized_value

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

    async def upsert_one(
        self,
        *,
        model: Mapping[str, Any],
        car_data: Mapping[str, Any],
        run_id: str,
        city_id: int | None = None,
        area_id: int | None = None,
        platform_id: int | None = None,
        show_offer_upfront: bool = False,
        source_model_run_id: str | None = None,
    ) -> CarUpsertResult:
        normalized_run_id = self._normalize_run_id(run_id)

        car = CarWaleCar.create(
            model=model,
            car_data=car_data,
            run_id=normalized_run_id,
            city_id=city_id,
            area_id=area_id,
            platform_id=platform_id,
            show_offer_upfront=(show_offer_upfront),
            source_model_run_id=(source_model_run_id),
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CARS_COLLECTION)

        document = car.to_mongo_document()

        document.pop(
            "_id",
            None,
        )

        created_at = document.pop(
            "createdAt",
            car.created_at,
        )

        update_result = await collection.update_one(
            {
                "_id": car.document_id,
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
                "_id": car.document_id,
            }
        )

        if stored_document is None:
            raise RuntimeError(
                "CarWale car was upserted but "
                "could not be read back: "
                f"_id={car.document_id}"
            )

        stored_car = CarWaleCar.model_validate(stored_document)

        return CarUpsertResult(
            car=stored_car,
            matched=(update_result.matched_count),
            modified=(update_result.modified_count),
            inserted=(1 if update_result.upserted_id is not None else 0),
            total_versions=(stored_car.total_versions),
        )

    async def get_by_document_id(
        self,
        document_id: str,
    ) -> CarWaleCar | None:
        if not isinstance(
            document_id,
            str,
        ):
            raise ValueError("document_id must be a string")

        normalized_document_id = document_id.strip()

        if not normalized_document_id:
            raise ValueError("document_id cannot be empty")

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CARS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": normalized_document_id,
            }
        )

        if document is None:
            return None

        return CarWaleCar.model_validate(document)

    async def get_by_ids(
        self,
        *,
        make_id: int,
        model_id: int,
    ) -> CarWaleCar | None:
        normalized_make_id = self._validate_positive_integer(
            make_id,
            field_name="make_id",
        )

        normalized_model_id = self._validate_positive_integer(
            model_id,
            field_name="model_id",
        )

        document_id = CarWaleCar.build_document_id(
            make_id=normalized_make_id,
            model_id=normalized_model_id,
        )

        return await self.get_by_document_id(document_id)

    async def require_by_ids(
        self,
        *,
        make_id: int,
        model_id: int,
    ) -> CarWaleCar:
        car = await self.get_by_ids(
            make_id=make_id,
            model_id=model_id,
        )

        if car is None:
            raise LookupError(
                f"CarWale car was not found: make_id={make_id}, model_id={model_id}"
            )

        return car

    async def get_by_masking_names(
        self,
        *,
        make_masking_name: str,
        model_masking_name: str,
    ) -> CarWaleCar | None:
        normalized_make_masking_name = self._normalize_masking_name(
            make_masking_name,
            field_name=("make_masking_name"),
        )

        normalized_model_masking_name = self._normalize_masking_name(
            model_masking_name,
            field_name=("model_masking_name"),
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CARS_COLLECTION)

        document = await collection.find_one(
            {
                "makeMaskingName": (normalized_make_masking_name),
                "modelMaskingName": (normalized_model_masking_name),
            }
        )

        if document is None:
            return None

        return CarWaleCar.model_validate(document)

    async def require_by_masking_names(
        self,
        *,
        make_masking_name: str,
        model_masking_name: str,
    ) -> CarWaleCar:
        car = await self.get_by_masking_names(
            make_masking_name=(make_masking_name),
            model_masking_name=(model_masking_name),
        )

        if car is None:
            raise LookupError(
                "CarWale car was not found: "
                f"make={make_masking_name!r}, "
                f"model={model_masking_name!r}"
            )

        return car

    async def count(
        self,
        *,
        make_id: int | None = None,
    ) -> int:
        query: dict[str, Any] = {}

        if make_id is not None:
            query["makeId"] = self._validate_positive_integer(
                make_id,
                field_name="make_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CARS_COLLECTION)

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        make_id: int | None = None,
    ) -> AsyncIterator[CarWaleCar]:
        query: dict[str, Any] = {}

        if make_id is not None:
            query["makeId"] = self._validate_positive_integer(
                make_id,
                field_name="make_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CARS_COLLECTION)

        cursor = collection.find(query).sort(
            [
                (
                    "makeName",
                    1,
                ),
                (
                    "modelName",
                    1,
                ),
                (
                    "makeId",
                    1,
                ),
                (
                    "modelId",
                    1,
                ),
            ]
        )

        async for document in cursor:
            yield CarWaleCar.model_validate(document)

    async def list_all(
        self,
        *,
        make_id: int | None = None,
    ) -> list[CarWaleCar]:
        cars: list[CarWaleCar] = []

        async for car in self.iter_all(make_id=make_id):
            cars.append(car)

        return cars

    async def iter_versions(
        self,
        *,
        make_id: int | None = None,
        model_id: int | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Yield every version stored inside carwale_cars.

        This method will later become the MongoDB input
        source for the city-price scraper.
        """
        query: dict[str, Any] = {}

        if make_id is not None:
            query["makeId"] = self._validate_positive_integer(
                make_id,
                field_name="make_id",
            )

        if model_id is not None:
            query["modelId"] = self._validate_positive_integer(
                model_id,
                field_name="model_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CARS_COLLECTION)

        projection = {
            "_id": 1,
            "makeId": 1,
            "makeName": 1,
            "makeMaskingName": 1,
            "modelId": 1,
            "modelName": 1,
            "modelMaskingName": 1,
            "lastRunId": 1,
            "data.versions": 1,
        }

        cursor = collection.find(
            query,
            projection,
        ).sort(
            [
                (
                    "makeId",
                    1,
                ),
                (
                    "modelId",
                    1,
                ),
            ]
        )

        async for document in cursor:
            data = document.get("data")

            if not isinstance(
                data,
                Mapping,
            ):
                continue

            versions = data.get("versions")

            if not isinstance(
                versions,
                list,
            ):
                continue

            for version in versions:
                if not isinstance(
                    version,
                    Mapping,
                ):
                    continue

                yield {
                    "carDocumentId": (document.get("_id")),
                    "makeId": (document.get("makeId")),
                    "makeName": (document.get("makeName")),
                    "makeMaskingName": (document.get("makeMaskingName")),
                    "modelId": (document.get("modelId")),
                    "modelName": (document.get("modelName")),
                    "modelMaskingName": (document.get("modelMaskingName")),
                    "sourceCarRunId": (document.get("lastRunId")),
                    "version": dict(version),
                }

    async def get_version_ids(
        self,
        *,
        make_id: int | None = None,
        model_id: int | None = None,
    ) -> set[int]:
        version_ids: set[int] = set()

        async for version_record in self.iter_versions(
            make_id=make_id,
            model_id=model_id,
        ):
            version = version_record.get("version")

            if not isinstance(
                version,
                Mapping,
            ):
                continue

            version_id = version.get("versionId")

            if (
                isinstance(version_id, int)
                and not isinstance(
                    version_id,
                    bool,
                )
                and version_id > 0
            ):
                version_ids.add(version_id)

        return version_ids

    async def count_versions(
        self,
        *,
        make_id: int | None = None,
        model_id: int | None = None,
    ) -> int:
        total_versions = 0

        async for _ in self.iter_versions(
            make_id=make_id,
            model_id=model_id,
        ):
            total_versions += 1

        return total_versions

    async def delete_not_seen_in_run(
        self,
        *,
        run_id: str,
        make_id: int | None = None,
    ) -> int:
        """
        Delete car documents not seen in a completed run.

        Do not call this automatically unless the run is
        known to have processed the complete selected model
        set successfully.
        """
        normalized_run_id = self._normalize_run_id(run_id)

        query: dict[str, Any] = {
            "lastRunId": {
                "$ne": normalized_run_id,
            }
        }

        if make_id is not None:
            query["makeId"] = self._validate_positive_integer(
                make_id,
                field_name="make_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_CARS_COLLECTION)

        result = await collection.delete_many(query)

        return result.deleted_count


carwale_car_repository = CarWaleCarRepository()
