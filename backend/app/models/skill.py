import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.job import JobDescription


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )
    category: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    resume_skills: Mapped[List["ResumeSkill"]] = relationship("ResumeSkill", back_populates="skill", cascade="all, delete-orphan")
    job_skills: Mapped[List["JobSkill"]] = relationship("JobSkill", back_populates="skill", cascade="all, delete-orphan")


class ResumeSkill(Base, TimestampMixin):
    __tablename__ = "resume_skills"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    resume_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    proficiency_level: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    years_experience: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    # Relationships
    resume: Mapped["Resume"] = relationship("Resume", back_populates="resume_skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="resume_skills")


class JobSkill(Base, TimestampMixin):
    __tablename__ = "job_skills"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("job_descriptions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    is_required: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    minimum_proficiency: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    # Relationships
    job_description: Mapped["JobDescription"] = relationship("JobDescription", back_populates="job_skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="job_skills")
