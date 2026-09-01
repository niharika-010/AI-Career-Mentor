"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Layers, FileText, Briefcase, Sparkles, ArrowRight, ShieldCheck, CheckCircle2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBarLoader } from "@/components/ui/ProgressBarLoader";
import { useToast } from "@/components/ui/Toast";
import { DEMO_RESUMES, DEMO_JOBS, DEMO_ANALYSES } from "@/lib/demoData";

export default function AnalyzePage() {
  const router = useRouter();
  const { toast } = useToast();

  const [selectedResumeId, setSelectedResumeId] = useState(DEMO_RESUMES[0].id);
  const [selectedJobId, setSelectedJobId] = useState(DEMO_JOBS[0].id);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleRunAnalysis = () => {
    setIsAnalyzing(true);
    toast({ title: "Executing Deterministic Match Engine...", description: "Parsing spaCy entities & computing vector similarity.", type: "info" });
  };

  const handleAnalysisComplete = () => {
    setIsAnalyzing(false);
    toast({ title: "Screening Completed!", description: "Target Overall Match Score: 87.5%", type: "success" });
    router.push(`/analysis/${DEMO_ANALYSES[0].id}`);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <Layers className="w-8 h-8 text-purple-400" />
          <span>Screen & Analyze Match</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Select a candidate resume and target job description to compute deterministic match sub-scores.
        </p>
      </div>

      {/* ASCII Progress Loader Modal/Banner when analyzing */}
      {isAnalyzing && (
        <ProgressBarLoader
          label="Analyzing Resume..."
          durationMs={2500}
          onComplete={handleAnalysisComplete}
          steps={[
            "Step 1/3: Extracting document text stream & spaCy NER skills...",
            "Step 2/3: Computing SentenceTransformer semantic vectors...",
            "Step 3/3: Evaluating 8-category deterministic score matrix...",
          ]}
        />
      )}

      {/* Selector Card */}
      {!isAnalyzing && (
        <Card className="border-purple-500/30">
          <CardHeader>
            <div className="flex items-center space-x-2 text-xs font-semibold text-purple-300">
              <ShieldCheck className="w-4 h-4 text-purple-400" />
              <span>0% LLM Score Variance Guarantee</span>
            </div>
            <CardTitle className="text-xl">Match Configuration</CardTitle>
            <CardDescription>Match formulas use fixed 8-category weights (Skills 35%, Semantic 20%, Experience 15%, Projects 10%, Education 5%, Certifications 5%, ATS 5%, Keywords 5%).</CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* Step 1: Select Resume */}
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-2">
                <FileText className="w-4 h-4 text-purple-400" />
                <span>1. Select Candidate Resume</span>
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {DEMO_RESUMES.map((res) => (
                  <div
                    key={res.id}
                    onClick={() => setSelectedResumeId(res.id)}
                    className={`p-4 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                      selectedResumeId === res.id
                        ? "bg-purple-600/20 border-purple-500 text-white shadow-lg shadow-purple-500/10"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <div className="min-w-0 pr-2">
                      <p className="text-xs font-bold text-white truncate">{res.file_name}</p>
                      <p className="text-[10px] text-slate-400 mt-0.5">{res.experience_years} YOE • {res.skills.length} Extracted Skills</p>
                    </div>
                    {selectedResumeId === res.id && <CheckCircle2 className="w-5 h-5 text-purple-400 flex-shrink-0" />}
                  </div>
                ))}
              </div>
            </div>

            {/* Step 2: Select Job Description */}
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-2">
                <Briefcase className="w-4 h-4 text-cyan-400" />
                <span>2. Select Target Job Description</span>
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {DEMO_JOBS.map((job) => (
                  <div
                    key={job.id}
                    onClick={() => setSelectedJobId(job.id)}
                    className={`p-4 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                      selectedJobId === job.id
                        ? "bg-cyan-600/20 border-cyan-500 text-white shadow-lg shadow-cyan-500/10"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <div className="min-w-0 pr-2">
                      <p className="text-xs font-bold text-white truncate">{job.title}</p>
                      <p className="text-[10px] text-cyan-400 mt-0.5">{job.company_name} ({job.required_yoe}+ YOE Req)</p>
                    </div>
                    {selectedJobId === job.id && <CheckCircle2 className="w-5 h-5 text-cyan-400 flex-shrink-0" />}
                  </div>
                ))}
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-4 border-t border-slate-800">
              <Button
                variant="gradient"
                size="lg"
                className="w-full"
                onClick={handleRunAnalysis}
              >
                <Sparkles className="w-5 h-5 mr-2" />
                <span>Execute Deterministic Match Screening</span>
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
