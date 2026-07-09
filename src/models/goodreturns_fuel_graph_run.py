from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class GoodReturnsFuelGraphRun:
    run_id: str
    timeframe: str
    fuel_types: list[str]
    total: int
    queued: int
    skipped: int = 0
    success: int = 0
    failed: int = 0
    refresh_existing: bool = False
    has_static_token: bool = False
    source: str = "goodreturns"
    type: str = "fuel_graph_prices"
    status: str = "running"
    started_at: datetime = field(default_factory=utc_now)
    finished_at: datetime | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    @property
    def id(self) -> str:
        return self.run_id

    def to_mongo(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "source": self.source,
            "type": self.type,
            "status": self.status,
            "timeframe": self.timeframe,
            "fuelTypes": self.fuel_types,
            "total": self.total,
            "queued": self.queued,
            "skipped": self.skipped,
            "success": self.success,
            "failed": self.failed,
            "refreshExisting": self.refresh_existing,
            "hasStaticToken": self.has_static_token,
            "startedAt": self.started_at,
            "finishedAt": self.finished_at,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }
