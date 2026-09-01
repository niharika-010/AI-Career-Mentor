from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class MatchItem(BaseModel):
    """Represents a pair match between a resume item and job requirement with score and explanation."""
    resume_item: str
    job_requirement: str
    similarity: float = Field(..., ge=0.0, le=1.0, description="Raw cosine similarity score 0.0 - 1.0")
    score: float = Field(..., ge=0.0, le=100.0, description="Normalized match score 0 - 100")
    match: bool = Field(..., description="True if similarity >= threshold")
    explanation: str = Field(..., description="Detailed human-readable explanation of why the match occurred or failed")

    model_config = ConfigDict(from_attributes=True)


class DomainMatchResult(BaseModel):
    """Match results for a specific domain (Skills, Experience, Projects, Education, Certifications)."""
    domain: str
    score: float = Field(..., ge=0.0, le=100.0)
    weight: float = Field(default=1.0)
    matched_items: List[MatchItem] = Field(default_factory=list)
    unmatched_requirements: List[str] = Field(default_factory=list)
    summary: str = Field(default="")

    model_config = ConfigDict(from_attributes=True)


class SemanticMatchRequest(BaseModel):
    """Input payload for semantic matching request."""
    resume_id: Optional[str] = None
    job_description_id: Optional[str] = None
    resume_text: Optional[str] = None
    job_text: Optional[str] = None
    resume_intelligence: Optional[Dict[str, Any]] = None
    job_intelligence: Optional[Dict[str, Any]] = None


class SemanticMatchResponse(BaseModel):
    """Unified response model for semantic resume-job matching."""
    overall_score: float = Field(..., ge=0.0, le=100.0)
    match_grade: str = Field(..., description="e.g. Excellent Match, Strong Match, Good Match, Moderate Match, Low Match")
    skill_match: DomainMatchResult
    experience_match: DomainMatchResult
    project_match: DomainMatchResult
    education_match: DomainMatchResult
    certification_match: DomainMatchResult
    key_strengths: List[str] = Field(default_factory=list)
    missing_gaps: List[str] = Field(default_factory=list)
    matched_at: str = Field(default_factory=str)

    model_config = ConfigDict(from_attributes=True)
