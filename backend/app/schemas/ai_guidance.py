from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


# 1. Resume Summary
class ResumeSummaryRequest(BaseModel):
    resume_text: str = Field(..., description="Raw resume text")
    target_role: Optional[str] = Field(None, description="Optional target job title")


class ResumeSummaryResponse(BaseModel):
    executive_summary: str = Field(..., description="Professional executive summary")
    key_highlights: List[str] = Field(default_factory=list, description="Top 3-5 career achievements")
    suggested_roles: List[str] = Field(default_factory=list, description="Top aligned career roles")

    model_config = ConfigDict(from_attributes=True)


# 2. Rewrite Bullet (Project / Experience)
class RewriteBulletRequest(BaseModel):
    original_text: str = Field(..., description="Original bullet point or paragraph to rewrite")
    target_job_description: Optional[str] = Field(None, description="Target job description context")
    target_role: Optional[str] = Field(None, description="Target role")


class RewriteBulletResponse(BaseModel):
    original_text: str
    rewritten_bullet: str = Field(..., description="Action-oriented, quantified optimized bullet")
    action_verbs_used: List[str] = Field(default_factory=list)
    metrics_highlighted: List[str] = Field(default_factory=list)
    ats_optimization_notes: str = Field(..., description="Explanation of ATS improvements")

    model_config = ConfigDict(from_attributes=True)


# 3. Cover Letter
class CoverLetterRequest(BaseModel):
    resume_text: str
    job_description_text: str
    company_name: Optional[str] = Field("Hiring Manager", description="Company or recipient name")
    job_title: Optional[str] = Field("Target Position", description="Job title")


class CoverLetterResponse(BaseModel):
    salutation: str = Field(default="Dear Hiring Manager,")
    executive_intro: str = Field(..., description="Engaging opening hook and role alignment")
    body_paragraphs: List[str] = Field(default_factory=list, description="1-2 core value proposition paragraphs")
    closing: str = Field(..., description="Professional closing call to action")
    full_cover_letter: str = Field(..., description="Formatted full text cover letter")

    model_config = ConfigDict(from_attributes=True)


# 4. Interview Prep
class InterviewPrepRequest(BaseModel):
    job_title: str
    job_description_text: Optional[str] = None
    candidate_skills: List[str] = Field(default_factory=list)


class InterviewQuestionItem(BaseModel):
    question: str = Field(..., description="Targeted interview question text")
    category: str = Field(..., description="Technical, Behavioral, HR, Project, or Role-specific")
    difficulty: str = Field(default="Intermediate", description="Beginner, Intermediate, or Advanced")
    why_this_question: str = Field(..., description="Grounding rationale linking to JD requirements or candidate background")
    suggested_topics: List[str] = Field(default_factory=list, description="Key concepts, tools, or topics to address")
    recommended_answer_framework: str = Field(..., description="STAR framework tips or technical answer structure")

    model_config = ConfigDict(from_attributes=True)


class InterviewPrepResponse(BaseModel):
    questions: List[InterviewQuestionItem] = Field(default_factory=list, description="Categorized & grounded interview questions")
    technical_questions: List[InterviewQuestionItem] = Field(default_factory=list)
    behavioral_questions: List[InterviewQuestionItem] = Field(default_factory=list)
    star_tips: List[str] = Field(default_factory=list)
    total_questions: int = Field(default=0)

    model_config = ConfigDict(from_attributes=True)


# 5. Skill Gap Roadmap
class SkillGapRoadmapRequest(BaseModel):
    candidate_skills: List[str]
    required_skills: List[str]
    target_role: Optional[str] = "Target Role"


class SkillProficiencyItem(BaseModel):
    skill: str
    proficiency_percentage: int = Field(..., description="0-100 score")
    status: str = Field(default="Mastered", description="Current or Missing")

    model_config = ConfigDict(from_attributes=True)


class WeeklyRoadmapStepItem(BaseModel):
    week_number: int = Field(..., description="1, 2, 3, 4...")
    title: str = Field(..., description="e.g. Docker Fundamentals")
    focus_skills: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)
    project_milestone: str = Field(..., description="e.g. Docker + AWS Project")

    model_config = ConfigDict(from_attributes=True)


class LearningMilestone(BaseModel):
    skill: str
    priority: str = Field(..., description="High, Medium, or Low")
    estimated_weeks: int = Field(default=2)
    recommended_projects: List[str] = Field(default_factory=list)
    free_resources: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class SkillGapRoadmapResponse(BaseModel):
    current_skills_proficiency: List[SkillProficiencyItem] = Field(default_factory=list)
    missing_skills_proficiency: List[SkillProficiencyItem] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    weekly_roadmap: List[WeeklyRoadmapStepItem] = Field(default_factory=list)
    learning_milestones: List[LearningMilestone] = Field(default_factory=list)
    total_estimated_weeks: int = Field(default=4)

    model_config = ConfigDict(from_attributes=True)


# 6. Career Recommendations
class CareerRecommendationsRequest(BaseModel):
    candidate_skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    education_degree: Optional[str] = Field(None, description="e.g. Bachelor's in Computer Science, AI/ML Master's")
    projects: List[str] = Field(default_factory=list)
    experience_years: float = 0.0
    preferred_industry: Optional[str] = Field(None, description="e.g. Artificial Intelligence, Tech, Finance")
    current_title: Optional[str] = None


class CareerRoleRecommendation(BaseModel):
    role_title: str
    fit_percentage: float = Field(..., ge=0.0, le=100.0)
    salary_range_estimate: str = Field(default="Competitive")
    key_reasons: List[str] = Field(default_factory=list)
    evidence_bullets: List[str] = Field(default_factory=list, description="Grounding evidence starting with checkmarks")
    matching_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class CareerRecommendationsResponse(BaseModel):
    recommended_roles: List[CareerRoleRecommendation] = Field(default_factory=list)
    industry_insights: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
