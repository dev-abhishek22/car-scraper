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
from src.models.cardekho_model import (
    CarDekhoModel,
)

CARDEKHO_MODELS_COLLECTION = "cardekho_models"


@dataclass(
    frozen=True,
    slots=True,
)
class ModelBulkUpsertResult:
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


class CarDekhoModelRepository:
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
    def _normalize_optional_run_id(
        run_id: str | None,
    ) -> str | None:
        if run_id is None:
            return None

        normalized_run_id = run_id.strip()

        return normalized_run_id or None

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
                "model_status must be CURRENT, " "UPCOMING, or DISCONTINUED"
            )

        return normalized_status

    async def bulk_upsert(
        self,
        *,
        brand: Mapping[str, Any],
        models: Sequence[Mapping[str, Any]],
        run_id: str,
        source_brand_run_id: str | None = None,
    ) -> ModelBulkUpsertResult:
        if not models:
            return ModelBulkUpsertResult(
                received=0,
                processed=0,
                matched=0,
                modified=0,
                inserted=0,
            )

        normalized_run_id = self._normalize_run_id(run_id)

        normalized_source_brand_run_id = self._normalize_optional_run_id(
            source_brand_run_id
        )

        deduplicated_models: dict[
            str,
            CarDekhoModel,
        ] = {}

        for model_data in models:
            model = CarDekhoModel.create(
                brand=brand,
                model=model_data,
                run_id=normalized_run_id,
                source_brand_run_id=(normalized_source_brand_run_id),
            )

            deduplicated_models[model.document_id] = model

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_MODELS_COLLECTION)

        operations: list[UpdateOne] = []

        for model in deduplicated_models.values():
            document = model.to_mongo_document()

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
                        "_id": model.document_id,
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

        return ModelBulkUpsertResult(
            received=len(models),
            processed=len(operations),
            matched=result.matched_count,
            modified=result.modified_count,
            inserted=result.upserted_count,
        )

    async def upsert_one(
        self,
        *,
        brand: Mapping[str, Any],
        model_data: Mapping[str, Any],
        run_id: str,
        source_brand_run_id: str | None = None,
    ) -> CarDekhoModel:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_source_brand_run_id = self._normalize_optional_run_id(
            source_brand_run_id
        )

        model = CarDekhoModel.create(
            brand=brand,
            model=model_data,
            run_id=normalized_run_id,
            source_brand_run_id=(normalized_source_brand_run_id),
        )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_MODELS_COLLECTION)

        document = model.to_mongo_document()

        document.pop(
            "_id",
            None,
        )

        created_at = document.pop(
            "createdAt",
            model.created_at,
        )

        await collection.update_one(
            {
                "_id": model.document_id,
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
                "_id": model.document_id,
            }
        )

        if stored_document is None:
            raise RuntimeError(
                "CarDekho model was upserted but "
                "could not be read back: "
                f"_id={model.document_id}"
            )

        return CarDekhoModel.model_validate(stored_document)

    async def get_by_model_id(
        self,
        model_id: int,
    ) -> CarDekhoModel | None:
        normalized_model_id = self._validate_positive_integer(
            model_id,
            field_name="model_id",
        )

        document_id = CarDekhoModel.build_document_id(normalized_model_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_MODELS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return CarDekhoModel.model_validate(document)

    async def require_by_model_id(
        self,
        model_id: int,
    ) -> CarDekhoModel:
        model = await self.get_by_model_id(model_id)

        if model is None:
            raise LookupError("CarDekho model was not found: " f"model_id={model_id}")

        return model

    async def get_by_slugs(
        self,
        *,
        brand_slug: str,
        model_slug: str,
    ) -> CarDekhoModel | None:
        normalized_brand_slug = self._normalize_slug(
            brand_slug,
            field_name="brand_slug",
        )

        normalized_model_slug = self._normalize_slug(
            model_slug,
            field_name="model_slug",
        )

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_MODELS_COLLECTION)

        document = await collection.find_one(
            {
                "brandSlug": (normalized_brand_slug),
                "slug": (normalized_model_slug),
            }
        )

        if document is None:
            return None

        return CarDekhoModel.model_validate(document)

    async def require_by_slugs(
        self,
        *,
        brand_slug: str,
        model_slug: str,
    ) -> CarDekhoModel:
        model = await self.get_by_slugs(
            brand_slug=brand_slug,
            model_slug=model_slug,
        )

        if model is None:
            raise LookupError(
                "CarDekho model was not found: "
                f"brand={brand_slug!r}, "
                f"model={model_slug!r}"
            )

        return model

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

        collection = self._connection.collection(CARDEKHO_MODELS_COLLECTION)

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        brand_slug: str | None = None,
        model_status: str | None = None,
    ) -> AsyncIterator[CarDekhoModel]:
        query: dict[str, Any] = {}

        if brand_slug is not None:
            query["brandSlug"] = self._normalize_slug(
                brand_slug,
                field_name="brand_slug",
            )

        if model_status is not None:
            query["modelStatus"] = self._normalize_model_status(model_status)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_MODELS_COLLECTION)

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
            yield CarDekhoModel.model_validate(document)

    async def list_all(
        self,
        *,
        brand_slug: str | None = None,
        model_status: str | None = None,
    ) -> list[CarDekhoModel]:
        models: list[CarDekhoModel] = []

        async for model in self.iter_all(
            brand_slug=brand_slug,
            model_status=model_status,
        ):
            models.append(model)

        return models

    async def get_model_ids(
        self,
        *,
        brand_slug: str | None = None,
        model_status: str | None = None,
    ) -> set[int]:
        query: dict[str, Any] = {}

        if brand_slug is not None:
            query["brandSlug"] = self._normalize_slug(
                brand_slug,
                field_name="brand_slug",
            )

        if model_status is not None:
            query["modelStatus"] = self._normalize_model_status(model_status)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_MODELS_COLLECTION)

        cursor = collection.find(
            query,
            {
                "_id": 0,
                "id": 1,
            },
        )

        model_ids: set[int] = set()

        async for document in cursor:
            model_id = document.get("id")

            if (
                isinstance(model_id, int)
                and not isinstance(model_id, bool)
                and model_id > 0
            ):
                model_ids.add(model_id)

        return model_ids

    async def delete_not_seen_for_brand(
        self,
        *,
        brand_slug: str,
        run_id: str,
    ) -> int:
        normalized_brand_slug = self._normalize_slug(
            brand_slug,
            field_name="brand_slug",
        )

        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARDEKHO_MODELS_COLLECTION)

        result = await collection.delete_many(
            {
                "brandSlug": (normalized_brand_slug),
                "lastRunId": {
                    "$ne": normalized_run_id,
                },
            }
        )

        return result.deleted_count


cardekho_model_repository = CarDekhoModelRepository()
