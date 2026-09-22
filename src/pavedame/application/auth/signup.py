from dataclasses import dataclass
from uuid import UUID

from pavedame.application.common.ports.transaction_manager import TransactionManager
from pavedame.application.common.ports.user_gateway import UserGateway
from pavedame.application.common.services.current_user import CurrentUserService
from pavedame.application.errors import AlreadyAuthenticatedError, AuthenticationError, UserAlreadyExistsError
from pavedame.domain.user import User, UserService


@dataclass(frozen=True, kw_only=True, slots=True)
class SignUpData:
    username: str
    password: str
    email: str


@dataclass(frozen=True, kw_only=True, slots=True)
class SignUpView:
    id: UUID


class SignUpHandler:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        user_service: UserService,
        user_gateway: UserGateway,
        transaction_manager: TransactionManager,
    ) -> None:
        self._current_user_service = current_user_service
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, data: SignUpData) -> SignUpView:

        try:
            await self._current_user_service.get_current_user()
            msg = "Already authenticated"
            raise AlreadyAuthenticatedError(msg)
        except AuthenticationError:
            pass

        normalized_email = data.email.strip().lower()

        new_user: User = self._user_service.create_user(
            username=data.username,
            email=normalized_email,
            password=data.password,
        )

        user = await self._user_gateway.get_user_by_email(new_user.email)

        if user is not None:
            msg = "User already exists"
            raise UserAlreadyExistsError(msg)

        await self._user_gateway.add(new_user)
        await self._transaction_manager.commit()

        return SignUpView(
            id=new_user.id,
        )
