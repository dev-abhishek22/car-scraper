from src.clients.client import ExternalHttpClient
from src.external.constants.carwale import (
    CARWALE_BASE_URL,
    CARWALE_DEFAULT_HEADERS,
)
from user_agents import choose_user_agent


def create_carwale_client() -> ExternalHttpClient:
    user_agent = choose_user_agent(
        category="CHROME_USER_AGENTS",
    )

    return ExternalHttpClient(
        base_url=CARWALE_BASE_URL,
        user_agent=user_agent,
        default_headers=CARWALE_DEFAULT_HEADERS,
        cookies={
            "CurrentLanguage": "en",
        },
        min_request_interval=2.0,
        max_retries=3,
    )
