import uuid
import enum
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.job import JobDescription
    from app.models.analysis import AnalysisResult, AnalysisHistory
    from app.models.guidance import CareerRecommendation


class UserRole(str, enum.Enum):
    CANDIDATE = "CANDIDATE"
    RECRUITER = "RECRUITER"
    ADMIN = "ADMIN"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role"),
        default=UserRole.CANDIDATE,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    resumes: Mapped[List["Resume"]] = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    job_descriptions: Mapped[List["JobDescription"]] = relationship("JobDescription", back_populates="user", cascade="all, delete-orphan")
    analyses: Mapped[List["AnalysisResult"]] = relationship("AnalysisResult", back_populates="user", cascade="all, delete-orphan")
    analysis_histories: Mapped[List["AnalysisHistory"]] = relationship("AnalysisHistory", back_populates="user", cascade="all, delete-orphan")
    career_recommendations: Mapped[List["CareerRecommendation"]] = relationship("CareerRecommendation", back_populates="user", cascade="all, delete-orphan")
