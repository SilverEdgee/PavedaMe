from pavedame.application.common.ports.session_gateway import SessionGateway
from pavedame.application.common.ports.user_gateway import UserGateway
from pavedame.application.common.services.auth_session import AuthSessionService
from pavedame.application.errors import AuthenticationError
from pavedame.domain.user import User


class CurrentUserService:
    def __init__(
            self,
            auth_session_service: AuthSessionService,
            user_gateway: UserGateway,
            session_gateway: SessionGateway,
    ):
        self._auth_session_service = auth_session_service
        self._user_gateway = user_gateway
        self._session_gateway = session_gateway
        self._cached_user = None

    async def get_current_user(self) -> User:
        if self._cached_user is not None:
            return self._cached_user

        session = await self._session_gateway.get_session()

        if session is None:
            msg = "AuthSession not found"
            raise AuthenticationError(msg)

        user = await self._user_gateway.get_user_by_id(session.user_id)

        if user is None:
            msg = "User not found"
            await self._auth_session_service.invalidate_all_user_sessions()
            raise AuthenticationError(msg)

        self._cached_user = user

        return self._cached_user



