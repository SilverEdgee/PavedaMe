from datetime import datetime
from typing import Protocol


class EmailVerificationTokenTimer(Protocol):
    @property
    def expires_at(self) -> datetime: ...
