"use client";

import React from "react";
import { motion } from "framer-motion";

interface ScoreRingProps {
  score?: number; // 0 to 100
  size?: number; // ring dimension in px
  strokeWidth?: number;
  label?: string;
}

export const ScoreRing: React.FC<ScoreRingProps> = ({
  score = 0,
  size = 180,
  strokeWidth = 14,
  label = "Overall Match Score",
}) => {
  const safeScore = typeof score === "number" && !isNaN(score) ? score : 0;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (safeScore / 100) * circumference;

  let strokeColor = "stroke-emerald-400";
  let textColor = "text-emerald-400";
  let bgGlow = "shadow-emerald-500/20";

  if (safeScore < 60) {
    strokeColor = "stroke-rose-400";
    textColor = "text-rose-400";
    bgGlow = "shadow-rose-500/20";
  } else if (safeScore < 75) {
    strokeColor = "stroke-amber-400";
    textColor = "text-amber-400";
    bgGlow = "shadow-amber-500/20";
  }

  return (
    <div className="flex flex-col items-center justify-center text-center">
      <div className={`relative flex items-center justify-center rounded-full p-2 ${bgGlow}`} style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background Ring */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            className="stroke-slate-800"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Animated Progress Ring */}
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            className={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>
        {/* Score Value Center */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-4xl font-extrabold tracking-tight ${textColor}`}>
            {safeScore.toFixed(1)}%
          </span>
          <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mt-0.5">
            {safeScore >= 75 ? "Strong Match" : safeScore >= 60 ? "Moderate Match" : "Low Match"}
          </span>
        </div>
      </div>
      {label && <p className="text-xs font-semibold text-slate-300 mt-3">{label}</p>}
    </div>
  );
};
