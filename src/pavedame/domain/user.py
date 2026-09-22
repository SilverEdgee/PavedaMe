from dataclasses import dataclass

from pavedame.domain.ports import PasswordHasher, UserID, UserIDGenerator


@dataclass(kw_only=True)
class User:
    id: UserID
    username: str
    password: bytes
    email: str
    is_verified: bool = False


class UserService:
    def __init__(
        self,
        user_id_generator: UserIDGenerator,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_id_generator = user_id_generator
        self._password_hasher = password_hasher

    def create_user(
        self,
        username: str,
        password: str,
        email: str,
    ) -> User:

        password = self._password_hasher.hash_password(password)
        return User(
            id=self._user_id_generator(),
            username=username,
            password=password,
            email=email,
        )

    def verify_password(self, *, user_password: bytes, entered_password: str) -> bool:
        return self._password_hasher.verify_password(user_password=user_password, entered_password=entered_password)

    @staticmethod
    def change_username(user: User, new_username: str) -> None:
        user.username = new_username

    @staticmethod
    def change_email(user: User, new_email: str) -> None:
        user.email = new_email

    def change_password(self, user: User, new_password: str) -> None:
        new_password = self._password_hasher.hash_password(new_password)
        user.password = new_password
