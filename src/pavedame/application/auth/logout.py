from pavedame.application.common.services.auth_session import AuthSessionService


class LogoutHandler:
    def __init__(
        self,
        auth_service: AuthSessionService,
    ) -> None:
        self._auth_session_service = auth_service

    async def __call__(self) -> None:
        await self._auth_session_service.invalidate_current_session()
