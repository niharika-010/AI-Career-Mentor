"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Users, Filter, ArrowUpRight, Upload, Sparkles, CheckCircle2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Dropzone } from "@/components/ui/Dropzone";
import { useToast } from "@/components/ui/Toast";

export default function RecruiterPage() {
  const { toast } = useToast();
  const [minScore, setMinScore] = useState(70);

  const candidates = [
    { id: "cand-1", name: "Sarah Jenkins", email: "sarah@example.com", score: 87.5, skills_count: 14, yoe: 6.5, status: "Shortlisted" },
    { id: "cand-2", name: "Michael Chang", email: "michael@example.com", score: 78.0, skills_count: 9, yoe: 4.0, status: "Under Review" },
    { id: "cand-3", name: "Elena Rostova", email: "elena@example.com", score: 91.2, skills_count: 18, yoe: 7.0, status: "Top Applicant" },
    { id: "cand-4", name: "David Kim", email: "david@example.com", score: 62.4, skills_count: 6, yoe: 2.5, status: "Unsuitable" },
  ];

  const filteredCandidates = candidates.filter((c) => c.score >= minScore);

  const handleBatchUpload = (file: File) => {
    toast({ title: "Batch Resumes Uploading...", description: file.name, type: "info" });
    setTimeout(() => {
      toast({ title: "Batch Resumes Processed!", description: "4 candidate files parsed & scored against open job vacancy.", type: "success" });
    }, 2000);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <Users className="w-8 h-8 text-purple-400" />
          <span>Recruiter Workspace & Batch Screening</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Screen multiple candidate resumes simultaneously against open enterprise vacancies.
        </p>
      </div>

      {/* Batch Upload Dropzone */}
      <Card>
        <CardHeader>
          <CardTitle>Batch Resume Upload</CardTitle>
          <CardDescription>Upload ZIP or multiple PDF candidate resumes to execute automated batch scoring.</CardDescription>
        </CardHeader>
        <CardContent>
          <Dropzone onFileSelect={handleBatchUpload} label="Upload Multiple Resumes (ZIP / PDF)" />
        </CardContent>
      </Card>

      {/* Scoreboard Table */}
      <Card className="space-y-4">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
          <div>
            <CardTitle>Ranked Candidate Scoreboard</CardTitle>
            <CardDescription>Target Vacancy: Senior AI Full Stack Engineer</CardDescription>
          </div>

          {/* Threshold Filter */}
          <div className="flex items-center space-x-3">
            <span className="text-xs text-slate-400 font-semibold">Min Score:</span>
            <input
              type="range"
              min="50"
              max="90"
              value={minScore}
              onChange={(e) => setMinScore(Number(e.target.value))}
              className="w-32 accent-purple-500 cursor-pointer"
            />
            <span className="text-xs font-bold text-purple-400 w-10">{minScore}%</span>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-900/80 border-b border-slate-800 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                  <th className="p-4">Rank & Candidate</th>
                  <th className="p-4">Extracted YOE</th>
                  <th className="p-4">Skills Count</th>
                  <th className="p-4">Match Score</th>
                  <th className="p-4">Status</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/80 text-xs">
                {filteredCandidates.map((cand, idx) => (
                  <tr key={cand.id} className="hover:bg-slate-900/40 transition">
                    <td className="p-4">
                      <div className="flex items-center space-x-3">
                        <span className="w-6 h-6 rounded-full bg-purple-500/20 text-purple-400 font-extrabold flex items-center justify-center text-[10px]">
                          #{idx + 1}
                        </span>
                        <div>
                          <p className="font-bold text-white">{cand.name}</p>
                          <p className="text-[10px] text-slate-400">{cand.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="p-4 text-slate-300 font-semibold">{cand.yoe} Years</td>
                    <td className="p-4 text-slate-300">{cand.skills_count} Skills</td>
                    <td className="p-4">
                      <Badge variant={cand.score >= 85 ? "success" : cand.score >= 70 ? "warning" : "error"}>
                        {cand.score.toFixed(1)}% Match
                      </Badge>
                    </td>
                    <td className="p-4">
                      <span className="text-[11px] font-bold text-purple-300">{cand.status}</span>
                    </td>
                    <td className="p-4 text-right">
                      <Link href={`/analysis/ans-101`}>
                        <Button variant="glass" size="sm">
                          <span>View Full Profile</span>
                          <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
                        </Button>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
