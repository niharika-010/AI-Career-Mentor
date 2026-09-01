"use client";

import React from "react";
import { TrendingUp, Clock, BookOpen, Sparkles, CheckCircle2, ArrowRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { DEMO_ANALYSES } from "@/lib/demoData";

export default function SkillGapPage() {
  const roadmap = DEMO_ANALYSES[0].skill_roadmap;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <TrendingUp className="w-8 h-8 text-amber-400" />
          <span>Skill Gap Action Roadmap</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Prioritized learning trajectory designed to elevate target match score from 87.5% to 95%+.
        </p>
      </div>

      {/* Target Progress Card */}
      <Card className="border-amber-500/30 bg-gradient-to-r from-amber-900/10 via-slate-900/40 to-purple-900/10">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <CardTitle>Score Improvement Potential</CardTitle>
            <CardDescription>Completing this 3-week roadmap increases match rank to Tier-1 Candidate.</CardDescription>
          </div>
          <div className="flex items-center space-x-3">
            <div className="text-right">
              <p className="text-[10px] text-slate-400 uppercase font-bold">Current Score</p>
              <p className="text-xl font-bold text-amber-400">87.5%</p>
            </div>
            <ArrowRight className="w-5 h-5 text-slate-600" />
            <div className="text-right">
              <p className="text-[10px] text-slate-400 uppercase font-bold">Target Score</p>
              <p className="text-xl font-bold text-emerald-400">95.0%</p>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Roadmap List */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
          Prioritized Learning Tasks ({roadmap.length})
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {roadmap.map((item, idx) => (
            <Card key={idx} className="flex flex-col justify-between space-y-4 hover:border-amber-500/40 transition">
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <h4 className="text-base font-bold text-white">{item.skill}</h4>
                  <Badge variant={item.priority === "High" ? "error" : "warning"}>
                    {item.priority} Priority
                  </Badge>
                </div>

                <div className="flex items-center space-x-2 text-xs text-slate-400">
                  <Clock className="w-4 h-4 text-amber-400" />
                  <span>Estimated Timeframe: <strong className="text-white">{item.timeframe}</strong></span>
                </div>

                <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center space-x-3 text-xs">
                  <BookOpen className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                  <span className="text-slate-300 font-medium">{item.resource}</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
