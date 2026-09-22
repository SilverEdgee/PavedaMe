from pydantic import BaseModel, Field


class SMTPConfig(BaseModel):
    host: str = Field(
        alias="SMTP_HOST",
        description="SMTP server host.",
    )

    port: int = Field(
        alias="SMTP_PORT",
        description="SMTP server port.",
        ge=1,
        le=65535,
    )

    username: str = Field(
        alias="SMTP_USERNAME",
        description="SMTP account username.",
    )

    password: str = Field(
        alias="SMTP_PASSWORD",
        description="SMTP account app password.",
    )

    from_name: str = Field(
        alias="SMTP_FROM_NAME",
        description="Sender name displayed in an email client.",
    )

    start_tls: bool = Field(
        alias="SMTP_START_TLS",
        description="Upgrade the SMTP connection using STARTTLS.",
    )

    timeout: float = Field(
        alias="SMTP_TIMEOUT",
        description="SMTP operation timeout in seconds.",
        gt=0,
    )
