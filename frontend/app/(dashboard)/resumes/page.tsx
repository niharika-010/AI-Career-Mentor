"use client";

import React, { useState } from "react";
import { FileText, Trash2, Eye, RotateCcw } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Dropzone } from "@/components/ui/Dropzone";
import { Modal } from "@/components/ui/Modal";
import { EmptyState } from "@/components/ui/EmptyState";
import { useToast } from "@/components/ui/Toast";
import { DEMO_RESUMES, DemoResume } from "@/lib/demoData";

export default function ResumesPage() {
  const { toast } = useToast();
  const [resumes, setResumes] = useState<DemoResume[]>(DEMO_RESUMES);
  const [selectedResume, setSelectedResume] = useState<DemoResume | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = (file: File) => {
    setIsUploading(true);
    toast({ title: "Uploading resume...", description: file.name, type: "info" });

    setTimeout(() => {
      const newResume: DemoResume = {
        id: `res-${Date.now()}`,
        file_name: file.name,
        file_type: file.type || "application/pdf",
        file_size_bytes: file.size,
        uploaded_at: new Date().toISOString(),
        summary: "Extracted candidate experience summary and structural section blocks.",
        skills: ["Python", "FastAPI", "TypeScript", "React", "PostgreSQL"],
        experience_years: 5.0,
      };

      setResumes((prev) => [newResume, ...prev]);
      setIsUploading(false);
      toast({ title: "Resume parsed successfully!", description: `${file.name} is ready for screening.`, type: "success" });
    }, 1500);
  };

  const handleDelete = (id: string, name: string) => {
    setResumes((prev) => prev.filter((r) => r.id !== id));
    toast({ title: "Resume deleted", description: name, type: "warning" });
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
          onClick={() => setResumes(resumes.length > 0 ? [] : DEMO_RESUMES)}
          className="text-xs text-slate-400 hover:text-white px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 flex items-center space-x-1.5 transition self-start md:self-auto"
          title="Toggle Empty State View for QA Testing"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>{resumes.length > 0 ? "Test Empty State" : "Restore Demo Data"}</span>
        </button>
      </div>

      {/* Upload Dropzone Card */}
      <Card>
        <CardHeader>
          <CardTitle>Upload New Resume</CardTitle>
          <CardDescription>Drag and drop PDF or DOCX resume file to run automatic spaCy NER parsing.</CardDescription>
        </CardHeader>
        <CardContent>
          <Dropzone onFileSelect={handleFileUpload} />
        </CardContent>
      </Card>

      {/* Resumes Grid OR Empty State */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 flex items-center space-x-2">
          <span>Parsed Resumes ({resumes.length})</span>
        </h3>

        {resumes.length === 0 ? (
          <EmptyState
            title="No Resumes Uploaded Yet"
            description="Upload your PDF or DOCX resume to start screening against target job descriptions."
            actionLabel="Upload First Resume"
            onAction={() => window.scrollTo({ top: 0, behavior: "smooth" })}
            icon={FileText}
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {resumes.map((resume) => (
              <Card key={resume.id} className="flex flex-col justify-between space-y-4 hover:border-purple-500/40 transition">
                <div className="space-y-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                        <FileText className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-white truncate max-w-[200px] sm:max-w-[260px]">
                          {resume.file_name}
                        </h4>
                        <p className="text-[11px] text-slate-400">
                          Uploaded {new Date(resume.uploaded_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <Badge variant="success">{resume.experience_years} YOE</Badge>
                  </div>

                  <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                    {resume.summary}
                  </p>

                  {/* Skill Badges */}
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {resume.skills.map((skill, i) => (
                      <span key={i} className="px-2 py-0.5 rounded-lg text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Card Actions */}
                <div className="flex items-center justify-between pt-3 border-t border-slate-800/80">
                  <Button variant="glass" size="sm" onClick={() => setSelectedResume(resume)}>
                    <Eye className="w-3.5 h-3.5 mr-1" />
                    View Parsed AST
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
            ))}
          </div>
        )}
      </div>

      {/* AST Details Modal */}
      {selectedResume && (
        <Modal
          isOpen={!!selectedResume}
          onClose={() => setSelectedResume(null)}
          title={`Parsed AST Details: ${selectedResume.file_name}`}
        >
          <div className="space-y-4 text-xs">
            <div>
              <span className="font-bold text-slate-300">File Type:</span> <span className="text-slate-400">{selectedResume.file_type}</span>
            </div>
            <div>
              <span className="font-bold text-slate-300">Summary:</span>
              <p className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 mt-1 leading-relaxed">
                {selectedResume.summary}
              </p>
            </div>
            <div>
              <span className="font-bold text-slate-300">Extracted Skills:</span>
              <div className="flex flex-wrap gap-1.5 mt-1.5">
                {selectedResume.skills.map((s, idx) => (
                  <Badge key={idx} variant="purple">{s}</Badge>
                ))}
              </div>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}
