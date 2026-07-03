from __future__ import annotations

import asyncio
import re
import time
from collections.abc import AsyncIterable, AsyncIterator, Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any

from src.clients.client import (
    ExternalAccessDeniedError,
    ExternalClientError,
    ExternalJsonDecodeError,
    ExternalRateLimitError,
    ExternalResponseError,
)
from src.external.executors.carwale.city_price import CarWaleCityPriceExecutor
from src.logger.logger import logger_service
from src.models.carwale_city_price import CarWaleCityPrice
from src.models.carwale_city_price_failure import CarWaleCityPriceFailure
from src.models.carwale_city_price_job import CarWaleCityPriceJob
from src.repositories.carwale_city_price_failure_repository import (
    CarWaleCityPriceFailureRepository,
)
from src.repositories.carwale_city_price_repository import CarWaleCityPriceRepository
from src.repositories.carwale_city_price_run_repository import (
    CarWaleCityPriceRunRepository,
)

HTTP_STATUS_PATTERN = re.compile(r"\bstatus=(\d{3})\b")

RETRYABLE_HTTP_STATUS_CODES = {
    408,
    425,
    429,
    500,
    502,
    503,
    504,
}

STOP_REASON_ACCESS_DENIED = "external_access_denied"


@dataclass(slots=True)
class CarWaleCityPricePipelineStats:
    produced: int = 0
    skipped: int = 0
    successful: int = 0
    failed: int = 0
    written: int = 0
    inserted: int = 0
    matched: int = 0
    modified: int = 0
    failure_records_written: int = 0
    failure_samples: list[dict[str, Any]] = field(default_factory=list)

    @property
    def completed(self) -> int:
        return self.successful + self.failed

    def progress_dict(self) -> dict[str, int]:
        return {
            "produced": self.produced,
            "skipped": self.skipped,
            "successful": self.successful,
            "failed": self.failed,
            "written": self.written,
            "inserted": self.inserted,
            "matched": self.matched,
            "modified": self.modified,
            "failureRecordsWritten": (self.failure_records_written),
        }

    def to_dict(
        self,
        *,
        elapsed_seconds: float,
        stopped_early: bool,
        stop_reason: str | None,
        stop_http_status: int | None,
    ) -> dict[str, Any]:
        average_rps = 0.0

        if elapsed_seconds > 0:
            average_rps = self.completed / elapsed_seconds

        return {
            **self.progress_dict(),
            "completed": self.completed,
            "failureRecordsWritten": self.failure_records_written,
            "elapsedSeconds": round(elapsed_seconds, 2),
            "averageRequestsPerSecond": round(average_rps, 2),
            "stoppedEarly": stopped_early,
            "stopReason": stop_reason,
            "stopHttpStatus": stop_http_status,
            "failureSamples": self.failure_samples,
        }


