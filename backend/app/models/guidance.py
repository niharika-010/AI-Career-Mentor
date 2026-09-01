import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.analysis import AnalysisResult


class Report(Base, TimestampMixin):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    analysis_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("analysis_results.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )
    file_format: Mapped[str] = mapped_column(
        String(20),
        default="PDF",
        nullable=False,
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship
    analysis: Mapped["AnalysisResult"] = relationship("AnalysisResult", back_populates="reports")


class CoverLetter(Base, TimestampMixin):
    __tablename__ = "cover_letters"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    analysis_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("analysis_results.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    target_company: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # Relationship
    analysis: Mapped["AnalysisResult"] = relationship("AnalysisResult", back_populates="cover_letters")


class InterviewSession(Base, TimestampMixin):
    __tablename__ = "interview_sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    analysis_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("analysis_results.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    questions: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="GENERATED",
        nullable=False,
    )

    # Relationship
    analysis: Mapped["AnalysisResult"] = relationship("AnalysisResult", back_populates="interview_sessions")


class SkillGap(Base, TimestampMixin):
    __tablename__ = "skill_gaps"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    analysis_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("analysis_results.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    missing_skills: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    recommendations: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # Relationship
    analysis: Mapped["AnalysisResult"] = relationship("AnalysisResult", back_populates="skill_gaps")


class CareerRecommendation(Base, TimestampMixin):
    __tablename__ = "career_recommendations"

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
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    priority: Mapped[str] = mapped_column(
        String(20),
        default="MEDIUM",
        nullable=False,
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="career_recommendations")
