from fastapi import APIRouter
from app.services.model_service import model_service

router = APIRouter()

@router.get("/info",
            summary="Get Model Information",
            description="Get model information such as loaded status and device",
            )
async def model_info():
    return {
        "loaded": model_service.model_Loaded(),
        "device": "cpu"
    }

@router.post("/reply")
async def model_reply(text: str):
    response = model_service.reply(text)
    return {
        "response" : response
    }


