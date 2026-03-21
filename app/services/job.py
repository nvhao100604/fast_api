
from pytest import Session

from app.crud import job as job_crud

def get_job_by_name(db: Session, name: str):
    return job_crud.get_job_by_name(db, name=name)