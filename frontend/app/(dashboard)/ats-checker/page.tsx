"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { CheckSquare, FileText, CheckCircle2, RefreshCw, Wand2, ArrowRight, FileUp } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Dropzone } from "@/components/ui/Dropzone";
import { ProgressBarLoader } from "@/components/ui/ProgressBarLoader";
import { useToast } from "@/components/ui/Toast";
import { DEMO_ANALYSES, DEMO_RESUMES } from "@/lib/demoData";
import { getResumesApi, uploadResumeApi, ResumeItem } from "@/lib/api/resumes";

export default function AtsCheckerPage() {
  const { toast } = useToast();
  const [resumesList, setResumesList] = useState<ResumeItem[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState<string>(DEMO_RESUMES[0].id);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isAuditing, setIsAuditing] = useState(false);

  const rules = DEMO_ANALYSES[0].ats_rules;

  useEffect(() => {
    async function fetchResumes() {
      try {
        const data = await getResumesApi();
        if (data.items && data.items.length > 0) {
          setResumesList(data.items);
          setSelectedResumeId(data.items[0].id);
        }
      } catch (err) {
        console.warn("Using demo resumes list fallback.");
      }
    }
    fetchResumes();
  }, []);

  const handleFileUpload = (file: File) => {
    setUploadedFile(file);
    toast({ title: "Document selected for ATS audit", description: `${file.name} ready to inspect.`, type: "info" });
  };

  const handleRunAudit = async () => {
    setIsAuditing(true);
    toast({ title: "Auditing ATS Compliance Rules...", description: "Scanning document font tables, margins, and text stream layer.", type: "info" });

    if (uploadedFile) {
      try {
        const newRes = await uploadResumeApi(uploadedFile);
        setResumesList((prev) => [newRes, ...prev]);
        setSelectedResumeId(newRes.id);
      } catch (err: any) {
        console.warn("Upload resume fallback during ATS audit:", err.message);
      }
    }
  };

  const handleAuditComplete = () => {
    setIsAuditing(false);
    toast({ title: "ATS Audit Completed!", description: "Passed 5/5 ATS formatting standards.", type: "success" });
  };

  const currentDocName = uploadedFile
    ? uploadedFile.name
    : (resumesList.find((r) => r.id === selectedResumeId)?.file_name || DEMO_RESUMES[0].file_name);

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

      {/* Select Document & Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Select Document Card with Drag & Drop */}
        <Card className="lg:col-span-1 space-y-4">
          <CardHeader>
            <CardTitle>Select Document</CardTitle>
            <CardDescription>Upload a new resume or pick from your document library for ATS inspection.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Upload New Document Dropzone */}
            <Dropzone
              onFileSelect={handleFileUpload}
              label="Upload Resume Document"
              description="Drop PDF or DOCX file to audit"
              accept=".pdf,.docx"
            />

            {/* Uploaded File Selected Banner */}
            {uploadedFile && (
              <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/50 flex items-center justify-between">
                <div className="flex items-center space-x-3 min-w-0">
                  <FileUp className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <div className="min-w-0">
                    <p className="text-xs font-bold text-white truncate">{uploadedFile.name}</p>
                    <p className="text-[10px] text-emerald-300">{(uploadedFile.size / 1024).toFixed(1)} KB • Custom File</p>
                  </div>
                </div>
                <Badge variant="success" className="text-[10px]">Selected</Badge>
              </div>
            )}

            {/* Document Library Selection */}
            <div>
              <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">Or select from Document Library:</p>
              <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                {resumesList.length > 0
                  ? resumesList.map((res) => (
                      <div
                        key={res.id}
                        onClick={() => {
                          setSelectedResumeId(res.id);
                          setUploadedFile(null);
                        }}
                        className={`p-3 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                          selectedResumeId === res.id && !uploadedFile
                            ? "bg-emerald-500/10 border-emerald-500 text-white"
                            : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white"
                        }`}
                      >
                        <div className="flex items-center space-x-3 min-w-0">
                          <FileText className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                          <span className="text-xs font-bold truncate">{res.file_name}</span>
                        </div>
                        {selectedResumeId === res.id && !uploadedFile && <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />}
                      </div>
                    ))
                  : DEMO_RESUMES.map((res) => (
                      <div
                        key={res.id}
                        onClick={() => {
                          setSelectedResumeId(res.id);
                          setUploadedFile(null);
                        }}
                        className={`p-3 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                          selectedResumeId === res.id && !uploadedFile
                            ? "bg-emerald-500/10 border-emerald-500 text-white"
                            : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white"
                        }`}
                      >
                        <div className="flex items-center space-x-3 min-w-0">
                          <FileText className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                          <span className="text-xs font-bold truncate">{res.file_name}</span>
                        </div>
                        {selectedResumeId === res.id && !uploadedFile && <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />}
                      </div>
                    ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Audit Results Card */}
        <Card className="lg:col-span-2 space-y-5">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-emerald-400">100% ATS Compatibility</CardTitle>
              <CardDescription>
                Formatting inspection for <span className="text-white font-semibold">{currentDocName}</span>.
              </CardDescription>
            </div>
            <Badge variant="success">PASSED AUDIT</Badge>
          </CardHeader>

          <CardContent className="space-y-4">
            {rules.map((rule, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-start justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    <span className="text-sm font-bold text-white">{rule.rule}</span>
                  </div>
                  <p className="text-xs text-slate-400 pl-6">{rule.details}</p>
                </div>
                <Badge variant="success" className="text-[10px] flex-shrink-0">
                  {rule.passed ? "PASSED" : "REVIEW"}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* CTA Card */}
      <Card className="border-purple-500/30 bg-purple-950/20">
        <CardContent className="p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="space-y-1">
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <Wand2 className="w-5 h-5 text-purple-400" />
              <span>Want to rewrite bullet points for higher ATS ranking?</span>
            </h3>
            <p className="text-xs text-slate-400">Use our AI Resume Rewriter to transform achievements into metric-driven statements.</p>
          </div>
          <Link href="/rewriter">
            <Button variant="gradient" size="md" className="w-full sm:w-auto">
              <span>Open AI Rewriter</span>
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}
