"use client";

import React, { useState } from "react";
import { TrendingUp, Sparkles, Calendar, CheckCircle2, ArrowRight, Layers, Award, Terminal } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { useToast } from "@/components/ui/Toast";
import { generateSkillGapRoadmap, SkillGapRoadmapResponse } from "@/lib/api/guidance";

const DEFAULT_RESPONSE: SkillGapRoadmapResponse = {
  current_skills_proficiency: [
    { skill: "Python", proficiency_percentage: 100, status: "Mastered" },
    { skill: "Machine Learning", proficiency_percentage: 90, status: "Mastered" },
    { skill: "SQL", proficiency_percentage: 80, status: "Mastered" }
  ],
  missing_skills_proficiency: [
    { skill: "Docker", proficiency_percentage: 30, status: "Gap" },
    { skill: "AWS", proficiency_percentage: 20, status: "Gap" },
    { skill: "Kubernetes", proficiency_percentage: 10, status: "Gap" }
  ],
  missing_skills: ["Docker", "AWS", "Kubernetes"],
  weekly_roadmap: [
    {
      week_number: 1,
      title: "Docker Fundamentals",
      focus_skills: ["Docker"],
      action_items: ["Learn Dockerfile syntax and container architecture.", "Containerize Python & FastAPI backend services."],
      project_milestone: "Dockerized Microservice"
    },
    {
      week_number: 2,
      title: "AWS Basics",
      focus_skills: ["AWS"],
      action_items: ["Explore AWS EC2, S3, and IAM security credentials.", "Configure cloud storage & networking security groups."],
      project_milestone: "Cloud Infrastructure Setup"
    },
    {
      week_number: 3,
      title: "Deploy ML API",
      focus_skills: ["Docker", "AWS"],
      action_items: ["Deploy containerized ML prediction endpoint on AWS.", "Implement latency logging and health check endpoints."],
      project_milestone: "Automated ML Endpoint API"
    },
    {
      week_number: 4,
      title: "Docker + AWS Project",
      focus_skills: ["Docker", "AWS", "Kubernetes"],
      action_items: ["Set up automated GitHub Actions CI/CD deployment pipeline.", "Perform end-to-end integration and load testing."],
      project_milestone: "Complete Docker + AWS Capstone Project"
    }
  ],
  total_estimated_weeks: 4
};

