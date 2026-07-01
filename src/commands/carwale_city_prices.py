from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipelines.carwale_city_price_pipeline import (
    CarWaleCityPricePipeline,
)
from src.databases.mongodb import (
    mongo_connection,
)
from src.external.executors.carwale.async_client_factory import (
    create_carwale_async_client,
)
from src.external.executors.carwale.city_price import (
    CarWaleCityPriceExecutor,
)
from src.external.executors.carwale.city_price_jobs import (
    iter_carwale_city_price_jobs,
)
from src.repositories.carwale_city_price_repository import (
    carwale_city_price_repository,
)

DEFAULT_CARS_DIRECTORY = Path("data/raw/carwale/car")

DEFAULT_CITIES_FILE = Path("data/raw/carwale/cities.json")


async def run_carwale_city_prices(
    *,
    cars_directory: str | Path = (DEFAULT_CARS_DIRECTORY),
    cities_file: str | Path = (DEFAULT_CITIES_FILE),
    brand: str | None = None,
    model: str | None = None,
    city: str | None = None,
    workers: int = 5,
    requests_per_second: float = 2.0,
    mongo_batch_size: int = 100,
    max_jobs: int | None = None,
) -> dict[str, Any]:
    jobs = iter_carwale_city_price_jobs(
        cars_directory=cars_directory,
        cities_file=cities_file,
        selected_brand=brand,
        selected_model=model,
        selected_city=city,
        max_jobs=max_jobs,
    )

    try:
        await mongo_connection.connect()

        async with create_carwale_async_client(
            concurrency=workers,
            requests_per_second=(requests_per_second),
        ) as client:
            executor = CarWaleCityPriceExecutor(client)

            pipeline = CarWaleCityPricePipeline(
                executor=executor,
                repository=(carwale_city_price_repository),
                workers=workers,
                job_queue_size=max(
                    workers * 20,
                    100,
                ),
                result_queue_size=max(
                    workers * 20,
                    100,
                ),
                mongo_batch_size=(mongo_batch_size),
                progress_interval=10.0,
            )

            summary = await pipeline.run(jobs)

            return {
                "command": ("carwale-city-prices"),
                "brand": brand,
                "model": model,
                "city": city,
                "workers": workers,
                "requestsPerSecond": (requests_per_second),
                "mongoBatchSize": (mongo_batch_size),
                "maxJobs": max_jobs,
                "carsDirectory": str(Path(cars_directory)),
                "citiesFile": str(Path(cities_file)),
                "httpMetrics": (client.metrics_snapshot()),
                **summary,
            }

    finally:
        await mongo_connection.close()
