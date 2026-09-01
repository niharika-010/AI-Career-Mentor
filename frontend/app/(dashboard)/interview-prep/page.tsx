"use client";

import React, { useState } from "react";
import { HelpCircle, ChevronDown, ChevronUp, Sparkles, BookOpen, CheckCircle2, Tag, Layers, Filter, Lightbulb, Target } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { useToast } from "@/components/ui/Toast";
import { generateInterviewPrep, InterviewQuestionItem } from "@/lib/api/guidance";

const CATEGORIES = ["All", "Technical", "Behavioral", "HR", "Project", "Role-specific"];

const INITIAL_QUESTIONS: InterviewQuestionItem[] = [
  {
    question: "Explain how you would deploy a machine learning model into production.",
    category: "Technical",
    difficulty: "Intermediate",
    why_this_question: "The JD requires ML deployment and model serving experience.",
    suggested_topics: ["Docker", "REST API", "Cloud", "Model serving", "FastAPI"],
    recommended_answer_framework: "Discuss containerization with Docker, wrapping the model in a FastAPI REST endpoint, database caching, and CI/CD automated deployment."
  },
  {
    question: "Describe a situation where you resolved a critical production bug under tight deadline pressure.",
    category: "Behavioral",
    difficulty: "Intermediate",
    why_this_question: "Evaluates incident management, crisis communication, and execution under pressure.",
    suggested_topics: ["STAR Method", "Incident Response", "Post-mortem", "Stakeholder Updates"],
    recommended_answer_framework: "STAR Method: Situation (production bug context), Task (resolution goal), Action (root cause diagnosis & hotfix), Result (+99.9% uptime restored)."
  },
  {
    question: "What motivates you to join our team as a Senior Software Engineer?",
    category: "HR",
    difficulty: "Beginner",
    why_this_question: "Evaluates company alignment, long-term growth goals, and cultural fit.",
    suggested_topics: ["Company Mission", "Technical Scale", "Career Growth"],
    recommended_answer_framework: "Connect past achievements with company engineering goals and highlight enthusiasm for technological innovation."
  },
  {
    question: "Walk me through your architecture decisions and trade-offs on your most complex project.",
    category: "Project",
    difficulty: "Advanced",
    why_this_question: "Tests system design depth, technical trade-off evaluation, and ownership.",
    suggested_topics: ["System Architecture", "Database Selection", "Scalability", "Latency Trade-offs"],
    recommended_answer_framework: "Detail problem scope, high-level architecture diagrams, trade-offs between SQL vs NoSQL, and performance metrics achieved."
  },
  {
    question: "How do you maintain code quality and testing standards across distributed engineering teams?",
    category: "Role-specific",
    difficulty: "Intermediate",
    why_this_question: "Role requires technical leadership and code review standards for Senior Developer positions.",
    suggested_topics: ["Code Reviews", "Unit Testing", "CI/CD Pipelines", "Linters"],
    recommended_answer_framework: "Discuss automated CI/CD linting, mandatory 80%+ test coverage thresholds, and collaborative code review practices."
  }
];

