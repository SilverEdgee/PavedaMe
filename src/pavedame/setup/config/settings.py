import os

from pydantic import BaseModel, Field

from pavedame.setup.config.database import PostgresConfig, SQLAlchemyConfig


class AppConfig(BaseModel):

    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**os.environ),
    )

    sqlalchemy: SQLAlchemyConfig = Field(
        default_factory=lambda: SQLAlchemyConfig(**os.environ),
    )
