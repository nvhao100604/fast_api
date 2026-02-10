from sqlalchemy.orm import Session

from app.crud import candidate_crud
from app.models.candidate import Candidate

def get_candidates(db: Session, filter: dict, page: int = 1, limit: int = 100):
    if page < 1 or limit < 1:
        raise ValueError("Page and limit must be a positive integer.")

    skip = (page - 1) * limit
    return candidate_crud.get_candidates(db=db, filter=filter, skip=skip, limit=limit)

def post_candidate(candidate: dict, db: Session):
    if candidate_crud.get_candidate_by_email(db, candidate["Email"])==False:
        raise ValueError("This email has existed.")
    if candidate_crud.get_candidate_by_phone(db, candidate["Phone"])==False:
        raise ValueError("This phone number has existed.")
    
    new_candidate = Candidate(**candidate)
    return candidate_crud.post_candidate(candidate=new_candidate, db=db)

def update_candidate(candidate: dict, db: Session, id: int):
    if candidate_crud.get_candidate_by_id(id)==False:
        raise ValueError(f"No candidate with id={id}.")
    if candidate_crud.get_candidate_by_email(db, candidate["Email"])==False:
        raise ValueError("This email has existed.")
    if candidate_crud.get_candidate_by_phone(db, candidate["Phone"])==False:
        raise ValueError("This phone number has existed.")
    
    return candidate_crud.update_candidate(candidate_fields=candidate, db=db, id=id)

def delete_candidate(db: Session, id: int):
    if candidate_crud.get_candidate_by_id(id)==False:
        raise ValueError(f"No candidate with id={id}.")
    
    return candidate_crud.delete_candidate(db=db, id=id)

def get_candidate(db: Session, id: int):
    if candidate_crud.get_candidate_by_id(id)==False:
        raise ValueError(f"No candidate with id={id}.")
    
    return candidate_crud.get_candidate(db=db, id=id)