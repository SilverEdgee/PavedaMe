from typing import Protocol


class EmailSender(Protocol):
    async def send_verification_email(self, recipient: str, verification_url: str) -> None: ...
