from typing import Protocol


class SessionIDGenerator(Protocol):

    def __call__(self) -> str: ...
