"use client";

import React, { useState } from "react";
import Link from "next/link";
import { CheckSquare, FileText, CheckCircle2, RefreshCw, Wand2, ArrowRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ProgressBarLoader } from "@/components/ui/ProgressBarLoader";
import { useToast } from "@/components/ui/Toast";
import { DEMO_ANALYSES, DEMO_RESUMES } from "@/lib/demoData";

export default function AtsCheckerPage() {
  const { toast } = useToast();
  const [selectedResumeId, setSelectedResumeId] = useState(DEMO_RESUMES[0].id);
  const [isAuditing, setIsAuditing] = useState(false);

  const rules = DEMO_ANALYSES[0].ats_rules;

  const handleRunAudit = () => {
    setIsAuditing(true);
    toast({ title: "Auditing ATS Compliance Rules...", description: "Scanning document font tables, margins, and text stream layer.", type: "info" });
  };

  const handleAuditComplete = () => {
    setIsAuditing(false);
    toast({ title: "ATS Audit Completed!", description: "Passed 5/5 ATS formatting standards.", type: "success" });
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
            <CheckSquare className="w-8 h-8 text-emerald-400" />
            <span>ATS Formatting Checker</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Test candidate resume files against ATS parser rules (Workday, Greenhouse, Taleo compatibility).
          </p>
        </div>

        <Button variant="gradient" size="md" isLoading={isAuditing} onClick={handleRunAudit}>
          <RefreshCw className={`w-4 h-4 mr-2 ${isAuditing ? "animate-spin" : ""}`} />
          <span>Re-Run ATS Audit</span>
        </Button>
      </div>

      {/* Progress Loader Banner */}
      {isAuditing && (
        <ProgressBarLoader
          label="Auditing ATS Resume Rules..."
          durationMs={2000}
          onComplete={handleAuditComplete}
          steps={[
            "Step 1/3: Verifying PDF font tables and text searchability...",
            "Step 2/3: Checking section header standards & word count limits...",
            "Step 3/3: Validating single-column layout structure...",
          ]}
        />
      )}

      {/* Select Resume & Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1 space-y-4">
          <CardHeader>
            <CardTitle>Select Document</CardTitle>
            <CardDescription>Target resume file for formatting rule inspection.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {DEMO_RESUMES.map((res) => (
              <div
                key={res.id}
                onClick={() => setSelectedResumeId(res.id)}
                className={`p-3.5 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                  selectedResumeId === res.id
                    ? "bg-emerald-500/10 border-emerald-500 text-white"
                    : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                <div className="flex items-center space-x-3 min-w-0">
                  <FileText className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span className="text-xs font-bold truncate">{res.file_name}</span>
                </div>
                {selectedResumeId === res.id && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Audit Results Card */}
        <Card className="lg:col-span-2 space-y-5">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-emerald-400">100% ATS Compatibility</CardTitle>
              <CardDescription>All 5 deterministic ATS formatting standards verified.</CardDescription>
            </div>
            <Badge variant="success">PASSED AUDIT</Badge>
          </CardHeader>

          <CardContent className="space-y-4">
            {rules.map((item, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-start space-x-4">
                <div className="w-8 h-8 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 flex-shrink-0 mt-0.5">
                  <CheckCircle2 className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-bold text-white">{item.rule}</h4>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">{item.details}</p>
                </div>
                <Badge variant="success">PASS</Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Prominent Onboarding Next Step Banner: Resume Bullet Rewriter */}
      <Card className="border-purple-500/40 bg-gradient-to-r from-purple-950/20 via-slate-900/40 to-cyan-950/20 p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 flex-shrink-0">
            <Wand2 className="w-6 h-6" />
          </div>
          <div>
            <Badge variant="purple" className="mb-1">Next Step in Workflow</Badge>
            <h3 className="text-lg font-bold text-white">Optimize Bullet Points with Resume Rewriter</h3>
            <p className="text-xs text-slate-400 mt-0.5">Inject action verbs, quantified metrics, and target job keywords.</p>
          </div>
        </div>
        <Link href="/rewriter">
          <Button variant="gradient" size="md">
            <span>Proceed to Resume Rewriter</span>
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </Link>
      </Card>
    </div>
  );
}
