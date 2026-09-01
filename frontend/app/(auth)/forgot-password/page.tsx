"use client";

import { useState } from "react";
import Link from "next/link";
import { Sparkles, Mail, CheckCircle2, AlertCircle, ArrowLeft, ArrowRight } from "lucide-react";
import { authApi } from "@/lib/api/auth";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [resetToken, setResetToken] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    setMessage("");
    setResetToken("");

    try {
      const resp = await authApi.forgotPassword(email);
      setMessage(resp.message);
      if (resp.reset_token) {
        setResetToken(resp.reset_token);
      }
    } catch (err: any) {
      setError(err.message || "Failed to initiate password recovery.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <div className="w-full max-w-md">
        {/* Logo Branding */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-purple-500/25 mb-3">
            <Sparkles className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight gradient-text">Recover Password</h1>
          <p className="text-xs text-slate-400 mt-1">Enter your email to receive recovery instructions</p>
        </div>

        {/* Card */}
        <div className="glass-card rounded-2xl p-8 shadow-2xl border border-slate-800">
          {error && (
            <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 flex items-start space-x-3 text-red-300 text-sm">
              <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {message ? (
            <div className="space-y-6 text-center">
              <div className="w-14 h-14 rounded-2xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center mx-auto text-emerald-400">
                <CheckCircle2 className="w-8 h-8" />
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">{message}</p>

              {resetToken && (
                <div className="p-4 rounded-xl bg-purple-950/60 border border-purple-500/30 text-left text-xs">
                  <span className="font-bold text-purple-300 block mb-1">Development Reset Token:</span>
                  <code className="break-all font-mono text-purple-200">{resetToken}</code>
                  <div className="mt-3">
                    <Link
                      href={`/reset-password?token=${encodeURIComponent(resetToken)}`}
                      className="inline-flex items-center text-xs font-bold text-cyan-400 hover:text-cyan-300 space-x-1"
                    >
                      <span>Proceed to Reset Password</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              )}

              <Link
                href="/login"
                className="inline-flex items-center justify-center space-x-2 text-sm font-semibold text-purple-400 hover:text-purple-300 pt-4"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Return to Sign In</span>
              </Link>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Registered Email
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <Mail className="w-4 h-4" />
                  </div>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="candidate@example.com"
                    required
                    className="w-full pl-10 pr-4 py-3 bg-slate-900/80 border border-slate-700/80 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3.5 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white shadow-lg shadow-purple-600/25 flex items-center justify-center space-x-2 transition disabled:opacity-50"
              >
                {isLoading ? <span>Sending...</span> : <span>Send Instructions</span>}
              </button>

              <div className="text-center pt-4">
                <Link
                  href="/login"
                  className="inline-flex items-center space-x-1.5 text-xs text-slate-400 hover:text-slate-200 transition"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>Back to Sign In</span>
                </Link>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
