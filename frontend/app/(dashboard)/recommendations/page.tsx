"use client";

import React from "react";
import { Award, DollarSign, Target, Briefcase, ArrowUpRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

export default function RecommendationsPage() {
  const recommendations = [
    {
      title: "Senior AI Full Stack Engineer",
      match_pct: 92,
      salary_range: "$140,000 - $185,000 / yr",
      key_fit: "High overlap with Python FastAPI, TypeScript, and Docker containerization.",
      demand: "Very High",
    },
    {
      title: "Lead Backend Systems Architect",
      match_pct: 88,
      salary_range: "$155,000 - $200,000 / yr",
      key_fit: "Strong experience ratio with PostgreSQL async architectures.",
      demand: "High",
    },
    {
      title: "DevOps & Cloud Integration Specialist",
      match_pct: 78,
      salary_range: "$130,000 - $170,000 / yr",
      key_fit: "Requires adding Kubernetes & Terraform infrastructure skills.",
      demand: "Moderate",
    },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <Award className="w-8 h-8 text-purple-400" />
          <span>Career Path Recommendations</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Automated target job role matching based on your canonical skill graph and experience YOE profile.
        </p>
      </div>

      {/* Roles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {recommendations.map((role, idx) => (
          <Card key={idx} className="flex flex-col justify-between space-y-4 hover:border-purple-500/40 transition">
            <div className="space-y-3">
              <div className="flex items-start justify-between">
                <Badge variant="purple">{role.match_pct}% Profile Match</Badge>
                <Badge variant="info">{role.demand} Demand</Badge>
              </div>

              <h4 className="text-base font-bold text-white leading-snug">{role.title}</h4>

              <div className="flex items-center space-x-2 text-xs text-emerald-400 font-bold">
                <DollarSign className="w-4 h-4" />
                <span>{role.salary_range}</span>
              </div>

              <p className="text-xs text-slate-300 bg-slate-900/60 p-3 rounded-xl border border-slate-800 leading-relaxed">
                {role.key_fit}
              </p>
            </div>

            <div className="pt-3 border-t border-slate-800/80 flex justify-end">
              <Button variant="glass" size="sm">
                <span>View Job Board Matches</span>
                <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
