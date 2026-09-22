from dataclasses import dataclass
from types import MappingProxyType

from fastapi import status, FastAPI, Request
from starlette.responses import JSONResponse

from pavedame.application.errors.errors import AuthenticationError, AuthorizationError, AlreadyAuthenticatedError


@dataclass(frozen=True, slots=True)
class ExceptionSchema:
    description: str



class ExceptionHandler:

    _ERROR_MAPPING: MappingProxyType[type[Exception], int] = MappingProxyType(
        {
            AuthenticationError: status.HTTP_401_UNAUTHORIZED,
            AuthorizationError: status.HTTP_403_FORBIDDEN,
            AlreadyAuthenticatedError: status.HTTP_409_CONFLICT,
        }
    )

    def __init__(self, app: FastAPI):
        self._app = app

    async def _handle(self, _: Request, exc: Exception) -> JSONResponse:
        status_code = self._ERROR_MAPPING.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
        msg = str(exc)
        response = ExceptionSchema(description=msg)

        return JSONResponse(content=response, status_code=status_code)

    def setup_exception_handler(self):
        for exc_class in self._ERROR_MAPPING:
            self._app.add_exception_handler(exc_class, self._handle)
        self._app.add_exception_handler(Exception, self._handle)
