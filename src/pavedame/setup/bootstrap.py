from functools import lru_cache

from fastapi import FastAPI

from pavedame.presentation.common.exc_handler import ExceptionHandler
from pavedame.setup.config.settings import AppConfig


@lru_cache(maxsize=1)
def setup_config() -> AppConfig:
    return AppConfig()

def setup_exc_handler(app: FastAPI) -> None:
    exc = ExceptionHandler(app)
    exc.setup_exception_handler()
