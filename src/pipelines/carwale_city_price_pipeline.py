from __future__ import annotations

import asyncio
import time
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from src.external.executors.carwale.city_price import (
    CarWaleCityPriceExecutor,
)
from src.logger.logger import logger_service
from src.models.carwale_city_price import (
    CarWaleCityPrice,
)
from src.models.carwale_city_price_job import (
    CarWaleCityPriceJob,
)
from src.repositories.carwale_city_price_repository import (
    CarWaleCityPriceRepository,
)


@dataclass(slots=True)
class CarWaleCityPricePipelineStats:
    produced: int = 0
    successful: int = 0
    failed: int = 0

    written: int = 0
    inserted: int = 0
    matched: int = 0
    modified: int = 0

    failure_samples: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(
        self,
        *,
        elapsed_seconds: float,
    ) -> dict[str, Any]:
        completed = self.successful + self.failed

        requests_per_second = 0.0

        if elapsed_seconds > 0:
            requests_per_second = completed / elapsed_seconds

        return {
            "produced": self.produced,
            "successful": self.successful,
            "failed": self.failed,
            "completed": completed,
            "written": self.written,
            "inserted": self.inserted,
            "matched": self.matched,
            "modified": self.modified,
            "elapsedSeconds": round(
                elapsed_seconds,
                2,
            ),
            "averageRequestsPerSecond": round(
                requests_per_second,
                2,
            ),
            "failureSamples": (self.failure_samples),
        }


