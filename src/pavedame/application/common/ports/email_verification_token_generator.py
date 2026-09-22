from typing import Protocol

from pavedame.application.auth.email_verification_model import EmailVerificationTokenID, RawEmailVerificationToken


class EmailVerificationTokenIDGenerator(Protocol):
    def __call__(self) -> EmailVerificationTokenID: ...


class EmailVerificationTokenGenerator(Protocol):
    def __call__(self) -> RawEmailVerificationToken: ...
