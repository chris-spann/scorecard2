import sys
from unittest.mock import patch

import pytest
from pydantic import PostgresDsn

from app.core.config import Settings


class TestConfig:
    def test_throw_test_database_url_not_set(self):
        with patch.dict("sys.modules", {"pytest": None}), pytest.raises(Exception):
            Settings(
                DATABASE_URL=PostgresDsn(scheme="postgres", url="postgres://database_url:password@user/app"),  # type: ignore
                TEST_DATABASE_URL=None,
                ASYNC_DATABASE_URL=None,
                SECRET_KEY="secret",
            )

    def test_build_test_database_url(self):
        with patch.dict("sys.modules", {"pytest": None}):
            config = Settings(
                DATABASE_URL=PostgresDsn(scheme="postgres", url="postgres://database_url:password@user/app"),  # type: ignore
                TEST_DATABASE_URL=PostgresDsn(scheme="postgres", url="postgres://test_database_url:password@user/app"),  # type: ignore
                ASYNC_DATABASE_URL=None,
                SECRET_KEY="secret",
            )
            assert config.DATABASE_URL == "postgresql://test_database_url:password@user/app"

    def test_build_test_database_url_fallback(self):
        with patch.dict("sys.modules", {}):
            sys.modules.pop("pytest", None)
            config = Settings(
                DATABASE_URL=PostgresDsn(scheme="postgres", url="postgres://database_url:password@user/app"),  # type: ignore
                TEST_DATABASE_URL=PostgresDsn(scheme="postgres", url="postgres://test_database_url:password@user/app"),  # type: ignore
                ASYNC_DATABASE_URL=None,
                SECRET_KEY="secret",
            )
            assert config.DATABASE_URL == "postgresql://database_url:password@user/app"
