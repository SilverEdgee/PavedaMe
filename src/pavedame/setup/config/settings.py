import os

from pydantic import BaseModel, Field

from pavedame.setup.config.database import PostgresConfig, SQLAlchemyConfig
from pavedame.setup.config.email import SMTPConfig
from pavedame.setup.config.uvicorn import UvicornConfig


class AppConfig(BaseModel):
    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**os.environ),
    )

    sqlalchemy: SQLAlchemyConfig = Field(
        default_factory=lambda: SQLAlchemyConfig(**os.environ),
    )

    uvicorn: UvicornConfig = Field(
        default_factory=lambda: UvicornConfig(**os.environ),
    )

    smtp: SMTPConfig = Field(
        default_factory=lambda: SMTPConfig(**os.environ),
    )
