from pavedame.application.auth.email_verification_model import EmailVerificationToken, RawEmailVerificationToken
from pavedame.application.common.ports.email_verification_token_gateway import EmailVerificationTokenGateway
from pavedame.application.common.ports.email_verification_token_generator import (
    EmailVerificationTokenGenerator,
    EmailVerificationTokenIDGenerator,
)
from pavedame.application.common.ports.email_verification_token_hasher import EmailVerificationTokenHasher
from pavedame.application.common.ports.email_verification_token_timer import EmailVerificationTokenTimer
from pavedame.application.common.ports.transaction_manager import TransactionManager
from pavedame.domain.ports import UserID


class EmailVerificationTokenService:
    def __init__(
        self,
        token_id_generator: EmailVerificationTokenIDGenerator,
        token_generator: EmailVerificationTokenGenerator,
        token_hasher: EmailVerificationTokenHasher,
        token_timer: EmailVerificationTokenTimer,
    ) -> None:
        self._token_id_generator = token_id_generator
        self._token_generator = token_generator
        self._token_hasher = token_hasher
        self._token_timer = token_timer

    def create_token(self, user_id: UserID) -> tuple[EmailVerificationToken, RawEmailVerificationToken]:
        raw_token = self._token_generator()
        token = EmailVerificationToken(
            id=self._token_id_generator(),
            user_id=user_id,
            token_hash=self._token_hasher.hash_token(raw_token),
            expires_at=self._token_timer.expires_at,
        )
        return token, raw_token


class EmailVerificationService:
    def __init__(
        self,
        token_service: EmailVerificationTokenService,
        token_gateway: EmailVerificationTokenGateway,
        transaction_manager: TransactionManager,
    ) -> None:
        self._token_service = token_service
        self._token_gateway = token_gateway
        self._transaction_manager = transaction_manager

    async def issue_token(self, user_id: UserID) -> RawEmailVerificationToken:
        token, raw_token = self._token_service.create_token(user_id)

        await self._token_gateway.delete_for_user(user_id)
        await self._token_gateway.add(token)
        await self._transaction_manager.commit()

        return raw_token
