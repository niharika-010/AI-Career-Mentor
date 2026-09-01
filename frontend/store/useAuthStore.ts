import { create } from "zustand";
import { UserProfile, authApi, LoginPayload, RegisterPayload } from "../lib/api/auth";

interface AuthState {
  user: UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  login: (payload: LoginPayload) => Promise<UserProfile>;
  register: (payload: RegisterPayload) => Promise<UserProfile>;
  logout: () => void;
  fetchMe: () => Promise<UserProfile | null>;
  clearError: () => void;
  setUser: (user: UserProfile | null) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: typeof window !== "undefined" ? localStorage.getItem("access_token") : null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (payload) => {
    set({ isLoading: true, error: null });
    try {
      const data = await authApi.login(payload);
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      set({ user: data.user, token: data.access_token, isAuthenticated: true, isLoading: false });
      return data.user;
    } catch (err: any) {
      set({ error: err.message || "Login failed", isLoading: false });
      throw err;
    }
  },

  register: async (payload) => {
    set({ isLoading: true, error: null });
    try {
      const data = await authApi.register(payload);
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      set({ user: data.user, token: data.access_token, isAuthenticated: true, isLoading: false });
      return data.user;
    } catch (err: any) {
      set({ error: err.message || "Registration failed", isLoading: false });
      throw err;
    }
  },

  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    set({ user: null, token: null, isAuthenticated: false, error: null });
  },

  fetchMe: async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return null;

    set({ isLoading: true });
    try {
      const user = await authApi.getMe();
      set({ user, isAuthenticated: true, isLoading: false });
      return user;
    } catch {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      set({ user: null, token: null, isAuthenticated: false, isLoading: false });
      return null;
    }
  },

  clearError: () => set({ error: null }),
  setUser: (user) => set({ user }),
}));
