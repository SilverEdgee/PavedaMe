from pydantic import BaseModel, Field


class UvicornConfig(BaseModel):
    host: str = Field(
        alias="UVICORN_HOST",
        description="Uvicorn host.",
    )

    port: int = Field(
        alias="UVICORN_PORT",
        description="Uvicorn port.",
        ge=1,
        le=65535,
    )
