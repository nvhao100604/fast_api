from fastapi import APIRouter
from app.api.v1.routers import  health, model_info  , users , auth 

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=['Health'])
api_router.include_router(model_info.router, prefix="/model", tags=['Model'])
api_router.include_router(users.router, prefix="/users", tags=['Users'])
api_router.include_router(auth.router, prefix="/auth", tags=['Auth'])


