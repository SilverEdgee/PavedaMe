import os

from pydantic import BaseModel, Field

from pavedame.setup.config.postgres import PostgresConfig


class AppConfig(BaseModel):

    postgres: PostgresConfig = Field(
        default_factory=PostgresConfig(**os.environ),


    )
