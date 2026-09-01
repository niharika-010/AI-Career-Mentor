"use client";

import React, { useState } from "react";
import { HelpCircle, ChevronDown, ChevronUp, Sparkles, BookOpen, CheckCircle2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { DEMO_ANALYSES } from "@/lib/demoData";

export default function InterviewPrepPage() {
  const [questions, setQuestions] = useState(DEMO_ANALYSES[0].interview_questions);
  const [expandedIndex, setExpandedIndex] = useState<number | null>(0);

  const toggleExpand = (idx: number) => {
    setExpandedIndex(expandedIndex === idx ? null : idx);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <HelpCircle className="w-8 h-8 text-emerald-400" />
          <span>Interview Preparation</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Role-specific technical, system design, and behavioral interview questions tailored to target job requirements.
        </p>
      </div>

      {/* Questions List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
            Target Role Q&A Strategy Cards ({questions.length})
          </h3>
        </div>

        <div className="space-y-4">
          {questions.map((q, idx) => (
            <Card key={idx} className="hover:border-emerald-500/40 transition">
              <div
                onClick={() => toggleExpand(idx)}
                className="flex items-start justify-between cursor-pointer space-x-4"
              >
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 flex-shrink-0 mt-0.5 font-bold text-xs">
                    Q{idx + 1}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-white leading-snug">{q.question}</h4>
                    <span className="inline-block mt-1">
                      <Badge variant="purple">{q.category}</Badge>
                    </span>
                  </div>
                </div>
                <button className="text-slate-400 hover:text-white p-1">
                  {expandedIndex === idx ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                </button>
              </div>

              {/* Answer Content */}
              {expandedIndex === idx && (
                <div className="pt-4 border-t border-slate-800/80 mt-4 space-y-3">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    Recommended High-Score Answer Strategy:
                  </span>
                  <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-200 leading-relaxed space-y-2">
                    <p>{q.expected_answer}</p>
                  </div>
                </div>
              )}
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
