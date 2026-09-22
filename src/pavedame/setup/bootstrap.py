from functools import lru_cache

from fastapi import FastAPI

from pavedame.infrastructure.persistence.models import map_auth_session_table, map_user_table
from pavedame.presentation.common.exc_handler import ExceptionHandler
from pavedame.presentation.routes.auth.handlers import auth_router
from pavedame.setup.config.settings import AppConfig


@lru_cache(maxsize=1)
def setup_config() -> AppConfig:
    return AppConfig()

def setup_exc_handler(app: FastAPI) -> None:
    exc = ExceptionHandler(app)
    exc.setup_exception_handler()

def setup_map_configs() -> None:
    map_auth_session_table()
    map_user_table()

def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
