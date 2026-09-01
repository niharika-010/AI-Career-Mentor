"use client";

import React, { useState } from "react";
import Link from "next/link";
import { History, Search, ArrowUpRight, FileText, RotateCcw } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { EmptyState } from "@/components/ui/EmptyState";
import { DEMO_ANALYSES } from "@/lib/demoData";

export default function HistoryPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [historyItems, setHistoryItems] = useState(DEMO_ANALYSES);

  const filteredHistory = historyItems.filter(
    (item) =>
      item.job_title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.company_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
            <History className="w-8 h-8 text-cyan-400" />
            <span>Analysis Evaluation History</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Historical audit log of all deterministic resume screening evaluations.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setHistoryItems(historyItems.length > 0 ? [] : DEMO_ANALYSES)}
            className="text-xs text-slate-400 hover:text-white px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 flex items-center space-x-1.5 transition"
            title="Toggle Empty State View for QA Testing"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>{historyItems.length > 0 ? "Test Empty State" : "Restore Demo Data"}</span>
          </button>

          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search evaluation history..."
              className="w-64 pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
          </div>
        </div>
      </div>

      {/* History Table Card OR Empty State */}
      {filteredHistory.length === 0 ? (
        <EmptyState
          title="No Analysis History"
          description="Your previous resume analyses will appear here."
          actionLabel="Run First Analysis"
          actionHref="/analyze"
          icon={History}
        />
      ) : (
        <Card className="overflow-hidden">
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-900/80 border-b border-slate-800 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                    <th className="p-4">Candidate Resume</th>
                    <th className="p-4">Target Job Posting</th>
                    <th className="p-4">Overall Score</th>
                    <th className="p-4">Evaluation Date</th>
                    <th className="p-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/80 text-xs">
                  {filteredHistory.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-900/40 transition">
                      <td className="p-4">
                        <div className="flex items-center space-x-2.5">
                          <FileText className="w-4 h-4 text-purple-400 flex-shrink-0" />
                          <span className="font-bold text-white max-w-[200px] truncate">{item.resume_name}</span>
                        </div>
                      </td>
                      <td className="p-4">
                        <div>
                          <p className="font-bold text-white">{item.job_title}</p>
                          <p className="text-[10px] text-cyan-400">{item.company_name}</p>
                        </div>
                      </td>
                      <td className="p-4">
                        <Badge variant={item.overall_score >= 75 ? "success" : "warning"}>
                          {item.overall_score.toFixed(1)}% Match
                        </Badge>
                      </td>
                      <td className="p-4 text-slate-400">
                        {new Date(item.created_at).toLocaleDateString()}
                      </td>
                      <td className="p-4 text-right">
                        <Link href={`/analysis/${item.id}`}>
                          <Button variant="glass" size="sm">
                            <span>View Audit Report</span>
                            <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
                          </Button>
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
