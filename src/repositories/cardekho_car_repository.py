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
from src.models.cardekho_car import (
    CarDekhoCar,
)

CARDEKHO_CARS_COLLECTION = "cardekho_cars"


@dataclass(
    frozen=True,
    slots=True,
)
class CarUpsertResult:
    car: CarDekhoCar
    matched: int
    modified: int
    inserted: int
    total_variants: int
    total_comparisons: int
    total_similar_cars: int

    def to_dict(
        self,
    ) -> dict[str, Any]:
        return {
            "documentId": self.car.document_id,
            "modelId": self.car.model_id,
            "brandSlug": self.car.brand_slug,
            "modelSlug": self.car.slug,
            "carSlug": self.car.car_slug,
            "matched": self.matched,
            "modified": self.modified,
            "inserted": self.inserted,
            "totalVariants": self.total_variants,
            "totalComparisons": self.total_comparisons,
            "totalSimilarCars": self.total_similar_cars,
        }


class CarDekhoCarRepository:
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
    def _normalize_slug(
        value: str,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

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

    @staticmethod
    def _normalize_model_status(
        model_status: str,
    ) -> str:
        if not isinstance(
            model_status,
            str,
        ):
            raise ValueError("model_status must be a string")

        normalized_status = model_status.strip().upper()

        if normalized_status not in {
            "CURRENT",
            "UPCOMING",
            "DISCONTINUED",
        }:
            raise ValueError(
                "model_status must be CURRENT, " "UPCOMING, or DISCONTINUED"
            )

        return normalized_status

    async def upsert_one(
        self,
        *,
        model: Mapping[str, Any],
        car_data: Mapping[str, Any],
        run_id: str,
        source_model_run_id: str | None = None,
    ) -> CarUpsertResult:
        normalized_run_id = self._normalize_run_id(
            run_id,
        )

        car = CarDekhoCar.create(
            model=model,
            car_data=car_data,
            run_id=normalized_run_id,
            source_model_run_id=(source_model_run_id),
        )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CARS_COLLECTION)

        document = car.to_mongo_document()

        document.pop(
            "_id",
            None,
        )

        created_at = document.pop(
            "createdAt",
            car.created_at,
        )

        result = await collection.update_one(
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
                "CarDekho car was upserted but "
                "could not be read back: "
                f"_id={car.document_id}"
            )

        stored_car = CarDekhoCar.model_validate(stored_document)

        return CarUpsertResult(
            car=stored_car,
            matched=result.matched_count,
            modified=result.modified_count,
            inserted=(1 if result.upserted_id is not None else 0),
            total_variants=(stored_car.total_variants),
            total_comparisons=(stored_car.total_comparisons),
            total_similar_cars=(stored_car.total_similar_cars),
        )

    async def get_by_model_id(
        self,
        model_id: int,
    ) -> CarDekhoCar | None:
        normalized_model_id = self._validate_positive_integer(
            model_id,
            field_name="model_id",
        )

        document_id = CarDekhoCar.build_document_id(normalized_model_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CARS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return CarDekhoCar.model_validate(document)

    async def require_by_model_id(
        self,
        model_id: int,
    ) -> CarDekhoCar:
        car = await self.get_by_model_id(model_id)

        if car is None:
            raise LookupError("CarDekho car was not found: " f"model_id={model_id}")

        return car

    async def get_by_slugs(
        self,
        *,
        brand_slug: str,
        model_slug: str,
    ) -> CarDekhoCar | None:
        normalized_brand_slug = self._normalize_slug(
            brand_slug,
            field_name="brand_slug",
        )

        normalized_model_slug = self._normalize_slug(
            model_slug,
            field_name="model_slug",
        )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CARS_COLLECTION)

        document = await collection.find_one(
            {
                "brandSlug": (normalized_brand_slug),
                "slug": (normalized_model_slug),
            }
        )

        if document is None:
            return None

        return CarDekhoCar.model_validate(document)

    async def require_by_slugs(
        self,
        *,
        brand_slug: str,
        model_slug: str,
    ) -> CarDekhoCar:
        car = await self.get_by_slugs(
            brand_slug=brand_slug,
            model_slug=model_slug,
        )

        if car is None:
            raise LookupError(
                "CarDekho car was not found: "
                f"brand={brand_slug!r}, "
                f"model={model_slug!r}"
            )

        return car

    async def get_by_car_slug(
        self,
        car_slug: str,
    ) -> CarDekhoCar | None:
        normalized_car_slug = self._normalize_slug(
            car_slug,
            field_name="car_slug",
        )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CARS_COLLECTION)

        document = await collection.find_one(
            {
                "carSlug": normalized_car_slug,
            }
        )

        if document is None:
            return None

        return CarDekhoCar.model_validate(document)

    async def require_by_car_slug(
        self,
        car_slug: str,
    ) -> CarDekhoCar:
        car = await self.get_by_car_slug(car_slug)

        if car is None:
            raise LookupError("CarDekho car was not found: " f"car_slug={car_slug!r}")

        return car

    async def count(
        self,
        *,
        brand_slug: str | None = None,
        model_status: str | None = None,
    ) -> int:
        query: dict[str, Any] = {}

        if brand_slug is not None:
            query["brandSlug"] = self._normalize_slug(
                brand_slug,
                field_name="brand_slug",
            )

        if model_status is not None:
            query["modelStatus"] = self._normalize_model_status(model_status)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CARS_COLLECTION)

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        brand_slug: str | None = None,
        model_status: str | None = None,
    ) -> AsyncIterator[CarDekhoCar]:
        query: dict[str, Any] = {}

        if brand_slug is not None:
            query["brandSlug"] = self._normalize_slug(
                brand_slug,
                field_name="brand_slug",
            )

        if model_status is not None:
            query["modelStatus"] = self._normalize_model_status(model_status)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CARS_COLLECTION)

        cursor = collection.find(query).sort(
            [
                (
                    "brandName",
                    1,
                ),
                (
                    "modelStatus",
                    1,
                ),
                (
                    "modelName",
                    1,
                ),
                (
                    "id",
                    1,
                ),
            ]
        )

        async for document in cursor:
            yield CarDekhoCar.model_validate(document)

    async def list_all(
        self,
        *,
        brand_slug: str | None = None,
        model_status: str | None = None,
    ) -> list[CarDekhoCar]:
        cars: list[CarDekhoCar] = []

        async for car in self.iter_all(
            brand_slug=brand_slug,
            model_status=model_status,
        ):
            cars.append(car)

        return cars

    async def iter_variants(
        self,
        *,
        brand_slug: str | None = None,
        model_id: int | None = None,
        model_status: str | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Yield every minimal variant stored inside
        cardekho_cars.

        This method can later be used as the MongoDB
        input source for the CarDekho trims scraper.
        """

        query: dict[str, Any] = {}

        if brand_slug is not None:
            query["brandSlug"] = self._normalize_slug(
                brand_slug,
                field_name="brand_slug",
            )

        if model_id is not None:
            query["id"] = self._validate_positive_integer(
                model_id,
                field_name="model_id",
            )

        if model_status is not None:
            query["modelStatus"] = self._normalize_model_status(model_status)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CARS_COLLECTION)

        projection = {
            "_id": 1,
            "id": 1,
            "brandId": 1,
            "brandName": 1,
            "brandSlug": 1,
            "name": 1,
            "slug": 1,
            "carSlug": 1,
            "modelName": 1,
            "modelStatus": 1,
            "lastRunId": 1,
            "variants": 1,
        }

        cursor = collection.find(
            query,
            projection,
        ).sort(
            [
                (
                    "brandName",
                    1,
                ),
                (
                    "modelName",
                    1,
                ),
                (
                    "id",
                    1,
                ),
            ]
        )

        async for document in cursor:
            variants = document.get("variants")

            if not isinstance(
                variants,
                list,
            ):
                continue

            for variant in variants:
                if not isinstance(
                    variant,
                    Mapping,
                ):
                    continue

                yield {
                    "carDocumentId": (document.get("_id")),
                    "modelId": (document.get("id")),
                    "brandId": (document.get("brandId")),
                    "brandName": (document.get("brandName")),
                    "brandSlug": (document.get("brandSlug")),
                    "modelName": (document.get("modelName")),
                    "modelSlug": (document.get("slug")),
                    "carSlug": (document.get("carSlug")),
                    "modelStatus": (document.get("modelStatus")),
                    "sourceCarRunId": (document.get("lastRunId")),
                    "variant": dict(variant),
                }

    async def get_variant_ids(
        self,
        *,
        brand_slug: str | None = None,
        model_id: int | None = None,
        model_status: str | None = None,
    ) -> set[int]:
        variant_ids: set[int] = set()

        async for variant_record in self.iter_variants(
            brand_slug=brand_slug,
            model_id=model_id,
            model_status=model_status,
        ):
            variant = variant_record.get("variant")

            if not isinstance(
                variant,
                Mapping,
            ):
                continue

            variant_id = variant.get("id")

            if (
                isinstance(variant_id, int)
                and not isinstance(
                    variant_id,
                    bool,
                )
                and variant_id > 0
            ):
                variant_ids.add(variant_id)

        return variant_ids

    async def count_variants(
        self,
        *,
        brand_slug: str | None = None,
        model_id: int | None = None,
        model_status: str | None = None,
    ) -> int:
        total_variants = 0

        async for _ in self.iter_variants(
            brand_slug=brand_slug,
            model_id=model_id,
            model_status=model_status,
        ):
            total_variants += 1

        return total_variants

    async def delete_not_seen_in_run(
        self,
        *,
        run_id: str,
        brand_slug: str | None = None,
    ) -> int:
        """
        Delete car documents not seen in a completed run.

        Do not call this automatically. It is only safe
        when the run processed the complete selected model
        set successfully.
        """

        normalized_run_id = self._normalize_run_id(run_id)

        query: dict[str, Any] = {
            "lastRunId": {
                "$ne": normalized_run_id,
            }
        }

        if brand_slug is not None:
            query["brandSlug"] = self._normalize_slug(
                brand_slug,
                field_name="brand_slug",
            )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_CARS_COLLECTION)

        result = await collection.delete_many(query)

        return result.deleted_count


cardekho_car_repository = CarDekhoCarRepository()
