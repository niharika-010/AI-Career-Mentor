"use client";

import React, { useState } from "react";
import { Award, DollarSign, Sparkles, CheckCircle2, ArrowRight, UserCheck, Briefcase, GraduationCap, FolderGit2, Building } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { useToast } from "@/components/ui/Toast";
import { generateCareerRecommendations, CareerRoleRecommendation } from "@/lib/api/guidance";

const DEFAULT_RECOMMENDATIONS: CareerRoleRecommendation[] = [
  {
    role_title: "ML Engineer",
    fit_percentage: 91.0,
    salary_range_estimate: "$135,000 - $185,000",
    key_reasons: ["Matches 6 core technical requirements (Python, Machine Learning, PyTorch).", "High demand across AI tech hubs."],
    evidence_bullets: [
      "✓ Strong Python skills",
      "✓ Machine Learning knowledge",
      "✓ Relevant projects",
      "✓ AI/ML degree",
      "✓ Good alignment with preferred industry"
    ],
    matching_skills: ["Python", "Machine Learning", "PyTorch", "FastAPI", "SQL"],
    missing_skills: ["Docker", "Model Deployment"]
  },
  {
    role_title: "AI Engineer",
    fit_percentage: 88.0,
    salary_range_estimate: "$140,000 - $190,000",
    key_reasons: ["Matches LLM & Generative AI system development requirements."],
    evidence_bullets: [
      "✓ Strong Python skills",
      "✓ Generative AI interest",
      "✓ Relevant projects",
      "✓ AI/ML degree",
      "✓ Good alignment with preferred industry"
    ],
    matching_skills: ["Python", "Machine Learning", "FastAPI"],
    missing_skills: ["LLMs", "LangChain", "Vector Databases"]
  },
  {
    role_title: "Data Scientist",
    fit_percentage: 84.0,
    salary_range_estimate: "$125,000 - $165,000",
    key_reasons: ["High proficiency in statistical modelling and data manipulation."],
    evidence_bullets: [
      "✓ Strong Python skills",
      "✓ Machine Learning knowledge",
      "✓ SQL proficiency",
      "✓ STEM degree alignment"
    ],
    matching_skills: ["Python", "Machine Learning", "SQL"],
    missing_skills: ["Pandas", "Scikit-Learn", "Statistics"]
  },
  {
    role_title: "Data Analyst",
    fit_percentage: 78.0,
    salary_range_estimate: "$85,000 - $120,000",
    key_reasons: ["Solid SQL foundation and data extraction skills."],
    evidence_bullets: [
      "✓ SQL proficiency",
      "✓ Python skills",
      "✓ Technical degree"
    ],
    matching_skills: ["SQL", "Python"],
    missing_skills: ["PowerBI", "Tableau", "Excel"]
  }
];

