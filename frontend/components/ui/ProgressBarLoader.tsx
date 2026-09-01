"use client";

import React, { useState, useEffect } from "react";
import { Sparkles, CheckCircle2 } from "lucide-react";

interface ProgressBarLoaderProps {
  label?: string;
  durationMs?: number;
  onComplete?: () => void;
  steps?: string[];
}

export const ProgressBarLoader: React.FC<ProgressBarLoaderProps> = ({
  label = "Analyzing Resume...",
  durationMs = 2000,
  onComplete,
  steps = [
    "Step 1/3: Extracting document text stream & spaCy NER skills...",
    "Step 2/3: Computing SentenceTransformer semantic vectors...",
    "Step 3/3: Evaluating 8-category deterministic score matrix...",
  ],
}) => {
  const [progress, setProgress] = useState(0);
  const [currentStepIdx, setCurrentStepIdx] = useState(0);

  useEffect(() => {
    const intervalTime = 40;
    const increment = (100 / (durationMs / intervalTime));

    const timer = setInterval(() => {
      setProgress((prev) => {
        const next = prev + increment;
        if (next >= 100) {
          clearInterval(timer);
          if (onComplete) onComplete();
          return 100;
        }

        // Update step index based on progress percentage
        if (next > 66) setCurrentStepIdx(2);
        else if (next > 33) setCurrentStepIdx(1);
        else setCurrentStepIdx(0);

        return next;
      });
    }, intervalTime);

    return () => clearInterval(timer);
  }, [durationMs, onComplete]);

  // Generate 20-character ASCII block progress bar (e.g. ████████████████░░░░)
  const totalBlocks = 20;
  const filledBlocks = Math.floor((progress / 100) * totalBlocks);
  const emptyBlocks = totalBlocks - filledBlocks;
  const asciiBar = "█".repeat(filledBlocks) + "░".repeat(emptyBlocks);

  return (
    <div className="w-full glass-card rounded-2xl p-6 border border-purple-500/40 bg-slate-950/90 shadow-2xl font-mono text-xs space-y-4">
      {/* Title Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2 text-purple-400 font-bold">
          <Sparkles className="w-4 h-4 animate-spin text-purple-400" />
          <span className="text-sm text-white">{label}</span>
        </div>
        <span className="font-extrabold text-cyan-400 text-sm">
          {Math.round(progress)}%
        </span>
      </div>

      {/* ASCII Block Bar */}
      <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-center font-bold tracking-widest overflow-x-auto text-purple-400 select-none">
        <span className="text-purple-400">{asciiBar}</span>
      </div>

      {/* Current Execution Step */}
      <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800/80">
        <span className="truncate pr-2 text-cyan-300">
          {steps[currentStepIdx] || steps[0]}
        </span>
        {progress === 100 ? (
          <span className="flex items-center text-emerald-400 font-bold flex-shrink-0">
            <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Complete
          </span>
        ) : (
          <span className="text-purple-400 animate-pulse font-bold flex-shrink-0">
            Processing...
          </span>
        )}
      </div>
    </div>
  );
};
