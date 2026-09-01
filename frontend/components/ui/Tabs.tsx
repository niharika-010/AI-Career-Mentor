"use client";

import React from "react";
import { motion } from "framer-motion";

export interface TabOption {
  id: string;
  label: string;
  badge?: string | number;
}

interface TabsProps {
  tabs: TabOption[];
  activeTab: string;
  onChange: (id: string) => void;
}

export const Tabs: React.FC<TabsProps> = ({ tabs, activeTab, onChange }) => {
  return (
    <div className="flex space-x-1 p-1.5 bg-slate-900/80 rounded-2xl border border-slate-800">
      {tabs.map((t) => {
        const isActive = activeTab === t.id;
        return (
          <button
            key={t.id}
            onClick={() => onChange(t.id)}
            className={`relative flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition flex items-center justify-center space-x-2 ${
              isActive ? "text-white" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            {isActive && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 bg-gradient-to-r from-purple-600/30 to-cyan-600/30 border border-purple-500/40 rounded-xl shadow-lg"
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
            )}
            <span className="relative z-10">{t.label}</span>
            {t.badge !== undefined && (
              <span
                className={`relative z-10 px-2 py-0.5 rounded-full text-[10px] font-bold ${
                  isActive ? "bg-purple-500 text-white" : "bg-slate-800 text-slate-400"
                }`}
              >
                {t.badge}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
};
