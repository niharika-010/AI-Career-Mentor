"use client";

import React from "react";

interface LogoProps {
  size?: "sm" | "md" | "lg" | "xl";
  showText?: boolean;
  className?: string;
}

export const Logo: React.FC<LogoProps> = ({
  size = "md",
  showText = true,
  className = "",
}) => {
  const iconDimensions = {
    sm: "w-8 h-8",
    md: "w-10 h-10",
    lg: "w-12 h-12",
    xl: "w-16 h-16",
  };

  const textSizes = {
    sm: "text-sm",
    md: "text-base",
    lg: "text-xl",
    xl: "text-2xl",
  };

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      {/* Custom Enterprise AI Career Badge Icon */}
      <div
        className={`relative ${iconDimensions[size]} rounded-2xl bg-gradient-to-tr from-purple-600 via-indigo-600 to-cyan-500 p-[1.5px] shadow-lg shadow-purple-500/25 transition-transform hover:scale-105`}
      >
        <div className="w-full h-full rounded-[14px] bg-slate-950 flex items-center justify-center relative overflow-hidden">
          {/* Subtle Inner Glow */}
          <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/20 to-cyan-500/20 blur-sm"></div>

          {/* SVG Vector Icon: Career Compass & Neural AI Nodes */}
          <svg
            className="w-3/5 h-3/5 relative z-10 text-white"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            {/* Outer Diamond Orbit */}
            <path d="M12 2L2 12l10 10 10-10L12 2z" className="text-purple-400 opacity-80" />
            {/* Inner Career Target Star */}
            <circle cx="12" cy="12" r="3" fill="currentColor" className="text-cyan-400" />
            <path d="M12 6v3M12 15v3M6 12h3M15 12h3" className="text-white" />
          </svg>
        </div>
      </div>

      {/* Brand Text */}
      {showText && (
        <div className="flex flex-col">
          <span className={`font-black tracking-tight gradient-text ${textSizes[size]}`}>
            AI Career Mentor
          </span>
          <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest -mt-0.5">
            Enterprise Screening
          </span>
        </div>
      )}
    </div>
  );
};
