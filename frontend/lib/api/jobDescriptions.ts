import { API_BASE_URL } from "./client";

export interface ParsedJobRequirements {
  doc_type: string;
  raw_text: string;
  clean_text: string;
  sections: Record<string, string>;
  extracted_skills: string[];
  experience_years: number;
  metadata: {
    word_count: number;
    character_count: number;
    estimated_reading_time_minutes: number;
    section_count: number;
    preprocessed: boolean;
  };
}

export interface JobDescriptionItem {
  id: string;
  user_id: string;
  title: string;
  company_name?: string | null;
  raw_text: string;
  parsed_requirements: ParsedJobRequirements;
  file_name?: string | null;
  file_path?: string | null;
  file_type?: string | null;
  file_size_bytes?: number | null;
  scan_status: string;
  created_at: string;
  updated_at: string;
}

export interface JobDescriptionListResponse {
  items: JobDescriptionItem[];
  total: number;
}

export async function createJobDescriptionJsonApi(
  title: string,
  companyName: string | undefined,
  rawText: string
): Promise<JobDescriptionItem> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE_URL}/job-descriptions/text`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      title,
      company_name: companyName || null,
      raw_text: rawText,
    }),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to create job description");
  return data as JobDescriptionItem;
}

export async function uploadJobDescriptionFileApi(
  file?: File,
  title?: string,
  companyName?: string,
  rawText?: string,
  onProgress?: (percent: number) => void
): Promise<JobDescriptionItem> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${API_BASE_URL}/job-descriptions`);

    if (token) {
      xhr.setRequestHeader("Authorization", `Bearer ${token}`);
    }

    if (xhr.upload && onProgress) {
      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
          const percent = Math.round((event.loaded / event.total) * 100);
          onProgress(percent);
        }
      };
    }

    xhr.onload = () => {
      try {
        const response = JSON.parse(xhr.responseText);
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(response as JobDescriptionItem);
        } else {
          const errorMsg = response.detail || "Upload failed with status " + xhr.status;
          reject(new Error(errorMsg));
        }
      } catch (err) {
        reject(new Error("Invalid JSON response from server"));
      }
    };

    xhr.onerror = () => {
      reject(new Error("Network error during upload"));
    };

    const formData = new FormData();
    if (file) formData.append("file", file);
    if (title) formData.append("title", title);
    if (companyName) formData.append("company_name", companyName);
    if (rawText) formData.append("raw_text", rawText);

    xhr.send(formData);
  });
}

export async function getJobDescriptionsApi(skip = 0, limit = 50): Promise<JobDescriptionListResponse> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE_URL}/job-descriptions?skip=${skip}&limit=${limit}`, { headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to fetch job descriptions");
  return data as JobDescriptionListResponse;
}

export async function getJobDescriptionApi(id: string): Promise<JobDescriptionItem> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE_URL}/job-descriptions/${id}`, { headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to fetch job description");
  return data as JobDescriptionItem;
}

export async function deleteJobDescriptionApi(id: string): Promise<{ message: string; id: string }> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE_URL}/job-descriptions/${id}`, { method: "DELETE", headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to delete job description");
  return data;
}
