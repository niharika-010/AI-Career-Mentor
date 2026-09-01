"use client";

import React from "react";
import { motion } from "framer-motion";

interface CategoryProgressBarProps {
  label: string;
  weight: string; // e.g. "35%"
  score: number;  // 0 to 100
  color?: string; // tailwind bg color
}

export const CategoryProgressBar: React.FC<CategoryProgressBarProps> = ({
  label,
  weight,
  score,
  color = "bg-purple-500",
}) => {
  return (
    <div className="space-y-1.5">
      <div className="flex justify-between items-center text-xs font-semibold">
        <span className="text-slate-200 flex items-center space-x-1.5">
          <span>{label}</span>
          <span className="text-[10px] text-slate-400 font-normal">({weight})</span>
        </span>
        <span className="text-white font-bold">{score.toFixed(1)}%</span>
      </div>
      <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${color}`}
          initial={{ width: 0 }}
          animate={{ width: `${Math.min(100, Math.max(0, score))}%` }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
      </div>
    </div>
  );
};
