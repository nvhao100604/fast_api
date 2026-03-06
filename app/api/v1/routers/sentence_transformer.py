from fastapi import APIRouter, logger
from app.services.sentence_transformer_service import model_service

router = APIRouter()


@router.get(
    "/info",
    summary="Get Model Information",
    description="Get model information such as loaded status and device",
)
async def model_info():
    return {"loaded": model_service.model_loaded(), "device": "cpu"}


@router.get("/health")
async def model_health():
    """Check apakah model sudah loaded"""
    try:
        return model_service.health_check()
    except Exception as e:
        logger.error(f"Error checking model status: {str(e)}")
        return False


@router.post("/reply")
async def model_reply(text: str):
    response = model_service._validate_text(text, "Input")
    return {"response": response}

@router.post("/embed")
async def model_embed(text: str):
    embedding = model_service.generate_cv_embedding(text)
    return {"embedding": embedding}

