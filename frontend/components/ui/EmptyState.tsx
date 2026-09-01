"use client";

import React from "react";
import Link from "next/link";
import { Sparkles, ArrowRight, LucideIcon } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionLabel?: string;
  actionHref?: string;
  onAction?: () => void;
  icon?: LucideIcon;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = "No Resume Analyses Yet",
  description = "Upload your resume and a job description to receive your first career analysis.",
  actionLabel = "Analyze My Resume",
  actionHref = "/analyze",
  onAction,
  icon: Icon = Sparkles,
}) => {
  return (
    <Card className="p-12 text-center flex flex-col items-center justify-center space-y-5 border-dashed border-slate-800 bg-slate-900/30">
      {/* Icon Badge */}
      <div className="w-16 h-16 rounded-3xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 shadow-xl shadow-purple-500/10">
        <Icon className="w-8 h-8" />
      </div>

      {/* Text */}
      <div className="space-y-2 max-w-sm">
        <h3 className="text-xl font-extrabold text-white tracking-tight">{title}</h3>
        <p className="text-xs text-slate-400 leading-relaxed">{description}</p>
      </div>

      {/* CTA Button */}
      {actionHref ? (
        <Link href={actionHref}>
          <Button variant="gradient" size="md">
            <span>{actionLabel}</span>
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </Link>
      ) : onAction ? (
        <Button variant="gradient" size="md" onClick={onAction}>
          <span>{actionLabel}</span>
          <ArrowRight className="w-4 h-4 ml-2" />
        </Button>
      ) : null}
    </Card>
  );
};
