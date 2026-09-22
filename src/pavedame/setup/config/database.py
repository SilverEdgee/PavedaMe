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


class SQLAlchemyConfig(BaseModel):
    pool_pre_ping: bool = Field(
        alias="DB_POOL_PRE_PING",
        description="Enable database pool pre ping.",
    )

    pool_size: int = Field(
        alias="DB_POOL_SIZE",
        description="Database connection pool size.",
    )

    pool_recycle: int = Field(
        alias="DB_POOL_RECYCLE",
        description="Database connection pool recycle.",
    )

    max_overflow: int = Field(
        alias="DB_POOL_MAX_OVERFLOW",
        description="Database connection pool max overflow.",
    )

    echo: bool = Field(
        alias="DB_ECHO",
        description="Enable echo mode.",
        validate_default=False,
    )

    auto_flush: bool = Field(
        alias="DB_AUTO_FLUSH",
        description="Enable auto flush mode.",
        validate_default=False,
    )
