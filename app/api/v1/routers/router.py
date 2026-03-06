from fastapi import APIRouter
from app.api.v1.routers import  health, job, sentence_transformer, users , auth

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=['Health'])
api_router.include_router(sentence_transformer.router, prefix="/sentence-transformer", tags=['SentenceTransformer'])
api_router.include_router(users.router, prefix="/users", tags=['Users'])
api_router.include_router(auth.router, prefix="/auth", tags=['Auth'])
api_router.include_router(job.router, prefix="/jobs", tags=['Jobs'])

