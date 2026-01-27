from fastapi import APIRouter
from app.api.v1.routers import health, model_info   # ✅ ĐÚNG

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health")
api_router.include_router(model_info.router, prefix="/model")