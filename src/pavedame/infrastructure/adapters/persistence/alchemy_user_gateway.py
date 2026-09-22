from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pavedame.application.common.ports.user_gateway import UserGateway
from pavedame.domain.ports import UserID
from pavedame.domain.user import User
from pavedame.infrastructure.adapters.persistence.constraints import DB_QUERY_FAILED
from pavedame.infrastructure.errors import GatewayError
from pavedame.infrastructure.persistence.models import user_table


class AlchemyUserGateway(UserGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: User) -> None:
        self._session.add(user)

    async def delete_by_id(self, user_id: UserID) -> None:
        stmt = delete(User).where(user_table.c.id == user_id)
        try:
            await self._session.execute(stmt)
        except SQLAlchemyError as error:
            raise GatewayError(DB_QUERY_FAILED) from error

    async def get_user_by_id(self, user_id: UserID) -> User | None:
        stmt = select(User).where(user_table.c.id == user_id)
        try:
            result = await self._session.execute(stmt)
        except SQLAlchemyError as error:
            raise GatewayError(DB_QUERY_FAILED) from error

        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(user_table.c.email == email)
        try:
            result = await self._session.execute(stmt)
        except SQLAlchemyError as error:
            raise GatewayError(DB_QUERY_FAILED) from error

        return result.scalar_one_or_none()
