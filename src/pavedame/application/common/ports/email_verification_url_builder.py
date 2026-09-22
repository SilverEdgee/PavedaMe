from typing import Protocol

from pavedame.application.auth.email_verification_model import RawEmailVerificationToken


class EmailVerificationURLBuilder(Protocol):
    def build(self, token: RawEmailVerificationToken) -> str: ...
