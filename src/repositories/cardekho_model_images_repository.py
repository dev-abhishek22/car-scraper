from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from pymongo import ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection

from src.databases.mongodb import mongo_connection
from src.models.cardekho_model_images import CarDekhoModelImages


CARDEKHO_MODEL_IMAGES_COLLECTION = "cardekho_model_images"


class CarDekhoModelImagesRepository:
    def _collection(self) -> AsyncCollection:
        return mongo_connection.collection(
            CARDEKHO_MODEL_IMAGES_COLLECTION,
        )

    async def exists_by_model_id(
        self,
        model_id: int,
    ) -> bool:
        document = await self._collection().find_one(
            {
                "_id": CarDekhoModelImages.build_document_id(
                    model_id,
                ),
            },
            {
                "_id": 1,
            },
        )

        return document is not None

    async def upsert_one(
        self,
        *,
        model: dict[str, Any],
        images_data: list[dict[str, Any]],
        title: str,
        run_id: str,
    ) -> CarDekhoModelImages:
        existing_document = await self._collection().find_one(
            {
                "_id": CarDekhoModelImages.build_document_id(
                    model["modelId"],
                ),
            },
        )

        created_at = None

        if existing_document is not None:
            created_at = existing_document.get("createdAt")

        document = CarDekhoModelImages.create(
            model=model,
            images_data=images_data,
            title=title,
            run_id=run_id,
            created_at=created_at,
        )

        stored_document = await self._collection().find_one_and_replace(
            {
                "_id": document.document_id,
            },
            document.to_mongo_document(),
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        if stored_document is None:
            raise RuntimeError(
                "Failed to upsert CarDekho model images document: "
                f"{document.document_id}"
            )

        return CarDekhoModelImages.model_validate(
            stored_document,
        )

    async def get_by_model_id(
        self,
        model_id: int,
    ) -> CarDekhoModelImages | None:
        document = await self._collection().find_one(
            {
                "_id": CarDekhoModelImages.build_document_id(
                    model_id,
                ),
            },
        )

        if document is None:
            return None

        return CarDekhoModelImages.model_validate(
            document,
        )

    async def require_by_model_id(
        self,
        model_id: int,
    ) -> CarDekhoModelImages:
        document = await self.get_by_model_id(
            model_id,
        )

        if document is None:
            raise LookupError(
                "CarDekho model images document not found: "
                f"model_id={model_id}"
            )

        return document

    async def get_by_model_slug(
        self,
        model_slug: str,
    ) -> CarDekhoModelImages | None:
        document = await self._collection().find_one(
            {
                "modelSlug": model_slug,
            },
        )

        if document is None:
            return None

        return CarDekhoModelImages.model_validate(
            document,
        )

    async def count(self) -> int:
        return await self._collection().count_documents({})

    async def iter_all(
        self,
    ) -> Iterator[CarDekhoModelImages]:
        cursor = self._collection().find({})

        async for document in cursor:
            yield CarDekhoModelImages.model_validate(
                document,
            )

    async def list_all(
        self,
    ) -> list[CarDekhoModelImages]:
        return [
            document
            async for document in self.iter_all()
        ]


cardekho_model_images_repository = CarDekhoModelImagesRepository()
