from __future__ import annotations

from typing import Any

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from src.config.settings import settings
from src.logger.logger import logger_service

MongoDocument = dict[str, Any]


class MongoConnection:
    def __init__(self) -> None:
        self._client: AsyncMongoClient[MongoDocument] | None = None

        self._database: AsyncDatabase[MongoDocument] | None = None

    async def connect(self) -> None:
        if self._client is not None:
            return

        client = AsyncMongoClient[MongoDocument](
            settings.mongo_uri,
            appname=settings.APP_NAME,
            minPoolSize=settings.MONGO_MIN_POOL_SIZE,
            maxPoolSize=settings.MONGO_MAX_POOL_SIZE,
            serverSelectionTimeoutMS=(settings.MONGO_SERVER_SELECTION_TIMEOUT_MS),
            connectTimeoutMS=(settings.MONGO_CONNECT_TIMEOUT_MS),
            socketTimeoutMS=(settings.MONGO_SOCKET_TIMEOUT_MS),
            waitQueueTimeoutMS=(settings.MONGO_WAIT_QUEUE_TIMEOUT_MS),
            retryReads=True,
            retryWrites=True,
            tz_aware=True,
        )

        try:
            await client.admin.command("ping")

        except Exception:
            await client.close()
            raise

        self._client = client
        self._database = client[settings.mongo_database]

        logger_service.info(
            (f"MongoDB connected successfully: database={settings.mongo_database}"),
            context="MongoDB",
        )

    @property
    def client(
        self,
    ) -> AsyncMongoClient[MongoDocument]:
        if self._client is None:
            raise RuntimeError("MongoDB is not connected")

        return self._client

    @property
    def database(
        self,
    ) -> AsyncDatabase[MongoDocument]:
        if self._database is None:
            raise RuntimeError("MongoDB is not connected")

        return self._database

    def collection(
        self,
        name: str,
    ) -> AsyncCollection[MongoDocument]:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Collection name cannot be empty")

        return self.database[normalized_name]

    async def ping(self) -> dict[str, Any]:
        await self.connect()

        result = await self.client.admin.command("ping")

        return dict(result)

    async def close(self) -> None:
        if self._client is None:
            return

        await self._client.close()

        self._client = None
        self._database = None

        logger_service.info(
            "MongoDB connection closed",
            context="MongoDB",
        )


mongo_connection = MongoConnection()
