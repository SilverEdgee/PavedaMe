from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pavedame.application.auth.session_model import AuthSession, SessionID
from pavedame.application.common.ports.session_gateway import SessionGateway
from pavedame.domain.ports import UserID
from pavedame.infrastructure.adapters.persistence.constraints import DB_QUERY_FAILED
from pavedame.infrastructure.errors import GatewayError
from pavedame.infrastructure.persistence.models import auth_table


class AlchemyAuthSessionGateway(SessionGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, auth_session: AuthSession) -> None:
        self._session.add(auth_session)

    async def delete_by_id(self, session_id: SessionID) -> None:
        stmt = delete(AuthSession).where(auth_table.c.id == session_id)
        try:
            await self._session.execute(stmt)
        except SQLAlchemyError as e:
            raise GatewayError(DB_QUERY_FAILED) from e

    async def get_session(self, session_id: SessionID) -> AuthSession | None:
        try:
            auth_session: AuthSession | None = await self._session.get(AuthSession, session_id)
        except SQLAlchemyError as e:
            raise GatewayError(DB_QUERY_FAILED) from e

        return auth_session

    async def delete_all_for_user(self, user_id: UserID) -> None:
        stmt = delete(AuthSession).where(auth_table.c.user_id == user_id)
        try:
            await self._session.execute(stmt)
        except SQLAlchemyError as e:
            raise GatewayError(DB_QUERY_FAILED) from e
