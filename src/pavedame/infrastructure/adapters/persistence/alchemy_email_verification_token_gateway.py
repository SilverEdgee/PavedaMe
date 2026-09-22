from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pavedame.application.auth.email_verification_model import (
    EmailVerificationToken,
    EmailVerificationTokenHash,
)
from pavedame.application.common.ports.email_verification_token_gateway import EmailVerificationTokenGateway
from pavedame.domain.ports import UserID
from pavedame.infrastructure.adapters.persistence.constraints import DB_QUERY_FAILED
from pavedame.infrastructure.errors import GatewayError
from pavedame.infrastructure.persistence.models import email_verification_token_table


class AlchemyEmailVerificationTokenGateway(EmailVerificationTokenGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, token: EmailVerificationToken) -> None:
        self._session.add(token)

    async def get_by_hash(self, token_hash: EmailVerificationTokenHash) -> EmailVerificationToken | None:
        stmt = select(EmailVerificationToken).where(email_verification_token_table.c.token_hash == token_hash)
        try:
            result = await self._session.execute(stmt)
        except SQLAlchemyError as error:
            raise GatewayError(DB_QUERY_FAILED) from error

        return result.scalar_one_or_none()

    async def delete_for_user(self, user_id: UserID) -> None:
        stmt = delete(EmailVerificationToken).where(email_verification_token_table.c.user_id == user_id)
        try:
            await self._session.execute(stmt)
        except SQLAlchemyError as error:
            raise GatewayError(DB_QUERY_FAILED) from error
