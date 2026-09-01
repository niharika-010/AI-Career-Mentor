"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  FileText,
  Briefcase,
  Layers,
  CheckSquare,
  Wand2,
  FileCheck,
  HelpCircle,
  TrendingUp,
  Award,
  History,
  Users,
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  UserCheck,
} from "lucide-react";
import { useAuthStore } from "@/store/useAuthStore";
import { Logo } from "@/components/ui/Logo";

export const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const isRecruiter = user?.role === "RECRUITER";

  const navItems = [
    { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { label: "Resume Analysis", href: "/analyze", icon: Layers },
    { label: "ATS Checker", href: "/ats-checker", icon: CheckSquare },
    { label: "Resume Rewriter", href: "/rewriter", icon: Wand2 },
    { label: "Cover Letter", href: "/cover-letter", icon: FileCheck },
    { label: "Interview Prep", href: "/interview-prep", icon: HelpCircle },
    { label: "Skill Gap", href: "/skill-gap", icon: TrendingUp },
    { label: "Recommendations", href: "/recommendations", icon: Award },
    { label: "Resumes", href: "/resumes", icon: FileText },
    { label: "Job Descriptions", href: "/jobs", icon: Briefcase },
    { label: "History", href: "/history", icon: History },
    ...(isRecruiter ? [{ label: "Recruiter Mode", href: "/recruiter", icon: Users }] : []),
    { label: "Settings", href: "/settings", icon: Settings },
  ];

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <aside
      className={`relative h-screen sticky top-0 flex flex-col glass-card border-r border-slate-800 backdrop-blur-2xl transition-all duration-300 z-30 ${
        isCollapsed ? "w-20" : "w-64"
      }`}
    >
      {/* Brand Header */}
      <div className="p-4 flex items-center justify-between border-b border-slate-800/80">
        <Link href="/dashboard" className="flex items-center overflow-hidden">
          <Logo size="sm" showText={!isCollapsed} />
        </Link>
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-slate-800 transition hidden sm:block"
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Role Badge */}
      {!isCollapsed && (
        <div className="px-5 pt-4">
          <div className="px-3 py-1.5 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center space-x-2 text-xs font-semibold text-purple-300">
            <UserCheck className="w-4 h-4 text-purple-400" />
            <span>{isRecruiter ? "Recruiter Workspace" : "Candidate Account"}</span>
          </div>
        </div>
      )}

      {/* Navigation List */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-1 custom-scrollbar">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition ${
                isActive
                  ? "bg-gradient-to-r from-purple-600/30 to-cyan-600/30 text-white border border-purple-500/40 shadow-md shadow-purple-500/10"
                  : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/60"
              }`}
              title={isCollapsed ? item.label : undefined}
            >
              <Icon className={`w-4 h-4 flex-shrink-0 ${isActive ? "text-purple-400" : "text-slate-400"}`} />
              {!isCollapsed && <span className="truncate">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* User Footer */}
      <div className="p-4 border-t border-slate-800/80">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <div className="flex items-center space-x-3 min-w-0 pr-2">
              <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-purple-600 to-cyan-500 flex items-center justify-center text-white font-bold text-xs shadow-md">
                {user?.full_name ? user.full_name[0].toUpperCase() : "U"}
              </div>
              <div className="flex flex-col min-w-0">
                <span className="text-xs font-bold text-white truncate">{user?.full_name || "Active User"}</span>
                <span className="text-[10px] text-slate-400 truncate">{user?.email || "user@example.com"}</span>
              </div>
            </div>
          )}
          <button
            onClick={handleLogout}
            className="text-slate-400 hover:text-rose-400 p-2 rounded-xl hover:bg-rose-500/10 transition"
            title="Log Out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
};