class CarWaleCityPricePipeline:
    def __init__(
        self,
        *,
        executor: CarWaleCityPriceExecutor,
        repository: CarWaleCityPriceRepository,
        failure_repository: CarWaleCityPriceFailureRepository,
        run_repository: CarWaleCityPriceRunRepository,
        workers: int = 10,
        job_queue_size: int = 500,
        result_queue_size: int = 500,
        failure_queue_size: int = 500,
        mongo_batch_size: int = 250,
        failure_batch_size: int | None = None,
        resume_check_batch_size: int = 1_000,
        progress_interval: float = 10.0,
        failure_sample_limit: int = 50,
        retry_terminal_failures: bool = False,
    ) -> None:
        if workers < 1:
            raise ValueError("workers must be at least 1")
        if job_queue_size < workers:
            raise ValueError("job_queue_size cannot be lower than workers")
        if result_queue_size < 1:
            raise ValueError("result_queue_size must be at least 1")
        if failure_queue_size < 1:
            raise ValueError("failure_queue_size must be at least 1")
        if mongo_batch_size < 1:
            raise ValueError("mongo_batch_size must be at least 1")
        if resume_check_batch_size < 1:
            raise ValueError("resume_check_batch_size must be at least 1")
        if progress_interval <= 0:
            raise ValueError("progress_interval must be greater than zero")
        if failure_sample_limit < 0:
            raise ValueError("failure_sample_limit cannot be negative")

        # Persist every failed job immediately. Failures are normally rare,
        # and saving one-by-one prevents records from remaining only in memory.
        resolved_failure_batch_size = (
            1 if failure_batch_size is None else failure_batch_size
        )

        if resolved_failure_batch_size < 1:
            raise ValueError("failure_batch_size must be at least 1")

        self._executor = executor
        self._repository = repository
        self._failure_repository = failure_repository
        self._run_repository = run_repository
        self._workers = workers
        self._job_queue_size = job_queue_size
        self._result_queue_size = result_queue_size
        self._failure_queue_size = failure_queue_size
        self._mongo_batch_size = mongo_batch_size
        self._failure_batch_size = resolved_failure_batch_size
        self._resume_check_batch_size = resume_check_batch_size
        self._progress_interval = progress_interval
        self._failure_sample_limit = failure_sample_limit
        self._retry_terminal_failures = retry_terminal_failures
        self._stats = CarWaleCityPricePipelineStats()
        self._stop_reason: str | None = None
        self._stop_http_status: int | None = None
        self._access_denied_failure_recorded = False

    @property
    def stats(self) -> CarWaleCityPricePipelineStats:
        return self._stats

    @property
    def stop_reason(self) -> str | None:
        return self._stop_reason

    @property
    def stop_http_status(self) -> int | None:
        return self._stop_http_status

    def progress_snapshot(self) -> dict[str, int]:
        return self._stats.progress_dict()

    @staticmethod
    async def _iterate_jobs(
        jobs: Iterable[CarWaleCityPriceJob] | AsyncIterable[CarWaleCityPriceJob],
    ) -> AsyncIterator[CarWaleCityPriceJob]:
        if isinstance(jobs, AsyncIterable):
            async for job in jobs:
                yield job
            return

        for job in jobs:
            yield job

    @staticmethod
    def _extract_http_status(error: BaseException) -> int | None:
        match = HTTP_STATUS_PATTERN.search(str(error))

        if match is None:
            return None

        try:
            return int(match.group(1))
        except ValueError:
            return None

    @classmethod
    def _classify_failure(
        cls,
        error: BaseException,
    ) -> tuple[bool, int | None]:
        http_status = cls._extract_http_status(error)

        # Do not retry 403 immediately. Store it as retryable so a later
        # failed-only resume can retry it after the external block is gone.
        if isinstance(error, ExternalAccessDeniedError):
            return True, http_status or 403

        if isinstance(error, ExternalRateLimitError):
            return True, http_status or 429

        if http_status is not None:
            return http_status in RETRYABLE_HTTP_STATUS_CODES, http_status

        if isinstance(error, ExternalJsonDecodeError):
            return False, None

        if isinstance(error, ExternalResponseError):
            return False, None

        if isinstance(error, ExternalClientError):
            return True, None

        return False, None

    def _open_circuit_breaker(
        self,
        *,
        stop_event: asyncio.Event,
        reason: str,
        http_status: int | None,
    ) -> bool:
        if stop_event.is_set():
            return False

        self._stop_reason = reason
        self._stop_http_status = http_status
        stop_event.set()
        return True

    @staticmethod
    def _is_local_access_denied_rejection(
        error: ExternalAccessDeniedError,
    ) -> bool:
        return "access-denied circuit is open" in str(error).lower()

    async def _queue_candidate_batch(
        self,
        *,
        run_id: str,
        candidate_batch: Sequence[CarWaleCityPriceJob],
        job_queue: asyncio.Queue[CarWaleCityPriceJob | None],
        stop_event: asyncio.Event,
    ) -> None:
        if not candidate_batch or stop_event.is_set():
            return

        job_ids = [job.item_key for job in candidate_batch]
        completed_job_ids = await self._repository.get_completed_job_ids(
            job_ids=job_ids,
            run_id=run_id,
        )

        if stop_event.is_set():
            return

        terminal_job_ids: set[str] = set()

        if not self._retry_terminal_failures:
            terminal_job_ids = await self._failure_repository.get_terminal_job_ids(
                run_id=run_id,
                job_ids=job_ids,
            )

        for job in candidate_batch:
            if stop_event.is_set():
                return

            if job.item_key in completed_job_ids:
                self._stats.skipped += 1
                continue

            if job.item_key in terminal_job_ids:
                self._stats.skipped += 1
                continue

            await job_queue.put(job)
            self._stats.produced += 1

    async def _produce(
        self,
        *,
        run_id: str,
        jobs: Iterable[CarWaleCityPriceJob] | AsyncIterable[CarWaleCityPriceJob],
        job_queue: asyncio.Queue[CarWaleCityPriceJob | None],
        stop_event: asyncio.Event,
    ) -> None:
        candidate_batch: list[CarWaleCityPriceJob] = []
        signal_workers = False

        try:
            async for job in self._iterate_jobs(jobs):
                if stop_event.is_set():
                    break

                candidate_batch.append(job)

                if len(candidate_batch) < self._resume_check_batch_size:
                    continue

                await self._queue_candidate_batch(
                    run_id=run_id,
                    candidate_batch=candidate_batch,
                    job_queue=job_queue,
                    stop_event=stop_event,
                )
                candidate_batch.clear()

            if candidate_batch and not stop_event.is_set():
                await self._queue_candidate_batch(
                    run_id=run_id,
                    candidate_batch=candidate_batch,
                    job_queue=job_queue,
                    stop_event=stop_event,
                )
                candidate_batch.clear()

            signal_workers = True

        finally:
            # During Ctrl+C or a TaskGroup failure, all workers are cancelled
            # as well. Waiting to enqueue sentinels into a full queue would
            # deadlock because no worker would remain to consume them.
            if signal_workers:
                for _ in range(self._workers):
                    await job_queue.put(None)

    def _record_failure_sample(
        self,
        *,
        job: CarWaleCityPriceJob,
        error: BaseException,
        retryable: bool,
        http_status: int | None,
        access_denied: bool,
    ) -> None:
        if len(self._stats.failure_samples) < self._failure_sample_limit:
            self._stats.failure_samples.append(
                {
                    "itemKey": job.item_key,
                    "versionId": job.version_id,
                    "cityId": job.city_id,
                    "cityMaskingName": job.city_masking_name,
                    "errorType": type(error).__name__,
                    "errorMessage": str(error),
                    "httpStatus": http_status,
                    "retryable": retryable,
                }
            )

        if access_denied:
            return

        logger_service.error(
            (
                "CarWale city-price request failed: "
                f"key={job.item_key}, "
                f"version_id={job.version_id}, "
                f"city_id={job.city_id}, "
                f"city={job.city_masking_name}, "
                f"retryable={retryable}, "
                f"http_status={http_status}, "
                f"error_type={type(error).__name__}, "
                f"error={str(error).strip() or 'Unknown failure'}"
            ),
            context="CarWaleCityPricePipeline",
        )

    async def _worker(
        self,
        *,
        run_id: str,
        worker_number: int,
        job_queue: asyncio.Queue[CarWaleCityPriceJob | None],
        result_queue: asyncio.Queue[CarWaleCityPrice | None],
        failure_queue: asyncio.Queue[CarWaleCityPriceFailure | None],
        stop_event: asyncio.Event,
    ) -> None:
        while True:
            job = await job_queue.get()

            try:
                if job is None:
                    await result_queue.put(None)
                    await failure_queue.put(None)
                    return

                # A job already waiting in memory was not attempted. Discard
                # it from this process only; normal resume will regenerate it.
                if stop_event.is_set():
                    continue

                try:
                    record = await self._executor.execute(job)
                    await result_queue.put(record)
                    self._stats.successful += 1

                except ExternalAccessDeniedError as error:
                    retryable, http_status = self._classify_failure(error)
                    local_rejection = self._is_local_access_denied_rejection(error)

                    opened = self._open_circuit_breaker(
                        stop_event=stop_event,
                        reason=STOP_REASON_ACCESS_DENIED,
                        http_status=http_status or 403,
                    )

                    if opened:
                        logger_service.error(
                            (
                                "CarWale access denied. The global "
                                "circuit breaker is open. New requests "
                                "will stop and MongoDB queues will flush."
                            ),
                            exception=error,
                            context="CarWaleCityPricePipeline",
                        )

                    # Only the request that actually received the remote
                    # 401/403 is a failure. Workers rejected locally after
                    # the HTTP client's circuit opens were never attempted
                    # and must remain pending for normal resume.
                    if not local_rejection and not self._access_denied_failure_recorded:
                        self._access_denied_failure_recorded = True

                        failure = CarWaleCityPriceFailure.create(
                            run_id=run_id,
                            job=job,
                            error=error,
                            retryable=retryable,
                            http_status=http_status,
                        )
                        await failure_queue.put(failure)
                        self._stats.failed += 1

                        self._record_failure_sample(
                            job=job,
                            error=error,
                            retryable=retryable,
                            http_status=http_status,
                            access_denied=True,
                        )

                    continue

                except Exception as error:
                    retryable, http_status = self._classify_failure(error)

                    failure = CarWaleCityPriceFailure.create(
                        run_id=run_id,
                        job=job,
                        error=error,
                        retryable=retryable,
                        http_status=http_status,
                    )
                    await failure_queue.put(failure)
                    self._stats.failed += 1

                    self._record_failure_sample(
                        job=job,
                        error=error,
                        retryable=retryable,
                        http_status=http_status,
                        access_denied=False,
                    )

                if self._stats.completed > 0 and self._stats.completed % 10_000 == 0:
                    logger_service.debug(
                        (f"CarWale city-price worker active: worker={worker_number}"),
                        context="CarWaleCityPricePipeline",
                    )

            finally:
                job_queue.task_done()

    async def _flush_result_batch(
        self,
        *,
        run_id: str,
        batch: list[CarWaleCityPrice],
    ) -> None:
        if not batch:
            return

        job_ids = [record.document_id for record in batch]
        result = await self._repository.bulk_upsert(
            batch,
            run_id=run_id,
        )

        self._stats.written += result.processed
        self._stats.inserted += result.inserted
        self._stats.matched += result.matched
        self._stats.modified += result.modified

        try:
            await self._failure_repository.mark_resolved(
                run_id=run_id,
                job_ids=job_ids,
            )
        except Exception as error:
            logger_service.warning(
                (
                    "City-price records were saved, but matching failures "
                    "could not be marked resolved: "
                    f"run_id={run_id}, count={len(job_ids)}"
                ),
                context="CarWaleCityPricePipeline",
            )
            logger_service.error(
                "Failure resolution update failed",
                exception=error,
                context="CarWaleCityPricePipeline",
            )

        batch.clear()

    async def _flush_failure_batch(
        self,
        *,
        batch: list[CarWaleCityPriceFailure],
    ) -> None:
        if not batch:
            return

        result = await self._failure_repository.bulk_upsert(batch)
        self._stats.failure_records_written += result.processed
        batch.clear()

    @staticmethod
    def _drain_result_queue(
        *,
        result_queue: asyncio.Queue[CarWaleCityPrice | None],
        batch: list[CarWaleCityPrice],
    ) -> None:
        while True:
            try:
                record = result_queue.get_nowait()
            except asyncio.QueueEmpty:
                return

            try:
                if record is not None:
                    batch.append(record)
            finally:
                result_queue.task_done()

    @staticmethod
    def _drain_failure_queue(
        *,
        failure_queue: asyncio.Queue[CarWaleCityPriceFailure | None],
        batch: list[CarWaleCityPriceFailure],
    ) -> None:
        while True:
            try:
                failure = failure_queue.get_nowait()
            except asyncio.QueueEmpty:
                return

            try:
                if failure is not None:
                    batch.append(failure)
            finally:
                failure_queue.task_done()

    async def _flush_all_results(
        self,
        *,
        run_id: str,
        batch: list[CarWaleCityPrice],
    ) -> None:
        while batch:
            current_batch = batch[: self._mongo_batch_size]
            current_batch_size = len(current_batch)
            await asyncio.shield(
                self._flush_result_batch(
                    run_id=run_id,
                    batch=current_batch,
                )
            )
            del batch[:current_batch_size]

    async def _flush_all_failures(
        self,
        *,
        batch: list[CarWaleCityPriceFailure],
    ) -> None:
        while batch:
            current_batch = batch[: self._failure_batch_size]
            current_batch_size = len(current_batch)
            await asyncio.shield(self._flush_failure_batch(batch=current_batch))
            del batch[:current_batch_size]

    async def _write_results(
        self,
        *,
        run_id: str,
        result_queue: asyncio.Queue[CarWaleCityPrice | None],
        completed_event: asyncio.Event,
    ) -> None:
        completed_workers = 0
        batch: list[CarWaleCityPrice] = []

        try:
            while completed_workers < self._workers:
                record = await result_queue.get()

                try:
                    if record is None:
                        completed_workers += 1
                        continue

                    batch.append(record)

                    if len(batch) >= self._mongo_batch_size:
                        await self._flush_result_batch(
                            run_id=run_id,
                            batch=batch,
                        )
                finally:
                    result_queue.task_done()

        finally:
            try:
                self._drain_result_queue(
                    result_queue=result_queue,
                    batch=batch,
                )
                await self._flush_all_results(
                    run_id=run_id,
                    batch=batch,
                )
            finally:
                completed_event.set()

    async def _write_failures(
        self,
        *,
        failure_queue: asyncio.Queue[CarWaleCityPriceFailure | None],
        completed_event: asyncio.Event,
    ) -> None:
        completed_workers = 0
        batch: list[CarWaleCityPriceFailure] = []

        try:
            while completed_workers < self._workers:
                failure = await failure_queue.get()

                try:
                    if failure is None:
                        completed_workers += 1
                        continue

                    batch.append(failure)

                    if len(batch) >= self._failure_batch_size:
                        await self._flush_failure_batch(batch=batch)
                finally:
                    failure_queue.task_done()

        finally:
            try:
                self._drain_failure_queue(
                    failure_queue=failure_queue,
                    batch=batch,
                )
                await self._flush_all_failures(batch=batch)
            finally:
                completed_event.set()

    async def _report_progress(
        self,
        *,
        run_id: str,
        started_at: float,
        result_writer_completed: asyncio.Event,
        failure_writer_completed: asyncio.Event,
    ) -> None:
        while True:
            if result_writer_completed.is_set() and failure_writer_completed.is_set():
                return

            try:
                await asyncio.wait_for(
                    asyncio.gather(
                        result_writer_completed.wait(),
                        failure_writer_completed.wait(),
                    ),
                    timeout=self._progress_interval,
                )
            except TimeoutError:
                elapsed_seconds = time.monotonic() - started_at
                average_rps = 0.0

                if elapsed_seconds > 0:
                    average_rps = self._stats.completed / elapsed_seconds

                await self._run_repository.update_progress(
                    run_id,
                    progress=self.progress_snapshot(),
                )

                logger_service.info(
                    (
                        "CarWale city-price progress: "
                        f"run_id={run_id}, "
                        f"produced={self._stats.produced}, "
                        f"skipped={self._stats.skipped}, "
                        f"completed={self._stats.completed}, "
                        f"successful={self._stats.successful}, "
                        f"failed={self._stats.failed}, "
                        f"written={self._stats.written}, "
                        "failure_records="
                        f"{self._stats.failure_records_written}, "
                        f"average_rps={average_rps:.2f}"
                    ),
                    context="CarWaleCityPricePipeline",
                )

    async def run(
        self,
        jobs: Iterable[CarWaleCityPriceJob] | AsyncIterable[CarWaleCityPriceJob],
        *,
        run_id: str,
    ) -> dict[str, Any]:
        normalized_run_id = run_id.strip()

        if not normalized_run_id:
            raise ValueError("run_id cannot be empty")

        self._stats = CarWaleCityPricePipelineStats()
        self._stop_reason = None
        self._stop_http_status = None
        self._access_denied_failure_recorded = False

        started_at = time.monotonic()
        stop_event = asyncio.Event()

        job_queue: asyncio.Queue[CarWaleCityPriceJob | None] = asyncio.Queue(
            maxsize=self._job_queue_size
        )
        result_queue: asyncio.Queue[CarWaleCityPrice | None] = asyncio.Queue(
            maxsize=self._result_queue_size
        )
        failure_queue: asyncio.Queue[CarWaleCityPriceFailure | None] = asyncio.Queue(
            maxsize=self._failure_queue_size
        )

        result_writer_completed = asyncio.Event()
        failure_writer_completed = asyncio.Event()

        async with asyncio.TaskGroup() as group:
            group.create_task(
                self._produce(
                    run_id=normalized_run_id,
                    jobs=jobs,
                    job_queue=job_queue,
                    stop_event=stop_event,
                ),
                name="carwale-city-price-producer",
            )

            for worker_number in range(1, self._workers + 1):
                group.create_task(
                    self._worker(
                        run_id=normalized_run_id,
                        worker_number=worker_number,
                        job_queue=job_queue,
                        result_queue=result_queue,
                        failure_queue=failure_queue,
                        stop_event=stop_event,
                    ),
                    name=(f"carwale-city-price-worker-{worker_number}"),
                )

            group.create_task(
                self._write_results(
                    run_id=normalized_run_id,
                    result_queue=result_queue,
                    completed_event=result_writer_completed,
                ),
                name="carwale-city-price-result-writer",
            )
            group.create_task(
                self._write_failures(
                    failure_queue=failure_queue,
                    completed_event=failure_writer_completed,
                ),
                name="carwale-city-price-failure-writer",
            )
            group.create_task(
                self._report_progress(
                    run_id=normalized_run_id,
                    started_at=started_at,
                    result_writer_completed=result_writer_completed,
                    failure_writer_completed=failure_writer_completed,
                ),
                name="carwale-city-price-progress",
            )

        elapsed_seconds = time.monotonic() - started_at

        await self._run_repository.update_progress(
            normalized_run_id,
            progress=self.progress_snapshot(),
        )

        return self._stats.to_dict(
            elapsed_seconds=elapsed_seconds,
            stopped_early=self._stop_reason is not None,
            stop_reason=self._stop_reason,
            stop_http_status=self._stop_http_status,
        )
