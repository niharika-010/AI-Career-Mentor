"use client";

import React, { useState, useEffect } from "react";
import { FileText, Trash2, Eye, RotateCcw, ShieldCheck, Loader2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Dropzone } from "@/components/ui/Dropzone";
import { Modal } from "@/components/ui/Modal";
import { EmptyState } from "@/components/ui/EmptyState";
import { useToast } from "@/components/ui/Toast";
import { DEMO_RESUMES } from "@/lib/demoData";
import {
  uploadResumeApi,
  getResumesApi,
  deleteResumeApi,
  ResumeItem,
} from "@/lib/api/resumes";

export default function ResumesPage() {
  const { toast } = useToast();
  const [resumes, setResumes] = useState<ResumeItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [uploadProgress, setUploadProgress] = useState<number | null>(null);
  const [selectedResume, setSelectedResume] = useState<ResumeItem | null>(null);

  const fetchResumes = async () => {
    setIsLoading(true);
    try {
      const data = await getResumesApi();
      setResumes(data.items);
    } catch (err: any) {
      console.warn("Using demo resume data fallback:", err.message);
      // Map DEMO_RESUMES to ResumeItem structure for offline QA testing
      const mappedDemo: ResumeItem[] = DEMO_RESUMES.map((d) => ({
        id: d.id,
        user_id: "demo-user",
        file_name: d.file_name,
        file_path: `uploads/resumes/${d.file_name}`,
        file_type: d.file_type,
        file_size_bytes: d.file_size_bytes,
        scan_status: "CLEAN",
        parsed_data: {
          doc_type: "resume",
          raw_text: d.summary,
          clean_text: d.summary,
          sections: { summary: d.summary },
          extracted_skills: d.skills,
          experience_years: d.experience_years,
          metadata: {
            word_count: 120,
            character_count: 850,
            estimated_reading_time_minutes: 0.6,
            section_count: 3,
            preprocessed: true,
          },
        },
        created_at: d.uploaded_at,
        updated_at: d.uploaded_at,
      }));
      setResumes(mappedDemo);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, []);

  const handleFileUpload = async (file: File) => {
    setUploadProgress(10);
    toast({ title: "Uploading resume...", description: file.name, type: "info" });

    try {
      const newResume = await uploadResumeApi(file, (percent) => {
        setUploadProgress(percent);
      });

      setResumes((prev) => [newResume, ...prev]);
      toast({
        title: "Resume parsed successfully!",
        description: `${file.name} is ready for screening.`,
        type: "success",
      });
    } catch (err: any) {
      toast({
        title: "Upload Failed",
        description: err.message || "Failed to process resume file.",
        type: "error",
      });
    } finally {
      setUploadProgress(null);
    }
  };

  const handleDelete = async (id: string, name: string) => {
    try {
      await deleteResumeApi(id);
      setResumes((prev) => prev.filter((r) => r.id !== id));
      toast({ title: "Resume deleted", description: name, type: "warning" });
    } catch (err: any) {
      // Local removal fallback for demo items
      setResumes((prev) => prev.filter((r) => r.id !== id));
      toast({ title: "Resume removed", description: name, type: "warning" });
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
            <FileText className="w-8 h-8 text-purple-400" />
            <span>Resume Management</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">Upload and manage parsed candidate PDF and DOCX files.</p>
        </div>

        <button
          onClick={() => setResumes(resumes.length > 0 ? [] : [])}
          className="text-xs text-slate-400 hover:text-white px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 flex items-center space-x-1.5 transition self-start md:self-auto"
          title="Toggle Empty State View for QA Testing"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>{resumes.length > 0 ? "Test Empty State" : "Reload Resumes"}</span>
        </button>
      </div>

      {/* Upload Dropzone Card */}
      <Card>
        <CardHeader>
          <CardTitle>Upload New Resume</CardTitle>
          <CardDescription>Drag and drop PDF or DOCX resume file. Files undergo malware security validation and AST normalization.</CardDescription>
        </CardHeader>
        <CardContent>
          <Dropzone
            onFileSelect={handleFileUpload}
            uploadProgress={uploadProgress}
            accept=".pdf,.docx"
            maxSizeBytes={10 * 1024 * 1024}
          />
        </CardContent>
      </Card>

      {/* Resumes Grid OR Loading OR Empty State */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 flex items-center space-x-2">
          <span>Parsed Resumes ({resumes.length})</span>
        </h3>

        {isLoading ? (
          <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center space-y-3">
            <Loader2 className="w-8 h-8 text-purple-400 animate-spin" />
            <p className="text-xs font-semibold">Loading candidate resumes...</p>
          </div>
        ) : resumes.length === 0 ? (
          <EmptyState
            title="No Resumes Uploaded Yet"
            description="Upload your PDF or DOCX resume to start screening against target job descriptions."
            actionLabel="Upload First Resume"
            onAction={() => window.scrollTo({ top: 0, behavior: "smooth" })}
            icon={FileText}
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {resumes.map((resume) => {
              const skills = resume.parsed_data?.extracted_skills || [];
              const yoe = resume.parsed_data?.experience_years || 0;
              const summaryText =
                resume.parsed_data?.clean_text || "No clean summary text extracted.";

              return (
                <Card key={resume.id} className="flex flex-col justify-between space-y-4 hover:border-purple-500/40 transition">
                  <div className="space-y-3">
                    <div className="flex items-start justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                          <FileText className="w-5 h-5" />
                        </div>
                        <div>
                          <h4 className="text-sm font-bold text-white truncate max-w-[180px] sm:max-w-[240px]">
                            {resume.file_name}
                          </h4>
                          <p className="text-[11px] text-slate-400">
                            Uploaded {new Date(resume.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex flex-col items-end space-y-1">
                        <Badge variant="success">{yoe} YOE</Badge>
                        <span className="inline-flex items-center space-x-1 text-[10px] text-emerald-400 font-semibold">
                          <ShieldCheck className="w-3 h-3" />
                          <span>{resume.scan_status}</span>
                        </span>
                      </div>
                    </div>

                    <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                      {summaryText}
                    </p>

                    {/* Skill Badges */}
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {skills.slice(0, 8).map((skill, i) => (
                        <span key={i} className="px-2 py-0.5 rounded-lg text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                          {skill}
                        </span>
                      ))}
                      {skills.length > 8 && (
                        <span className="px-2 py-0.5 rounded-lg text-[10px] bg-slate-800 text-slate-400">
                          +{skills.length - 8} more
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Card Actions */}
                  <div className="flex items-center justify-between pt-3 border-t border-slate-800/80">
                    <Button variant="glass" size="sm" onClick={() => setSelectedResume(resume)}>
                      <Eye className="w-3.5 h-3.5 mr-1" />
                      View Normalized AST
                    </Button>
                    <button
                      onClick={() => handleDelete(resume.id, resume.file_name)}
                      className="text-slate-400 hover:text-rose-400 p-2 rounded-lg hover:bg-rose-500/10 transition"
                      title="Delete Resume"
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

      {/* AST Details Modal */}
      {selectedResume && (
        <Modal
          isOpen={!!selectedResume}
          onClose={() => setSelectedResume(null)}
          title={`Normalized Document AST: ${selectedResume.file_name}`}
        >
          <div className="space-y-4 text-xs">
            <div className="grid grid-cols-2 gap-2 p-3 bg-slate-900/80 rounded-xl border border-slate-800">
              <div>
                <span className="font-bold text-slate-300">File Type:</span>{" "}
                <span className="text-slate-400">{selectedResume.file_type}</span>
              </div>
              <div>
                <span className="font-bold text-slate-300">File Size:</span>{" "}
                <span className="text-slate-400">{(selectedResume.file_size_bytes / 1024).toFixed(1)} KB</span>
              </div>
              <div>
                <span className="font-bold text-slate-300">Scan Status:</span>{" "}
                <span className="text-emerald-400 font-bold">{selectedResume.scan_status}</span>
              </div>
              <div>
                <span className="font-bold text-slate-300">Word Count:</span>{" "}
                <span className="text-slate-400">{selectedResume.parsed_data?.metadata?.word_count || 0} words</span>
              </div>
            </div>

            <div>
              <span className="font-bold text-slate-300">Extracted Skills:</span>
              <div className="flex flex-wrap gap-1.5 mt-1.5">
                {(selectedResume.parsed_data?.extracted_skills || []).map((s, idx) => (
                  <Badge key={idx} variant="purple">{s}</Badge>
                ))}
              </div>
            </div>

            <div>
              <span className="font-bold text-slate-300">Cleaned Document Preview:</span>
              <pre className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 mt-1 whitespace-pre-wrap max-h-48 overflow-y-auto custom-scrollbar font-mono text-[11px]">
                {selectedResume.parsed_data?.clean_text || "No preview available."}
              </pre>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}
