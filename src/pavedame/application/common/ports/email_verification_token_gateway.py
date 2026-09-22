from typing import Protocol

from pavedame.application.auth.email_verification_model import (
    EmailVerificationToken,
    EmailVerificationTokenHash,
)
from pavedame.domain.ports import UserID


class EmailVerificationTokenGateway(Protocol):
    async def add(self, token: EmailVerificationToken) -> None: ...

    async def get_by_hash(self, token_hash: EmailVerificationTokenHash) -> EmailVerificationToken | None: ...

    async def delete_for_user(self, user_id: UserID) -> None: ...
