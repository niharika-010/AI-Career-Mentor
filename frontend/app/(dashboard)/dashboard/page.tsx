"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Sparkles, FileText, Briefcase, Layers, ArrowUpRight, TrendingUp, ShieldCheck, CheckCircle2, RotateCcw } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ScoreRing } from "@/components/visualizers/ScoreRing";
import { EmptyState } from "@/components/ui/EmptyState";
import { DEMO_ANALYSES, DEMO_RESUMES, DEMO_JOBS } from "@/lib/demoData";

export default function DashboardPage() {
  const [analyses, setAnalyses] = useState(DEMO_ANALYSES);
  const latestAnalysis = analyses[0];

  return (
    <div className="space-y-8">
      {/* Welcome Hero Banner */}
      <div className="glass-card rounded-2xl p-8 border border-purple-500/30 bg-gradient-to-r from-purple-900/20 via-slate-900/40 to-cyan-900/20 relative overflow-hidden flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-2xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-xs font-semibold text-purple-300 mb-1">
            <ShieldCheck className="w-3.5 h-3.5 text-purple-400" />
            <span>Deterministic Scoring Core Active</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Welcome back to <span className="gradient-text">AI Career Mentor</span>
          </h1>
          <p className="text-sm text-slate-300 leading-relaxed">
            Screen resumes against target job descriptions with zero score hallucination. View exact category sub-scores and actionable AI suggestions.
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <Link href="/analyze">
            <Button variant="gradient" size="md">
              <Layers className="w-4 h-4 mr-2" />
              Run Match Analysis
            </Button>
          </Link>
          <button
            onClick={() => setAnalyses(analyses.length > 0 ? [] : DEMO_ANALYSES)}
            className="text-xs text-slate-400 hover:text-white px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 flex items-center space-x-1.5 transition"
            title="Toggle Empty State View for QA Testing"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>{analyses.length > 0 ? "Test Empty State" : "Restore Demo Data"}</span>
          </button>
        </div>
      </div>

      {/* Overview Stat Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Target Match Score</p>
              <h3 className="text-3xl font-extrabold text-white mt-1">
                {analyses.length > 0 ? `${latestAnalysis.overall_score}%` : "--"}
              </h3>
              <p className="text-xs text-emerald-400 flex items-center mt-1 font-medium">
                <TrendingUp className="w-3.5 h-3.5 mr-1" /> {analyses.length > 0 ? "+14% vs last evaluation" : "No score calculated"}
              </p>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <Sparkles className="w-6 h-6" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Resumes</p>
              <h3 className="text-3xl font-extrabold text-white mt-1">{DEMO_RESUMES.length}</h3>
              <p className="text-xs text-slate-400 mt-1">PDF & DOCX Parsed</p>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
              <FileText className="w-6 h-6" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Target Job Postings</p>
              <h3 className="text-3xl font-extrabold text-white mt-1">{DEMO_JOBS.length}</h3>
              <p className="text-xs text-slate-400 mt-1">Requirements Extracted</p>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Briefcase className="w-6 h-6" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">ATS Pass Rate</p>
              <h3 className="text-3xl font-extrabold text-emerald-400 mt-1">
                {analyses.length > 0 ? "100%" : "--"}
              </h3>
              <p className="text-xs text-slate-400 mt-1">5/5 Rules Passed</p>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <CheckCircle2 className="w-6 h-6" />
            </div>
          </div>
        </Card>
      </div>

      {/* Main Grid: Latest Match Analysis OR Empty State */}
      {analyses.length === 0 ? (
        <EmptyState
          title="No Resume Analyses Yet"
          description="Upload your resume and a job description to receive your first career analysis."
          actionLabel="Analyze My Resume"
          actionHref="/analyze"
          icon={Layers}
        />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left 2 Cols: Latest Evaluation Breakdown */}
          <Card className="lg:col-span-2 space-y-6">
            <CardHeader className="flex flex-row items-center justify-between border-b border-slate-800/80 pb-4">
              <div>
                <CardTitle>Latest Match Analysis</CardTitle>
                <CardDescription>Evaluated against {latestAnalysis.job_title} at {latestAnalysis.company_name}</CardDescription>
              </div>
              <Link href={`/analysis/${latestAnalysis.id}`}>
                <Button variant="outline" size="sm">
                  <span>Full Audit Report</span>
                  <ArrowUpRight className="w-4 h-4 ml-1" />
                </Button>
              </Link>
            </CardHeader>

            <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
              {/* Score Ring */}
              <div className="flex justify-center">
                <ScoreRing score={latestAnalysis.overall_score} size={160} />
              </div>

              {/* Sub-score Summary */}
              <div className="md:col-span-2 space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Key Weight Breakdown</h4>
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                    <span className="text-slate-400">Skills Match (35%)</span>
                    <span className="font-bold text-emerald-400">{latestAnalysis.skills_score}%</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                    <span className="text-slate-400">Semantic Vector (20%)</span>
                    <span className="font-bold text-cyan-400">{latestAnalysis.semantic_score}%</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                    <span className="text-slate-400">Experience YOE (15%)</span>
                    <span className="font-bold text-purple-400">{latestAnalysis.experience_score}%</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                    <span className="text-slate-400">ATS Rules (5%)</span>
                    <span className="font-bold text-emerald-400">{latestAnalysis.ats_score}%</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Right 1 Col: Quick Feature Navigation Cards */}
          <Card className="space-y-4">
            <CardHeader>
              <CardTitle>AI Guidance Tools</CardTitle>
              <CardDescription>Instant career enhancement features</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Link href="/rewriter" className="block p-3.5 rounded-xl glass-card border border-slate-800 hover:border-purple-500/40 transition group">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white group-hover:text-purple-300">Resume Bullet Rewriter</span>
                  <Badge variant="purple">Actionable</Badge>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">Optimize bullet points for maximum impact score.</p>
              </Link>

              <Link href="/cover-letter" className="block p-3.5 rounded-xl glass-card border border-slate-800 hover:border-cyan-500/40 transition group">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white group-hover:text-cyan-300">Cover Letter Generator</span>
                  <Badge variant="info">Tailored</Badge>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">Draft company-specific application letters.</p>
              </Link>

              <Link href="/interview-prep" className="block p-3.5 rounded-xl glass-card border border-slate-800 hover:border-emerald-500/40 transition group">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white group-hover:text-emerald-300">Interview Preparation</span>
                  <Badge variant="success">Q&A Strategy</Badge>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">Role-specific technical & behavioral prep cards.</p>
              </Link>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
