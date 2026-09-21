from dataclasses import dataclass

from pavedame.application.common.ports.user_gateway import UserGateway
from pavedame.application.common.services.auth_session import AuthSessionService
from pavedame.application.common.services.current_user import CurrentUserService
from pavedame.application.errors.errors import AuthenticationError, AlreadyAuthenticatedError


@dataclass(frozen=True, kw_only=True, slots=True)
class LoginData:
    username: str
    password: str
    email: str


class LoginHandler:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        user_gateway: UserGateway,
        auth_service: AuthSessionService,
        user_service: UserService,
    ) -> None:
        self._current_user_service = current_user_service
        self._user_gateway = user_gateway
        self._auth_session_service = auth_service
        self._user_service = user_service


    async def __call__(self, data: LoginData) -> None:

        try:
            await self._current_user_service.get_current_user()
            msg = "You are already logged in."
            raise AlreadyAuthenticatedError(msg)
        except AuthenticationError:
            pass

        user = await self._user_gateway.get_user_by_email(data.email)

        if user is None:
            msg = f"No user with email '{data.email}' found."
            raise AuthenticationError(msg)

        if not self._user_service.verify_password(data.password, user.password):
            msg = f"Password mismatch. Please try again."
            raise AuthenticationError(msg)

        await self._auth_session_service.create_session(user_id=user.id)



