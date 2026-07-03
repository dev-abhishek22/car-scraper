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
from src.models.carwale_model import (
    CarWaleModel,
)


CARWALE_MODELS_COLLECTION = "carwale_models"


@dataclass(frozen=True, slots=True)
class ModelBulkUpsertResult:
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


class CarWaleModelRepository:
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
    def _normalize_masking_name(
        value: str,
        *,
        field_name: str,
    ) -> str:
        normalized_value = value.strip().lower()

        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        return normalized_value

    async def bulk_upsert(
        self,
        *,
        brand: Mapping[str, Any],
        models: Sequence[Mapping[str, Any]],
        run_id: str,
        source_brand_run_id: str | None = None,
    ) -> ModelBulkUpsertResult:
        """
        Upsert every model returned for one CarWale brand.

        Existing models are updated in place. New models are
        inserted. Models missing from the response are not
        deleted automatically.
        """
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
            CarWaleModel,
        ] = {}

        for model_data in models:
            model = CarWaleModel.create(
                brand=brand,
                model=model_data,
                run_id=normalized_run_id,
                source_brand_run_id=(normalized_source_brand_run_id),
            )

            deduplicated_models[model.document_id] = model

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_MODELS_COLLECTION)

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
    ) -> CarWaleModel:
        normalized_run_id = self._normalize_run_id(run_id)

        normalized_source_brand_run_id = self._normalize_optional_run_id(
            source_brand_run_id
        )

        model = CarWaleModel.create(
            brand=brand,
            model=model_data,
            run_id=normalized_run_id,
            source_brand_run_id=(normalized_source_brand_run_id),
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_MODELS_COLLECTION)

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
                "CarWale model was upserted but could "
                "not be read back: "
                f"_id={model.document_id}"
            )

        return CarWaleModel.model_validate(stored_document)

    async def get_by_ids(
        self,
        *,
        make_id: int,
        model_id: int,
    ) -> CarWaleModel | None:
        normalized_make_id = self._validate_positive_integer(
            make_id,
            field_name="make_id",
        )

        normalized_model_id = self._validate_positive_integer(
            model_id,
            field_name="model_id",
        )

        document_id = CarWaleModel.build_document_id(
            make_id=normalized_make_id,
            model_id=normalized_model_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_MODELS_COLLECTION)

        document = await collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return CarWaleModel.model_validate(document)

    async def require_by_ids(
        self,
        *,
        make_id: int,
        model_id: int,
    ) -> CarWaleModel:
        model = await self.get_by_ids(
            make_id=make_id,
            model_id=model_id,
        )

        if model is None:
            raise LookupError(
                f"CarWale model was not found: make_id={make_id}, model_id={model_id}"
            )

        return model

    async def get_by_masking_names(
        self,
        *,
        make_masking_name: str,
        model_masking_name: str,
    ) -> CarWaleModel | None:
        normalized_make_masking_name = self._normalize_masking_name(
            make_masking_name,
            field_name="make_masking_name",
        )

        normalized_model_masking_name = self._normalize_masking_name(
            model_masking_name,
            field_name="model_masking_name",
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_MODELS_COLLECTION)

        document = await collection.find_one(
            {
                "makeMaskingName": (normalized_make_masking_name),
                "modelMaskingName": (normalized_model_masking_name),
            }
        )

        if document is None:
            return None

        return CarWaleModel.model_validate(document)

    async def require_by_masking_names(
        self,
        *,
        make_masking_name: str,
        model_masking_name: str,
    ) -> CarWaleModel:
        model = await self.get_by_masking_names(
            make_masking_name=(make_masking_name),
            model_masking_name=(model_masking_name),
        )

        if model is None:
            raise LookupError(
                "CarWale model was not found: "
                f"make={make_masking_name!r}, "
                f"model={model_masking_name!r}"
            )

        return model

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

        collection = self._connection.collection(CARWALE_MODELS_COLLECTION)

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        make_id: int | None = None,
    ) -> AsyncIterator[CarWaleModel]:
        query: dict[str, Any] = {}

        if make_id is not None:
            query["makeId"] = self._validate_positive_integer(
                make_id,
                field_name="make_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_MODELS_COLLECTION)

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
            yield CarWaleModel.model_validate(document)

    async def list_all(
        self,
        *,
        make_id: int | None = None,
    ) -> list[CarWaleModel]:
        models: list[CarWaleModel] = []

        async for model in self.iter_all(make_id=make_id):
            models.append(model)

        return models

    async def get_model_ids(
        self,
        *,
        make_id: int | None = None,
    ) -> set[tuple[int, int]]:
        query: dict[str, Any] = {}

        if make_id is not None:
            query["makeId"] = self._validate_positive_integer(
                make_id,
                field_name="make_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_MODELS_COLLECTION)

        cursor = collection.find(
            query,
            {
                "_id": 0,
                "makeId": 1,
                "modelId": 1,
            },
        )

        model_ids: set[tuple[int, int]] = set()

        async for document in cursor:
            stored_make_id = document.get("makeId")

            stored_model_id = document.get("modelId")

            if (
                isinstance(stored_make_id, int)
                and not isinstance(
                    stored_make_id,
                    bool,
                )
                and stored_make_id > 0
                and isinstance(stored_model_id, int)
                and not isinstance(
                    stored_model_id,
                    bool,
                )
                and stored_model_id > 0
            ):
                model_ids.add(
                    (
                        stored_make_id,
                        stored_model_id,
                    )
                )

        return model_ids

    async def delete_not_seen_for_make(
        self,
        *,
        make_id: int,
        run_id: str,
    ) -> int:
        """
        Delete models for one make that were not seen in
        the specified run.

        Do not call this automatically unless the model API
        response for this make completed successfully and is
        known to contain the complete model list.
        """
        normalized_make_id = self._validate_positive_integer(
            make_id,
            field_name="make_id",
        )

        normalized_run_id = self._normalize_run_id(run_id)

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_MODELS_COLLECTION)

        result = await collection.delete_many(
            {
                "makeId": normalized_make_id,
                "lastRunId": {
                    "$ne": normalized_run_id,
                },
            }
        )

        return result.deleted_count


carwale_model_repository = CarWaleModelRepository()
