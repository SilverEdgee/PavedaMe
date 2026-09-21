from datetime import datetime
from typing import Protocol


class SessionTimer(Protocol):

    def session_expires_at(self) -> datetime: ...