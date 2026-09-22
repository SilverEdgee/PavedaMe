import uuid

import bcrypt

from pavedame.domain.ports import UserIDGenerator, PasswordHasher
from pavedame.domain.user import UserID


class UUID4UserIDGenerator(UserIDGenerator):

    def __call__(self) -> UserID:
        return UserID(uuid.uuid4())


class BcryptPasswordHasher(PasswordHasher):

    def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

    def verify_password(self, *, user_password: bytes, entered_password: str) -> bool:
        return bcrypt.checkpw(entered_password.encode("utf8"), user_password)