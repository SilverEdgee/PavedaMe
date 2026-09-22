from fastapi import FastAPI

from pavedame.setup.bootstrap import setup_config, setup_exc_handler


def create_app() -> FastAPI:
    #add exception_handler, configuration
    setup_config()
    setup_exc_handler()
    app: FastAPI = FastAPI(
        version="1.0.0",
        title="PavedaMe API",
        description="API for managing organization's notifications",
        contact={"name": "Dzianis Pametska", "email": "denispometko8@gmail.com"},
    )

    return app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)