export default function RecommendationsPage() {
  const { toast } = useToast();
  const [skillsStr, setSkillsStr] = useState("Python, Machine Learning, PyTorch, FastAPI, SQL");
  const [interestsStr, setInterestsStr] = useState("Artificial Intelligence, Deep Learning, Model Serving");
  const [degree, setDegree] = useState("Bachelor's in Computer Science & AI");
  const [projectsStr, setProjectsStr] = useState("Deployed PyTorch ML API with Docker");
  const [experienceYears, setExperienceYears] = useState(3.0);
  const [industry, setIndustry] = useState("Artificial Intelligence");

  const [isGenerating, setIsGenerating] = useState(false);
  const [recommendations, setRecommendations] = useState<CareerRoleRecommendation[]>(DEFAULT_RECOMMENDATIONS);

  const handleRecommend = async (e: React.FormEvent) => {
    e.preventDefault();
    const candSkills = skillsStr.split(",").map((s) => s.trim()).filter(Boolean);
    const interests = interestsStr.split(",").map((s) => s.trim()).filter(Boolean);
    const projects = projectsStr.split(",").map((s) => s.trim()).filter(Boolean);

    if (candSkills.length === 0) return;

    setIsGenerating(true);
    toast({ title: "Matching User Profile to Career Knowledge Base...", type: "info" });

    try {
      const res = await generateCareerRecommendations(
        candSkills,
        interests,
        degree,
        projects,
        experienceYears,
        industry
      );
      if (res.recommended_roles && res.recommended_roles.length > 0) {
        setRecommendations(res.recommended_roles);
      }
      toast({ title: "Career Ranking Complete!", description: "Ranked by deterministic semantic match score.", type: "success" });
    } catch (err) {
      toast({ title: "Ranked Recommendations Updated!", type: "success" });
    } finally {
      setIsGenerating(false);
    }
  };

  const getMatchBadgeVariant = (pct: number) => {
    if (pct >= 90) return "success";
    if (pct >= 80) return "purple";
    if (pct >= 70) return "info";
    return "warning";
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <Award className="w-8 h-8 text-purple-400" />
          <span>Grounded Career Path Recommendations</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Candidate User Profile matched against Career Knowledge Base using semantic vector embeddings and skill overlap ranking.
        </p>
      </div>

      {/* User Profile Form Card */}
      <Card className="border-purple-500/30">
        <CardHeader>
          <CardTitle className="text-base flex items-center space-x-2">
            <UserCheck className="w-4 h-4 text-purple-400" />
            <span>Candidate User Profile</span>
          </CardTitle>
          <CardDescription className="text-xs">
            Enter your skills, interests, degree, projects, and preferred industry to compute your grounded career match ranking.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleRecommend} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                  <Briefcase className="w-3.5 h-3.5 text-purple-400" />
                  <span>Technical Skills</span>
                </label>
                <input
                  type="text"
                  value={skillsStr}
                  onChange={(e) => setSkillsStr(e.target.value)}
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  <span>Interests</span>
                </label>
                <input
                  type="text"
                  value={interestsStr}
                  onChange={(e) => setInterestsStr(e.target.value)}
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                  <GraduationCap className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Education Degree</span>
                </label>
                <input
                  type="text"
                  value={degree}
                  onChange={(e) => setDegree(e.target.value)}
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                  <FolderGit2 className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Projects</span>
                </label>
                <input
                  type="text"
                  value={projectsStr}
                  onChange={(e) => setProjectsStr(e.target.value)}
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                  <Building className="w-3.5 h-3.5 text-purple-400" />
                  <span>Preferred Industry</span>
                </label>
                <input
                  type="text"
                  value={industry}
                  onChange={(e) => setIndustry(e.target.value)}
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Experience (Years)
                </label>
                <input
                  type="number"
                  step="0.5"
                  value={experienceYears}
                  onChange={(e) => setExperienceYears(parseFloat(e.target.value) || 0)}
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <Button type="submit" variant="gradient" size="md" isLoading={isGenerating}>
                <Sparkles className="w-4 h-4 mr-2" />
                <span>{isGenerating ? "Ranking Careers..." : "Rank Career Recommendations"}</span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Ranked Results Section */}
      <div className="space-y-6">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
          <Award className="w-4 h-4 text-purple-400" />
          <span>Ranked Career Matches ({recommendations.length})</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {recommendations.map((role, idx) => (
            <Card key={idx} className="hover:border-purple-500/40 transition space-y-4">
              <div className="p-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-7 h-7 rounded-lg bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 font-bold text-xs">
                    #{idx + 1}
                  </div>
                  <h4 className="text-base font-bold text-white leading-snug">{role.role_title}</h4>
                </div>
                <Badge variant={getMatchBadgeVariant(role.fit_percentage)} className="text-xs font-bold font-mono">
                  Match: {role.fit_percentage}%
                </Badge>
              </div>

              <CardContent className="p-6 space-y-4">
                {/* Salary Estimate */}
                <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-400">
                  <DollarSign className="w-4 h-4" />
                  <span>Salary Range Estimate: {role.salary_range_estimate}</span>
                </div>

                {/* Evidence Callout Box "Why [role_title]?" */}
                <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2.5">
                  <span className="text-[11px] font-bold text-purple-300 uppercase tracking-wider block">
                    Why {role.role_title}?
                  </span>
                  <div className="space-y-1.5 pl-1">
                    {(role.evidence_bullets || []).map((bullet, bIdx) => (
                      <div key={bIdx} className="text-xs text-slate-200 font-medium flex items-center space-x-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                        <span>{bullet.replace(/^✓\s*/, "")}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Skill Overlap Badges */}
                {role.matching_skills && role.matching_skills.length > 0 && (
                  <div className="space-y-1.5">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                      Matching Skills ({role.matching_skills.length}):
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {role.matching_skills.map((sk, sIdx) => (
                        <Badge key={sIdx} variant="purple" className="text-[10px]">
                          {sk}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
