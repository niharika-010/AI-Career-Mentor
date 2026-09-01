"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Eye, EyeOff, Lock, Mail, User, Check, X, AlertCircle, ArrowRight, Briefcase, UserCheck } from "lucide-react";
import { useAuthStore } from "@/store/useAuthStore";
import { Logo } from "@/components/ui/Logo";

export default function RegisterPage() {
  const router = useRouter();
  const { register, isLoading, error, clearError } = useAuthStore();

  const [role, setRole] = useState<"CANDIDATE" | "RECRUITER">("CANDIDATE");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [localError, setLocalError] = useState("");

  // Password Strength Criteria
  const pwdChecks = {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /[0-9]/.test(password),
    special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password),
  };

  const isPasswordValid = Object.values(pwdChecks).every(Boolean);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    setLocalError("");

    if (!isPasswordValid) {
      setLocalError("Please meet all password requirements before registering.");
      return;
    }

    try {
      await register({
        email,
        password,
        full_name: fullName,
        role,
      });

      // Navigate to Login page as requested in onboarding flow
      router.push("/login?registered=true");
    } catch (err: any) {
      setLocalError(err.message || "Registration failed. Please check your input.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <div className="w-full max-w-md">
        {/* Logo Branding */}
        <div className="flex flex-col items-center mb-6">
          <Link href="/">
            <Logo size="lg" />
          </Link>
          <p className="text-xs text-slate-400 mt-2">Start screening resumes with deterministic AI</p>
        </div>

        {/* Card */}
        <div className="glass-card rounded-2xl p-8 shadow-2xl border border-slate-800">
          {(localError || error) && (
            <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 flex items-start space-x-3 text-red-300 text-sm">
              <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
              <span>{localError || error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Role Selection */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                I am registering as:
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setRole("CANDIDATE")}
                  className={`py-3 px-4 rounded-xl text-xs font-bold border flex items-center justify-center space-x-2 transition ${
                    role === "CANDIDATE"
                      ? "bg-purple-600/20 border-purple-500 text-white shadow-lg shadow-purple-500/10"
                      : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <UserCheck className="w-4 h-4 text-purple-400" />
                  <span>Job Candidate</span>
                </button>
                <button
                  type="button"
                  onClick={() => setRole("RECRUITER")}
                  className={`py-3 px-4 rounded-xl text-xs font-bold border flex items-center justify-center space-x-2 transition ${
                    role === "RECRUITER"
                      ? "bg-cyan-600/20 border-cyan-500 text-white shadow-lg shadow-cyan-500/10"
                      : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <Briefcase className="w-4 h-4 text-cyan-400" />
                  <span>Recruiter</span>
                </button>
              </div>
            </div>

            {/* Full Name */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Full Name
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <User className="w-4 h-4" />
                </div>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Jane Doe"
                  required
                  className="w-full pl-10 pr-4 py-3 bg-slate-900/80 border border-slate-700/80 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                />
              </div>
            </div>

            {/* Email Address */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Email Address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Mail className="w-4 h-4" />
                </div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="jane@example.com"
                  required
                  className="w-full pl-10 pr-4 py-3 bg-slate-900/80 border border-slate-700/80 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="w-full pl-10 pr-10 py-3 bg-slate-900/80 border border-slate-700/80 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-200"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              {/* Realtime Password Checklist */}
              {password.length > 0 && (
                <div className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800 grid grid-cols-2 gap-2 text-xs">
                  <div className={`flex items-center space-x-1.5 ${pwdChecks.length ? "text-emerald-400" : "text-slate-500"}`}>
                    {pwdChecks.length ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
                    <span>Min 8 chars</span>
                  </div>
                  <div className={`flex items-center space-x-1.5 ${pwdChecks.uppercase ? "text-emerald-400" : "text-slate-500"}`}>
                    {pwdChecks.uppercase ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
                    <span>Uppercase (A-Z)</span>
                  </div>
                  <div className={`flex items-center space-x-1.5 ${pwdChecks.lowercase ? "text-emerald-400" : "text-slate-500"}`}>
                    {pwdChecks.lowercase ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
                    <span>Lowercase (a-z)</span>
                  </div>
                  <div className={`flex items-center space-x-1.5 ${pwdChecks.number ? "text-emerald-400" : "text-slate-500"}`}>
                    {pwdChecks.number ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
                    <span>Number (0-9)</span>
                  </div>
                  <div className={`flex items-center space-x-1.5 ${pwdChecks.special ? "text-emerald-400" : "text-slate-500"}`}>
                    {pwdChecks.special ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
                    <span>Special (!@#$)</span>
                  </div>
                </div>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading || !isPasswordValid}
              className="w-full py-3.5 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white shadow-lg shadow-purple-600/25 flex items-center justify-center space-x-2 transition disabled:opacity-40"
            >
              {isLoading ? (
                <span>Registering Account...</span>
              ) : (
                <>
                  <span>Create Account & Sign In</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Footer Link */}
          <div className="mt-8 text-center text-xs text-slate-400 border-t border-slate-800/80 pt-6">
            Already have an account?{" "}
            <Link href="/login" className="font-bold text-purple-400 hover:text-purple-300 transition">
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
