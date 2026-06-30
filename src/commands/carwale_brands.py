from __future__ import annotations

from typing import Any

from src.external.executors.carwale.brands import (
    CarWaleBrandsExecutor,
)
from src.external.executors.carwale.client_factory import (
    create_carwale_client,
)
from src.storage.json_storage import JsonStorage


def run_carwale_brands(
    *,
    page_id: int = 2,
    platform_id: int = 1,
    show_request: bool = False,
    save_request: bool = False,
    include_sensitive_request_data: bool = False,
) -> dict[str, Any]:
    request_file = (
        "data/raw/carwale/requests/brands_request.json" if save_request else None
    )

    with create_carwale_client() as client:
        executor = CarWaleBrandsExecutor(
            client=client,
        )

        make_list = executor.execute(
            page_id=page_id,
            platform_id=platform_id,
            show_request=show_request,
            request_log_file=request_file,
            include_sensitive_request_data=(include_sensitive_request_data),
        )

    files = JsonStorage.save(
        directory="data/raw/carwale",
        file_name="brands",
        data=make_list,
    )

    return {
        "command": "carwale-brands",
        "brands_count": len(make_list),
        "output_file": str(files["latest_file"]),
        "archive_file": (str(files["archive_file"]) if files["archive_file"] else None),
        "request_file": request_file,
    }
