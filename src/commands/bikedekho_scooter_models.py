from __future__ import annotations

from typing import Any

from src.commands.bikedekho_models import run_bikedekho_models


async def run_bikedekho_scooter_models(**kwargs: Any) -> dict[str, Any]:
    return await run_bikedekho_models(vehicle_type="scooters", **kwargs)
