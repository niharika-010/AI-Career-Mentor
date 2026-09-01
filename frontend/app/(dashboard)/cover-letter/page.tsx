"use client";

import React, { useState } from "react";
import { FileCheck, Sparkles, Copy, Download, Check } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { useToast } from "@/components/ui/Toast";
import { DEMO_ANALYSES, DEMO_JOBS } from "@/lib/demoData";

export default function CoverLetterPage() {
  const { toast } = useToast();
  const [selectedJobId, setSelectedJobId] = useState(DEMO_JOBS[0].id);
  const [coverLetterText, setCoverLetterText] = useState(DEMO_ANALYSES[0].cover_letter);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isCopied, setIsCopied] = useState(false);

  const handleGenerate = () => {
    setIsGenerating(true);
    toast({ title: "Generating Tailored Cover Letter...", description: "Synthesizing target job requirements with candidate experience.", type: "info" });

    setTimeout(() => {
      setIsGenerating(false);
      toast({ title: "Cover Letter Ready!", description: "Tailored for Nexus Artificial Intelligence.", type: "success" });
    }, 1600);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(coverLetterText);
    setIsCopied(true);
    toast({ title: "Cover letter copied to clipboard!", type: "success" });
    setTimeout(() => setIsCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([coverLetterText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Cover_Letter_Nexus_AI.txt";
    a.click();
    toast({ title: "Cover letter file downloaded!", type: "success" });
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <FileCheck className="w-8 h-8 text-cyan-400" />
          <span>Cover Letter Generator</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Draft tailored, professional cover letters matching candidate experience to target company roles.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Settings */}
        <Card className="lg:col-span-1 space-y-4">
          <CardHeader>
            <CardTitle>Configuration</CardTitle>
            <CardDescription>Select target job posting to tailor cover letter context.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Target Job Posting
              </label>
              <select
                value={selectedJobId}
                onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setSelectedJobId(e.target.value)}
                className="w-full px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              >
                {DEMO_JOBS.map((j) => (
                  <option key={j.id} value={j.id}>
                    {j.title} ({j.company_name})
                  </option>
                ))}
              </select>
            </div>

            <Button
              variant="gradient"
              size="md"
              className="w-full"
              isLoading={isGenerating}
              onClick={handleGenerate}
            >
              <Sparkles className="w-4 h-4 mr-2" />
              <span>{isGenerating ? "Synthesizing Letter..." : "Generate Cover Letter"}</span>
            </Button>
          </CardContent>
        </Card>

        {/* Right Column: Generated Letter Preview */}
        <Card className="lg:col-span-2 space-y-4 border-cyan-500/30">
          <CardHeader className="flex flex-row items-center justify-between border-b border-slate-800/80 pb-4">
            <div>
              <CardTitle>Generated Cover Letter</CardTitle>
              <CardDescription>Tailored for Nexus Artificial Intelligence</CardDescription>
            </div>
            <div className="flex space-x-2">
              <Button variant="glass" size="sm" onClick={handleCopy}>
                {isCopied ? <Check className="w-3.5 h-3.5 mr-1 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 mr-1" />}
                <span>{isCopied ? "Copied" : "Copy"}</span>
              </Button>
              <Button variant="outline" size="sm" onClick={handleDownload}>
                <Download className="w-3.5 h-3.5 mr-1" />
                <span>Download .txt</span>
              </Button>
            </div>
          </CardHeader>

          <CardContent>
            <textarea
              value={coverLetterText}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setCoverLetterText(e.target.value)}
              rows={14}
              className="w-full p-5 bg-slate-900/80 border border-slate-800 rounded-xl text-xs text-slate-200 leading-relaxed focus:outline-none focus:ring-2 focus:ring-cyan-500 custom-scrollbar font-mono"
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
