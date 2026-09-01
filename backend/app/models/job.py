import uuid
from typing import List, Dict, Any, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.skill import JobSkill
    from app.models.analysis import AnalysisResult


class JobDescription(Base, TimestampMixin):
    __tablename__ = "job_descriptions"

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
        index=True,
    )
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    parsed_requirements: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="job_descriptions")
    job_skills: Mapped[List["JobSkill"]] = relationship("JobSkill", back_populates="job_description", cascade="all, delete-orphan")
    analyses: Mapped[List["AnalysisResult"]] = relationship("AnalysisResult", back_populates="job_description", cascade="all, delete-orphan")
