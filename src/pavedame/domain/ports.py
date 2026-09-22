from typing import Protocol

from pavedame.domain.user import UserID


class UserIDGenerator(Protocol):

    def __call__(self) -> UserID: ...


class PasswordHasher(Protocol):

    def verify_password(self, *, user_password: bytes, entered_password: str) -> bool: ...

    def hash_password(self, password: str) -> bytes: ...