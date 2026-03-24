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
from app.crud.cv_skill import get_cv_skills
from app.crud.job_skill import get_job_skills
from app.crud.match_result import create_match_result
from app.services.cv import *
from app.services.job_service import *
from app.services.education import *
from app.models import CVEmbedding, JobEmbedding, MatchResult

# ------------------------------------------------------------------------------
# SentenceTransformerClient instance
# ------------------------------------------------------------------------------
sentence_transformer_client = sentence_transformer_client


def match_job_result_service(
    db: Session, current_user, cv_id: int, job_id: int
) -> Dict[str, float]:
    # Lấy chi tiết CV
    cv_detail = get_cv_details(db, cv_id, current_user)
    cv_skill_detail = get_cv_skills(db, cv_detail.Id)

    # Lấy chi tiết Job
    job_detail = get_job_detail(db, job_id)
    job_skill_detail = get_job_skills(db, job_detail.Id)

    # Lấy embedding của CV
    cv_cleantext_embedding_vec = _embedding(cv_detail.CleanText or "")
    cv_skill_embedding_vec = _embedding(_skills_to_text(cv_skill_detail) or "")
    cv_experience_level_embedding_vec = _embedding(
        _experiences_to_text(cv_detail.experiences)
    )
    cv_education_level_embedding_vec = _embedding(
        _educations_to_text(cv_detail.educations)
    )

    # Lấy embedding của Job
    job_requirement_embedding_vec = _embedding(job_detail.RequirementsText or "")
    job_skill_embedding_vec = _embedding(_skills_to_text(job_skill_detail) or "")
    job_experience_level_embedding_vec = _embedding(str(job_detail.MinExperience or ""))
    job_education_level_embedding_vec = _embedding(str(job_detail.EducationLevel or ""))

    semantic_match_score = calculate_semantic_similarity(
        job_requirement_embedding_vec, cv_cleantext_embedding_vec
    )

    skill_match_score = calculate_semantic_similarity(
        job_skill_embedding_vec, cv_skill_embedding_vec
    )

    experience_match_score = calculate_semantic_similarity(
        job_experience_level_embedding_vec, cv_experience_level_embedding_vec
    )

    education_match_score = calculate_semantic_similarity(
        job_education_level_embedding_vec, cv_education_level_embedding_vec
    )

    final_total_match_result = (
        semantic_match_score
        + skill_match_score
        + experience_match_score
        + education_match_score
    ) / 4.0

    store_cv_embedding(db, cv_id, cv_detail.CleanText)
    store_job_embedding(db, job_id, job_detail.RequirementsText)
    store_match_result(
        db,
        cv_id,
        job_id,
        semantic_match_score,
        skill_match_score,
        experience_match_score,
        education_match_score,
        final_total_match_result,
    )

    return {
        "semantic_match": semantic_match_score,
        "skill_match": skill_match_score,
        "experience_match": experience_match_score,
        "education_match": education_match_score,
        "final_total_match_result": final_total_match_result,
    }


# ------------------------------------------------------------------------------
# Matching CV and Job Service
# ------------------------------------------------------------------------------
def _skills_to_text(skills):
    if not skills:
        return ""

    names = []
    for s in skills:
        if not s:
            continue
        if hasattr(s, "skill") and getattr(s, "skill") is not None:
            nm = getattr(s.skill, "Name", None)
            if nm:
                names.append(str(nm))
            continue
        if hasattr(s, "Name"):
            names.append(str(getattr(s, "Name")))
            continue
        if hasattr(s, "SkillId"):
            names.append(str(getattr(s, "SkillId")))
            continue
        names.append(str(s))

    return ", ".join(names)


def _experiences_to_text(experiences):
    if not experiences:
        return ""

    parts = []
    for e in experiences:
        if not e:
            continue

        company = getattr(e, "Company", "")
        position = getattr(e, "Position", "")
        duration = getattr(e, "DurationMonths", "")

        p = " ".join([str(x) for x in [company, position, duration] if x])
        if p:
            parts.append(p)

    return " | ".join(parts)


def _educations_to_text(educations):
    if not educations:
        return ""

    parts = []
    for edu in educations:
        if not edu:
            continue

        degree = getattr(edu, "Degree", "")
        major = getattr(edu, "Major", "")
        school = getattr(edu, "School", "")
        level = getattr(edu, "Level", "")

        p = " ".join([str(x) for x in [degree, major, school, level] if x])
        if p:
            parts.append(p)

    return " | ".join(parts)


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
def _embedding(text: str):
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
    try:
        return embedding_crud.save_cv_embedding(
            db,
            {
                "CVId": cv_id,
                "ModelName": sentence_transformer_client.model_name,
                "Vector": _embedding(text),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store CV embedding",
        )
    finally:
        db.close()


def store_job_embedding(db: Session, job_id: int, text: str):
    try:
        return embedding_crud.save_job_embedding(
            db,
            {
                "JobId": job_id,
                "ModelName": sentence_transformer_client.model_name,
                "Vector": _embedding(text),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store Job embedding",
        )
    finally:
        db.close()


def store_match_result(
    db: Session,
    cv_id: int,
    job_id: int,
    semantic_score: Decimal,
    skill_score: Decimal,
    experience_score: Decimal,
    education_score: Decimal,
    total_score: Decimal,
):
    try:
        return create_match_result(
            db,
            CVId=cv_id,
            JobId=job_id,
            SemanticScore=Decimal(semantic_score),
            SkillScore=Decimal(skill_score),
            ExperienceScore=Decimal(experience_score),
            EducationScore=Decimal(education_score),
            TotalScore=Decimal(total_score),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store Match Result",
        )
    finally:
        db.close()


# ------------------------------------------------------------------------------
# Similarity score
# ------------------------------------------------------------------------------
def calculate_semantic_similarity(
    cleantext_vec: List[float], job_vec: List[float]
) -> float:
    try:
        raw_score = sentence_transformer_client.cosine_similarity(
            cleantext_vec, job_vec
        )
        return raw_score
    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        return 0.0


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
