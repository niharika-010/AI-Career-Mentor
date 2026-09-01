from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class ComponentScores(BaseModel):
    """0-100 normalized scores for all 8 scoring components."""
    skills: float = Field(..., ge=0.0, le=100.0)
    semantic_similarity: float = Field(..., ge=0.0, le=100.0)
    experience: float = Field(..., ge=0.0, le=100.0)
    projects: float = Field(..., ge=0.0, le=100.0)
    education: float = Field(..., ge=0.0, le=100.0)
    certifications: float = Field(..., ge=0.0, le=100.0)
    ats: float = Field(..., ge=0.0, le=100.0)
    keywords: float = Field(..., ge=0.0, le=100.0)

    model_config = ConfigDict(from_attributes=True)


class AnalysisConfidence(BaseModel):
    """Deterministic Analysis Confidence metrics (Confidence in analysis quality, NOT hiring probability)."""
    confidence_score: float = Field(..., ge=0.0, le=100.0)
    confidence_level: str = Field(..., description="High, Medium, or Low")
    confidence_reasons: List[str] = Field(default_factory=list, description="Breakdown of factors contributing to confidence rating")

    model_config = ConfigDict(from_attributes=True)


class DeterministicMatchResponse(BaseModel):
    """Unified response for pure backend-calculated deterministic resume match scoring."""
    overall_score: float = Field(..., ge=0.0, le=100.0, description="Weighted total score 0 - 100")
    component_scores: ComponentScores
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    explanations: Dict[str, str] = Field(default_factory=dict, description="Component-by-component deterministic formula explanations")
    analysis_confidence: Optional[AnalysisConfidence] = None
    calculated_at: str = Field(default_factory=str)

    model_config = ConfigDict(from_attributes=True)
