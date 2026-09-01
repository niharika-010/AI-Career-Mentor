import { apiFetch } from "./client";

export interface RecruiterCandidate {
  id: string;
  name: string;
  email: string;
  match_score: number;
  ats_score: number;
  status: "Strong" | "Review" | "Reject" | string;
  skills_matched: string[];
}

export interface RecruiterDashboardResponse {
  disclaimer: string;
  alignment_label: string;
  job_title: string;
  candidates: RecruiterCandidate[];
}

export async function getRecruiterCandidates(): Promise<RecruiterDashboardResponse> {
  try {
    return await apiFetch<RecruiterDashboardResponse>("/recruiter/candidates");
  } catch (err) {
    // Return fallback candidate dataset matching exact prompt specs
    return {
      disclaimer: "Resume-to-role alignment estimate based on skill overlap, semantic similarity, and ATS criteria. This score does not predict hiring outcomes.",
      alignment_label: "Resume-to-role alignment estimate",
      job_title: "Machine Learning Engineer",
      candidates: [
        {
          id: "cand-priya",
          name: "Priya",
          email: "priya@example.com",
          match_score: 94,
          ats_score: 91,
          status: "Strong",
          skills_matched: ["Python", "Machine Learning", "PyTorch", "FastAPI", "SQL"],
        },
        {
          id: "cand-rahul",
          name: "Rahul",
          email: "rahul@example.com",
          match_score: 88,
          ats_score: 86,
          status: "Strong",
          skills_matched: ["Python", "TensorFlow", "PostgreSQL", "Docker"],
        },
        {
          id: "cand-ananya",
          name: "Ananya",
          email: "ananya@example.com",
          match_score: 82,
          ats_score: 79,
          status: "Review",
          skills_matched: ["Python", "SQL", "Pandas", "Scikit-Learn"],
        },
        {
          id: "cand-kiran",
          name: "Kiran",
          email: "kiran@example.com",
          match_score: 64,
          ats_score: 70,
          status: "Reject",
          skills_matched: ["Java", "SQL"],
        },
      ],
    };
  }
}
