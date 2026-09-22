from email.message import EmailMessage
from email.utils import formataddr

import aiosmtplib
from aiosmtplib.errors import SMTPException

from pavedame.application.common.ports.email_sender import EmailSender
from pavedame.infrastructure.errors import EmailDeliveryError
from pavedame.setup.config.email import SMTPConfig


class GmailSMTPEmailSender(EmailSender):
    def __init__(self, config: SMTPConfig) -> None:
        self._config = config

    async def send_verification_email(self, recipient: str, verification_url: str) -> None:
        message = EmailMessage()
        message["From"] = formataddr((self._config.from_name, self._config.username))
        message["To"] = recipient
        message["Subject"] = "Confirm your email in PavedaMe"
        message.set_content(
            "You can confirm your email, using this link:\n"
            f"{verification_url}\n\n"
            "If you haven't registered in PavedaMe, ignore this message.",
        )

        try:
            await aiosmtplib.send(
                message,
                hostname=self._config.host,
                port=self._config.port,
                username=self._config.username,
                password=self._config.password,
                start_tls=self._config.start_tls,
                timeout=self._config.timeout,
            )
        except (SMTPException, OSError, TimeoutError) as error:
            msg = "Failed to send verification email"
            raise EmailDeliveryError(msg) from error
