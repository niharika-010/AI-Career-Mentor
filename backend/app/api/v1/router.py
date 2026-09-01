from fastapi import APIRouter
from app.api.v1.endpoints import auth, health, resumes, job_descriptions, analysis, guidance, recruiter

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(job_descriptions.router, prefix="/job-descriptions", tags=["Job Descriptions"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(guidance.router, prefix="/guidance", tags=["Guidance AI"])
api_router.include_router(recruiter.router, prefix="/recruiter", tags=["Recruiter Mode"])
