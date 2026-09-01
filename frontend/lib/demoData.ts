export interface DemoResume {
  id: string;
  file_name: string;
  file_type: string;
  file_size_bytes: number;
  uploaded_at: string;
  summary: string;
  skills: string[];
  experience_years: number;
}

export interface DemoJob {
  id: string;
  title: string;
  company_name: string;
  required_skills: string[];
  optional_skills: string[];
  required_yoe: number;
  education_level: string;
  created_at: string;
}

export interface DemoAnalysis {
  id: string;
  resume_id: string;
  job_id: string;
  resume_name: string;
  job_title: string;
  company_name: string;
  overall_score: number;
  skills_score: number;       // 35%
  semantic_score: number;     // 20%
  experience_score: number;   // 15%
  project_score: number;      // 10%
  education_score: number;    // 5%
  certification_score: number;// 5%
  ats_score: number;          // 5%
  keyword_score: number;      // 5%
  created_at: string;
  matched_skills: string[];
  missing_skills: string[];
  ats_rules: { rule: string; passed: boolean; details: string }[];
  bullet_rewrites: { original: string; optimized: string; impact: string }[];
  cover_letter: string;
  interview_questions: { question: string; category: string; expected_answer: string }[];
  skill_roadmap: { skill: string; priority: "High" | "Medium" | "Low"; timeframe: string; resource: string }[];
}

export const DEMO_RESUMES: DemoResume[] = [
  {
    id: "res-001",
    file_name: "Sarah_Jenkins_Senior_FullStack_Engineer.pdf",
    file_type: "application/pdf",
    file_size_bytes: 1240000,
    uploaded_at: "2026-08-30T10:15:00Z",
    summary: "Senior Full Stack Engineer with 6+ years of experience building distributed web services with Next.js, Python FastAPI, PostgreSQL, and AWS.",
    skills: ["Python", "FastAPI", "TypeScript", "Next.js", "React", "PostgreSQL", "Docker", "AWS", "GraphQL", "Tailwind CSS"],
    experience_years: 6.5,
  },
  {
    id: "res-002",
    file_name: "Michael_Chang_Backend_Developer.docx",
    file_type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    file_size_bytes: 840000,
    uploaded_at: "2026-08-28T14:22:00Z",
    summary: "Backend Developer specializing in high-throughput API architectures, microservices, and database optimization.",
    skills: ["Python", "Django", "PostgreSQL", "Redis", "Celery", "Docker", "Git"],
    experience_years: 4.0,
  },
];

export const DEMO_JOBS: DemoJob[] = [
  {
    id: "job-001",
    title: "Senior AI Full Stack Engineer",
    company_name: "Nexus Artificial Intelligence",
    required_skills: ["Python", "FastAPI", "TypeScript", "Next.js", "PostgreSQL", "Docker"],
    optional_skills: ["Tailwind CSS", "Sentence Transformers", "Redis", "AWS"],
    required_yoe: 5,
    education_level: "Bachelor's Degree in CS or related",
    created_at: "2026-08-29T09:00:00Z",
  },
  {
    id: "job-002",
    title: "Lead Backend Developer",
    company_name: "Quantum Cloud Labs",
    required_skills: ["Python", "PostgreSQL", "Redis", "FastAPI", "Kubernetes"],
    optional_skills: ["GraphQL", "gRPC", "Terraform"],
    required_yoe: 6,
    education_level: "Master's Degree preferred",
    created_at: "2026-08-27T11:30:00Z",
  },
];

export const DEMO_ANALYSES: DemoAnalysis[] = [
  {
    id: "ans-101",
    resume_id: "res-001",
    job_id: "job-001",
    resume_name: "Sarah_Jenkins_Senior_FullStack_Engineer.pdf",
    job_title: "Senior AI Full Stack Engineer",
    company_name: "Nexus Artificial Intelligence",
    overall_score: 87.5,
    skills_score: 92.0,      // 35%
    semantic_score: 88.0,    // 20%
    experience_score: 95.0,  // 15%
    project_score: 85.0,     // 10%
    education_score: 100.0,  // 5%
    certification_score: 70.0,// 5%
    ats_score: 95.0,         // 5%
    keyword_score: 85.0,     // 5%
    created_at: "2026-08-31T18:45:00Z",
    matched_skills: ["Python", "FastAPI", "TypeScript", "Next.js", "PostgreSQL", "Docker", "Tailwind CSS", "AWS"],
    missing_skills: ["Kubernetes", "gRPC", "Vector Search / PGVector"],
    ats_rules: [
      { rule: "Contact Details Present", passed: true, details: "Email and Phone number detected in standard header." },
      { rule: "Standard Section Titles", passed: true, details: "Found Experience, Education, Skills, and Projects." },
      { rule: "Text Searchable Format", passed: true, details: "PDF text density normal. Not scanned image." },
      { rule: "Resume Word Count", passed: true, details: "Length is 680 words (Optimal range 400-1000)." },
      { rule: "No Complex Tables / Columns", passed: true, details: "Clean single-column ATS readable layout." },
    ],
    bullet_rewrites: [
      {
        original: "Built backend APIs for candidate web app using FastAPI.",
        optimized: "Architected 14+ async FastAPI REST endpoints with PostgreSQL & Pydantic v2, reducing API response latency by 38%.",
        impact: "+14% Impact Score",
      },
      {
        original: "Worked on Next.js frontend components.",
        optimized: "Developed responsive Next.js 14 App Router UI components using TypeScript & Tailwind CSS, supporting 10,000+ monthly active users.",
        impact: "+12% Impact Score",
      },
    ],
    cover_letter: `Dear Hiring Manager at Nexus Artificial Intelligence,

I am writing to express my enthusiastic interest in the Senior AI Full Stack Engineer position. With over 6 years of experience building high-performance web applications using Python (FastAPI), TypeScript, Next.js, and cloud architectures, I am eager to contribute to your engineering team.

In my recent projects, I architected async backend services that reduced system latency by 38% while deploying scalable Next.js interfaces. My experience aligning technical execution with product goals makes me a strong fit for your team.

Thank you for your time and consideration.

Sincerely,
Sarah Jenkins`,
    interview_questions: [
      {
        question: "How do you maintain deterministic consistency when combining deterministic scoring code with non-deterministic LLMs?",
        category: "System Architecture",
        expected_answer: "Isolate mathematical score evaluation into pure Python functions with fixed formula weights, passing only the static audit JSON to the LLM for text generation.",
      },
      {
        question: "Explain async session management in SQLAlchemy 2.0 with PostgreSQL asyncpg driver.",
        category: "Backend Deep-Dive",
        expected_answer: "Use async_sessionmaker bound to create_async_engine. Ensure explicit eager loading (e.g. selectinload) to prevent MissingGreenlet errors on lazy relationship access.",
      },
    ],
    skill_roadmap: [
      { skill: "Kubernetes & Helm", priority: "High", timeframe: "2 Weeks", resource: "CKAD Kubernetes Certification Course" },
      { skill: "PGVector & Semantic Search", priority: "Medium", timeframe: "1 Week", resource: "PostgreSQL Vector Embeddings Guide" },
    ],
  },
];
