from typing import Protocol

from pavedame.application.auth.session_model import SessionID


class SessionIDGenerator(Protocol):
    def __call__(self) -> SessionID: ...
