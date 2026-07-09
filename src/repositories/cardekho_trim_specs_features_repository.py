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
from src.models.cardekho_trim_specs_features import (
    CarDekhoTrimSpecsFeatures,
)

CARDEKHO_TRIM_SPECS_FEATURES_COLLECTION = "cardekho_trim_specs_features"


@dataclass(
    frozen=True,
    slots=True,
)
class TrimSpecsFeaturesUpsertResult:
    trim_specs_features: CarDekhoTrimSpecsFeatures
    matched: int
    modified: int
    inserted: int

    def to_dict(
        self,
    ) -> dict[str, Any]:
        return {
            "documentId": (self.trim_specs_features.document_id),
            "variantId": (self.trim_specs_features.variant_id),
            "brandId": (self.trim_specs_features.brand_id),
            "modelId": (self.trim_specs_features.model_id),
            "matched": self.matched,
            "modified": self.modified,
            "inserted": self.inserted,
        }


class CarDekhoTrimSpecsFeaturesRepository:
    def __init__(
        self,
        connection: MongoConnection = (mongo_connection),
    ) -> None:
        self._connection = connection

    @staticmethod
    def _validate_positive_integer(
        value: int,
        *,
        field_name: str,
    ) -> int:
        if (
            isinstance(
                value,
                bool,
            )
            or not isinstance(
                value,
                int,
            )
            or value <= 0
        ):
            raise ValueError(f"{field_name} must be a positive integer")

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

    async def upsert_one(
        self,
        *,
        variant_record: Mapping[str, Any],
        response_data: Mapping[str, Any],
        run_id: str,
    ) -> TrimSpecsFeaturesUpsertResult:
        normalized_run_id = self._normalize_run_id(run_id)

        trim_specs_features = CarDekhoTrimSpecsFeatures.create(
            variant_record=variant_record,
            response_data=response_data,
            run_id=normalized_run_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

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
                "Cardekho trim specs/features "
                "document was upserted but "
                "could not be read back: "
                f"_id="
                f"{trim_specs_features.document_id}"
            )

        stored_trim_specs_features = CarDekhoTrimSpecsFeatures.model_validate(
            stored_document
        )

        return TrimSpecsFeaturesUpsertResult(
            trim_specs_features=(stored_trim_specs_features),
            matched=(update_result.matched_count),
            modified=(update_result.modified_count),
            inserted=(1 if update_result.upserted_id is not None else 0),
        )

    async def get_by_variant_id(
        self,
        variant_id: int,
    ) -> CarDekhoTrimSpecsFeatures | None:
        normalized_variant_id = self._validate_positive_integer(
            variant_id,
            field_name="variant_id",
        )

        document_id = CarDekhoTrimSpecsFeatures.build_document_id(
            variant_id=(normalized_variant_id),
        )

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        document = await collection.find_one(
            {
                "_id": document_id,
            }
        )

        if document is None:
            return None

        return CarDekhoTrimSpecsFeatures.model_validate(document)

    async def require_by_variant_id(
        self,
        variant_id: int,
    ) -> CarDekhoTrimSpecsFeatures:
        trim_specs_features = await self.get_by_variant_id(variant_id)

        if trim_specs_features is None:
            raise LookupError(
                "Cardekho trim "
                "specs/features document "
                "was not found: "
                f"variant_id={variant_id}"
            )

        return trim_specs_features

    async def exists_by_variant_id(
        self,
        variant_id: int,
    ) -> bool:
        normalized_variant_id = self._validate_positive_integer(
            variant_id,
            field_name="variant_id",
        )

        document_id = CarDekhoTrimSpecsFeatures.build_document_id(
            variant_id=(normalized_variant_id),
        )

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        document = await collection.find_one(
            {
                "_id": document_id,
            },
            {
                "_id": 1,
            },
        )

        return document is not None

    async def get_existing_variant_ids(
        self,
        variant_ids: Sequence[int],
    ) -> set[int]:
        if not variant_ids:
            return set()

        normalized_variant_ids: list[int] = []

        seen_variant_ids: set[int] = set()

        for variant_id in variant_ids:
            normalized_variant_id = self._validate_positive_integer(
                variant_id,
                field_name="variant_id",
            )

            if normalized_variant_id in seen_variant_ids:
                continue

            seen_variant_ids.add(normalized_variant_id)

            normalized_variant_ids.append(normalized_variant_id)

        document_ids = [
            (
                CarDekhoTrimSpecsFeatures.build_document_id(
                    variant_id=variant_id,
                )
            )
            for variant_id in normalized_variant_ids
        ]

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        cursor = collection.find(
            {
                "_id": {
                    "$in": document_ids,
                },
            },
            {
                "_id": 1,
                "variantId": 1,
            },
        )

        existing_variant_ids: set[int] = set()

        async for document in cursor:
            variant_id = document.get("variantId")

            if (
                isinstance(
                    variant_id,
                    int,
                )
                and not isinstance(
                    variant_id,
                    bool,
                )
                and variant_id > 0
            ):
                existing_variant_ids.add(variant_id)

        return existing_variant_ids

    async def count(
        self,
        *,
        brand_id: int | None = None,
        model_id: int | None = None,
    ) -> int:
        query: dict[str, Any] = {}

        if brand_id is not None:
            query["brandId"] = self._validate_positive_integer(
                brand_id,
                field_name="brand_id",
            )

        if model_id is not None:
            query["modelId"] = self._validate_positive_integer(
                model_id,
                field_name="model_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        brand_id: int | None = None,
        model_id: int | None = None,
    ) -> AsyncIterator[CarDekhoTrimSpecsFeatures]:
        query: dict[str, Any] = {}

        if brand_id is not None:
            query["brandId"] = self._validate_positive_integer(
                brand_id,
                field_name="brand_id",
            )

        if model_id is not None:
            query["modelId"] = self._validate_positive_integer(
                model_id,
                field_name="model_id",
            )

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        cursor = collection.find(query).sort(
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
                    "variantName",
                    1,
                ),
                (
                    "variantId",
                    1,
                ),
            ]
        )

        async for document in cursor:
            yield (CarDekhoTrimSpecsFeatures.model_validate(document))

    async def delete_by_variant_id(
        self,
        variant_id: int,
    ) -> int:
        normalized_variant_id = self._validate_positive_integer(
            variant_id,
            field_name="variant_id",
        )

        document_id = CarDekhoTrimSpecsFeatures.build_document_id(
            variant_id=(normalized_variant_id),
        )

        await self._connection.connect()

        collection = self._connection.collection(
            CARDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        result = await collection.delete_one(
            {
                "_id": document_id,
            }
        )

        return result.deleted_count


cardekho_trim_specs_features_repository = CarDekhoTrimSpecsFeaturesRepository()
