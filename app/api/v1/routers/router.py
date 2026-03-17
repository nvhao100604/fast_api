from fastapi import APIRouter
from app.api.v1.routers import  embedding, health, job, users , auth

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=['Health'])
api_router.include_router(embedding.router, prefix="/cvembeddings", tags=['CV Embeddings'])
api_router.include_router(embedding.router, prefix="/jobembeddings", tags=['Job Embeddings'])
# api_router.include_router(embedding.router, prefix="/jobembeddings", tags=['Job Embeddings'])
api_router.include_router(users.router, prefix="/users", tags=['Users'])
api_router.include_router(auth.router, prefix="/auth", tags=['Auth'])
api_router.include_router(job.router, prefix="/jobs", tags=['Jobs'])

