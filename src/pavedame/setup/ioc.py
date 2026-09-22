from collections.abc import Iterable
from datetime import timedelta
from typing import Final

from dishka import Provider, Scope
from starlette.requests import Request
from starlette.responses import Response

from pavedame.application.auth.login import LoginHandler
from pavedame.application.auth.logout import LogoutHandler
from pavedame.application.auth.signup import SignUpHandler
from pavedame.application.common.ports.session_gateway import SessionGateway
from pavedame.application.common.ports.session_id_generator import SessionIDGenerator
from pavedame.application.common.ports.session_timer import SessionTimer
from pavedame.application.common.ports.session_transport import SessionTransport
from pavedame.application.common.ports.transaction_manager import TransactionManager
from pavedame.application.common.ports.user_gateway import UserGateway
from pavedame.application.common.services.auth_session import AuthSessionService
from pavedame.application.common.services.current_user import CurrentUserService
from pavedame.domain.ports import PasswordHasher, UserIDGenerator
from pavedame.domain.user import UserService
from pavedame.infrastructure.adapters.auth import AuthSessionTimer, SecretsAuthIdGenerator
from pavedame.infrastructure.adapters.common.cookie_auth_session_transport import CookieAuthSessionTransport
from pavedame.infrastructure.adapters.common.user import BcryptPasswordHasher, UUID4UserIDGenerator
from pavedame.infrastructure.adapters.persistence.alchemy_session_gateway import AlchemyAuthSessionGateway
from pavedame.infrastructure.adapters.persistence.alchemy_transcation_manager import AlchemyTransactionManager
from pavedame.infrastructure.adapters.persistence.alchemy_user_gateway import AlchemyUserGateway
from pavedame.infrastructure.persistence.provider import get_engine, get_session, get_sessionmaker
from pavedame.setup.config.database import PostgresConfig, SQLAlchemyConfig


def get_session_timer() -> SessionTimer:
    return AuthSessionTimer(ttl=timedelta(hours=1))


def get_response() -> Response:
    return Response()


def configs_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.from_context(provides=PostgresConfig)
    provider.from_context(provides=SQLAlchemyConfig)
    return provider


def db_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(source=get_engine, scope=Scope.APP)
    provider.provide(source=get_sessionmaker, scope=Scope.APP)
    provider.provide(source=get_session)
    return provider


def domain_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.APP)
    provider.provide(source=BcryptPasswordHasher, provides=PasswordHasher)
    provider.provide(source=UUID4UserIDGenerator, provides=UserIDGenerator)
    provider.provide(source=UserService)
    return provider


def auth_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.from_context(provides=Request)
    provider.provide(source=get_response)
    provider.provide(source=get_session_timer, provides=SessionTimer, scope=Scope.APP)
    provider.provide(source=SecretsAuthIdGenerator, provides=SessionIDGenerator, scope=Scope.APP)
    provider.provide(source=CookieAuthSessionTransport, provides=SessionTransport)
    provider.provide(source=AuthSessionService)
    provider.provide(source=CurrentUserService)
    return provider


def gateway_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(source=AlchemyTransactionManager, provides=TransactionManager)
    provider.provide(source=AlchemyUserGateway, provides=UserGateway)
    provider.provide(source=AlchemyAuthSessionGateway, provides=SessionGateway)
    return provider


def handler_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide_all(SignUpHandler, LoginHandler, LogoutHandler)
    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        configs_provider(),
        db_provider(),
        domain_provider(),
        auth_provider(),
        gateway_provider(),
        handler_provider(),
    )
