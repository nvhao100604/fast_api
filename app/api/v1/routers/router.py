from fastapi import APIRouter
from app.api.v1.routers import  applicant, cv, education, experience, health, model_info, skill  , users , auth, application_router, job

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=['Health'])
api_router.include_router(model_info.router, prefix="/model", tags=['Model'])
api_router.include_router(users.router, prefix="/users", tags=['Users'])
api_router.include_router(auth.router, prefix="/auth", tags=['Auth'])
api_router.include_router(job.router, prefix="/jobs", tags=['Jobs'])
api_router.include_router(application_router.router, prefix="/Applications", tags=['Applications Tracking'])

public_router = APIRouter()
public_router.include_router(cv.public_router, prefix="/cvs", tags=['CV'])

private_router = APIRouter()
private_router.include_router(cv.private_router, prefix="/cvs", tags=['CV'])
private_router.include_router(applicant.router, prefix="/applicants", tags=["Applicant Management"])
private_router.include_router(education.router, prefix="/education", tags=['Education'])
private_router.include_router(experience.router, prefix="/experience", tags=['Experience'])
private_router.include_router(skill.router, prefix="/skills", tags=['Skills'])

api_router.include_router(public_router)
api_router.include_router(private_router)


