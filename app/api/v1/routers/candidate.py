
from typing import List
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.v1.schemas.candidate import CandidateBase, CandidateCreate, CandidateFilter, CandidateResponse, CandidateUpdate
from app.api.v1.schemas.response import ResponseSchema
from app.services import candidate_services


router = APIRouter()

@router.get(
    "",
    response_model=ResponseSchema[List[CandidateResponse]],
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ResponseSchema}},
    summary="Get candidate list.",
    description="Retrieve a list of all candidates.",
)
async def get_candidates(
    filter: CandidateFilter,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db : Session = Depends(get_db)
):
    filter_dict = filter.model_dump(exclude_none=True)
    candidates, total = candidate_services.get_candidates(
        filter=filter_dict,
        page=page,
        limit=limit,
        db=db
    )

    return ResponseSchema[List[CandidateResponse]](
        data=candidates,
        message="Get candidate list successfully.",
        meta={
            "page": page,
            "limit": limit,
            "total": total
        }
    )

@router.post(
    "",
    response_model=ResponseSchema[CandidateResponse],
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ResponseSchema}},
    summary="Create candidate.",
    description="Create new candidates add to the database.",
)
async def post_candidate(
    candidate: CandidateCreate,
    db : Session = Depends(get_db)
):
    candidate_data = candidate.model_dump(exclude_unset=True)
    candidate_response = candidate_services.post_candidate(
        candidate=candidate_data,
        db=db
    )
    return ResponseSchema[List[CandidateResponse]](
        data=candidate_response,
        message="Create new candidate successfully."
    )

@router.get(
    "/{id}",
    response_model=ResponseSchema[CandidateResponse],
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ResponseSchema}},
    summary="Get candidate information.",
    description="Get candidate information in the database.",
)
async def get_candidate(
    Id: int = Path(..., ge=1),
    db : Session = Depends(get_db)
):
    candidate_response = candidate_services.get_candidate(
        id=Id,
        db=db
    )
    return ResponseSchema[List[CandidateResponse]](
        data=candidate_response,
        message="Get candidate information successfully."
    )

@router.put(
    "/{id}",
    response_model=ResponseSchema[CandidateResponse],
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ResponseSchema}},
    summary="Update candidate.",
    description="Update candidate information in the database.",
)
async def put_candidate(
    candidate: CandidateBase,
    Id: int = Path(..., ge=1),
    db : Session = Depends(get_db)
):
    candidate_data = candidate.model_dump(exclude_unset=True)
    candidate_response = candidate_services.update_candidate(
        candidate=candidate_data,
        id=Id,
        db=db
    )
    return ResponseSchema[List[CandidateResponse]](
        data=candidate_response,
        message="Update candidate information successfully."
    )

@router.patch(
    "/{id}",
    response_model=ResponseSchema[CandidateResponse],
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ResponseSchema}},
    summary="Update candidate.",
    description="Update candidate information in the database.",
)
async def patch_candidate(
    candidate: CandidateUpdate,
    Id: int = Path(..., ge=1),
    db : Session = Depends(get_db)
):
    candidate_data = candidate.model_dump(exclude_unset=True)
    candidate_response = candidate_services.update_candidate(
        candidate=candidate_data,
        id=Id,
        db=db
    )
    return ResponseSchema[List[CandidateResponse]](
        data=candidate_response,
        message="Update candidate information successfully."
    )

@router.delete(
    "/{id}",
    response_model=ResponseSchema[CandidateResponse],
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ResponseSchema}},
    summary="Delete candidate.",
    description="Delete candidate from the database.",
)
async def delete_candidate(
    Id: int = Path(..., ge=1),
    db : Session = Depends(get_db)
):
    candidate_response = candidate_services.delete_candidate(
        id=Id,
        db=db
    )
    return ResponseSchema[List[CandidateResponse]](
        data=candidate_response,
        message="Delete candidate successfully."
    )
