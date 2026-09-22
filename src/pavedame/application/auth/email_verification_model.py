from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from pavedame.domain.ports import UserID

EmailVerificationTokenID = NewType("EmailVerificationTokenID", UUID)
RawEmailVerificationToken = NewType("RawEmailVerificationToken", str)
EmailVerificationTokenHash = NewType("EmailVerificationTokenHash", str)


@dataclass(kw_only=True)
class EmailVerificationToken:
    id: EmailVerificationTokenID
    user_id: UserID
    token_hash: EmailVerificationTokenHash
    expires_at: datetime
    used_at: datetime | None = None
