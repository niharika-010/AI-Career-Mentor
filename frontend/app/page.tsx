"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ShieldCheck,
  ArrowRight,
  Wand2,
  Users,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { ScoreRing } from "@/components/visualizers/ScoreRing";
import { Logo } from "@/components/ui/Logo";

export default function LandingPage() {
  const [demoScore, setDemoScore] = useState(87.5);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-purple-500 selection:text-white">
      {/* Top Navbar */}
      <header className="sticky top-0 z-50 glass-card border-b border-slate-800/80 backdrop-blur-xl px-6 py-4 flex items-center justify-between">
        <Link href="/">
          <Logo size="md" />
        </Link>

        <div className="flex items-center space-x-4">
          <Link href="/login">
            <Button variant="ghost" size="sm">Log In</Button>
          </Link>
          <Link href="/register">
            <Button variant="gradient" size="sm">Get Started Free</Button>
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative px-6 pt-20 pb-16 max-w-7xl mx-auto text-center space-y-8">
        <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-xs font-semibold text-purple-300">
          <ShieldCheck className="w-4 h-4 text-purple-400" />
          <span>Enterprise ATS Resume Screening Platform</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight max-w-4xl mx-auto leading-[1.1]">
          Screen Resumes with <span className="gradient-text">100% Deterministic Precision</span>
        </h1>

        <p className="text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Zero LLM score hallucination. Mathematical 8-category match formulas combined with spaCy NER entity extraction and Gemini explainable career guidance.
        </p>

        <div className="flex flex-wrap justify-center gap-4 pt-4">
          <Link href="/register">
            <Button variant="gradient" size="lg">
              <span>Launch Candidate Dashboard</span>
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </Link>
          <Link href="/login">
            <Button variant="glass" size="lg">
              <span>Recruiter Portal</span>
            </Button>
          </Link>
        </div>

        {/* Live Playground Widget Preview */}
        <div className="pt-12 max-w-4xl mx-auto">
          <div className="glass-card rounded-3xl p-8 border border-purple-500/30 shadow-2xl bg-gradient-to-b from-slate-900/80 to-slate-950 flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="space-y-4 text-left max-w-md">
              <span className="text-xs font-bold uppercase tracking-wider text-purple-400">Interactive Preview</span>
              <h3 className="text-xl font-bold text-white">8-Category Weighted Sub-Score Matrix</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Matches are calculated mathematically: Skills 35%, Semantic Vector 20%, Experience 15%, Projects 10%, Education 5%, Certifications 5%, ATS Rules 5%, Keywords 5%.
              </p>

              <div className="space-y-2 text-xs font-semibold">
                <div className="flex justify-between text-slate-300">
                  <span>Skills Overlap (35%)</span>
                  <span className="text-emerald-400">92.0%</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Semantic Vector (20%)</span>
                  <span className="text-cyan-400">88.0%</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Experience Ratio (15%)</span>
                  <span className="text-purple-400">95.0%</span>
                </div>
              </div>
            </div>

            <div className="flex justify-center">
              <ScoreRing score={demoScore} size={220} label="Target Job Match Score" />
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="px-6 py-20 max-w-7xl mx-auto space-y-12 border-t border-slate-900">
        <div className="text-center space-y-3">
          <h2 className="text-3xl font-extrabold text-white">Enterprise Feature Architecture</h2>
          <p className="text-xs text-slate-400 max-w-xl mx-auto">Built for modern tech candidates and enterprise recruitment teams.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-3 hover:border-purple-500/40 transition">
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-white">Deterministic Scoring Engine</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Pure Python scoring logic enforces 100% reproducible results. LLMs never make up scores.
            </p>
          </div>

          <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-3 hover:border-cyan-500/40 transition">
            <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
              <Wand2 className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-white">Resume Bullet Rewriter</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Transform weak experience sentences into metric-driven bullet points aligned with target job postings.
            </p>
          </div>

          <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-3 hover:border-emerald-500/40 transition">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Users className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-white">Recruiter Batch Screening</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Rank hundreds of applicant resumes instantly with candidate scoreboard sorting and threshold filters.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-900 px-6 py-8 text-center text-xs text-slate-500">
        <p>© 2026 AI Career Assistant Platform. Built with Next.js, FastAPI, spaCy & Sentence Transformers.</p>
      </footer>
    </div>
  );
}
