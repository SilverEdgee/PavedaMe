from dataclasses import dataclass
from types import MappingProxyType

from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse

from pavedame.application.errors import (
    AlreadyAuthenticatedError,
    AuthenticationError,
    AuthorizationError,
    UserAlreadyExistsError,
)
from pavedame.infrastructure.errors import EntityAddError, GatewayError, InfrastructureError, RollbackError


@dataclass(frozen=True, slots=True)
class ExceptionSchema:
    description: str


class ExceptionHandler:
    _ERROR_MAPPING: MappingProxyType[type[Exception], int] = MappingProxyType(
        {
            AuthenticationError: status.HTTP_401_UNAUTHORIZED,
            AuthorizationError: status.HTTP_403_FORBIDDEN,
            AlreadyAuthenticatedError: status.HTTP_409_CONFLICT,
            UserAlreadyExistsError: status.HTTP_409_CONFLICT,
            GatewayError: status.HTTP_503_SERVICE_UNAVAILABLE,
            EntityAddError: status.HTTP_409_CONFLICT,
            RollbackError: status.HTTP_503_SERVICE_UNAVAILABLE,
            InfrastructureError: status.HTTP_503_SERVICE_UNAVAILABLE,
        }
    )

    def __init__(self, app: FastAPI) -> None:
        self._app = app

    async def _handle(self, _: Request, exc: Exception) -> JSONResponse:
        status_code = self._ERROR_MAPPING.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JSONResponse(content={"description": str(exc)}, status_code=status_code)

    def setup_exception_handler(self) -> None:
        for exc_class in self._ERROR_MAPPING:
            self._app.add_exception_handler(exc_class, self._handle)
        self._app.add_exception_handler(Exception, self._handle)
