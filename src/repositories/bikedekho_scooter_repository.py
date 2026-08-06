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
from src.models.bikedekho_scooter import (
    BikeDekhoScooter,
)

BIKEDEKHO_SCOOTERS_COLLECTION = "bikedekho_scooters"


@dataclass(
    frozen=True,
    slots=True,
)
class ScooterUpsertResult:
    scooter: BikeDekhoScooter
    matched: int
    modified: int
    inserted: int
    total_variants: int
    total_comparisons: int
    total_similar_scooters: int

    def to_dict(
        self,
    ) -> dict[str, Any]:
        return {
            "documentId": (self.scooter.document_id),
            "modelId": (self.scooter.model_id),
            "brandSlug": (self.scooter.brand_slug),
            "modelSlug": (self.scooter.slug),
            "scooterSlug": (self.scooter.scooter_slug),
            "matched": self.matched,
            "modified": self.modified,
            "inserted": self.inserted,
            "totalVariants": (self.total_variants),
            "totalComparisons": (self.total_comparisons),
            "totalSimilarScooters": (self.total_similar_scooters),
        }


class BikeDekhoScooterRepository:
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
            raise ValueError(f"{field_name} must be " "a positive integer")

        return value

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
    def _normalize_slug(
        value: str,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(
            value,
            str,
        ):
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
                "model_status must be " "CURRENT, UPCOMING, " "or DISCONTINUED"
            )

        return normalized_status

    async def upsert_one(
        self,
        *,
        model: Mapping[str, Any],
        scooter_data: Mapping[str, Any],
        run_id: str,
        source_model_run_id: str | None = None,
    ) -> ScooterUpsertResult:
        normalized_run_id = self._normalize_run_id(run_id)

        scooter = BikeDekhoScooter.create(
            model=model,
            scooter_data=scooter_data,
            run_id=normalized_run_id,
            source_model_run_id=(source_model_run_id),
        )

        await self._connection.connect()

        collection = self._connection.collection(BIKEDEKHO_SCOOTERS_COLLECTION)

        document = scooter.to_mongo_document()

        document.pop(
            "_id",
            None,
        )

        created_at = document.pop(
            "createdAt",
            scooter.created_at,
        )

        result = await collection.update_one(
            {
                "_id": scooter.document_id,
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
                "_id": scooter.document_id,
            }
        )

        if stored_document is None:
            raise RuntimeError(
                "BikeDekho scooter was upserted "
                "but could not be read back: "
                f"_id={scooter.document_id}"
            )

        stored_scooter = BikeDekhoScooter.model_validate(stored_document)

        return ScooterUpsertResult(
            scooter=stored_scooter,
            matched=(result.matched_count),
            modified=(result.modified_count),
            inserted=(1 if result.upserted_id is not None else 0),
            total_variants=(stored_scooter.total_variants),
            total_comparisons=(stored_scooter.total_comparisons),
            total_similar_scooters=(stored_scooter.total_similar_scooters),
        )

    async def get_by_model_id(
        self,
        model_id: int,
    ) -> BikeDekhoScooter | None:
        normalized_model_id = self._validate_positive_integer(
            model_id,
            field_name="model_id",
        )

        await self._connection.connect()

        collection = self._connection.collection(BIKEDEKHO_SCOOTERS_COLLECTION)

        document = await collection.find_one(
            {
                "id": normalized_model_id,
            }
        )

        if document is None:
            return None

        return BikeDekhoScooter.model_validate(document)

    async def require_by_model_id(
        self,
        model_id: int,
    ) -> BikeDekhoScooter:
        scooter = await self.get_by_model_id(model_id)

        if scooter is None:
            raise LookupError(
                "BikeDekho scooter was not " f"found: model_id={model_id}"
            )

        return scooter

    async def get_by_slugs(
        self,
        *,
        brand_slug: str,
        model_slug: str,
    ) -> BikeDekhoScooter | None:
        normalized_brand_slug = self._normalize_slug(
            brand_slug,
            field_name="brand_slug",
        )

        normalized_model_slug = self._normalize_slug(
            model_slug,
            field_name="model_slug",
        )

        await self._connection.connect()

        collection = self._connection.collection(BIKEDEKHO_SCOOTERS_COLLECTION)

        document = await collection.find_one(
            {
                "brandSlug": (normalized_brand_slug),
                "slug": (normalized_model_slug),
            }
        )

        if document is None:
            return None

        return BikeDekhoScooter.model_validate(document)

    async def require_by_slugs(
        self,
        *,
        brand_slug: str,
        model_slug: str,
    ) -> BikeDekhoScooter:
        scooter = await self.get_by_slugs(
            brand_slug=brand_slug,
            model_slug=model_slug,
        )

        if scooter is None:
            raise LookupError(
                "BikeDekho scooter was not "
                "found: "
                f"brand={brand_slug!r}, "
                f"model={model_slug!r}"
            )

        return scooter

    async def get_by_scooter_slug(
        self,
        scooter_slug: str,
    ) -> BikeDekhoScooter | None:
        normalized_scooter_slug = self._normalize_slug(
            scooter_slug,
            field_name="scooter_slug",
        )

        await self._connection.connect()

        collection = self._connection.collection(BIKEDEKHO_SCOOTERS_COLLECTION)

        document = await collection.find_one(
            {
                "scooterSlug": (normalized_scooter_slug),
            }
        )

        if document is None:
            return None

        return BikeDekhoScooter.model_validate(document)

    async def require_by_scooter_slug(
        self,
        scooter_slug: str,
    ) -> BikeDekhoScooter:
        scooter = await self.get_by_scooter_slug(scooter_slug)

        if scooter is None:
            raise LookupError(
                "BikeDekho scooter was not "
                "found: "
                f"scooter_slug="
                f"{scooter_slug!r}"
            )

        return scooter

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

        collection = self._connection.collection(BIKEDEKHO_SCOOTERS_COLLECTION)

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        brand_slug: str | None = None,
        model_status: str | None = None,
    ) -> AsyncIterator[BikeDekhoScooter]:
        query: dict[str, Any] = {}

        if brand_slug is not None:
            query["brandSlug"] = self._normalize_slug(
                brand_slug,
                field_name="brand_slug",
            )

        if model_status is not None:
            query["modelStatus"] = self._normalize_model_status(model_status)

        await self._connection.connect()

        collection = self._connection.collection(BIKEDEKHO_SCOOTERS_COLLECTION)

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
            yield (BikeDekhoScooter.model_validate(document))

    async def list_all(
        self,
        *,
        brand_slug: str | None = None,
        model_status: str | None = None,
    ) -> list[BikeDekhoScooter]:
        scooters: list[BikeDekhoScooter] = []

        async for scooter in self.iter_all(
            brand_slug=brand_slug,
            model_status=model_status,
        ):
            scooters.append(scooter)

        return scooters

    async def delete_not_seen_in_run(
        self,
        *,
        run_id: str,
        brand_slug: str | None = None,
    ) -> int:
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

        collection = self._connection.collection(BIKEDEKHO_SCOOTERS_COLLECTION)

        result = await collection.delete_many(query)

        return result.deleted_count


bikedekho_scooter_repository = BikeDekhoScooterRepository()
