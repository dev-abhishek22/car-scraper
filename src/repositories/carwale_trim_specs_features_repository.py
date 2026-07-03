from __future__ import annotations

from collections.abc import (
    AsyncIterator,
    Mapping,
    Sequence,
)
from dataclasses import dataclass
from typing import Any

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.carwale_trim_specs_features import (
    CarWaleTrimSpecsFeatures,
)

CARWALE_TRIM_SPECS_FEATURES_COLLECTION = "carwale_trim_specs_features"


@dataclass(frozen=True, slots=True)
class TrimSpecsFeaturesUpsertResult:
    trim_specs_features: CarWaleTrimSpecsFeatures
    matched: int
    modified: int
    inserted: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "documentId": (self.trim_specs_features.document_id),
            "versionId": (self.trim_specs_features.version_id),
            "trimId": (self.trim_specs_features.trim_id),
            "makeId": (self.trim_specs_features.make_id),
            "modelId": (self.trim_specs_features.model_id),
            "matched": self.matched,
            "modified": self.modified,
            "inserted": self.inserted,
        }


class CarWaleTrimSpecsFeaturesRepository:
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

    async def upsert_one(
        self,
        *,
        version_record: Mapping[str, Any],
        response_data: Mapping[str, Any],
        run_id: str,
    ) -> TrimSpecsFeaturesUpsertResult:
        normalized_run_id = self._normalize_run_id(run_id)

        trim_specs_features = CarWaleTrimSpecsFeatures.create(
            version_record=version_record,
            response_data=response_data,
            run_id=normalized_run_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_TRIM_SPECS_FEATURES_COLLECTION)

        document = trim_specs_features.to_mongo_document()

        document.pop(
            "_id",
            None,
        )

        created_at = document.pop(
            "createdAt",
            trim_specs_features.created_at,
        )

        update_result = await collection.update_one(
            {
                "_id": (trim_specs_features.document_id),
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
                "_id": (trim_specs_features.document_id),
            }
        )

        if stored_document is None:
            raise RuntimeError(
                "CarWale trim specs/features "
                "document was upserted but could "
                "not be read back: "
                f"_id={trim_specs_features.document_id}"
            )

        stored_trim_specs_features = CarWaleTrimSpecsFeatures.model_validate(
            stored_document
        )

        return TrimSpecsFeaturesUpsertResult(
            trim_specs_features=(stored_trim_specs_features),
            matched=update_result.matched_count,
            modified=update_result.modified_count,
            inserted=(1 if update_result.upserted_id is not None else 0),
        )

    async def get_by_version_id(
        self,
        version_id: int,
    ) -> CarWaleTrimSpecsFeatures | None:
        normalized_version_id = self._validate_positive_integer(
            version_id,
            field_name="version_id",
        )

        document_id = CarWaleTrimSpecsFeatures.build_document_id(
            version_id=normalized_version_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_TRIM_SPECS_FEATURES_COLLECTION)

        document = await collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return CarWaleTrimSpecsFeatures.model_validate(document)

    async def require_by_version_id(
        self,
        version_id: int,
    ) -> CarWaleTrimSpecsFeatures:
        trim_specs_features = await self.get_by_version_id(version_id)

        if trim_specs_features is None:
            raise LookupError(
                "CarWale trim specs/features "
                "document was not found: "
                f"version_id={version_id}"
            )

        return trim_specs_features

    async def exists_by_version_id(
        self,
        version_id: int,
    ) -> bool:
        normalized_version_id = self._validate_positive_integer(
            version_id,
            field_name="version_id",
        )

        document_id = CarWaleTrimSpecsFeatures.build_document_id(
            version_id=normalized_version_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_TRIM_SPECS_FEATURES_COLLECTION)

        document = await collection.find_one(
            {
                "_id": document_id,
            },
            {
                "_id": 1,
            },
        )

        return document is not None

    async def get_existing_version_ids(
        self,
        version_ids: Sequence[int],
    ) -> set[int]:
        if not version_ids:
            return set()

        normalized_version_ids: list[int] = []
        seen_version_ids: set[int] = set()

        for version_id in version_ids:
            normalized_version_id = self._validate_positive_integer(
                version_id,
                field_name="version_id",
            )

            if normalized_version_id in seen_version_ids:
                continue

            seen_version_ids.add(normalized_version_id)

            normalized_version_ids.append(normalized_version_id)

        document_ids = [
            CarWaleTrimSpecsFeatures.build_document_id(
                version_id=version_id,
            )
            for version_id in normalized_version_ids
        ]

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_TRIM_SPECS_FEATURES_COLLECTION)

        cursor = collection.find(
            {
                "_id": {
                    "$in": document_ids,
                },
            },
            {
                "_id": 1,
                "versionId": 1,
            },
        )

        existing_version_ids: set[int] = set()

        async for document in cursor:
            version_id = document.get("versionId")

            if (
                isinstance(version_id, int)
                and not isinstance(
                    version_id,
                    bool,
                )
                and version_id > 0
            ):
                existing_version_ids.add(version_id)

        return existing_version_ids

    async def count(
        self,
        *,
        make_id: int | None = None,
        model_id: int | None = None,
        trim_id: int | None = None,
    ) -> int:
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

        if trim_id is not None:
            query["trimId"] = self._validate_positive_integer(
                trim_id,
                field_name="trim_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_TRIM_SPECS_FEATURES_COLLECTION)

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        make_id: int | None = None,
        model_id: int | None = None,
        trim_id: int | None = None,
    ) -> AsyncIterator[CarWaleTrimSpecsFeatures]:
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

        if trim_id is not None:
            query["trimId"] = self._validate_positive_integer(
                trim_id,
                field_name="trim_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_TRIM_SPECS_FEATURES_COLLECTION)

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
                    "trimName",
                    1,
                ),
                (
                    "versionId",
                    1,
                ),
            ]
        )

        async for document in cursor:
            yield (CarWaleTrimSpecsFeatures.model_validate(document))

    async def delete_by_version_id(
        self,
        version_id: int,
    ) -> int:
        normalized_version_id = self._validate_positive_integer(
            version_id,
            field_name="version_id",
        )

        document_id = CarWaleTrimSpecsFeatures.build_document_id(
            version_id=normalized_version_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(CARWALE_TRIM_SPECS_FEATURES_COLLECTION)

        result = await collection.delete_one(
            {
                "_id": document_id,
            }
        )

        return result.deleted_count


carwale_trim_specs_features_repository = CarWaleTrimSpecsFeaturesRepository()