class CarWaleCityPricePipeline:
    def __init__(
        self,
        *,
        executor: CarWaleCityPriceExecutor,
        repository: CarWaleCityPriceRepository,
        workers: int = 10,
        job_queue_size: int = 500,
        result_queue_size: int = 500,
        mongo_batch_size: int = 250,
        progress_interval: float = 10.0,
        failure_sample_limit: int = 50,
    ) -> None:
        if workers < 1:
            raise ValueError("workers must be at least 1")

        if job_queue_size < workers:
            raise ValueError("job_queue_size cannot be lower than workers")

        if result_queue_size < 1:
            raise ValueError("result_queue_size must be at least 1")

        if mongo_batch_size < 1:
            raise ValueError("mongo_batch_size must be at least 1")

        if progress_interval <= 0:
            raise ValueError("progress_interval must be greater than zero")

        self._executor = executor
        self._repository = repository

        self._workers = workers
        self._job_queue_size = job_queue_size
        self._result_queue_size = result_queue_size
        self._mongo_batch_size = mongo_batch_size
        self._progress_interval = progress_interval
        self._failure_sample_limit = failure_sample_limit

        self._stats = CarWaleCityPricePipelineStats()

    async def _produce(
        self,
        *,
        jobs: Iterable[CarWaleCityPriceJob],
        job_queue: asyncio.Queue[CarWaleCityPriceJob | None],
    ) -> None:
        try:
            for job in jobs:
                await job_queue.put(job)

                self._stats.produced += 1

        finally:
            for _ in range(self._workers):
                await job_queue.put(None)

    def _record_failure(
        self,
        *,
        job: CarWaleCityPriceJob,
        error: Exception,
    ) -> None:
        self._stats.failed += 1

        if len(self._stats.failure_samples) < self._failure_sample_limit:
            self._stats.failure_samples.append(
                {
                    "itemKey": job.item_key,
                    "versionId": (job.version_id),
                    "cityId": job.city_id,
                    "cityMaskingName": (job.city_masking_name),
                    "errorType": (type(error).__name__),
                    "errorMessage": str(error),
                }
            )

            logger_service.error(
                (f"CarWale city-price request failed: key={job.item_key}"),
                exception=error,
                context=("CarWaleCityPricePipeline"),
            )

        elif self._stats.failed % 1000 == 0:
            logger_service.warning(
                (f"CarWale city-price failures: count={self._stats.failed}"),
                context=("CarWaleCityPricePipeline"),
            )

    async def _worker(
        self,
        *,
        worker_number: int,
        job_queue: asyncio.Queue[CarWaleCityPriceJob | None],
        result_queue: asyncio.Queue[CarWaleCityPrice | None],
    ) -> None:
        while True:
            job = await job_queue.get()

            if job is None:
                await result_queue.put(None)
                return

            try:
                record = await self._executor.execute(job)

                await result_queue.put(record)

                self._stats.successful += 1

            except Exception as error:
                self._record_failure(
                    job=job,
                    error=error,
                )

                if self._stats.failed >= 10 and self._stats.successful == 0:
                    raise RuntimeError(
                        "The first 10 CarWale "
                        "city-price requests failed. "
                        "Stopping the pipeline."
                    ) from error

            if (self._stats.successful + self._stats.failed) % 10_000 == 0:
                logger_service.debug(
                    (f"CarWale city-price worker active: worker={worker_number}"),
                    context=("CarWaleCityPricePipeline"),
                )

    async def _flush_batch(
        self,
        batch: list[CarWaleCityPrice],
    ) -> None:
        if not batch:
            return

        result = await self._repository.bulk_upsert(batch)

        self._stats.written += result.processed
        self._stats.inserted += result.inserted
        self._stats.matched += result.matched
        self._stats.modified += result.modified

        batch.clear()

    async def _write_results(
        self,
        *,
        result_queue: asyncio.Queue[CarWaleCityPrice | None],
        completed_event: asyncio.Event,
    ) -> None:
        completed_workers = 0

        batch: list[CarWaleCityPrice] = []

        try:
            while completed_workers < self._workers:
                record = await result_queue.get()

                if record is None:
                    completed_workers += 1
                    continue

                batch.append(record)

                if len(batch) >= self._mongo_batch_size:
                    await self._flush_batch(batch)

            await self._flush_batch(batch)

        finally:
            completed_event.set()

    async def _report_progress(
        self,
        *,
        started_at: float,
        completed_event: asyncio.Event,
    ) -> None:
        while not completed_event.is_set():
            try:
                await asyncio.wait_for(
                    completed_event.wait(),
                    timeout=(self._progress_interval),
                )

            except TimeoutError:
                elapsed_seconds = time.monotonic() - started_at

                completed = self._stats.successful + self._stats.failed

                rate = 0.0

                if elapsed_seconds > 0:
                    rate = completed / elapsed_seconds

                logger_service.info(
                    (
                        "CarWale city-price progress: "
                        f"produced="
                        f"{self._stats.produced}, "
                        f"completed={completed}, "
                        f"successful="
                        f"{self._stats.successful}, "
                        f"failed="
                        f"{self._stats.failed}, "
                        f"written="
                        f"{self._stats.written}, "
                        f"average_rps={rate:.2f}"
                    ),
                    context=("CarWaleCityPricePipeline"),
                )

    async def run(
        self,
        jobs: Iterable[CarWaleCityPriceJob],
    ) -> dict[str, Any]:
        started_at = time.monotonic()

        job_queue: asyncio.Queue[CarWaleCityPriceJob | None] = asyncio.Queue(
            maxsize=self._job_queue_size
        )

        result_queue: asyncio.Queue[CarWaleCityPrice | None] = asyncio.Queue(
            maxsize=self._result_queue_size
        )

        completed_event = asyncio.Event()

        async with asyncio.TaskGroup() as group:
            group.create_task(
                self._produce(
                    jobs=jobs,
                    job_queue=job_queue,
                ),
                name=("carwale-city-price-producer"),
            )

            for worker_number in range(
                1,
                self._workers + 1,
            ):
                group.create_task(
                    self._worker(
                        worker_number=(worker_number),
                        job_queue=job_queue,
                        result_queue=(result_queue),
                    ),
                    name=(f"carwale-city-price-worker-{worker_number}"),
                )

            group.create_task(
                self._write_results(
                    result_queue=result_queue,
                    completed_event=(completed_event),
                ),
                name=("carwale-city-price-writer"),
            )

            group.create_task(
                self._report_progress(
                    started_at=started_at,
                    completed_event=(completed_event),
                ),
                name=("carwale-city-price-progress"),
            )

        elapsed_seconds = time.monotonic() - started_at

        return self._stats.to_dict(elapsed_seconds=elapsed_seconds)
