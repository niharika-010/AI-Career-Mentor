import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.models.resume import Resume
from app.models.job import JobDescription
from app.models.skill import Skill, ResumeSkill, JobSkill
from app.models.analysis import AnalysisResult, AnalysisHistory
from app.models.guidance import (
    Report,
    CoverLetter,
    InterviewSession,
    SkillGap,
    CareerRecommendation,
)


@pytest.mark.asyncio
async def test_user_creation(db_session: AsyncSession):
    user = User(
        email="candidate@example.com",
        hashed_password="hashed_pwd_secret",
        full_name="Jane Candidate",
        role=UserRole.CANDIDATE,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.email == "candidate@example.com"
    assert user.role == UserRole.CANDIDATE
    assert user.is_active is True
    assert user.created_at is not None


@pytest.mark.asyncio
async def test_all_13_models_and_relationships(db_session: AsyncSession):
    # 1. User
    user = User(
        email="recruiter@techcorp.com",
        hashed_password="hashed_pwd_recruiter",
        full_name="John Recruiter",
        role=UserRole.RECRUITER,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # 2. Resume
    resume = Resume(
        user_id=user.id,
        file_name="jane_doe_resume.pdf",
        file_path="/storage/resumes/jane_doe_resume.pdf",
        file_type="application/pdf",
        file_size_bytes=1048576,
        parsed_data={"contact": {"email": "jane@example.com"}, "sections": ["Experience", "Education"]},
    )
    db_session.add(resume)
    await db_session.commit()
    await db_session.refresh(resume)

    # 3. Job Description
    job = JobDescription(
        user_id=user.id,
        title="Senior Python Backend Engineer",
        company_name="TechCorp AI",
        raw_text="Looking for a Python engineer with FastAPI, PostgreSQL, and AWS experience.",
        parsed_requirements={"required_skills": ["Python", "FastAPI", "PostgreSQL"], "yoe_required": 5},
    )
    db_session.add(job)
    await db_session.commit()
    await db_session.refresh(job)

    # 4. Skill
    skill = Skill(
        name="Python",
        category="Programming Language",
        description="High-level interpreted programming language",
    )
    db_session.add(skill)
    await db_session.commit()
    await db_session.refresh(skill)

    # 5. ResumeSkill
    resume_skill = ResumeSkill(
        resume_id=resume.id,
        skill_id=skill.id,
        proficiency_level="Expert",
        years_experience=6.0,
    )
    db_session.add(resume_skill)

    # 6. JobSkill
    job_skill = JobSkill(
        job_id=job.id,
        skill_id=skill.id,
        is_required=True,
        minimum_proficiency="Senior",
    )
    db_session.add(job_skill)
    await db_session.commit()

    # 7. AnalysisResult
    analysis = AnalysisResult(
        user_id=user.id,
        resume_id=resume.id,
        job_id=job.id,
        overall_score=88.50,
        skills_score=90.0,
        semantic_score=85.0,
        experience_score=92.0,
        project_score=80.0,
        education_score=100.0,
        certification_score=75.0,
        ats_score=95.0,
        keyword_score=88.0,
        score_details={
            "matched_skills": ["Python", "FastAPI"],
            "missing_skills": ["Docker"],
            "ats_logs": ["Email present", "Clean format"],
        },
    )
    db_session.add(analysis)
    await db_session.commit()
    await db_session.refresh(analysis)

    # 8. AnalysisHistory
    history = AnalysisHistory(
        user_id=user.id,
        analysis_id=analysis.id,
        action="INITIAL_SCREENING",
        notes="Automated ATS screening executed cleanly.",
    )
    db_session.add(history)

    # 9. Report
    report = Report(
        analysis_id=analysis.id,
        file_path="/storage/reports/report_88.pdf",
        file_format="PDF",
    )
    db_session.add(report)

    # 10. CoverLetter
    cover_letter = CoverLetter(
        analysis_id=analysis.id,
        content="Dear Hiring Manager, I am writing to express my strong interest in the Senior Python Engineer role...",
        target_company="TechCorp AI",
    )
    db_session.add(cover_letter)

    # 11. InterviewSession
    interview = InterviewSession(
        analysis_id=analysis.id,
        questions={"technical": ["Explain FastAPI dependency injection", "How do async sessions work in SQLAlchemy 2?"]},
        status="GENERATED",
    )
    db_session.add(interview)

    # 12. SkillGap
    skill_gap = SkillGap(
        analysis_id=analysis.id,
        missing_skills=["Docker", "Kubernetes"],
        recommendations={"course": "Mastering Containerization with Docker"},
    )
    db_session.add(skill_gap)

    # 13. CareerRecommendation
    recommendation = CareerRecommendation(
        user_id=user.id,
        title="Obtain AWS Certified Solutions Architect",
        description="Adding cloud architecture certification will boost match score by 12%.",
        priority="HIGH",
    )
    db_session.add(recommendation)

    await db_session.commit()

    # Async Query with explicit selectinload for relationships
    stmt = (
        select(User)
        .options(
            selectinload(User.resumes),
            selectinload(User.job_descriptions),
            selectinload(User.analyses),
        )
        .where(User.id == user.id)
    )
    queried_user = (await db_session.execute(stmt)).scalar_one()

    assert queried_user.email == "recruiter@techcorp.com"
    assert len(queried_user.resumes) == 1
    assert len(queried_user.job_descriptions) == 1
    assert len(queried_user.analyses) == 1
    assert queried_user.analyses[0].overall_score == 88.50
    assert queried_user.analyses[0].skills_score == 90.0
