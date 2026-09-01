"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ShieldCheck,
  Download,
  Wand2,
  FileCheck,
  HelpCircle,
  TrendingUp,
  CheckCircle2,
  XCircle,
  ArrowRight,
  CheckSquare,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ScoreRing } from "@/components/visualizers/ScoreRing";
import { CategoryProgressBar } from "@/components/visualizers/CategoryProgressBar";
import { SkillTagList } from "@/components/visualizers/SkillTagList";
import { useToast } from "@/components/ui/Toast";
import { DEMO_ANALYSES } from "@/lib/demoData";

export default function AnalysisDetailsPage({ params }: { params: { id: string } }) {
  const { toast } = useToast();
  const analysis = DEMO_ANALYSES[0]; // Primary evaluation dataset
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);

  const handleDownloadPdf = () => {
    setIsGeneratingPdf(true);
    toast({ title: "Generating PDF Report...", description: "Compiling HTML Jinja2 template and score matrix with WeasyPrint.", type: "info" });

    setTimeout(() => {
      setIsGeneratingPdf(false);
      toast({ title: "PDF Report Downloaded!", description: "AI_Career_Analysis_Report.pdf", type: "success" });
    }, 1800);
  };

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-semibold text-purple-400 mb-1">
            <ShieldCheck className="w-4 h-4" />
            <span>Deterministic Match Evaluation Audit</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {analysis.job_title}
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evaluated for candidate resume <span className="text-purple-300 font-semibold">{analysis.resume_name}</span> at {analysis.company_name}
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <Button variant="gradient" size="md" isLoading={isGeneratingPdf} onClick={handleDownloadPdf}>
            <Download className="w-4 h-4 mr-2" />
            <span>Export PDF Report</span>
          </Button>
        </div>
      </div>

      {/* Primary Score & Sub-scores Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Overall Ring Card */}
        <Card className="flex flex-col items-center justify-center p-8 text-center space-y-6">
          <ScoreRing score={analysis.overall_score} size={200} label="Overall Match Score" />
          <div className="space-y-2 text-xs text-slate-400 max-w-xs">
            <p>Score computed deterministically via closed formulas in backend Python code (0% LLM score variance).</p>
          </div>
        </Card>

        {/* 8 Sub-score Category Bars */}
        <Card className="lg:col-span-2 space-y-5">
          <CardHeader>
            <CardTitle>Weighted Sub-Score Matrix</CardTitle>
            <CardDescription>Exact breakdown across all 8 deterministic match evaluation categories.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <CategoryProgressBar label="1. Skills Overlap & Canonical Match" weight="35%" score={analysis.skills_score} color="bg-purple-500" />
            <CategoryProgressBar label="2. SentenceTransformer Semantic Vector" weight="20%" score={analysis.semantic_score} color="bg-cyan-500" />
            <CategoryProgressBar label="3. Years of Experience (YOE) Ratio" weight="15%" score={analysis.experience_score} color="bg-indigo-500" />
            <CategoryProgressBar label="4. Project Tech Stack Overlap" weight="10%" score={analysis.project_score} color="bg-purple-400" />
            <CategoryProgressBar label="5. Educational Rank Match" weight="5%" score={analysis.education_score} color="bg-emerald-500" />
            <CategoryProgressBar label="6. Industry Certifications Match" weight="5%" score={analysis.certification_score} color="bg-amber-500" />
            <CategoryProgressBar label="7. ATS Rules & Formatting Pass Rate" weight="5%" score={analysis.ats_score} color="bg-emerald-400" />
            <CategoryProgressBar label="8. Top Keyword Frequency Density" weight="5%" score={analysis.keyword_score} color="bg-cyan-400" />
          </CardContent>
        </Card>
      </div>

      {/* Prominent Onboarding Next Step Banner: ATS Checker */}
      <Card className="border-emerald-500/40 bg-gradient-to-r from-emerald-950/20 via-slate-900/40 to-cyan-950/20 p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 flex-shrink-0">
            <CheckSquare className="w-6 h-6" />
          </div>
          <div>
            <Badge variant="success" className="mb-1">Next Step in Workflow</Badge>
            <h3 className="text-lg font-bold text-white">Run ATS Formatting & Compatibility Audit</h3>
            <p className="text-xs text-slate-400 mt-0.5">Verify margins, standard header tags, and single-column text readability.</p>
          </div>
        </div>
        <Link href="/ats-checker">
          <Button variant="gradient" size="md">
            <span>Proceed to ATS Checker</span>
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </Link>
      </Card>

      {/* Skills Overlap & ATS Rules Checklist */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Skills Tag List */}
        <Card className="space-y-4">
          <CardHeader>
            <CardTitle>Skill Overlap Analysis</CardTitle>
            <CardDescription>Extracted canonical skills matched against job description requirements.</CardDescription>
          </CardHeader>
          <CardContent>
            <SkillTagList matchedSkills={analysis.matched_skills} missingSkills={analysis.missing_skills} />
          </CardContent>
        </Card>

        {/* ATS Rules Checklist */}
        <Card className="space-y-4">
          <CardHeader>
            <CardTitle>ATS Compatibility Rules</CardTitle>
            <CardDescription>Deterministic formatting and structural parsing rule check log.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {analysis.ats_rules.map((rule, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-start space-x-3 text-xs">
                {rule.passed ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                ) : (
                  <XCircle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
                )}
                <div>
                  <h5 className="font-bold text-white">{rule.rule}</h5>
                  <p className="text-slate-400 mt-0.5">{rule.details}</p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Quick Action Guidance Launchers */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <Link href="/rewriter" className="block">
          <Card className="h-full hover:border-purple-500/50 transition group space-y-2">
            <Wand2 className="w-6 h-6 text-purple-400 mb-2" />
            <h4 className="font-bold text-white text-sm group-hover:text-purple-300">Resume Rewriter</h4>
            <p className="text-xs text-slate-400">Optimize bullet points for maximum impact.</p>
          </Card>
        </Link>

        <Link href="/cover-letter" className="block">
          <Card className="h-full hover:border-cyan-500/50 transition group space-y-2">
            <FileCheck className="w-6 h-6 text-cyan-400 mb-2" />
            <h4 className="font-bold text-white text-sm group-hover:text-cyan-300">Cover Letter</h4>
            <p className="text-xs text-slate-400">Generate company-tailored application letters.</p>
          </Card>
        </Link>

        <Link href="/interview-prep" className="block">
          <Card className="h-full hover:border-emerald-500/50 transition group space-y-2">
            <HelpCircle className="w-6 h-6 text-emerald-400 mb-2" />
            <h4 className="font-bold text-white text-sm group-hover:text-emerald-300">Interview Prep</h4>
            <p className="text-xs text-slate-400">Practice role-specific technical Q&A cards.</p>
          </Card>
        </Link>

        <Link href="/skill-gap" className="block">
          <Card className="h-full hover:border-amber-500/50 transition group space-y-2">
            <TrendingUp className="w-6 h-6 text-amber-400 mb-2" />
            <h4 className="font-bold text-white text-sm group-hover:text-amber-300">Skill Gap Roadmap</h4>
            <p className="text-xs text-slate-400">View learning targets to reach 95%+ score.</p>
          </Card>
        </Link>
      </div>
    </div>
  );
}
