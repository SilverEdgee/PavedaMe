from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from pavedame.domain.user import UserID

SessionID = NewType("SessionID", str)

@dataclass(frozen=True, kw_only=True)
class AuthSession:
    id: SessionID
    user_id: UserID
    exp: datetime
