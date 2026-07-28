from __future__ import annotations

from typing import Any

from src.commands.bikedekho_brands import run_bikedekho_brands


async def run_bikedekho_scooter_brands() -> dict[str, Any]:
    return await run_bikedekho_brands(vehicle_type="scooters")
