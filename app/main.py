from fastapi import FastAPI
from app.core.config import settings

from app.api.v1.routers import health, model_info

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=(
            "An automated recruitment screening platform leveraging FastAPI "
            "and the all-MiniLM-L6-v2 transformer model to evaluate candidate–job "
            "fit through semantic similarity analysis."
        ),
        version="1.0.0",
    )


    app.include_router(
        health.router,
        prefix=settings.API_V1_STR,
        tags=["Health"]
    )

    app.include_router(
        model_info.router,
        prefix=settings.API_V1_STR,
        tags=["Model"]
    )

    return app


app = create_app()