"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { History, Search, ArrowRight, FileText, CheckCircle2, ChevronRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { getAnalysisHistory, AnalysisHistoryItem } from "@/lib/api/analysis";

export default function HistoryPage() {
  const router = useRouter();
  const [historyItems, setHistoryItems] = useState<AnalysisHistoryItem[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      setIsLoading(true);
      try {
        const items = await getAnalysisHistory();
        setHistoryItems(items);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    loadHistory();
  }, []);

  const filteredItems = historyItems.filter((item) =>
    item.target_role.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-semibold text-cyan-400 mb-1">
            <History className="w-4 h-4" />
            <span>Saved Resume Evaluations</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Analysis History
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Clicking any record opens your detailed saved analysis audit report.
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search roles..."
            className="w-full sm:w-64 pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          />
        </div>
      </div>

      {/* Main Analysis History Card List */}
      <Card className="border-slate-800 bg-slate-900/60 p-2 sm:p-4">
        <CardHeader className="px-4 pt-4 pb-2 border-b border-slate-800/60 mb-2">
          <CardTitle className="text-lg font-bold text-white">Saved Evaluation Log</CardTitle>
          <CardDescription>Select a target role to view full deterministic breakdown and export PDF.</CardDescription>
        </CardHeader>

        <CardContent className="p-0 divide-y divide-slate-800/80">
          {isLoading ? (
            <div className="p-8 text-center text-xs text-slate-400 space-y-2">
              <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto" />
              <p>Loading analysis history entries...</p>
            </div>
          ) : filteredItems.length === 0 ? (
            <EmptyState
              title="No Analysis History Found"
              description="Run your first resume match evaluation to save history."
              actionLabel="Run First Analysis"
              actionHref="/analyze"
              icon={History}
            />
          ) : (
            filteredItems.map((item) => {
              const isHigh = item.overall_score >= 80;
              return (
                <div
                  key={item.id}
                  onClick={() => router.push(`/analysis/${item.id}`)}
                  className="group flex items-center justify-between p-4 rounded-xl hover:bg-slate-800/60 transition cursor-pointer space-x-4"
                >
                  {/* Left: Role Title */}
                  <div className="flex items-center space-x-3.5 min-w-0">
                    <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 flex-shrink-0 group-hover:scale-105 transition">
                      <FileText className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-sm sm:text-base font-bold text-white group-hover:text-purple-300 transition truncate">
                        {item.target_role}
                      </h3>
                      <p className="text-[11px] text-slate-400 flex items-center space-x-1">
                        <CheckCircle2 className="w-3 h-3 text-emerald-400 inline" />
                        <span>Deterministic Score Saved</span>
                      </p>
                    </div>
                  </div>

                  {/* Right: Score, Date, Arrow */}
                  <div className="flex items-center space-x-4 sm:space-x-8 flex-shrink-0">
                    {/* Score Badge */}
                    <div className="text-right">
                      <span
                        className={`inline-block px-3 py-1 rounded-lg text-sm font-extrabold ${
                          isHigh
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                            : "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                        }`}
                      >
                        {Math.round(item.overall_score)}%
                      </span>
                    </div>

                    {/* Formatted Date */}
                    <div className="text-xs font-semibold text-slate-400 min-w-[50px] text-right">
                      {item.date_label}
                    </div>

                    {/* Action Icon */}
                    <div className="w-8 h-8 rounded-lg bg-slate-800 group-hover:bg-purple-600 flex items-center justify-center text-slate-400 group-hover:text-white transition">
                      <ChevronRight className="w-4 h-4" />
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </CardContent>
      </Card>
    </div>
  );
}
