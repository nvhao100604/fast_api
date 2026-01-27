
from fastapi import APIRouter
from app.api.v1.routers.health import health
from app.api.v1.routers.model_info import model_info

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(model_info.router, prefix="/model", tags=["Model"])