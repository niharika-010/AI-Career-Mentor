"use client";

import React, { useState, useRef } from "react";
import { UploadCloud, FileText, CheckCircle2, AlertTriangle, X, Bug, Loader2 } from "lucide-react";

interface DropzoneProps {
  accept?: string;
  maxSizeBytes?: number; // default 10MB
  uploadProgress?: number | null;
  onFileSelect: (file: File) => void;
  label?: string;
  description?: string;
}

export const Dropzone: React.FC<DropzoneProps> = ({
  accept = ".pdf,.docx",
  maxSizeBytes = 10 * 1024 * 1024,
  uploadProgress = null,
  onFileSelect,
  label = "Upload Resume or Document",
  description = "PDF or DOCX format (Max size: 10 MB)",
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const allowedExtensions = accept
    .split(",")
    .map((ext) => ext.trim().toLowerCase().replace(".", ""));

  const handleFile = (file: File) => {
    setError(null);

    const extension = file.name.split(".").pop()?.toLowerCase() || "";
    if (!allowedExtensions.includes(extension)) {
      setError(`⚠ Unsupported file type '.${extension}'. Please upload ${accept.toUpperCase()} files.`);
      setSelectedFile(null);
      return;
    }

    if (file.size > maxSizeBytes) {
      const maxMb = (maxSizeBytes / (1024 * 1024)).toFixed(0);
      setError(`⚠ File size exceeds ${maxMb} MB limit. Please upload a smaller file.`);
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    onFileSelect(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const triggerInvalidFileTest = (e: React.MouseEvent) => {
    e.stopPropagation();
    const fakeInvalidFile = new File(["fake content"], "invalid_image.png", { type: "image/png" });
    handleFile(fakeInvalidFile);
  };

  return (
    <div className="w-full space-y-3">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition ${
          isDragOver
            ? "border-purple-500 bg-purple-500/10 scale-[1.01]"
            : "border-slate-800 hover:border-purple-500/40 bg-slate-900/40 hover:bg-slate-900/60"
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={accept}
          onChange={handleChange}
          className="hidden"
        />

        <div className="w-14 h-14 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 mb-4 shadow-lg shadow-purple-500/10">
          <UploadCloud className="w-7 h-7" />
        </div>

        <h4 className="text-base font-bold text-white mb-1">{label}</h4>
        <p className="text-xs text-slate-400 max-w-xs leading-relaxed">{description}</p>
        
        <div className="mt-4 flex flex-wrap gap-2 justify-center items-center">
          <span className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-purple-300 hover:bg-slate-700 transition">
            Choose File
          </span>

          <button
            type="button"
            onClick={triggerInvalidFileTest}
            className="px-3 py-1.5 rounded-lg text-[11px] font-semibold bg-amber-500/10 text-amber-300 border border-amber-500/30 hover:bg-amber-500/20 transition flex items-center space-x-1"
            title="QA Test: Trigger Unsupported File Error"
          >
            <Bug className="w-3.5 h-3.5 mr-1" />
            <span>Test Invalid File Error</span>
          </button>
        </div>
      </div>

      {/* Upload Progress Bar */}
      {uploadProgress !== null && (
        <div className="p-4 rounded-xl glass-card border border-purple-500/30 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-300">
            <span className="flex items-center space-x-2 font-semibold">
              <Loader2 className="w-4 h-4 text-purple-400 animate-spin" />
              <span>Uploading & Parsing Document...</span>
            </span>
            <span className="font-bold text-purple-400">{uploadProgress}%</span>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-purple-500 to-indigo-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/40 flex items-center space-x-3 text-rose-300 text-xs font-semibold shadow-lg shadow-rose-500/5 animate-pulse">
          <AlertTriangle className="w-5 h-5 text-rose-400 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {selectedFile && uploadProgress === null && (
        <div className="p-4 rounded-xl glass-card border border-purple-500/30 flex items-center justify-between">
          <div className="flex items-center space-x-3 min-w-0">
            <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center flex-shrink-0">
              <FileText className="w-5 h-5" />
            </div>
            <div className="min-w-0">
              <p className="text-sm font-semibold text-white truncate">{selectedFile.name}</p>
              <p className="text-xs text-slate-400">{(selectedFile.size / 1024).toFixed(1)} KB</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className="flex items-center space-x-1 text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/30">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Selected</span>
            </span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                clearFile();
              }}
              className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
