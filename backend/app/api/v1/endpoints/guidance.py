from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.ai_guidance import (
    ResumeSummaryRequest,
    ResumeSummaryResponse,
    RewriteBulletRequest,
    RewriteBulletResponse,
    CoverLetterRequest,
    CoverLetterResponse,
    InterviewPrepRequest,
    InterviewPrepResponse,
    SkillGapRoadmapRequest,
    SkillGapRoadmapResponse,
    CareerRecommendationsRequest,
    CareerRecommendationsResponse,
)
from app.services.gemini import gemini_service

router = APIRouter()


@router.post("/summary", response_model=ResumeSummaryResponse)
def generate_summary(
    payload: ResumeSummaryRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Generates an executive resume summary using Gemini AI service."""
    return gemini_service.generate_resume_summary(payload.resume_text, payload.target_role)


@router.post("/rewrite-project", response_model=RewriteBulletResponse)
def rewrite_project_bullet(
    payload: RewriteBulletRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Rewrites a project description bullet into an action-oriented metric-driven statement."""
    return gemini_service.rewrite_project(payload.original_text, payload.target_job_description)


@router.post("/rewrite-experience", response_model=RewriteBulletResponse)
def rewrite_experience_bullet(
    payload: RewriteBulletRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Rewrites an experience bullet point into an action-oriented metric-driven statement."""
    return gemini_service.rewrite_experience(payload.original_text, payload.target_job_description)


@router.post("/cover-letter", response_model=CoverLetterResponse)
def generate_cover_letter_endpoint(
    payload: CoverLetterRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Generates a tailored executive cover letter."""
    return gemini_service.generate_cover_letter(
        resume_text=payload.resume_text,
        job_description_text=payload.job_description_text,
        company_name=payload.company_name,
        job_title=payload.job_title,
    )


@router.post("/interview-prep", response_model=InterviewPrepResponse)
def generate_interview_prep(
    payload: InterviewPrepRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Generates technical and behavioral interview prep questions with STAR framework guidance."""
    return gemini_service.generate_interview_questions(
        job_title=payload.job_title,
        job_description_text=payload.job_description_text,
        candidate_skills=payload.candidate_skills,
    )


@router.post("/skill-gap", response_model=SkillGapRoadmapResponse)
def generate_skill_gap_roadmap_endpoint(
    payload: SkillGapRoadmapRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Generates a structured learning roadmap for missing skills."""
    return gemini_service.generate_skill_gap_roadmap(
        candidate_skills=payload.candidate_skills,
        required_skills=payload.required_skills,
        target_role=payload.target_role,
    )


@router.post("/recommendations", response_model=CareerRecommendationsResponse)
def generate_career_recommendations_endpoint(
    payload: CareerRecommendationsRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Generates career path recommendations grounded in candidate profile parameters."""
    return gemini_service.generate_career_recommendations(
        candidate_skills=payload.candidate_skills,
        interests=payload.interests,
        education_degree=payload.education_degree,
        projects=payload.projects,
        experience_years=payload.experience_years,
        preferred_industry=payload.preferred_industry,
        current_title=payload.current_title,
    )
