"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export type Theme = "dark" | "light";

interface ThemeState {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      theme: "dark",
      setTheme: (theme) => {
        if (typeof document !== "undefined") {
          if (theme === "light") {
            document.documentElement.classList.add("light");
            document.documentElement.classList.remove("dark");
          } else {
            document.documentElement.classList.add("dark");
            document.documentElement.classList.remove("light");
          }
        }
        set({ theme });
      },
      toggleTheme: () =>
        set((state) => {
          const nextTheme = state.theme === "dark" ? "light" : "dark";
          if (typeof document !== "undefined") {
            if (nextTheme === "light") {
              document.documentElement.classList.add("light");
              document.documentElement.classList.remove("dark");
            } else {
              document.documentElement.classList.add("dark");
              document.documentElement.classList.remove("light");
            }
          }
          return { theme: nextTheme };
        }),
    }),
    {
      name: "theme-storage",
    }
  )
);
