import logging
import sys
from pathlib import Path

from loguru import logger

from src.config.settings import settings


class SQLAlchemyHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            try:
                level: str | int = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            logger.bind(context="SQL").opt(
                exception=record.exc_info,
                depth=6,
            ).log(
                level,
                record.getMessage(),
            )
        except Exception:
            self.handleError(record)


class LoggerService:
    def __init__(self) -> None:
        log_directory = Path(settings.LOG_DIR)
        http_log_directory = log_directory / "http"

        log_directory.mkdir(parents=True, exist_ok=True)
        http_log_directory.mkdir(parents=True, exist_ok=True)

        logger.remove()
        logger.configure(
            extra={
                "context": "APP",
            }
        )

        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra[context]: <20}</cyan> | "
            "<level>{message}</level>"
        )

        file_format = (
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{extra[context]: <20} | "
            "{message}"
        )

        logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL,
            colorize=True,
            format=console_format,
            enqueue=True,
            backtrace=settings.is_development,
            diagnose=settings.is_development,
        )

        logger.add(
            log_directory / "app-{time:YYYY-MM-DD}.log",
            level="INFO",
            format=file_format,
            rotation="20 MB",
            retention="7 days",
            compression="zip",
            enqueue=True,
            backtrace=settings.is_development,
            diagnose=settings.is_development,
        )

        logger.add(
            log_directory / "error-{time:YYYY-MM-DD}.log",
            level="ERROR",
            format=file_format,
            rotation="20 MB",
            retention="14 days",
            compression="zip",
            enqueue=True,
            backtrace=settings.is_development,
            diagnose=settings.is_development,
        )

        logger.add(
            http_log_directory / "http-{time:YYYY-MM-DD}.log",
            level="INFO",
            format=file_format,
            rotation="20 MB",
            retention="7 days",
            compression="zip",
            enqueue=True,
            filter=lambda record: record["extra"].get("context") == "HTTP",
        )

    def info(
        self,
        message: str,
        context: str = "APP",
    ) -> None:
        logger.bind(context=context).info(message)

    def warning(
        self,
        message: str,
        context: str = "APP",
    ) -> None:
        logger.bind(context=context).warning(message)

    def debug(
        self,
        message: str,
        context: str = "APP",
    ) -> None:
        logger.bind(context=context).debug(message)

    def error(
        self,
        message: str,
        *,
        exception: BaseException | None = None,
        context: str = "APP",
    ) -> None:
        bound_logger = logger.bind(context=context)

        if exception is not None:
            bound_logger.opt(exception=exception).error(message)
            return

        bound_logger.error(message)

    def log_http_request(self, message: str) -> None:
        logger.bind(context="HTTP").info(message)


logger_service = LoggerService()
