from pavedame.application.auth.email_verification_model import RawEmailVerificationToken
from pavedame.application.common.ports.transaction_manager import TransactionManager
from pavedame.application.common.ports.user_gateway import UserGateway
from pavedame.application.common.services.auth_session import AuthSessionService
from pavedame.application.common.services.email_verification import EmailVerificationService
from pavedame.application.errors import InvalidEmailVerificationTokenError
from pavedame.domain.user import UserService


class VerifyEmailHandler:
    def __init__(
        self,
        verification_service: EmailVerificationService,
        user_gateway: UserGateway,
        user_service: UserService,
        transaction_manager: TransactionManager,
        auth_session_service: AuthSessionService,
    ) -> None:
        self._verification_service = verification_service
        self._user_gateway = user_gateway
        self._user_service = user_service
        self._transaction_manager = transaction_manager
        self._auth_session_service = auth_session_service

    async def __call__(self, token: RawEmailVerificationToken) -> None:
        verification_token = await self._verification_service.consume_token(token)
        user = await self._user_gateway.get_user_by_id(verification_token.user_id)

        if user is None:
            msg = "Invalid email verification token"
            raise InvalidEmailVerificationTokenError(msg)

        self._user_service.verify_email(user)
        await self._transaction_manager.commit()
        await self._auth_session_service.create_session(user.id)
