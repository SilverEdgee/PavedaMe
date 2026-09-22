from typing import Protocol

from pavedame.application.auth.session_model import SessionID


class SessionTransport(Protocol):

    async def deliver(self, session_id: SessionID) -> None: ...

    async def extract_id(self) -> str | None: ...

    async def remove_current(self) -> None: ...
