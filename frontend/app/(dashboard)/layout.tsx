"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { ToastProvider } from "@/components/ui/Toast";
import { useThemeStore } from "@/store/useThemeStore";
import { X } from "lucide-react";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const { theme } = useThemeStore();

  useEffect(() => {
    if (theme === "light") {
      document.documentElement.classList.add("light");
      document.documentElement.classList.remove("dark");
    } else {
      document.documentElement.classList.add("dark");
      document.documentElement.classList.remove("light");
    }
  }, [theme]);

  return (
    <ToastProvider>
      <div className="flex min-h-screen bg-slate-950 text-slate-100 selection:bg-purple-500 selection:text-white">
        {/* Desktop Sidebar */}
        <div className="hidden md:block">
          <Sidebar />
        </div>

        {/* Mobile Slide-Over Drawer */}
        {isMobileOpen && (
          <div className="fixed inset-0 z-50 flex md:hidden">
            <div
              className="fixed inset-0 bg-slate-950/80 backdrop-blur-md"
              onClick={() => setIsMobileOpen(false)}
            />
            <div className="relative flex-1 max-w-xs w-full bg-slate-900 border-r border-slate-800 z-10">
              <button
                onClick={() => setIsMobileOpen(false)}
                className="absolute top-4 right-4 text-slate-400 hover:text-white p-2"
                aria-label="Close Mobile Menu"
              >
                <X className="w-5 h-5" />
              </button>
              <Sidebar />
            </div>
          </div>
        )}

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0">
          <TopHeader onMobileMenuToggle={() => setIsMobileOpen(true)} />
          <main className="flex-1 p-4 sm:p-6 md:p-8 overflow-y-auto">{children}</main>
        </div>
      </div>
    </ToastProvider>
  );
}
