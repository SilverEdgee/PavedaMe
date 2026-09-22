import hashlib
import secrets
import uuid
from datetime import UTC, datetime, timedelta
from urllib.parse import urlencode

from pavedame.application.auth.email_verification_model import (
    EmailVerificationTokenHash,
    EmailVerificationTokenID,
    RawEmailVerificationToken,
)
from pavedame.application.common.ports.email_verification_token_generator import (
    EmailVerificationTokenGenerator,
    EmailVerificationTokenIDGenerator,
)
from pavedame.application.common.ports.email_verification_token_hasher import EmailVerificationTokenHasher
from pavedame.application.common.ports.email_verification_token_timer import EmailVerificationTokenTimer
from pavedame.application.common.ports.email_verification_url_builder import EmailVerificationURLBuilder
from pavedame.setup.config.email import EmailVerificationConfig


class UUID4EmailVerificationTokenIDGenerator(EmailVerificationTokenIDGenerator):
    def __call__(self) -> EmailVerificationTokenID:
        return EmailVerificationTokenID(uuid.uuid4())


class SecretsEmailVerificationTokenGenerator(EmailVerificationTokenGenerator):
    def __call__(self) -> RawEmailVerificationToken:
        return RawEmailVerificationToken(secrets.token_urlsafe(32))


class SHA256EmailVerificationTokenHasher(EmailVerificationTokenHasher):
    def hash_token(self, token: RawEmailVerificationToken) -> EmailVerificationTokenHash:
        digest = hashlib.sha256(token.encode()).hexdigest()
        return EmailVerificationTokenHash(digest)


class UTCEmailVerificationTokenTimer(EmailVerificationTokenTimer):
    def __init__(self, ttl: timedelta) -> None:
        self._ttl = ttl

    @property
    def expires_at(self) -> datetime:
        return datetime.now(UTC) + self._ttl


class PublicEmailVerificationURLBuilder(EmailVerificationURLBuilder):
    def __init__(self, config: EmailVerificationConfig) -> None:
        self._public_url = str(config.public_url).rstrip("/")

    def build(self, token: RawEmailVerificationToken) -> str:
        query = urlencode({"token": token})
        return f"{self._public_url}/auth/verify-email?{query}"
