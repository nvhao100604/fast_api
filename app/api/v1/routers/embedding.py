from typing import List


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from torch import embedding
from app.api.deps import get_db, get_current_user
from app.api.v1.schemas.response import ResponseSchema

from app.services.embedding import (
    model_loaded,
    generate_cv_embedding,
    store_cv_embedding,
    store_job_embedding,
)

router = APIRouter()


@router.get(
    "/info",
    summary="Get Model Information And Status",
    description="Get model information such as loaded status and device",
)
async def model_info():
    return {
        "model_loaded": model_loaded(),
        "device": "cuda" if model_loaded() else "cpu",
    }


@router.post("/cv_embed")
async def model_embed(cv_id: int, text: str, db: Session = Depends(get_db)):
    embedding = store_cv_embedding(db=db, cv_id=cv_id, text=text)
    # if hasattr(embedding, "tolist"):
    #     embedding = embedding.tolist()
    print(embedding)
    return ResponseSchema(
        success=True,
        message="CV embedding generated and stored successfully",
        data={"cv_id": cv_id},
    )


# @router.post("/embed_batch")
# async def model_embed_batch(texts: List[str]):
#     embeddings = [generate_cv_embedding(text) for text in texts]
#     return {"embeddings": embeddings}
