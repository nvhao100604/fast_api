from sqlalchemy import exists, func
from sqlalchemy.orm import Session

from app.models import Candidate

def get_candidate_by_email(db: Session, email: str):
    return db.query(exists().where(Candidate.Email==email)).scalar()

def get_candidate_by_phone(db: Session, phone: str):
    return db.query(exists().where(Candidate.Phone==phone)).scalar()

def get_candidate_by_id(db: Session, id: int):
    return db.query(exists().where(Candidate.Id==id)).scalar()

def get_candidate(db: Session, id: int):
    return db.query().filter(Candidate.Id==id).first()

def get_candidates(filter: dict, db: Session, skip: int = 0, limit: int = 100):
    query = db.query(Candidate)

    if "FullName" in filter:
        query = query.filter(
            func.unaccent(Candidate.FullName).ilike(func.unaccent(f"%{filter['FullName']}%"))
        )
    if "Email" in filter:
        query = query.filter(Candidate.Email.ilike(f"%{filter['Email']}%"))
    if "Phone" in filter:
        query = query.filter(Candidate.Phone.ilike(f"%{filter['Phone']}%"))
    if "Location" in filter:
        query = query.filter(
            func.unaccent(Candidate.Location).ilike(func.unaccent(f"%{filter['Location']}%"))
        )

    candidates = query.offset(skip).limit(limit).all()
    total = query.count()

    return candidates, total

def post_candidate(candidate: Candidate, db: Session):
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

def update_candidate(candidate_fields: dict, id: int, db: Session):
    candidate = db.query(Candidate).filter(Candidate.Id == id).first()
    if Candidate:
        for key, value in candidate_fields.items():
            setattr(candidate, key, value)
        db.commit()
        db.refresh(candidate)
    return candidate

def delete_candidate(id: int, db: Session):
    candidate = db.query(Candidate).filter(Candidate.Id == id).first()
    if Candidate:
        db.delete(candidate)
        db.commit()
    return candidate