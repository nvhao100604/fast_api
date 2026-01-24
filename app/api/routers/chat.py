from fastapi import APIRouter
from app.api.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_services import chat_service

router = APIRouter(tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return chat_service.handle_chat(req)
