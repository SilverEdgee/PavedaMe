from typing import Protocol


from pavedame.domain.user import UserID, User


class UserGateway(Protocol):

    async def add(self, user: User) -> None: ...

    async def delete_by_id(self, user_id: UserID) -> None: ...

    async def get_user_by_id(self, user_id: UserID) -> User: ...

    async def get_user_by_email(self, email: str) -> User: ...