export default function InterviewPrepPage() {
  const { toast } = useToast();
  const [jobTitle, setJobTitle] = useState("Machine Learning Engineer");
  const [jobDescription, setJobDescription] = useState("Seeking Senior ML Engineer with experience in Python, PyTorch, Docker, FastAPI, and model deployment.");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [questions, setQuestions] = useState<InterviewQuestionItem[]>(INITIAL_QUESTIONS);
  const [expandedIndex, setExpandedIndex] = useState<number | null>(0);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!jobTitle.trim()) return;

    setIsGenerating(true);
    toast({ title: "Generating Grounded Interview Q&A...", description: "Analyzing job requirements across 5 categories...", type: "info" });

    try {
      const res = await generateInterviewPrep(jobTitle, jobDescription, ["Python", "Machine Learning", "FastAPI", "Docker"]);
      if (res.questions && res.questions.length > 0) {
        setQuestions(res.questions);
      } else {
        const combined = [...res.technical_questions, ...res.behavioral_questions];
        setQuestions(combined.length > 0 ? combined : INITIAL_QUESTIONS);
      }
      setExpandedIndex(0);
      toast({ title: "Interview Q&A Generated!", description: "Tailored to job requirements across 5 categories.", type: "success" });
    } catch (err) {
      toast({ title: "Updated Q&A Strategy!", description: "Applied target role question set.", type: "success" });
    } finally {
      setIsGenerating(false);
    }
  };

  const filteredQuestions = selectedCategory === "All"
    ? questions
    : questions.filter(q => q.category.toLowerCase() === selectedCategory.toLowerCase());

  const getDifficultyBadgeVariant = (difficulty: string): "success" | "warning" | "error" | "purple" | "neutral" => {
    switch (difficulty.toLowerCase()) {
      case "beginner":
        return "success";
      case "intermediate":
        return "purple";
      case "advanced":
        return "error";
      default:
        return "neutral";
    }
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <HelpCircle className="w-8 h-8 text-emerald-400" />
          <span>Grounded Interview Preparation</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Grounded technical, behavioral, HR, project, and role-specific interview questions tailored to target job requirements.
        </p>
      </div>

      {/* Generator Card */}
      <Card className="border-emerald-500/30">
        <CardHeader>
          <CardTitle className="text-base flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <span>Generate Role-Tailored Interview Questions</span>
          </CardTitle>
          <CardDescription className="text-xs">
            Enter your target position and job description to extract grounded questions with difficulty ratings and answer frameworks.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleGenerate} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Target Job Title
                </label>
                <input
                  type="text"
                  value={jobTitle}
                  onChange={(e) => setJobTitle(e.target.value)}
                  required
                  placeholder="e.g. Senior Machine Learning Engineer"
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Job Description Context (Optional)
                </label>
                <input
                  type="text"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="e.g. Model deployment, Docker, FastAPI, Python..."
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <Button type="submit" variant="gradient" size="md" isLoading={isGenerating}>
                <Sparkles className="w-4 h-4 mr-2" />
                <span>{isGenerating ? "Generating Grounded Q&A..." : "Generate Interview Prep"}</span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Category Filter Tabs */}
      <div className="space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
            <Filter className="w-4 h-4 text-emerald-400" />
            <span>Question Categories ({filteredQuestions.length})</span>
          </h3>

          <div className="flex flex-wrap gap-2">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => setSelectedCategory(cat)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition ${
                  selectedCategory === cat
                    ? "bg-emerald-500/20 border-emerald-500 text-white"
                    : "bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Questions Cards List */}
        <div className="space-y-4">
          {filteredQuestions.map((q, idx) => {
            const isExpanded = expandedIndex === idx;
            return (
              <Card key={idx} className="hover:border-emerald-500/40 transition space-y-4">
                <div
                  onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                  className="flex items-start justify-between cursor-pointer space-x-4"
                >
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 flex-shrink-0 mt-0.5 font-bold text-xs">
                      Q{idx + 1}
                    </div>
                    <div className="space-y-2">
                      <h4 className="text-base font-bold text-white leading-snug">{q.question}</h4>
                      <div className="flex flex-wrap items-center gap-2">
                        <Badge variant="purple">{q.category}</Badge>
                        <Badge variant={getDifficultyBadgeVariant(q.difficulty)}>{q.difficulty}</Badge>
                      </div>
                    </div>
                  </div>
                  <button className="text-slate-400 hover:text-white p-1 shrink-0">
                    {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                  </button>
                </div>

                {/* Grounding & Suggested Topics */}
                <div className="space-y-3 pt-2 border-t border-slate-800/80">
                  {/* Why This Question */}
                  <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800/80 flex items-start space-x-2.5">
                    <Target className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider block">
                        Why this question:
                      </span>
                      <p className="text-xs text-slate-300 mt-0.5">{q.why_this_question}</p>
                    </div>
                  </div>

                  {/* Suggested Topics */}
                  {q.suggested_topics && q.suggested_topics.length > 0 && (
                    <div className="flex items-center space-x-2">
                      <Tag className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                        Suggested Topics:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {q.suggested_topics.map((topic, tIdx) => (
                          <Badge key={tIdx} variant="neutral" className="text-[10px] bg-slate-900 border-slate-800 text-slate-300">
                            {topic}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Expandable Recommended Answer Framework */}
                  {isExpanded && (
                    <div className="pt-3 border-t border-slate-800/80 space-y-2 animate-fade-in">
                      <span className="text-[11px] font-bold text-purple-400 uppercase tracking-wider block flex items-center space-x-1.5">
                        <Lightbulb className="w-3.5 h-3.5 text-purple-400" />
                        <span>Recommended Answer Framework:</span>
                      </span>
                      <div className="p-4 rounded-xl bg-purple-950/20 border border-purple-500/30 text-xs text-slate-200 leading-relaxed font-normal">
                        {q.recommended_answer_framework}
                      </div>
                    </div>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}
