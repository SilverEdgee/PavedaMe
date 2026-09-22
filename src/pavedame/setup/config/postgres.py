from pydantic import BaseModel, Field, PostgresDsn


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
        alias="POSTGRES_DB",
        description="Postgres database name",
    )

    driver: str = Field(
        alias="POSTGRES_DRIVER",
        description="Postgres driver name",
    )

    @property
    def uri(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.driver}",
                username=self.user,
                password=self.password,
                port=self.port,
                host=self.host,
                path=self.database,
            )
        )

