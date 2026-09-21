from pydantic import BaseModel, Field


class PostgresConfig(BaseModel):

    user: str = Field(
        alias="POSTGRES_USER",
        description="Postgres user name",
    )

    password: str = Field(
        alias="POSTGRES_PASSWORD",
        description="Postgres password",
    )

    host: str = Field(
        alias="POSTGRES_HOST",
        description="Postgres host name",
    )

    port: int = Field(
        alias="POSTGRES_PORT",
        description="Postgres port",
    )

    database: str = Field(
        alias="POSTGRES_DATABASE",
        description="Postgres database name",
    )

    driver: str = Field(
        alias="POSTGRES_DRIVER",
        description="Postgres driver name",
    )
