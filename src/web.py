from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from pavedame.setup.bootstrap import setup_config, setup_exc_handler, setup_map_configs, setup_routers
from pavedame.setup.config.database import PostgresConfig, SQLAlchemyConfig
from pavedame.setup.ioc import setup_providers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    clear_mappers()
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    config = setup_config()
    setup_map_configs()
    app: FastAPI = FastAPI(
        lifespan=lifespan,
        version="1.0.0",
        title="PavedaMe API",
        description="API for managing organization's notifications",
        contact={"name": "Dzianis Pametska", "email": "denispometko8@gmail.com"},
    )

    context = {
        PostgresConfig: config.postgres,
        SQLAlchemyConfig: config.sqlalchemy,
    }
    container: AsyncContainer = make_async_container(*setup_providers(), context=context)

    setup_routers(app)
    setup_exc_handler(app)
    setup_dishka(container, app)

    return app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
