"use client";

import React, { useState } from "react";
import { Briefcase, Plus, FileText, Check, Trash2, ArrowRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { useToast } from "@/components/ui/Toast";
import { DEMO_JOBS, DemoJob } from "@/lib/demoData";

export default function JobsPage() {
  const { toast } = useToast();
  const [jobs, setJobs] = useState<DemoJob[]>(DEMO_JOBS);
  const [showAddForm, setShowAddForm] = useState(false);

  const [title, setTitle] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [rawText, setRawText] = useState("");
  const [yoeRequired, setYoeRequired] = useState(3);

  const handleAddJob = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !rawText) return;

    const newJob: DemoJob = {
      id: `job-${Date.now()}`,
      title,
      company_name: companyName || "Tech Enterprise",
      required_skills: ["Python", "FastAPI", "PostgreSQL", "Docker"],
      optional_skills: ["Tailwind CSS", "Redis"],
      required_yoe: yoeRequired,
      education_level: "Bachelor's Degree",
      created_at: new Date().toISOString(),
    };

    setJobs((prev) => [newJob, ...prev]);
    setShowAddForm(false);
    setTitle("");
    setCompanyName("");
    setRawText("");
    toast({ title: "Job Description Created!", description: `${newJob.title} is now active for screening.`, type: "success" });
  };

  const handleDeleteJob = (id: string, name: string) => {
    setJobs((prev) => prev.filter((j) => j.id !== id));
    toast({ title: "Job posting deleted", description: name, type: "warning" });
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
            <Briefcase className="w-8 h-8 text-cyan-400" />
            <span>Job Descriptions</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">Manage target job postings and parsed skill requirements.</p>
        </div>
        <Button variant="gradient" size="md" onClick={() => setShowAddForm(!showAddForm)}>
          <Plus className="w-4 h-4 mr-1.5" />
          <span>Add New Job Description</span>
        </Button>
      </div>

      {/* Add Job Form */}
      {showAddForm && (
        <Card className="border-cyan-500/30">
          <CardHeader>
            <CardTitle>Create Target Job Description</CardTitle>
            <CardDescription>Paste raw job description text to parse required skills and experience requirements.</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddJob} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                    Job Title
                  </label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="e.g. Senior Backend Engineer"
                    required
                    className="w-full px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                    Company Name
                  </label>
                  <input
                    type="text"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    placeholder="e.g. Quantum Innovations"
                    className="w-full px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Required Years of Experience
                </label>
                <input
                  type="number"
                  value={yoeRequired}
                  onChange={(e) => setYoeRequired(Number(e.target.value))}
                  min={0}
                  max={20}
                  className="w-32 px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Raw Job Description Text
                </label>
                <textarea
                  value={rawText}
                  onChange={(e) => setRawText(e.target.value)}
                  rows={5}
                  placeholder="Paste the full job posting here..."
                  required
                  className="w-full p-4 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-cyan-500 custom-scrollbar"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-2">
                <Button type="button" variant="ghost" size="sm" onClick={() => setShowAddForm(false)}>
                  Cancel
                </Button>
                <Button type="submit" variant="gradient" size="sm">
                  <span>Save & Parse Job</span>
                  <ArrowRight className="w-4 h-4 ml-1" />
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Jobs List */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
          Target Job Postings ({jobs.length})
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {jobs.map((job) => (
            <Card key={job.id} className="flex flex-col justify-between space-y-4 hover:border-cyan-500/40 transition">
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <h4 className="text-base font-bold text-white">{job.title}</h4>
                    <p className="text-xs text-cyan-400 font-semibold">{job.company_name}</p>
                  </div>
                  <Badge variant="info">{job.required_yoe}+ YOE Required</Badge>
                </div>

                {/* Required Skills */}
                <div>
                  <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider block mb-1.5">
                    Required Technical Skills:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {job.required_skills.map((skill, idx) => (
                      <span key={idx} className="px-2.5 py-0.5 rounded-lg text-xs font-semibold bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Optional Skills */}
                {job.optional_skills.length > 0 && (
                  <div>
                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider block mb-1.5">
                      Optional / Desired:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {job.optional_skills.map((skill, idx) => (
                        <span key={idx} className="px-2 py-0.5 rounded-lg text-[10px] bg-slate-800 text-slate-400 border border-slate-700">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Card Footer */}
              <div className="flex items-center justify-between pt-3 border-t border-slate-800/80">
                <span className="text-[11px] text-slate-500">
                  Added {new Date(job.created_at).toLocaleDateString()}
                </span>
                <button
                  onClick={() => handleDeleteJob(job.id, job.title)}
                  className="text-slate-400 hover:text-rose-400 p-2 rounded-lg hover:bg-rose-500/10 transition"
                  title="Delete Job"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
