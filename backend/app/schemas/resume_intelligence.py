from typing import List, Optional, Generic, TypeVar, Any
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class FieldWithConfidence(BaseModel, Generic[T]):
    """Generic wrapper for any extracted field with confidence score and source attribution."""
    value: T
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    source: str = Field(default="heuristic")

    model_config = ConfigDict(from_attributes=True)


class ContactInfo(BaseModel):
    name: FieldWithConfidence[Optional[str]] = Field(
        default_factory=lambda: FieldWithConfidence(value=None, confidence=0.0, source="unknown")
    )
    email: FieldWithConfidence[Optional[str]] = Field(
        default_factory=lambda: FieldWithConfidence(value=None, confidence=0.0, source="unknown")
    )
    phone: FieldWithConfidence[Optional[str]] = Field(
        default_factory=lambda: FieldWithConfidence(value=None, confidence=0.0, source="unknown")
    )
    linkedin_url: FieldWithConfidence[Optional[str]] = Field(
        default_factory=lambda: FieldWithConfidence(value=None, confidence=0.0, source="unknown")
    )
    github_url: FieldWithConfidence[Optional[str]] = Field(
        default_factory=lambda: FieldWithConfidence(value=None, confidence=0.0, source="unknown")
    )
    location: FieldWithConfidence[Optional[str]] = Field(
        default_factory=lambda: FieldWithConfidence(value=None, confidence=0.0, source="unknown")
    )
    portfolio_url: FieldWithConfidence[Optional[str]] = Field(
        default_factory=lambda: FieldWithConfidence(value=None, confidence=0.0, source="unknown")
    )

    model_config = ConfigDict(from_attributes=True)


class SkillItem(BaseModel):
    name: str
    category: str = "technical"  # "technical" or "soft"
    subcategory: Optional[str] = None  # e.g., "languages", "frameworks", "databases", "cloud_devops"
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    source: str = "skills_section"

    model_config = ConfigDict(from_attributes=True)


class EducationItem(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    source: str = "education_section"

    model_config = ConfigDict(from_attributes=True)


class ExperienceItem(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    duration_months: Optional[int] = None
    location: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    source: str = "experience_section"

    model_config = ConfigDict(from_attributes=True)


class ProjectItem(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    url: Optional[str] = None
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    source: str = "projects_section"

    model_config = ConfigDict(from_attributes=True)


class CertificationItem(BaseModel):
    name: str
    issuer: Optional[str] = None
    date: Optional[str] = None
    credential_id: Optional[str] = None
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    source: str = "certifications_section"

    model_config = ConfigDict(from_attributes=True)


class AchievementItem(BaseModel):
    title: str
    description: Optional[str] = None
    date: Optional[str] = None
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    source: str = "achievements_section"

    model_config = ConfigDict(from_attributes=True)


class SpokenLanguageItem(BaseModel):
    language: str
    proficiency: Optional[str] = None  # e.g., "Native", "Fluent", "Intermediate", "Basic"
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    source: str = "languages_section"

    model_config = ConfigDict(from_attributes=True)


class ParsedResumeIntelligence(BaseModel):
    contact: ContactInfo = Field(default_factory=ContactInfo)
    summary: FieldWithConfidence[Optional[str]] = Field(
        default_factory=lambda: FieldWithConfidence(value=None, confidence=0.0, source="unknown")
    )
    skills: List[SkillItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    certifications: List[CertificationItem] = Field(default_factory=list)
    achievements: List[AchievementItem] = Field(default_factory=list)
    languages: List[SpokenLanguageItem] = Field(default_factory=list)
    
    overall_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    extraction_method: str = "deterministic_nlp"  # "deterministic_nlp", "llm_fallback", "hybrid"
    extracted_at: str = Field(default_factory=str)

    model_config = ConfigDict(from_attributes=True)
