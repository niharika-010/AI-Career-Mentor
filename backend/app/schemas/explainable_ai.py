from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.match_scoring import ComponentScores, AnalysisConfidence


class MatchedSkillsExplanation(BaseModel):
    """Evidence-backed explanation for matched skills."""
    score: float = Field(..., ge=0.0, le=100.0)
    evidence: List[str] = Field(default_factory=list, description="Extracted skill evidence from resume and JD")
    explanation: str = Field(..., description="Grounded explanation matching candidate skills to job requirements")
    matched_items: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class MissingSkillsExplanation(BaseModel):
    """Evidence-backed explanation for missing skills."""
    score: float = Field(..., ge=0.0, le=100.0)
    evidence: List[str] = Field(default_factory=list, description="Extracted un-matched requirements from JD")
    explanation: str = Field(..., description="Grounded explanation detailing missing skill gaps")
    missing_items: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ExperienceExplanation(BaseModel):
    """Evidence-backed explanation for experience relevance and YOE."""
    score: float = Field(..., ge=0.0, le=100.0)
    evidence: List[str] = Field(default_factory=list, description="Extracted YOE numbers and duty descriptions")
    explanation: str = Field(..., description="Grounded explanation comparing candidate YOE/roles to job requirements")
    cand_yoe: float = Field(default=0.0)
    job_min_yoe: float = Field(default=0.0)
    seniority_alignment: str = Field(default="Unspecified")

    model_config = ConfigDict(from_attributes=True)


class ProjectExplanation(BaseModel):
    """Evidence-backed explanation for project relevance."""
    score: float = Field(..., ge=0.0, le=100.0)
    evidence: List[str] = Field(default_factory=list, description="Extracted candidate project titles and tech stacks")
    explanation: str = Field(..., description="Grounded explanation assessing practical project relevance")
    relevant_projects: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class EducationExplanation(BaseModel):
    """Evidence-backed explanation for education qualifications."""
    score: float = Field(..., ge=0.0, le=100.0)
    evidence: List[str] = Field(default_factory=list, description="Extracted degree titles and fields of study")
    explanation: str = Field(..., description="Grounded explanation comparing candidate degree to job requirements")
    cand_degree: str = Field(default="Unspecified")
    job_degree: str = Field(default="Unspecified")

    model_config = ConfigDict(from_attributes=True)


class CertificationExplanation(BaseModel):
    """Evidence-backed explanation for certification relevance."""
    score: float = Field(..., ge=0.0, le=100.0)
    evidence: List[str] = Field(default_factory=list, description="Extracted candidate and required certifications")
    explanation: str = Field(..., description="Grounded explanation comparing certifications")
    matched_certs: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ATSExplanation(BaseModel):
    """Evidence-backed explanation for ATS formatting & structure."""
    score: float = Field(..., ge=0.0, le=100.0)
    evidence: List[str] = Field(default_factory=list, description="Extracted formatting readability signals")
    explanation: str = Field(..., description="Grounded explanation of ATS formatting strengths/flaws")
    readability_factors: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class KeywordExplanation(BaseModel):
    """Evidence-backed explanation for technical domain keywords."""
    score: float = Field(..., ge=0.0, le=100.0)
    evidence: List[str] = Field(default_factory=list, description="Extracted technical keywords coverage")
    explanation: str = Field(..., description="Grounded explanation of keyword coverage and density")
    matched_keywords: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ExplainableMatchResponse(BaseModel):
    """Unified Explainable AI Match Response aggregating machine-generated evidence and grounded explanations."""
    overall_score: float = Field(..., ge=0.0, le=100.0)
    component_scores: ComponentScores
    matched_skills_explanation: MatchedSkillsExplanation
    missing_skills_explanation: MissingSkillsExplanation
    experience_explanation: ExperienceExplanation
    project_explanation: ProjectExplanation
    education_explanation: EducationExplanation
    certification_explanation: CertificationExplanation
    ats_explanation: ATSExplanation
    keyword_explanation: KeywordExplanation
    analysis_confidence: Optional[AnalysisConfidence] = None
    calculated_at: str = Field(default_factory=str)

    model_config = ConfigDict(from_attributes=True)
