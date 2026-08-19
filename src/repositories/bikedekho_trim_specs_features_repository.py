from __future__ import annotations

from collections.abc import AsyncIterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.databases.mongodb import (
    MongoConnection,
    mongo_connection,
)
from src.models.bikedekho_trim_specs_features import (
    BikeDekhoTrimSpecsFeatures,
)

BIKEDEKHO_TRIM_SPECS_FEATURES_COLLECTION = "bikedekho_trim_specs_features"


@dataclass(
    frozen=True,
    slots=True,
)
class TrimSpecsFeaturesUpsertResult:
    trim_specs_features: BikeDekhoTrimSpecsFeatures
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


class BikeDekhoTrimSpecsFeaturesRepository:
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
    def _normalize_optional_string(
        value: Any,
    ) -> str | None:
        if not isinstance(
            value,
            str,
        ):
            return None

        normalized_value = value.strip()

        return normalized_value or None

    async def upsert_one(
        self,
        *,
        variant_record: Mapping[str, Any],
        response_data: Mapping[str, Any],
        run_id: str,
    ) -> TrimSpecsFeaturesUpsertResult:
        normalized_run_id = self._normalize_run_id(run_id)

        if not isinstance(
            variant_record,
            Mapping,
        ):
            raise ValueError("variant_record must be an object")

        if not isinstance(
            response_data,
            Mapping,
        ):
            raise ValueError("response_data must be an object")

        trim_specs_features = BikeDekhoTrimSpecsFeatures.create(
            variant_record=variant_record,
            response_data=response_data,
            run_id=normalized_run_id,
        )

        await self._connection.connect()

        collection = self._connection.collection(
            BIKEDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        document = trim_specs_features.to_mongo_document()

        existing_document = await collection.find_one(
            {
                "_id": (trim_specs_features.document_id),
            },
            {
                "_id": 0,
                "createdAt": 1,
            },
        )

        if isinstance(
            existing_document,
            Mapping,
        ) and isinstance(
            existing_document.get("createdAt"),
            datetime,
        ):
            document["createdAt"] = existing_document["createdAt"]

        result = await collection.replace_one(
            {
                "_id": (trim_specs_features.document_id),
            },
            document,
            upsert=True,
        )

        stored_document = await collection.find_one(
            {
                "_id": (trim_specs_features.document_id),
            }
        )

        if stored_document is None:
            raise RuntimeError(
                "BikeDekho trim specs/features "
                "document was upserted but could not "
                "be read back: "
                f"_id={trim_specs_features.document_id}"
            )

        stored_trim_specs_features = BikeDekhoTrimSpecsFeatures.model_validate(
            stored_document
        )

        return TrimSpecsFeaturesUpsertResult(
            trim_specs_features=(stored_trim_specs_features),
            matched=result.matched_count,
            modified=result.modified_count,
            inserted=(1 if result.upserted_id is not None else 0),
        )

    async def exists_by_variant_id(
        self,
        variant_id: int,
    ) -> bool:
        normalized_variant_id = self._validate_positive_integer(
            variant_id,
            field_name="variant_id",
        )

        await self._connection.connect()

        collection = self._connection.collection(
            BIKEDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        document = await collection.find_one(
            {
                "variantId": normalized_variant_id,
            },
            {
                "_id": 1,
            },
        )

        return document is not None

    async def get_by_variant_id(
        self,
        variant_id: int,
    ) -> BikeDekhoTrimSpecsFeatures | None:
        normalized_variant_id = self._validate_positive_integer(
            variant_id,
            field_name="variant_id",
        )

        await self._connection.connect()

        collection = self._connection.collection(
            BIKEDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        document = await collection.find_one(
            {
                "variantId": normalized_variant_id,
            }
        )

        if document is None:
            return None

        return BikeDekhoTrimSpecsFeatures.model_validate(document)

    async def require_by_variant_id(
        self,
        variant_id: int,
    ) -> BikeDekhoTrimSpecsFeatures:
        trim_specs_features = await self.get_by_variant_id(variant_id)

        if trim_specs_features is None:
            raise LookupError(
                "BikeDekho trim specs/features "
                "document was not found: "
                f"variant_id={variant_id}"
            )

        return trim_specs_features

    async def get_by_slugs(
        self,
        *,
        brand_slug: str,
        model_slug: str,
        variant_slug: str,
    ) -> BikeDekhoTrimSpecsFeatures | None:
        normalized_brand_slug = self._normalize_required_slug(
            brand_slug,
            field_name="brand_slug",
        )

        normalized_model_slug = self._normalize_required_slug(
            model_slug,
            field_name="model_slug",
        )

        normalized_variant_slug = self._normalize_required_slug(
            variant_slug,
            field_name="variant_slug",
        )

        await self._connection.connect()

        collection = self._connection.collection(
            BIKEDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        document = await collection.find_one(
            {
                "brandSlug": normalized_brand_slug,
                "modelSlug": normalized_model_slug,
                "variantSlug": normalized_variant_slug,
            }
        )

        if document is None:
            return None

        return BikeDekhoTrimSpecsFeatures.model_validate(document)

    async def require_by_slugs(
        self,
        *,
        brand_slug: str,
        model_slug: str,
        variant_slug: str,
    ) -> BikeDekhoTrimSpecsFeatures:
        trim_specs_features = await self.get_by_slugs(
            brand_slug=brand_slug,
            model_slug=model_slug,
            variant_slug=variant_slug,
        )

        if trim_specs_features is None:
            raise LookupError(
                "BikeDekho trim specs/features "
                "document was not found: "
                f"brand={brand_slug!r}, "
                f"model={model_slug!r}, "
                f"variant={variant_slug!r}"
            )

        return trim_specs_features

    async def count(
        self,
        *,
        brand_slug: str | None = None,
        model_slug: str | None = None,
        model_id: int | None = None,
        variant_status: str | None = None,
    ) -> int:
        query: dict[str, Any] = {}

        if brand_slug is not None:
            query["brandSlug"] = self._normalize_required_slug(
                brand_slug,
                field_name="brand_slug",
            )

        if model_slug is not None:
            query["modelSlug"] = self._normalize_required_slug(
                model_slug,
                field_name="model_slug",
            )

        if model_id is not None:
            query["modelId"] = self._validate_positive_integer(
                model_id,
                field_name="model_id",
            )

        if variant_status is not None:
            normalized_variant_status = self._normalize_optional_string(variant_status)

            if normalized_variant_status is not None:
                query["variantStatus"] = normalized_variant_status.upper()

        await self._connection.connect()

        collection = self._connection.collection(
            BIKEDEKHO_TRIM_SPECS_FEATURES_COLLECTION
        )

        return await collection.count_documents(query)

    async def iter_all(
        self,
        *,
        brand_slug: str | None = None,
        model_slug: str | None = None,
        model_id: int | None = None,
        variant_status: str | None = None,
    ) -> AsyncIterator[BikeDekhoTrimSpecsFeatures]:
        query: dict[str, Any] = {}

        if brand_slug is not None:
            query["brandSlug"] = self._normalize_required_slug(
                brand_slug,
                field_name="brand_slug",
            )

        if model_slug is not None:
            query["modelSlug"] = self._normalize_required_slug(
                model_slug,
                field_name="model_slug",
            )

        if model_id is not None:
            query["modelId"] = self._validate_positive_integer(
                model_id,
                field_name="model_id",
            )

        if variant_status is not None:
            normalized_variant_status = self._normalize_optional_string(variant_status)

            if normalized_variant_status is not None:
                query["variantStatus"] = normalized_variant_status.upper()

        await self._connection.connect()

        collection = self._connection.collection(
            BIKEDEKHO_TRIM_SPECS_FEATURES_COLLECTION
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
            yield (BikeDekhoTrimSpecsFeatures.model_validate(document))

    async def list_all(
        self,
        *,
        brand_slug: str | None = None,
        model_slug: str | None = None,
        model_id: int | None = None,
        variant_status: str | None = None,
    ) -> list[BikeDekhoTrimSpecsFeatures]:
        trim_specs_features: list[BikeDekhoTrimSpecsFeatures] = []

        async for item in self.iter_all(
            brand_slug=brand_slug,
            model_slug=model_slug,
            model_id=model_id,
            variant_status=variant_status,
        ):
            trim_specs_features.append(item)

        return trim_specs_features

    @staticmethod
    def _normalize_required_slug(
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


bikedekho_trim_specs_features_repository = BikeDekhoTrimSpecsFeaturesRepository()