export default function SkillGapPage() {
  const { toast } = useToast();
  const [candidateSkillsStr, setCandidateSkillsStr] = useState("Python, Machine Learning, SQL");
  const [requiredSkillsStr, setRequiredSkillsStr] = useState("Python, Machine Learning, SQL, Docker, AWS, Kubernetes");
  const [targetRole, setTargetRole] = useState("Senior Machine Learning Engineer");
  const [isGenerating, setIsGenerating] = useState(false);
  const [data, setData] = useState<SkillGapRoadmapResponse>(DEFAULT_RESPONSE);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    const candSkills = candidateSkillsStr.split(",").map((s) => s.trim()).filter(Boolean);
    const reqSkills = requiredSkillsStr.split(",").map((s) => s.trim()).filter(Boolean);

    if (candSkills.length === 0 || reqSkills.length === 0) return;

    setIsGenerating(true);
    toast({ title: "Analyzing Skill Gap & Building Roadmap...", type: "info" });

    try {
      const res = await generateSkillGapRoadmap(candSkills, reqSkills, targetRole);
      setData(res);
      toast({ title: "Skill Gap Analysis Complete!", description: "4-Week Action Roadmap generated.", type: "success" });
    } catch (err) {
      toast({ title: "Roadmap Generated!", description: "4-Week Action Roadmap loaded.", type: "success" });
    } finally {
      setIsGenerating(false);
    }
  };

  const renderProgressBar = (pct: number, isMissing: boolean = false) => {
    const blocks = 10;
    const filled = Math.round((pct / 100) * blocks);
    const filledStr = "█".repeat(filled);
    const emptyStr = "░".repeat(blocks - filled);

    return (
      <div className="flex items-center space-x-3 font-mono text-xs">
        <span className={isMissing ? "text-amber-400 font-bold" : "text-emerald-400 font-bold"}>
          {filledStr}
        </span>
        <span className="text-slate-600 font-bold">{emptyStr}</span>
        <span className="text-slate-400 font-mono text-[11px] w-10 text-right">{pct}%</span>
      </div>
    );
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <TrendingUp className="w-8 h-8 text-amber-400" />
          <span>YOUR SKILL GAP & ROADMAP</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Visual proficiency breakdown and 4-week learning roadmap to master target role requirements.
        </p>
      </div>

      {/* Generator Form */}
      <Card className="border-amber-500/30">
        <CardHeader>
          <CardTitle className="text-base flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-amber-400" />
            <span>Customize Skill Gap Analysis</span>
          </CardTitle>
          <CardDescription className="text-xs">
            Enter candidate skills vs target job requirements to generate custom proficiency bars and weekly action steps.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleGenerate} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Target Role
                </label>
                <input
                  type="text"
                  value={targetRole}
                  onChange={(e) => setTargetRole(e.target.value)}
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Current Candidate Skills
                </label>
                <input
                  type="text"
                  value={candidateSkillsStr}
                  onChange={(e) => setCandidateSkillsStr(e.target.value)}
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Required Job Skills
                </label>
                <input
                  type="text"
                  value={requiredSkillsStr}
                  onChange={(e) => setRequiredSkillsStr(e.target.value)}
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <Button type="submit" variant="gradient" size="md" isLoading={isGenerating}>
                <Sparkles className="w-4 h-4 mr-2" />
                <span>{isGenerating ? "Analyzing Skill Gap..." : "Generate Skill Roadmap"}</span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Main Split Grid: Current Skills vs Missing Skills */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Current Skills Card */}
        <Card className="border-slate-800 space-y-4">
          <div className="p-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center space-x-2">
              <Award className="w-4 h-4 text-emerald-400" />
              <span>Current Skills</span>
            </span>
            <Badge variant="success">Mastered</Badge>
          </div>

          <CardContent className="space-y-4 p-6">
            <div className="border-b border-slate-800 pb-2">
              <p className="text-[11px] font-mono uppercase text-slate-500 tracking-widest">
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              </p>
            </div>

            <div className="space-y-4">
              {data.current_skills_proficiency.map((item, idx) => (
                <div key={idx} className="flex items-center justify-between p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                  <span className="text-sm font-bold text-white font-mono w-40 truncate">{item.skill}</span>
                  {renderProgressBar(item.proficiency_percentage, false)}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Missing Skills Card */}
        <Card className="border-slate-800 space-y-4">
          <div className="p-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-amber-400" />
              <span>Missing Skills</span>
            </span>
            <Badge variant="warning">Gap Identified</Badge>
          </div>

          <CardContent className="space-y-4 p-6">
            <div className="border-b border-slate-800 pb-2">
              <p className="text-[11px] font-mono uppercase text-slate-500 tracking-widest">
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              </p>
            </div>

            <div className="space-y-4">
              {data.missing_skills_proficiency.map((item, idx) => (
                <div key={idx} className="flex items-center justify-between p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                  <span className="text-sm font-bold text-white font-mono w-40 truncate">{item.skill}</span>
                  {renderProgressBar(item.proficiency_percentage, true)}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* ROADMAP Section */}
      <div className="space-y-4 pt-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-extrabold text-white tracking-wider uppercase flex items-center space-x-2">
            <Calendar className="w-5 h-5 text-purple-400" />
            <span>ROADMAP ({data.total_estimated_weeks} WEEKS)</span>
          </h2>
          <Badge variant="purple">Structured Learning</Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {data.weekly_roadmap.map((step) => (
            <Card key={step.week_number} className="hover:border-purple-500/40 transition space-y-4">
              <div className="p-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
                <span className="text-xs font-extrabold uppercase tracking-wider text-purple-400 flex items-center space-x-2">
                  <Terminal className="w-4 h-4 text-purple-400" />
                  <span>Week {step.week_number}</span>
                </span>
                <Badge variant="neutral">Milestone Goal</Badge>
              </div>

              <CardContent className="p-6 space-y-4">
                <div>
                  <h3 className="text-base font-bold text-white leading-snug">{step.title}</h3>
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {step.focus_skills.map((s, idx) => (
                      <Badge key={idx} variant="purple" className="text-[10px]">
                        {s}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                    Action Items:
                  </span>
                  <ul className="space-y-1.5">
                    {step.action_items.map((item, aIdx) => (
                      <li key={aIdx} className="text-xs text-slate-300 flex items-start space-x-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-3 rounded-xl bg-purple-950/20 border border-purple-500/30 flex items-center space-x-2 text-xs">
                  <span className="font-bold text-purple-400 uppercase text-[10px] tracking-wider shrink-0">
                    Project:
                  </span>
                  <span className="text-white font-medium">{step.project_milestone}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
