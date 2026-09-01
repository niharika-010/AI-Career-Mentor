"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Users, Info, ShieldCheck, ArrowUpRight, CheckCircle2, AlertCircle, XCircle } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { getRecruiterCandidates, RecruiterCandidate } from "@/lib/api/recruiter";

export default function RecruiterPage() {
  const [candidates, setCandidates] = useState<RecruiterCandidate[]>([]);
  const [disclaimer, setDisclaimer] = useState("Resume-to-role alignment estimate.");
  const [jobTitle, setJobTitle] = useState("Machine Learning Engineer");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setIsLoading(true);
      try {
        const res = await getRecruiterCandidates();
        setCandidates(res.candidates);
        if (res.disclaimer) setDisclaimer(res.disclaimer);
        if (res.job_title) setJobTitle(res.job_title);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status.toLowerCase()) {
      case "strong":
        return <Badge variant="success" className="font-extrabold px-3 py-1 text-xs">Strong</Badge>;
      case "review":
        return <Badge variant="warning" className="font-extrabold px-3 py-1 text-xs">Review</Badge>;
      case "reject":
        return <Badge variant="error" className="font-extrabold px-3 py-1 text-xs">Reject</Badge>;
      default:
        return <Badge variant="neutral">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Page Title Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-semibold text-purple-400 mb-1">
            <Users className="w-4 h-4" />
            <span>Recruiter Batch Screening Workspace</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Candidates
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Deterministic candidate alignment evaluation against open target role: <span className="text-purple-300 font-semibold">{jobTitle}</span>
          </p>
        </div>
      </div>

      {/* Mandatory Ethical Wording Guardrail Notice */}
      <Card className="border-purple-500/40 bg-purple-950/20 p-5">
        <div className="flex items-start space-x-3.5">
          <div className="w-9 h-9 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-300 flex-shrink-0 mt-0.5">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div className="space-y-1">
            <h4 className="text-sm font-bold text-white flex items-center space-x-2">
              <span>Ethical AI Compliance Notice</span>
              <span className="text-[10px] font-extrabold text-purple-300 bg-purple-900/60 px-2 py-0.5 rounded-md border border-purple-700/50">
                Resume-to-role alignment estimate
              </span>
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed">
              This dashboard provides a <span className="font-bold text-white">Resume-to-role alignment estimate</span> based on skill overlap, canonical entity parsing, and ATS formatting rules. <span className="text-purple-200 font-medium">It does not predict hiring outcomes or replace human candidate evaluation.</span>
            </p>
          </div>
        </div>
      </Card>

      {/* Main Candidate Alignment Table Card */}
      <Card className="border-slate-800 bg-slate-900/60 overflow-hidden">
        <CardHeader className="px-6 pt-5 pb-3 border-b border-slate-800/80">
          <CardTitle className="text-lg font-bold text-white">Candidates Alignment Scoreboard</CardTitle>
          <CardDescription>Target Role: {jobTitle}</CardDescription>
        </CardHeader>

        <CardContent className="p-0">
          {isLoading ? (
            <div className="p-12 text-center text-xs text-slate-400 space-y-2">
              <div className="w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto" />
              <p>Loading candidate alignment records...</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-900/90 border-b border-slate-800 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                    <th className="py-4 px-6">Candidate</th>
                    <th className="py-4 px-6 text-center">Match</th>
                    <th className="py-4 px-6 text-center">ATS</th>
                    <th className="py-4 px-6 text-center">Status</th>
                    <th className="py-4 px-6 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/80 text-sm">
                  {candidates.map((cand) => (
                    <tr key={cand.id} className="hover:bg-slate-800/50 transition">
                      {/* Candidate Name */}
                      <td className="py-4 px-6 font-bold text-white">
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 rounded-full bg-purple-500/20 text-purple-300 font-extrabold flex items-center justify-center text-xs border border-purple-500/30">
                            {cand.name.charAt(0)}
                          </div>
                          <div>
                            <p className="font-bold text-white">{cand.name}</p>
                            <p className="text-[11px] text-slate-400 font-normal">{cand.email}</p>
                          </div>
                        </div>
                      </td>

                      {/* Match Score */}
                      <td className="py-4 px-6 text-center">
                        <span className="font-extrabold text-white text-base">{cand.match_score}</span>
                      </td>

                      {/* ATS Score */}
                      <td className="py-4 px-6 text-center">
                        <span className="font-bold text-slate-300 text-sm">{cand.ats_score}</span>
                      </td>

                      {/* Status Badge */}
                      <td className="py-4 px-6 text-center">
                        {getStatusBadge(cand.status)}
                      </td>

                      {/* Actions */}
                      <td className="py-4 px-6 text-right">
                        <Link href="/analysis/ans-101">
                          <Button variant="glass" size="sm">
                            <span>View Profile</span>
                            <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
                          </Button>
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
