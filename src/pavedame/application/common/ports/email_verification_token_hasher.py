from typing import Protocol

from pavedame.application.auth.email_verification_model import (
    EmailVerificationTokenHash,
    RawEmailVerificationToken,
)


class EmailVerificationTokenHasher(Protocol):
    def hash_token(self, token: RawEmailVerificationToken) -> EmailVerificationTokenHash: ...
