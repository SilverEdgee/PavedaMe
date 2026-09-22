from datetime import UTC, datetime

from pavedame.application.auth.email_verification_model import (
    EmailVerificationToken,
    EmailVerificationTokenHash,
    RawEmailVerificationToken,
)
from pavedame.application.common.ports.email_sender import EmailSender
from pavedame.application.common.ports.email_verification_token_gateway import EmailVerificationTokenGateway
from pavedame.application.common.ports.email_verification_token_generator import (
    EmailVerificationTokenGenerator,
    EmailVerificationTokenIDGenerator,
)
from pavedame.application.common.ports.email_verification_token_hasher import EmailVerificationTokenHasher
from pavedame.application.common.ports.email_verification_token_timer import EmailVerificationTokenTimer
from pavedame.application.common.ports.email_verification_url_builder import EmailVerificationURLBuilder
from pavedame.application.common.ports.transaction_manager import TransactionManager
from pavedame.application.errors import ExpiredEmailVerificationTokenError, InvalidEmailVerificationTokenError
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

    def hash_token(self, token: RawEmailVerificationToken) -> EmailVerificationTokenHash:
        return self._token_hasher.hash_token(token)


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

    async def consume_token(self, raw_token: RawEmailVerificationToken) -> EmailVerificationToken:
        token_hash = self._token_service.hash_token(raw_token)
        token = await self._token_gateway.get_by_hash(token_hash)

        if token is None or token.used_at is not None:
            msg = "Invalid email verification token"
            raise InvalidEmailVerificationTokenError(msg)

        now = datetime.now(UTC)
        if token.expires_at <= now:
            msg = "Email verification token has expired"
            raise ExpiredEmailVerificationTokenError(msg)

        token.used_at = now
        return token


class EmailVerificationDeliveryService:
    def __init__(
        self,
        verification_service: EmailVerificationService,
        url_builder: EmailVerificationURLBuilder,
        email_sender: EmailSender,
    ) -> None:
        self._verification_service = verification_service
        self._url_builder = url_builder
        self._email_sender = email_sender

    async def issue_and_send(self, user_id: UserID, email: str) -> None:
        token = await self._verification_service.issue_token(user_id)
        verification_url = self._url_builder.build(token)
        await self._email_sender.send_verification_email(email, verification_url)
