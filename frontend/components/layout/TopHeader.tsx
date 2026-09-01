"use client";

import React from "react";
import { usePathname } from "next/navigation";
import { Search, Bell, Sun, Moon, ChevronRight, User, Menu } from "lucide-react";
import { useAuthStore } from "@/store/useAuthStore";
import { useThemeStore } from "@/store/useThemeStore";

interface TopHeaderProps {
  onMobileMenuToggle?: () => void;
}

export const TopHeader: React.FC<TopHeaderProps> = ({ onMobileMenuToggle }) => {
  const pathname = usePathname();
  const { user } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();

  const getBreadcrumbs = () => {
    const parts = pathname.split("/").filter(Boolean);
    if (parts.length === 0) return [{ label: "Dashboard", href: "/dashboard" }];
    return parts.map((part, idx) => {
      const href = "/" + parts.slice(0, idx + 1).join("/");
      const label = part.charAt(0).toUpperCase() + part.slice(1).replace("-", " ");
      return { label, href };
    });
  };

  const breadcrumbs = getBreadcrumbs();

  return (
    <header className="h-16 sticky top-0 z-20 glass-card border-b border-slate-800/80 px-4 sm:px-6 flex items-center justify-between backdrop-blur-xl">
      {/* Left Section: Mobile Menu Button + Breadcrumb */}
      <div className="flex items-center space-x-3">
        {onMobileMenuToggle && (
          <button
            onClick={onMobileMenuToggle}
            className="md:hidden text-slate-400 hover:text-white p-2 rounded-xl hover:bg-slate-800/60 transition"
            aria-label="Open Mobile Menu"
          >
            <Menu className="w-5 h-5" />
          </button>
        )}

        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <span className="font-semibold text-slate-400">App</span>
          {breadcrumbs.map((b, i) => (
            <React.Fragment key={i}>
              <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
              <span className={i === breadcrumbs.length - 1 ? "font-bold text-white" : "hover:text-slate-200"}>
                {b.label}
              </span>
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Right Section: Header Actions */}
      <div className="flex items-center space-x-3 sm:space-x-4">
        {/* Search Bar */}
        <div className="relative hidden md:block">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search resumes, jobs..."
            aria-label="Search"
            className="w-56 pl-9 pr-4 py-1.5 bg-slate-900/80 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition"
          />
        </div>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="text-slate-400 hover:text-white p-2 rounded-xl hover:bg-slate-800/60 transition"
          title="Toggle Light / Dark Mode"
          aria-label="Toggle Light / Dark Mode"
        >
          {theme === "dark" ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-purple-400" />}
        </button>

        {/* Notification Bell */}
        <button
          className="relative text-slate-400 hover:text-white p-2 rounded-xl hover:bg-slate-800/60 transition"
          aria-label="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-purple-500 animate-pulse"></span>
        </button>

        {/* User Pill */}
        <div className="flex items-center space-x-2 pl-2 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center text-white text-xs font-bold shadow-md">
            <User className="w-4 h-4" />
          </div>
          <span className="text-xs font-semibold text-white hidden sm:inline-block">{user?.full_name || "Account"}</span>
        </div>
      </div>
    </header>
  );
};
