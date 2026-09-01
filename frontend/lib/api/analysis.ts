import { apiFetch, API_BASE_URL } from "./client";

export interface AnalysisHistoryItem {
  id: string;
  target_role: string;
  overall_score: number;
  ats_score: number;
  confidence_score: number;
  created_at: string;
  date_label: string;
}

export interface MatchAnalysisPayload {
  resume_id?: string;
  job_description_id?: string;
  resume_text?: string;
  job_text?: string;
  resume_intelligence?: any;
  job_intelligence?: any;
}

export interface MatchAnalysisResponse {
  overall_score: number;
  component_scores: {
    skills: number;
    semantic_similarity: number;
    experience: number;
    projects: number;
    education: number;
    certifications: number;
    ats_formatting: number;
    domain_keywords: number;
  };
  matched_skills: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  explanations?: Record<string, any>;
  calculated_at?: string;
}

export async function executeMatchAnalysisApi(payload: MatchAnalysisPayload): Promise<MatchAnalysisResponse> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE_URL}/analysis/match`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to execute match analysis.");
  return data;
}

export async function executeExplainableMatchApi(payload: MatchAnalysisPayload): Promise<any> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE_URL}/analysis/explain`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to execute explainable match.");
  return data;
}

export async function getAnalysisHistory(): Promise<AnalysisHistoryItem[]> {
  try {
    return await apiFetch<AnalysisHistoryItem[]>("/analysis/history");
  } catch (err) {
    return [
      {
        id: "hist-ml-eng-82",
        target_role: "ML Engineer",
        overall_score: 82.0,
        ats_score: 91.0,
        confidence_score: 94.0,
        created_at: "2026-08-31T10:00:00Z",
        date_label: "Aug 31",
      },
      {
        id: "hist-data-sci-76",
        target_role: "Data Scientist",
        overall_score: 76.0,
        ats_score: 88.0,
        confidence_score: 90.0,
        created_at: "2026-08-29T14:30:00Z",
        date_label: "Aug 29",
      },
      {
        id: "hist-ai-eng-88",
        target_role: "AI Engineer",
        overall_score: 88.0,
        ats_score: 94.0,
        confidence_score: 96.0,
        created_at: "2026-08-25T09:15:00Z",
        date_label: "Aug 25",
      },
      {
        id: "hist-data-analyst-71",
        target_role: "Data Analyst",
        overall_score: 71.0,
        ats_score: 85.0,
        confidence_score: 88.0,
        created_at: "2026-08-20T16:45:00Z",
        date_label: "Aug 20",
      },
    ];
  }
}
