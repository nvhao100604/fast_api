import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional, Dict, Tuple
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.clients.sentence_transformer import sentence_transformer_client

from app.api.v1.schemas.cv_embedding import CVEmbeddingCreate
from app.crud import embbeding as embedding_crud


sentence_transformer_client = sentence_transformer_client
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
# Health check
# ------------------------------------------------------------------------------
def model_loaded() -> bool:
    try:
        print("Checking model load status...")
        print(
            f"SentenceTransformerClient instance: {sentence_transformer_client.model}"
        )
        return sentence_transformer_client.model is not None
    except Exception:
        return False


# ------------------------------------------------------------------------------
# Embedding generation
# ------------------------------------------------------------------------------
def generate_cv_embedding(text: str):
    try:
        print(f"Generating embedding for text: {text[:30]}...")
        return sentence_transformer_client.encode(text, normalize=True)
    except Exception as e:
        logger.exception("Error generating CV embedding")
        raise


# ------------------------------------------------------------------------------
# Database store
# ------------------------------------------------------------------------------
def store_cv_embedding(db: Session, cv_id: int, text: str):
    return embedding_crud.save_cv_embedding(
        db,
        {
            "CVId": cv_id,
            "ModelName": sentence_transformer_client.model_name,
            "Vector": generate_cv_embedding(text),
        },
    )


def store_job_embedding(db: Session, job_id: int, vector: List[float]):
    return embedding_crud.save_job_embedding(
        db,
        {
            "JobId": job_id,
            "ModelName": sentence_transformer_client.model_name,
            "Vector": vector,
        },
    )


# ------------------------------------------------------------------------------
# Retrieve embedding
# ------------------------------------------------------------------------------
def _get_embedding(
    self, db: Session, model, field: str, value: int, embedding_type: EmbeddingType
):
    try:
        query = select(model).where(
            getattr(model, field) == value,
            model.ModelName == self.model_name,
            model.EmbeddingType == embedding_type,
        )
        return db.execute(query).scalars().first()
    except Exception as e:
        logger.error(f"Error retrieving embedding: {e}")
        return None


# def get_cv_embedding(self, db: Session, cv_id: int, embedding_type=EmbeddingType.ALL):
#     return self._get_embedding(db, CVEmbedding, "CVId", cv_id, embedding_type)


# def get_job_embedding(self, db: Session, job_id: int, embedding_type=EmbeddingType.ALL):
#     return self._get_embedding(db, JobEmbedding, "JobId", job_id, embedding_type)


# ------------------------------------------------------------------------------
# Similarity score
# ------------------------------------------------------------------------------
def calculate_semantic_similarity(
    self, cv_vector: List[float], job_vector: List[float]
) -> float:

    try:
        raw_score = self.client.cosine_similarity(cv_vector, job_vector)
        return (raw_score + 1) / 2  # normalize 0–1
    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        return 0.0


# ------------------------------------------------------------------------------
# Matching
# ------------------------------------------------------------------------------
def _save_match_result(
    self, db: Session, cv_id: int, job_id: int, score: float
) -> MatchResult:

    try:
        query = select(MatchResult).where(
            MatchResult.CVId == cv_id, MatchResult.JobId == job_id
        )
        match = db.execute(query).scalars().first()

        score_decimal = Decimal(str(round(score, 4)))

        if match:  # update existing
            match.SemanticScore = score_decimal
            match.EvaluatedAt = datetime.now(timezone.utc)
        else:  # create new
            match = MatchResult(CVId=cv_id, JobId=job_id, SemanticScore=score_decimal)
            db.add(match)

        db.commit()
        db.refresh(match)
        return match

    except Exception as e:
        db.rollback()
        logger.error(f"Error saving match result: {e}")
        raise


def match_cv_with_job(
    self, db: Session, cv_id: int, job_id: int
) -> Optional[Tuple[float, MatchResult]]:

    cv_emb = self.get_cv_embedding(db, cv_id)
    job_emb = self.get_job_embedding(db, job_id)

    if not cv_emb or not job_emb:
        logger.warning(f"Missing embedding for CV {cv_id} or Job {job_id}")
        return None

    score = self.calculate_semantic_similarity(cv_emb.Vector, job_emb.Vector)
    match_result = self._save_match_result(db, cv_id, job_id, score)

    return score, match_result


# ------------------------------------------------------------------------------
# Batch match
# ------------------------------------------------------------------------------
def batch_match_cv_with_jobs(
    self, db: Session, cv_id: int, job_ids: List[int]
) -> Dict[int, float]:

    result = {}
    cv_emb = self.get_cv_embedding(db, cv_id)

    if not cv_emb:
        logger.warning(f"No embedding found for CV {cv_id}")
        return result

    for job_id in job_ids:
        job_emb = self.get_job_embedding(db, job_id)
        if not job_emb:
            continue

        score = self.calculate_semantic_similarity(cv_emb.Vector, job_emb.Vector)
        result[job_id] = score

        try:
            self._save_match_result(db, cv_id, job_id, score)
        except Exception:
            pass

    return result


# ------------------------------------------------------------------------------
# Ranking
# ------------------------------------------------------------------------------
def get_top_matching_jobs(self, db: Session, cv_id: int, limit: int = 10) -> List[Dict]:

    try:
        query = (
            select(MatchResult)
            .where(MatchResult.CVId == cv_id)
            .order_by(MatchResult.SemanticScore.desc())
            .limit(limit)
        )

        matches = db.execute(query).scalars().all()
        results = []

        for m in matches:
            job = db.execute(select(Job).where(Job.Id == m.JobId)).scalars().first()
            if not job:
                continue

            results.append(
                {
                    "job_id": job.Id,
                    "job_title": job.Title,
                    "semantic_score": float(m.SemanticScore or 0),
                    "total_score": float(m.TotalScore or 0),
                }
            )

        return results

    except Exception as e:
        logger.error(f"Error fetching top jobs: {e}")
        return []
