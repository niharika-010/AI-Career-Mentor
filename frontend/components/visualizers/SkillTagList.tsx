import React from "react";
import { Check, Plus } from "lucide-react";

interface SkillTagListProps {
  matchedSkills: string[];
  missingSkills: string[];
}

export const SkillTagList: React.FC<SkillTagListProps> = ({ matchedSkills, missingSkills }) => {
  return (
    <div className="space-y-4">
      {/* Matched Skills */}
      <div>
        <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2.5 flex items-center space-x-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span>Matched Skills ({matchedSkills.length})</span>
        </h4>
        <div className="flex flex-wrap gap-2">
          {matchedSkills.map((skill, idx) => (
            <span
              key={idx}
              className="inline-flex items-center px-3 py-1 rounded-xl text-xs font-semibold bg-emerald-500/10 text-emerald-300 border border-emerald-500/30"
            >
              <Check className="w-3.5 h-3.5 mr-1 text-emerald-400" />
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Missing Skills */}
      {missingSkills.length > 0 && (
        <div>
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2.5 flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-rose-400"></span>
            <span>Missing / Recommended Skills ({missingSkills.length})</span>
          </h4>
          <div className="flex flex-wrap gap-2">
            {missingSkills.map((skill, idx) => (
              <span
                key={idx}
                className="inline-flex items-center px-3 py-1 rounded-xl text-xs font-semibold bg-rose-500/10 text-rose-300 border border-rose-500/30"
              >
                <Plus className="w-3.5 h-3.5 mr-1 text-rose-400" />
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
