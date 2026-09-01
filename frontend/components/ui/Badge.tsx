import React from "react";
import { clsx } from "clsx";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "success" | "warning" | "error" | "info" | "neutral" | "purple";
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = "neutral", className, ...props }) => {
  const variants = {
    success: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    warning: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    error: "bg-rose-500/10 text-rose-400 border-rose-500/30",
    info: "bg-cyan-500/10 text-cyan-400 border-cyan-500/30",
    purple: "bg-purple-500/10 text-purple-400 border-purple-500/30",
    neutral: "bg-slate-800/80 text-slate-300 border-slate-700",
  };

  return (
    <span
      className={clsx(
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border backdrop-blur-md",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};
