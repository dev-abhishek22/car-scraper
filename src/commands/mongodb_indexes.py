from __future__ import annotations

from typing import Any

from src.databases.mongodb import (
    mongo_connection,
)
from src.databases.mongodb_indexes import (
    ensure_mongodb_indexes,
)
from src.logger.logger import logger_service


async def run_mongodb_indexes() -> dict[str, Any]:
    """
    Create and verify all MongoDB indexes.

    This command is safe to run repeatedly.
    It does not delete collections or documents.
    """
    await mongo_connection.connect()

    try:
        created_indexes = await ensure_mongodb_indexes(
            connection=mongo_connection,
        )

        collection_summary = {
            collection_name: {
                "indexes": index_names,
                "totalIndexes": len(index_names),
            }
            for collection_name, index_names in created_indexes.items()
        }

        logger_service.info(
            (
                "MongoDB index initialization completed: "
                f"collections={len(collection_summary)}"
            ),
            context="MongoDBIndexesCommand",
        )

        return {
            "command": "mongodb-indexes",
            "status": "completed",
            "collections": collection_summary,
        }

    except Exception as error:
        logger_service.error(
            "MongoDB index initialization failed",
            exception=error,
            context="MongoDBIndexesCommand",
        )

        raise

    finally:
        await mongo_connection.close()
