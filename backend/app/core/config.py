import sys
from typing import Any, Optional

from pydantic import BaseSettings, HttpUrl, PostgresDsn, validator
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "Scorecard 2"

    SENTRY_DSN: HttpUrl | None = None

    API_PATH: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    # The following variables need to be defined in environment

    TEST_DATABASE_URL: Optional[PostgresDsn]
    DATABASE_URL: PostgresDsn
    ASYNC_DATABASE_URL: Optional[PostgresDsn]

    @validator("DATABASE_URL", pre=True)
    def build_test_database_url(cls, v: Optional[str], values: dict[str, Any]):
        """Overrides DATABASE_URL with TEST_DATABASE_URL in test environment."""
        url = v
        if "pytest" in sys.modules:
            if not values.get("TEST_DATABASE_URL"):
                raise Exception("pytest detected, but TEST_DATABASE_URL is not set in environment")
            url = values["TEST_DATABASE_URL"]
        if url:
            return url.replace("postgres://", "postgresql://")
        return url  # pragma: no cover

    @validator("ASYNC_DATABASE_URL")
    def build_async_database_url(cls, v: Optional[str], values: dict[str, Any]):
        """Builds ASYNC_DATABASE_URL from DATABASE_URL."""
        if "DATABASE_URL" in values:
            v = values["DATABASE_URL"]
            return v.replace("postgresql", "postgresql+asyncpg", 1) if v else v
        return  # pragma: no cover

    SECRET_KEY: str


settings = Settings.parse_obj({})
