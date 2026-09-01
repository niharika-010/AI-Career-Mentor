from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class RequirementItem(BaseModel):
    """Extracted job requirement item with category, required/preferred flag, confidence, and source_text."""
    name: str
    category: str  # e.g., "required_skill", "preferred_skill", "responsibility", "tool", "technology", "soft_skill", "certification", "keyword"
    requirement_type: str = "required"  # "required" or "preferred"
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    source_text: str = Field(default="")

    model_config = ConfigDict(from_attributes=True)


class JobExperienceRequirement(BaseModel):
    """Years of experience and seniority level requirements."""
    min_years: float = 0.0
    max_years: Optional[float] = None
    seniority_level: str = "Unspecified"  # "Entry-Level", "Mid-Level", "Senior", "Lead", "Principal", "Executive", "Unspecified"
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    source_text: str = Field(default="")

    model_config = ConfigDict(from_attributes=True)


class JobEducationRequirement(BaseModel):
    """Degree and academic requirements."""
    degree_level: str = "Unspecified"  # "Bachelor's", "Master's", "Ph.D.", "Associate's", "High School", "Equivalent Experience", "Unspecified"
    field_of_study: Optional[str] = None
    requirement_type: str = "required"  # "required" or "preferred"
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    source_text: str = Field(default="")

    model_config = ConfigDict(from_attributes=True)


class ParsedJobIntelligence(BaseModel):
    """Unified normalized Job Description Intelligence schema."""
    job_title: str = "Unspecified Title"
    raw_title: str = "Unspecified Title"
    company_name: Optional[str] = None
    industry: Optional[str] = None

    required_skills: List[RequirementItem] = Field(default_factory=list)
    preferred_skills: List[RequirementItem] = Field(default_factory=list)
    responsibilities: List[RequirementItem] = Field(default_factory=list)

    experience_requirement: JobExperienceRequirement = Field(default_factory=JobExperienceRequirement)
    education_requirement: JobEducationRequirement = Field(default_factory=JobEducationRequirement)
    certifications: List[RequirementItem] = Field(default_factory=list)

    technical_keywords: List[RequirementItem] = Field(default_factory=list)
    soft_skills: List[RequirementItem] = Field(default_factory=list)
    tools: List[RequirementItem] = Field(default_factory=list)
    technologies: List[RequirementItem] = Field(default_factory=list)

    overall_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    extraction_method: str = "deterministic_nlp"  # "deterministic_nlp", "llm_fallback", "hybrid"
    extracted_at: str = Field(default_factory=str)

    model_config = ConfigDict(from_attributes=True)
