from fastapi import FastAPI
from app.api.routers import chat

app = FastAPI(title="AI API Server")

app.include_router(chat.router, prefix="/api")
