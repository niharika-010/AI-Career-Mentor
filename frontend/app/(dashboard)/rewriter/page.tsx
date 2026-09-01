"use client";

import React, { useState } from "react";
import { Wand2, Sparkles, Copy, Check, ArrowRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { useToast } from "@/components/ui/Toast";
import { DEMO_ANALYSES } from "@/lib/demoData";

export default function RewriterPage() {
  const { toast } = useToast();
  const [originalBullet, setOriginalBullet] = useState("Built backend APIs for candidate web app using FastAPI.");
  const [focusArea, setFocusArea] = useState("Quantified Impact & Metrics");
  const [isGenerating, setIsGenerating] = useState(false);
  const [rewrites, setRewrites] = useState(DEMO_ANALYSES[0].bullet_rewrites);
  const [copiedIdx, setCopiedIdx] = useState<number | null>(null);

  const handleRewrite = (e: React.FormEvent) => {
    e.preventDefault();
    if (!originalBullet) return;
    setIsGenerating(true);
    toast({ title: "Rewriting Bullet Point...", description: "Injecting action verbs, technical keywords, and quantified metrics.", type: "info" });

    setTimeout(() => {
      const newRewrite = {
        original: originalBullet,
        optimized: `Engineered high-throughput ${originalBullet.toLowerCase().replace(".", "")} with async Python FastAPI & PostgreSQL, boosting throughput by 42% across 10,000+ requests.`,
        impact: "+16% Impact Score",
      };
      setRewrites((prev) => [newRewrite, ...prev]);
      setIsGenerating(false);
      toast({ title: "Bullet Point Rewritten!", description: "Optimized for maximum ATS impact score.", type: "success" });
    }, 1500);
  };

  const copyToClipboard = (text: string, idx: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    toast({ title: "Copied to clipboard!", type: "success" });
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <Wand2 className="w-8 h-8 text-purple-400" />
          <span>Resume Bullet Rewriter</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Transform weak resume sentences into high-impact, quantified bullet points optimized for target job descriptions.
        </p>
      </div>

      {/* Input Form Card */}
      <Card className="border-purple-500/30">
        <CardHeader>
          <CardTitle>Input Bullet Sentence</CardTitle>
          <CardDescription>Enter your existing resume bullet point to generate ATS-optimized variations.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleRewrite} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Original Bullet Point
              </label>
              <textarea
                value={originalBullet}
                onChange={(e) => setOriginalBullet(e.target.value)}
                rows={3}
                required
                placeholder="e.g. Worked on database performance..."
                className="w-full p-4 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500 custom-scrollbar"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Optimization Strategy
              </label>
              <div className="flex flex-wrap gap-2">
                {["Quantified Impact & Metrics", "Strong Action Verbs", "Skill & Tool Keyword Density"].map((strategy) => (
                  <button
                    key={strategy}
                    type="button"
                    onClick={() => setFocusArea(strategy)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition ${
                      focusArea === strategy
                        ? "bg-purple-600/30 border-purple-500 text-white"
                        : "bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {strategy}
                  </button>
                ))}
              </div>
            </div>

            <Button type="submit" variant="gradient" size="md" isLoading={isGenerating}>
              <Sparkles className="w-4 h-4 mr-2" />
              <span>{isGenerating ? "Generating ATS Rewrites..." : "Optimize Bullet Point"}</span>
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Side-by-Side Comparison List */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
          Generated Rewrites ({rewrites.length})
        </h3>

        <div className="space-y-4">
          {rewrites.map((item, idx) => (
            <Card key={idx} className="space-y-4 hover:border-purple-500/40 transition">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Original */}
                <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Original Bullet:</span>
                  <p className="text-xs text-slate-300 leading-relaxed">{item.original}</p>
                </div>

                {/* Optimized */}
                <div className="p-4 rounded-xl bg-purple-900/20 border border-purple-500/30 space-y-2 relative">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-purple-300 uppercase tracking-wider flex items-center space-x-1">
                      <Sparkles className="w-3 h-3 text-purple-400" />
                      <span>ATS Optimized (Recommended)</span>
                    </span>
                    <Badge variant="success">{item.impact}</Badge>
                  </div>
                  <p className="text-xs text-white font-medium leading-relaxed">{item.optimized}</p>
                </div>
              </div>

              {/* Action */}
              <div className="flex justify-end pt-2 border-t border-slate-800/80">
                <Button
                  variant="glass"
                  size="sm"
                  onClick={() => copyToClipboard(item.optimized, idx)}
                >
                  {copiedIdx === idx ? (
                    <>
                      <Check className="w-3.5 h-3.5 mr-1 text-emerald-400" />
                      <span className="text-emerald-400">Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5 mr-1" />
                      <span>Copy Bullet Point</span>
                    </>
                  )}
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
