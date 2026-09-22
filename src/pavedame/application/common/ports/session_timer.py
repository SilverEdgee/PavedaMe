from datetime import datetime
from typing import Protocol


class SessionTimer(Protocol):
    @property
    def session_expires_at(self) -> datetime: ...
