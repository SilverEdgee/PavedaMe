from dataclasses import dataclass
from typing import NewType
from uuid import UUID

SessionID = NewType('SessionID', UUID)

@dataclass(frozen=True, kw_only=True)
class Session:
    id: SessionID
    user_id: UserID
    exp: datetime
