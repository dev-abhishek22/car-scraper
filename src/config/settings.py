from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    APP_NAME: str = "car-api-scraper"
    APP_ENV: Literal[
        "development",
        "test",
        "production",
    ] = "development"

    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: str = "logs"
    SQL_LOGGING: bool = False

    # MySQL
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USERNAME: str
    DB_PASSWORD: SecretStr
    DB_DATABASE: str

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 5
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # MongoDB
    MONGO_URI: SecretStr | None = None
    MONGO_DATABASE: str = "car_api_scraper"

    MONGO_MIN_POOL_SIZE: int = 1
    MONGO_MAX_POOL_SIZE: int = 20

    MONGO_SERVER_SELECTION_TIMEOUT_MS: int = 5_000
    MONGO_CONNECT_TIMEOUT_MS: int = 10_000
    MONGO_SOCKET_TIMEOUT_MS: int = 30_000
    MONGO_WAIT_QUEUE_TIMEOUT_MS: int = 10_000

    # External APIs
    API_TIMEOUT: float = 30
    API_MAX_RETRIES: int = 3

    DATA_RETENTION_DAYS: int = 7

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def mongo_uri(self) -> str:
        if self.MONGO_URI is None:
            raise ValueError("MONGO_URI is not configured")

        uri = self.MONGO_URI.get_secret_value().strip()

        if not uri:
            raise ValueError("MONGO_URI cannot be empty")

        return uri

    @property
    def mongo_database(self) -> str:
        database = self.MONGO_DATABASE.strip()

        if not database:
            raise ValueError("MONGO_DATABASE cannot be empty")

        return database


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
