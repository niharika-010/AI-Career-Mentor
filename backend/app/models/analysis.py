import uuid
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from sqlalchemy import String, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.resume import Resume
    from app.models.job import JobDescription
    from app.models.guidance import Report, CoverLetter, InterviewSession, SkillGap


class AnalysisResult(Base, TimestampMixin):
    __tablename__ = "analysis_results"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    resume_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("job_descriptions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # Deterministic Sub-Scores (All range [0.0, 100.0])
    overall_score: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    skills_score: Mapped[float] = mapped_column(Float, nullable=False)       # 35%
    semantic_score: Mapped[float] = mapped_column(Float, nullable=False)     # 20%
    experience_score: Mapped[float] = mapped_column(Float, nullable=False)   # 15%
    project_score: Mapped[float] = mapped_column(Float, nullable=False)      # 10%
    education_score: Mapped[float] = mapped_column(Float, nullable=False)    # 5%
    certification_score: Mapped[float] = mapped_column(Float, nullable=False)# 5%
    ats_score: Mapped[float] = mapped_column(Float, nullable=False)          # 5%
    keyword_score: Mapped[float] = mapped_column(Float, nullable=False)      # 5%

    # Structured Audit JSON (Matched/Missing skills, keyword frequency map, ATS logs)
    score_details: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="analyses")
    resume: Mapped["Resume"] = relationship("Resume", back_populates="analyses")
    job_description: Mapped["JobDescription"] = relationship("JobDescription", back_populates="analyses")
    
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="analysis", cascade="all, delete-orphan")
    cover_letters: Mapped[List["CoverLetter"]] = relationship("CoverLetter", back_populates="analysis", cascade="all, delete-orphan")
    interview_sessions: Mapped[List["InterviewSession"]] = relationship("InterviewSession", back_populates="analysis", cascade="all, delete-orphan")
    skill_gaps: Mapped[List["SkillGap"]] = relationship("SkillGap", back_populates="analysis", cascade="all, delete-orphan")
    history_entries: Mapped[List["AnalysisHistory"]] = relationship("AnalysisHistory", back_populates="analysis", cascade="all, delete-orphan")


class AnalysisHistory(Base, TimestampMixin):
    __tablename__ = "analysis_history"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    analysis_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("analysis_results.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="analysis_histories")
    analysis: Mapped["AnalysisResult"] = relationship("AnalysisResult", back_populates="history_entries")
