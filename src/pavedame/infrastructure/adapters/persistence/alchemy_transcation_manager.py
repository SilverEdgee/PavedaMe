from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pavedame.application.common.ports.transaction_manager import TransactionManager
from pavedame.infrastructure.adapters.persistence.constraints import (
    DB_CONSTRAINT_VIOLATION,
    DB_QUERY_FAILED,
    DB_ROLLBACK_FAILED,
)
from pavedame.infrastructure.errors import EntityAddError, GatewayError, RollbackError


class AlchemyTransactionManager(TransactionManager):
    def __init__(self, session: AsyncSession):
        self._session = session
    async def commit(self) -> None:
        try:
            await self._session.commit()
        except IntegrityError as error:
            await self._session.rollback()
            raise EntityAddError(DB_CONSTRAINT_VIOLATION) from error
        except SQLAlchemyError as error:
            await self._session.rollback()
            raise GatewayError(DB_QUERY_FAILED) from error

    async def rollback(self) -> None:

        try:
            await self._session.rollback()
        except SQLAlchemyError as error:
            raise RollbackError(DB_ROLLBACK_FAILED) from error

    async def flush(self) -> None:

        try:
            await self._session.flush()
        except IntegrityError as error:
            await self._session.rollback()
            raise EntityAddError(DB_CONSTRAINT_VIOLATION) from error
        except SQLAlchemyError as error:
            await self._session.rollback()
            raise GatewayError(DB_QUERY_FAILED) from error
