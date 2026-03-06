from fastapi import APIRouter
from app.api.v1.routers import  cv, health, model_info  , users , auth

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=['Health'])
api_router.include_router(model_info.router, prefix="/model", tags=['Model'])
api_router.include_router(users.router, prefix="/users", tags=['Users'])
api_router.include_router(auth.router, prefix="/auth", tags=['Auth'])


public_router = APIRouter()
public_router.include_router(cv.public_router, prefix="/cvs", tags=['CV'])


private_router = APIRouter()
private_router.include_router(cv.private_router, prefix="/cvs", tags=['CV'])


api_router.include_router(public_router)
api_router.include_router(private_router)


