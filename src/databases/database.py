import logging
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config.settings import settings
from src.logger.logger import SQLAlchemyHandler, logger_service


DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD.get_secret_value(),
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_DATABASE,
)


engine = create_engine(
    DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,
    echo=False,
)


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def configure_sql_logging() -> None:
    if not settings.SQL_LOGGING:
        return

    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")

    has_sqlalchemy_handler = any(
        isinstance(handler, SQLAlchemyHandler) for handler in sqlalchemy_logger.handlers
    )

    if not has_sqlalchemy_handler:
        sqlalchemy_logger.addHandler(SQLAlchemyHandler())

    sqlalchemy_logger.setLevel(logging.INFO)
    sqlalchemy_logger.propagate = False


configure_sql_logging()


@contextmanager
def db_session() -> Iterator[Session]:
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def db_connection() -> None:
    try:
        with engine.connect() as connection:
            result = connection.scalar(text("SELECT 1"))

        if result != 1:
            raise RuntimeError("Unexpected database health-check result")

        logger_service.info(
            "Database connected successfully",
            context="Database",
        )

    except Exception as error:
        logger_service.error(
            "Database connection failed",
            exception=error,
            context="Database",
        )
        raise
