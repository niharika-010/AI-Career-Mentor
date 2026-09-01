import { API_BASE_URL } from "./client";

export interface ParsedResumeMetadata {
  word_count: number;
  character_count: number;
  estimated_reading_time_minutes: number;
  section_count: number;
  preprocessed: boolean;
}

export interface ParsedResumeData {
  doc_type: string;
  raw_text: string;
  clean_text: string;
  sections: Record<string, string>;
  extracted_skills: string[];
  experience_years: number;
  metadata: ParsedResumeMetadata;
}

export interface ResumeItem {
  id: string;
  user_id: string;
  file_name: string;
  file_path: string;
  file_type: string;
  file_size_bytes: number;
  scan_status: string;
  parsed_data: ParsedResumeData;
  created_at: string;
  updated_at: string;
}

export interface ResumeListResponse {
  items: ResumeItem[];
  total: number;
}

export async function uploadResumeApi(
  file: File,
  onProgress?: (percent: number) => void
): Promise<ResumeItem> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${API_BASE_URL}/resumes`);

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
          resolve(response as ResumeItem);
        } else {
          const errorMsg = response.detail || "Upload failed with status " + xhr.status;
          reject(new Error(errorMsg));
        }
      } catch (err) {
        reject(new Error("Invalid JSON response from server"));
      }
    };

    xhr.onerror = () => {
      reject(new Error("Network error during file upload"));
    };

    const formData = new FormData();
    formData.append("file", file);
    xhr.send(formData);
  });
}

export async function getResumesApi(skip = 0, limit = 50): Promise<ResumeListResponse> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE_URL}/resumes?skip=${skip}&limit=${limit}`, { headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to fetch resumes");
  return data as ResumeListResponse;
}

export async function getResumeApi(id: string): Promise<ResumeItem> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE_URL}/resumes/${id}`, { headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to fetch resume");
  return data as ResumeItem;
}

export async function deleteResumeApi(id: string): Promise<{ message: string; id: string }> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE_URL}/resumes/${id}`, { method: "DELETE", headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to delete resume");
  return data;
}
