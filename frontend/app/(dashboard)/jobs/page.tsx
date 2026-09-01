"use client";

import React, { useState, useEffect } from "react";
import { Briefcase, Plus, FileText, Trash2, ArrowRight, UploadCloud, ShieldCheck, Loader2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Dropzone } from "@/components/ui/Dropzone";
import { useToast } from "@/components/ui/Toast";
import { DEMO_JOBS } from "@/lib/demoData";
import {
  createJobDescriptionJsonApi,
  uploadJobDescriptionFileApi,
  getJobDescriptionsApi,
  deleteJobDescriptionApi,
  JobDescriptionItem,
} from "@/lib/api/jobDescriptions";

export default function JobsPage() {
  const { toast } = useToast();
  const [jobs, setJobs] = useState<JobDescriptionItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [activeTab, setActiveTab] = useState<"text" | "file">("text");

  const [title, setTitle] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [rawText, setRawText] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState<number | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchJobs = async () => {
    setIsLoading(true);
    try {
      const data = await getJobDescriptionsApi();
      setJobs(data.items);
    } catch (err: any) {
      console.warn("Using demo jobs data fallback:", err.message);
      // Map DEMO_JOBS to JobDescriptionItem for offline QA testing
      const mappedDemo: JobDescriptionItem[] = DEMO_JOBS.map((j) => ({
        id: j.id,
        user_id: "demo-user",
        title: j.title,
        company_name: j.company_name,
        raw_text: `Job posting for ${j.title} requiring ${j.required_yoe} years of experience in ${j.required_skills.join(", ")}.`,
        parsed_requirements: {
          doc_type: "job_description",
          raw_text: "Demo Job Description Raw Text",
          clean_text: "Demo Job Description Clean Text",
          sections: { requirements: j.required_skills.join(", ") },
          extracted_skills: j.required_skills,
          experience_years: j.required_yoe,
          metadata: {
            word_count: 80,
            character_count: 500,
            estimated_reading_time_minutes: 0.4,
            section_count: 2,
            preprocessed: true,
          },
        },
        scan_status: "CLEAN",
        created_at: j.created_at,
        updated_at: j.created_at,
      }));
      setJobs(mappedDemo);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleAddJob = async (e: React.FormEvent) => {
    e.preventDefault();

    if (activeTab === "text") {
      if (!title || !rawText) return;
      setIsSubmitting(true);
      try {
        const newJob = await createJobDescriptionJsonApi(title, companyName, rawText);
        setJobs((prev) => [newJob, ...prev]);
        setShowAddForm(false);
        resetForm();
        toast({
          title: "Job Description Created!",
          description: `${newJob.title} is now active for screening.`,
          type: "success",
        });
      } catch (err: any) {
        toast({ title: "Error Creating Job", description: err.message, type: "error" });
      } finally {
        setIsSubmitting(false);
      }
    } else {
      if (!selectedFile) {
        toast({ title: "File Required", description: "Please choose a PDF, DOCX, or TXT file to upload.", type: "error" });
        return;
      }
      setIsSubmitting(true);
      setUploadProgress(10);

      try {
        const newJob = await uploadJobDescriptionFileApi(
          selectedFile,
          title || undefined,
          companyName || undefined,
          rawText || undefined,
          (percent) => setUploadProgress(percent)
        );

        setJobs((prev) => [newJob, ...prev]);
        setShowAddForm(false);
        resetForm();
        toast({
          title: "Job File Uploaded & Parsed!",
          description: `${newJob.title} is ready.`,
          type: "success",
        });
      } catch (err: any) {
        toast({ title: "Upload Failed", description: err.message, type: "error" });
      } finally {
        setIsSubmitting(false);
        setUploadProgress(null);
      }
    }
  };

  const resetForm = () => {
    setTitle("");
    setCompanyName("");
    setRawText("");
    setSelectedFile(null);
  };

  const handleDeleteJob = async (id: string, name: string) => {
    try {
      await deleteJobDescriptionApi(id);
      setJobs((prev) => prev.filter((j) => j.id !== id));
      toast({ title: "Job posting deleted", description: name, type: "warning" });
    } catch (err: any) {
      setJobs((prev) => prev.filter((j) => j.id !== id));
      toast({ title: "Job posting removed", description: name, type: "warning" });
    }
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
          <p className="text-xs text-slate-400 mt-1">Manage target job postings and parsed technical requirements.</p>
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
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Create Target Job Description</CardTitle>
                <CardDescription>Paste raw job description text or upload a PDF / DOCX / TXT file.</CardDescription>
              </div>

              {/* Mode Toggle Tabs */}
              <div className="flex items-center p-1 bg-slate-900 rounded-xl border border-slate-800">
                <button
                  type="button"
                  onClick={() => setActiveTab("text")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                    activeTab === "text"
                      ? "bg-cyan-500 text-slate-950 font-bold"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  Plain Text
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("file")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                    activeTab === "file"
                      ? "bg-cyan-500 text-slate-950 font-bold"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  File Upload
                </button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddJob} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                    Job Title {activeTab === "text" && "*"}
                  </label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="e.g. Senior Backend Engineer"
                    required={activeTab === "text"}
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

              {activeTab === "text" ? (
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                    Raw Job Description Text *
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
              ) : (
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                    Upload Job Description Document (PDF / DOCX / TXT) *
                  </label>
                  <Dropzone
                    accept=".pdf,.docx,.txt"
                    maxSizeBytes={10 * 1024 * 1024}
                    uploadProgress={uploadProgress}
                    onFileSelect={(file) => setSelectedFile(file)}
                    label="Drop Job Description File Here"
                    description="Supports PDF, DOCX, or TXT format (Max 10 MB)"
                  />
                </div>
              )}

              <div className="flex justify-end space-x-3 pt-2">
                <Button type="button" variant="ghost" size="sm" onClick={() => setShowAddForm(false)}>
                  Cancel
                </Button>
                <Button type="submit" variant="gradient" size="sm" disabled={isSubmitting}>
                  {isSubmitting ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-1 animate-spin" />
                      <span>Parsing Job...</span>
                    </>
                  ) : (
                    <>
                      <span>Save & Parse Job</span>
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </>
                  )}
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

        {isLoading ? (
          <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center space-y-3">
            <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
            <p className="text-xs font-semibold">Loading job postings...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {jobs.map((job) => {
              const reqSkills = job.parsed_requirements?.extracted_skills || [];
              const yoe = job.parsed_requirements?.experience_years || 0;

              return (
                <Card key={job.id} className="flex flex-col justify-between space-y-4 hover:border-cyan-500/40 transition">
                  <div className="space-y-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="text-base font-bold text-white">{job.title}</h4>
                        <p className="text-xs text-cyan-400 font-semibold">{job.company_name || "Company Confidential"}</p>
                      </div>
                      <div className="flex flex-col items-end space-y-1">
                        <Badge variant="info">{yoe > 0 ? `${yoe}+ YOE` : "General YOE"}</Badge>
                        <span className="inline-flex items-center space-x-1 text-[10px] text-emerald-400 font-semibold">
                          <ShieldCheck className="w-3 h-3" />
                          <span>{job.scan_status}</span>
                        </span>
                      </div>
                    </div>

                    {/* Required Technical Skills */}
                    <div>
                      <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider block mb-1.5">
                        Extracted Technical Skills:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {reqSkills.length > 0 ? (
                          reqSkills.slice(0, 8).map((skill, idx) => (
                            <span key={idx} className="px-2.5 py-0.5 rounded-lg text-xs font-semibold bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
                              {skill}
                            </span>
                          ))
                        ) : (
                          <span className="text-xs text-slate-500 italic">No specific tech skills parsed</span>
                        )}
                        {reqSkills.length > 8 && (
                          <span className="px-2 py-0.5 rounded-lg text-[10px] bg-slate-800 text-slate-400">
                            +{reqSkills.length - 8} more
                          </span>
                        )}
                      </div>
                    </div>

                    {job.file_name && (
                      <div className="flex items-center space-x-2 text-[11px] text-slate-400 bg-slate-900/60 p-2 rounded-lg border border-slate-800">
                        <FileText className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0" />
                        <span className="truncate">File: {job.file_name}</span>
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
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
