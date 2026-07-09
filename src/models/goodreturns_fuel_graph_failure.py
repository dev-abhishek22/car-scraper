from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class GoodReturnsFuelGraphFailure:
    run_id: str
    city_id: int
    city_name: str
    city_slug: str
    fuel_type: str
    timeframe: str
    page_url: str | None
    error_type: str
    error_message: str
    http_status: int | None = None
    retryable: bool = True
    attempts: int = 1
    source: str = "goodreturns"
    status: str = "failed"
    first_failed_at: datetime = field(default_factory=utc_now)
    last_failed_at: datetime = field(default_factory=utc_now)
    resolved_at: datetime | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    @property
    def id(self) -> str:
        return f"{self.run_id}:{self.source}:{self.fuel_type}:{self.city_slug}:{self.timeframe}"

    def to_mongo(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "runId": self.run_id,
            "source": self.source,
            "cityId": self.city_id,
            "cityName": self.city_name,
            "citySlug": self.city_slug,
            "fuelType": self.fuel_type,
            "timeframe": self.timeframe,
            "pageUrl": self.page_url,
            "status": self.status,
            "httpStatus": self.http_status,
            "errorType": self.error_type,
            "errorMessage": self.error_message,
            "retryable": self.retryable,
            "attempts": self.attempts,
            "firstFailedAt": self.first_failed_at,
            "lastFailedAt": self.last_failed_at,
            "resolvedAt": self.resolved_at,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }
