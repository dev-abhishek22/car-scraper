from __future__ import annotations

from src.databases.mongodb import MongoConnection, mongo_connection
from src.repositories.bikedekho_model_repository import BikeDekhoModelRepository


BIKEDEKHO_SCOOTER_MODELS_COLLECTION = "bikedekho_scooter_models"


class BikeDekhoScooterModelRepository(BikeDekhoModelRepository):
    """Persist scooter models independently from motorcycle models."""

    def __init__(self, connection: MongoConnection = mongo_connection) -> None:
        super().__init__(
            connection=connection,
            collection_name=BIKEDEKHO_SCOOTER_MODELS_COLLECTION,
        )


bikedekho_scooter_model_repository = BikeDekhoScooterModelRepository()
