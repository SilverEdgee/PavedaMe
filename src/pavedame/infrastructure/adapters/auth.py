import secrets
from datetime import UTC, datetime, timedelta
from typing import override

from pavedame.application.auth.session_model import SessionID
from pavedame.application.common.ports.session_id_generator import SessionIDGenerator
from pavedame.application.common.ports.session_timer import SessionTimer


class AuthSessionTimer(SessionTimer):

    def __init__(self, ttl: timedelta):
        self._ttl = ttl

    @property
    def session_expires_at(self) -> datetime:
        return self._ttl + datetime.now(UTC)


class SecretsAuthIdGenerator(SessionIDGenerator):

    @override
    def __call__(self) -> SessionID:
        return SessionID(secrets.token_urlsafe(32))
