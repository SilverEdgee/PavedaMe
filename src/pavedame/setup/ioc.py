from collections.abc import Iterable
from datetime import timedelta
from typing import Final

from dishka import Provider, Scope
from starlette.requests import Request
from starlette.responses import Response

from pavedame.application.auth.login import LoginHandler
from pavedame.application.auth.logout import LogoutHandler
from pavedame.application.auth.signup import SignUpHandler
from pavedame.application.auth.verify_email import VerifyEmailHandler
from pavedame.application.common.ports.email_sender import EmailSender
from pavedame.application.common.ports.email_verification_token_gateway import EmailVerificationTokenGateway
from pavedame.application.common.ports.email_verification_token_generator import (
    EmailVerificationTokenGenerator,
    EmailVerificationTokenIDGenerator,
)
from pavedame.application.common.ports.email_verification_token_hasher import EmailVerificationTokenHasher
from pavedame.application.common.ports.email_verification_token_timer import EmailVerificationTokenTimer
from pavedame.application.common.ports.email_verification_url_builder import EmailVerificationURLBuilder
from pavedame.application.common.ports.session_gateway import SessionGateway
from pavedame.application.common.ports.session_id_generator import SessionIDGenerator
from pavedame.application.common.ports.session_timer import SessionTimer
from pavedame.application.common.ports.session_transport import SessionTransport
from pavedame.application.common.ports.transaction_manager import TransactionManager
from pavedame.application.common.ports.user_gateway import UserGateway
from pavedame.application.common.services.auth_session import AuthSessionService
from pavedame.application.common.services.current_user import CurrentUserService
from pavedame.application.common.services.email_verification import (
    EmailVerificationDeliveryService,
    EmailVerificationService,
    EmailVerificationTokenService,
)
from pavedame.domain.ports import PasswordHasher, UserIDGenerator
from pavedame.domain.user import UserService
from pavedame.infrastructure.adapters.auth import AuthSessionTimer, SecretsAuthIdGenerator
from pavedame.infrastructure.adapters.common.cookie_auth_session_transport import CookieAuthSessionTransport
from pavedame.infrastructure.adapters.common.user import BcryptPasswordHasher, UUID4UserIDGenerator
from pavedame.infrastructure.adapters.email_verification import (
    PublicEmailVerificationURLBuilder,
    SecretsEmailVerificationTokenGenerator,
    SHA256EmailVerificationTokenHasher,
    UTCEmailVerificationTokenTimer,
    UUID4EmailVerificationTokenIDGenerator,
)
from pavedame.infrastructure.adapters.gmail_smtp_email_sender import GmailSMTPEmailSender
from pavedame.infrastructure.adapters.persistence.alchemy_email_verification_token_gateway import (
    AlchemyEmailVerificationTokenGateway,
)
from pavedame.infrastructure.adapters.persistence.alchemy_session_gateway import AlchemyAuthSessionGateway
from pavedame.infrastructure.adapters.persistence.alchemy_transcation_manager import AlchemyTransactionManager
from pavedame.infrastructure.adapters.persistence.alchemy_user_gateway import AlchemyUserGateway
from pavedame.infrastructure.persistence.provider import get_engine, get_session, get_sessionmaker
from pavedame.setup.config.database import PostgresConfig, SQLAlchemyConfig
from pavedame.setup.config.email import EmailVerificationConfig, SMTPConfig


def get_session_timer() -> SessionTimer:
    return AuthSessionTimer(ttl=timedelta(hours=1))


def get_email_verification_token_timer(config: EmailVerificationConfig) -> EmailVerificationTokenTimer:
    return UTCEmailVerificationTokenTimer(ttl=timedelta(seconds=config.token_ttl_seconds))


def get_response() -> Response:
    return Response()


def configs_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.from_context(provides=PostgresConfig)
    provider.from_context(provides=SQLAlchemyConfig)
    provider.from_context(provides=SMTPConfig)
    provider.from_context(provides=EmailVerificationConfig)
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


def email_verification_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(
        source=UUID4EmailVerificationTokenIDGenerator,
        provides=EmailVerificationTokenIDGenerator,
        scope=Scope.APP,
    )
    provider.provide(
        source=SecretsEmailVerificationTokenGenerator,
        provides=EmailVerificationTokenGenerator,
        scope=Scope.APP,
    )
    provider.provide(
        source=SHA256EmailVerificationTokenHasher,
        provides=EmailVerificationTokenHasher,
        scope=Scope.APP,
    )
    provider.provide(
        source=get_email_verification_token_timer,
        provides=EmailVerificationTokenTimer,
        scope=Scope.APP,
    )
    provider.provide(source=EmailVerificationTokenService, scope=Scope.APP)
    provider.provide(
        source=PublicEmailVerificationURLBuilder,
        provides=EmailVerificationURLBuilder,
        scope=Scope.APP,
    )
    provider.provide(source=GmailSMTPEmailSender, provides=EmailSender, scope=Scope.APP)
    provider.provide(source=EmailVerificationService)
    provider.provide(source=EmailVerificationDeliveryService)
    return provider


def gateway_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(source=AlchemyTransactionManager, provides=TransactionManager)
    provider.provide(source=AlchemyUserGateway, provides=UserGateway)
    provider.provide(source=AlchemyAuthSessionGateway, provides=SessionGateway)
    provider.provide(source=AlchemyEmailVerificationTokenGateway, provides=EmailVerificationTokenGateway)
    return provider


def handler_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide_all(SignUpHandler, LoginHandler, LogoutHandler, VerifyEmailHandler)
    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        configs_provider(),
        db_provider(),
        domain_provider(),
        auth_provider(),
        email_verification_provider(),
        gateway_provider(),
        handler_provider(),
    )
