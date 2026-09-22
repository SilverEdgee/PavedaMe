from typing import Protocol

from pavedame.application.auth.session_model import AuthSession, SessionID
from pavedame.domain.ports import UserID


class SessionGateway(Protocol):
    async def add(self, session: AuthSession) -> None: ...

    async def delete_by_id(self, session_id: SessionID) -> None: ...

    async def delete_all_for_user(self, user_id: UserID) -> None: ...

    async def get_session(self, session_id: SessionID) -> AuthSession | None: ...
