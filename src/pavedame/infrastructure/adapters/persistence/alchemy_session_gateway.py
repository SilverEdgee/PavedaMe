from sqlalchemy.ext.asyncio import AsyncSession

from pavedame.application.auth.session_model import AuthSession, SessionID
from pavedame.application.common.ports.session_gateway import SessionGateway


class AlchemyAuthSessionGateway(SessionGateway):

    def __init__(self, session: AsyncSession):
        self._session = session


    async def add(self, auth_session: AuthSession) -> None:
        self._session.add(auth_session)

    async def delete_by_id(self, session_id: SessionID) -> None:
        stmt = delete(AuthSession).
