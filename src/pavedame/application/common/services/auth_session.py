from pavedame.application.auth.session_model import Session
from pavedame.application.common.ports.session_gateway import SessionGateway
from pavedame.application.common.ports.session_id_generator import SessionIDGenerator
from pavedame.application.common.ports.session_timer import SessionTimer
from pavedame.application.common.ports.session_transport import SessionTransport
from pavedame.application.common.ports.transaction_manager import TransactionManager
from pavedame.application.errors.errors import AuthenticationError


class AuthSessionService:
    def __init__(
            self,
            session_id_generator: SessionIDGenerator,
            session_timer: SessionTimer,
            session_gateway: SessionGateway,
            transaction_manager: TransactionManager,
            session_transport: SessionTransport
    ):
        self._session_id_generator = session_id_generator
        self._session_timer = session_timer
        self._session_gateway = session_gateway
        self._transaction_manager = transaction_manager
        self._session_transport = session_transport
        self._cached_session = None

    async def create_session(self, user_id: UserID) -> None:

        session_id = self._session_id_generator()

        expiration = self._session_timer.session_expires_at

        session = Session(
            user_id=user_id,
            session_id = session_id,
            expiration = expiration,
        )

        await self._session_gateway.add(session)
        await self._transaction_manager.commit()

        await self._session_transport.deliver(session_id)

    async def get_session(self) -> Session:

        if self._cached_session is not None:
            return self._cached_session

        session_id = await self._session_transport.extract_id()
        if session_id is None:
            msg = "Authentication failed"
            raise AuthenticationError(msg)

        session = await self._session_gateway.get_session(session_id)

        if session is None:
            msg = "Authentication failed"
            raise AuthenticationError(msg)

        self._cached_session = session
        return self._cached_session


    async def invalidate_all_user_sessions(self, user_id: UserID) -> None:
        await self._session_gateway.delete_all_for_user(user_id)

        self._cached_session = None

