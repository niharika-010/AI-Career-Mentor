import { apiFetch } from "./client";

export interface UserProfile {
  id: string;
  email: string;
  full_name: string | null;
  role: "CANDIDATE" | "RECRUITER" | "ADMIN";
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: UserProfile;
}

export interface RegisterPayload {
  email: string;
  password: string;
  full_name?: string;
  role?: "CANDIDATE" | "RECRUITER";
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface MsgResponse {
  message: string;
  reset_token?: string;
}

export const authApi = {
  register: (payload: RegisterPayload) =>
    apiFetch<AuthResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  login: (payload: LoginPayload) =>
    apiFetch<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  forgotPassword: (email: string) =>
    apiFetch<MsgResponse>("/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),

  resetPassword: (token: string, new_password: string) =>
    apiFetch<MsgResponse>("/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({ token, new_password }),
    }),

  getMe: () => apiFetch<UserProfile>("/auth/me"),
};
