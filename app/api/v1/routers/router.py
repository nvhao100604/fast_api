from fastapi import APIRouter
from app.api.v1.routers import candidate, health, model_info  

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=['Health'])
api_router.include_router(model_info.router, prefix="/model", tags=['Model'])
api_router.include_router(candidate.router, prefix="/candidates", tags=['Candidates'])
