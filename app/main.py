from fastapi import FastAPI
from app.api.v1.routers import health, model_info
from app.core.config import settings

app = FastAPI(
    title= settings.PROJECT_NAME,
    description="An automated recruitment screening platform leveraging FastAPI and the all-MiniLM-L6-v2 transformer model to evaluate candidate-job fit through semantic similarity analysis.",
    version="1.0.0",
)

app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(model_info.router, prefix=settings.API_V1_STR)