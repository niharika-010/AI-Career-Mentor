import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Career Assistant Platform | Production ATS Resume & Guidance",
  description: "AI-powered deterministic ATS resume screening, match scoring, and career path recommendations.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 antialiased selection:bg-purple-500 selection:text-white">
        <main>{children}</main>
      </body>
    </html>
  );
}
