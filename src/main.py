from src.databases.database import db_connection
from src.logger.logger import logger_service


def main() -> None:
    db_connection()

    logger_service.info(
        "Application initialized",
        context="Main",
    )


if __name__ == "__main__":
    main()
