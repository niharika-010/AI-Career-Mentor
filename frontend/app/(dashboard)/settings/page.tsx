"use client";

import React, { useState } from "react";
import { Settings, User, Shield, Key, Save, Check } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { useToast } from "@/components/ui/Toast";
import { useAuthStore } from "@/store/useAuthStore";

export default function SettingsPage() {
  const { toast } = useToast();
  const { user, setUser } = useAuthStore();

  const [fullName, setFullName] = useState(user?.full_name || "Sarah Jenkins");
  const [email] = useState(user?.email || "sarah.jenkins@example.com");
  const [role, setRole] = useState(user?.role || "CANDIDATE");
  const [isSaving, setIsSaving] = useState(false);

  const handleSaveProfile = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);

    setTimeout(() => {
      if (user) {
        setUser({ ...user, full_name: fullName, role });
      }
      setIsSaving(false);
      toast({ title: "Settings updated successfully!", type: "success" });
    }, 1000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
          <Settings className="w-8 h-8 text-purple-400" />
          <span>Account Settings & Preferences</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Manage your account details, workspace role, and security credentials.
        </p>
      </div>

      {/* Profile Card */}
      <Card className="border-purple-500/30">
        <CardHeader>
          <CardTitle>Profile Details</CardTitle>
          <CardDescription>Update your display name and default workspace perspective.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSaveProfile} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  value={email}
                  disabled
                  className="w-full px-4 py-2.5 bg-slate-900/40 border border-slate-800 rounded-xl text-sm text-slate-500 cursor-not-allowed"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Workspace Perspective Role
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div
                  onClick={() => setRole("CANDIDATE")}
                  className={`p-4 rounded-xl border cursor-pointer transition ${
                    role === "CANDIDATE"
                      ? "bg-purple-600/20 border-purple-500 text-white"
                      : "bg-slate-900 border-slate-800 text-slate-400"
                  }`}
                >
                  <h4 className="font-bold text-sm">Candidate Mode</h4>
                  <p className="text-xs text-slate-400 mt-1">Analyze your own resume against target job vacancies.</p>
                </div>

                <div
                  onClick={() => setRole("RECRUITER")}
                  className={`p-4 rounded-xl border cursor-pointer transition ${
                    role === "RECRUITER"
                      ? "bg-purple-600/20 border-purple-500 text-white"
                      : "bg-slate-900 border-slate-800 text-slate-400"
                  }`}
                >
                  <h4 className="font-bold text-sm">Recruiter Mode</h4>
                  <p className="text-xs text-slate-400 mt-1">Batch screen candidate resumes for hiring pipelines.</p>
                </div>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <Button type="submit" variant="gradient" size="md" isLoading={isSaving}>
                <Save className="w-4 h-4 mr-2" />
                <span>Save Profile Settings</span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
