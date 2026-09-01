import { apiFetch } from "./client";

export interface RewriteBulletResponse {
  original_text: string;
  rewritten_bullet: string;
  action_verbs_used: string[];
  metrics_highlighted: string[];
  ats_optimization_notes: string;
}

export interface CoverLetterResponse {
  salutation: string;
  executive_intro: string;
  body_paragraphs: string[];
  closing: string;
  full_cover_letter: string;
}

export interface InterviewQuestionItem {
  question: string;
  category: "Technical" | "Behavioral" | "HR" | "Project" | "Role-specific" | string;
  difficulty: "Beginner" | "Intermediate" | "Advanced" | string;
  why_this_question: string;
  suggested_topics: string[];
  recommended_answer_framework: string;
}

export interface InterviewPrepResponse {
  questions: InterviewQuestionItem[];
  technical_questions: InterviewQuestionItem[];
  behavioral_questions: InterviewQuestionItem[];
  star_tips: string[];
  total_questions?: number;
}

export async function rewriteBulletPoint(
  originalText: string,
  targetJd?: string,
  type: "project" | "experience" = "project"
): Promise<RewriteBulletResponse> {
  const endpoint = type === "experience" ? "/guidance/rewrite-experience" : "/guidance/rewrite-project";
  return apiFetch<RewriteBulletResponse>(endpoint, {
    method: "POST",
    body: JSON.stringify({
      original_text: originalText,
      target_job_description: targetJd,
    }),
  });
}

export async function generateCoverLetter(
  resumeText: string,
  jobText: string,
  companyName?: string,
  jobTitle?: string
): Promise<CoverLetterResponse> {
  return apiFetch<CoverLetterResponse>("/guidance/cover-letter", {
    method: "POST",
    body: JSON.stringify({
      resume_text: resumeText,
      job_description_text: jobText,
      company_name: companyName,
      job_title: jobTitle,
    }),
  });
}

export interface SkillProficiencyItem {
  skill: string;
  proficiency_percentage: number;
  status: string;
}

export interface WeeklyRoadmapStepItem {
  week_number: number;
  title: string;
  focus_skills: string[];
  action_items: string[];
  project_milestone: string;
}

export interface SkillGapRoadmapResponse {
  current_skills_proficiency: SkillProficiencyItem[];
  missing_skills_proficiency: SkillProficiencyItem[];
  missing_skills: string[];
  weekly_roadmap: WeeklyRoadmapStepItem[];
  total_estimated_weeks: number;
}

export async function generateInterviewPrep(
  jobTitle: string,
  jobDescriptionText?: string,
  candidateSkills: string[] = []
): Promise<InterviewPrepResponse> {
  return apiFetch<InterviewPrepResponse>("/guidance/interview-prep", {
    method: "POST",
    body: JSON.stringify({
      job_title: jobTitle,
      job_description_text: jobDescriptionText,
      candidate_skills: candidateSkills,
    }),
  });
}

export interface CareerRoleRecommendation {
  role_title: string;
  fit_percentage: number;
  salary_range_estimate: string;
  key_reasons: string[];
  evidence_bullets: string[];
  matching_skills: string[];
  missing_skills: string[];
}

export interface CareerRecommendationsResponse {
  recommended_roles: CareerRoleRecommendation[];
  industry_insights: string[];
}

export async function generateSkillGapRoadmap(
  candidateSkills: string[],
  requiredSkills: string[],
  targetRole?: string
): Promise<SkillGapRoadmapResponse> {
  return apiFetch<SkillGapRoadmapResponse>("/guidance/skill-gap", {
    method: "POST",
    body: JSON.stringify({
      candidate_skills: candidateSkills,
      required_skills: requiredSkills,
      target_role: targetRole || "Target Role",
    }),
  });
}

export async function generateCareerRecommendations(
  candidateSkills: string[],
  interests?: string[],
  educationDegree?: string,
  projects?: string[],
  experienceYears: number = 0.0,
  preferredIndustry?: string
): Promise<CareerRecommendationsResponse> {
  return apiFetch<CareerRecommendationsResponse>("/guidance/recommendations", {
    method: "POST",
    body: JSON.stringify({
      candidate_skills: candidateSkills,
      interests: interests || [],
      education_degree: educationDegree,
      projects: projects || [],
      experience_years: experienceYears,
      preferred_industry: preferredIndustry,
    }),
  });
}

export async function downloadAnalysisPdf(payload: Record<string, any>): Promise<void> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const response = await fetch(`${baseUrl}/analysis/pdf`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Failed to generate PDF report.");
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `AI_Career_Mentor_Report_${payload.target_role?.replace(/\s+/g, "_") || "Candidate"}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
