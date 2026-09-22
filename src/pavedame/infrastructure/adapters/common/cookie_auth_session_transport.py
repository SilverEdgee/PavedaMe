from starlette.requests import Request
from starlette.responses import Response

from pavedame.application.auth.session_model import SessionID
from pavedame.application.common.ports.session_transport import SessionTransport


class CookieAuthSessionTransport(SessionTransport):
    def __init__(self, request: Request, response: Response) -> None:
        self._request = request
        self._response = response

    async def deliver(self, session_id: SessionID) -> None:
        self._response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=self._request.url.scheme == "https",
            samesite="lax",
            path="/",
        )

    async def extract_id(self) -> str | None:
        return self._request.cookies.get("session_id")

    async def remove_current(self) -> None:
        self._response.delete_cookie(
            key="session_id",
            path="/",
        )
