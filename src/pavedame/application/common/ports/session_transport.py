from typing import Protocol

from pavedame.application.auth.session_model import SessionID


class SessionTransport(Protocol):

    async def deliver(self, session_id: SessionID): ...

    async def extract_id(self) -> SessionID: ...
