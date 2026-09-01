from typing import Dict, Any, Optional


class PromptManager:
    """Manages versioned, structured prompt templates requesting strict JSON output."""

    @staticmethod
    def get_resume_summary_prompt(resume_text: str, target_role: Optional[str] = None) -> str:
        role_clause = f"Target Role: {target_role}\n" if target_role else ""
        return (
            "You are an expert career consultant. Analyze the following resume and return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "executive_summary": "<3-4 sentence powerful professional summary>",\n'
            '  "key_highlights": ["<highlight 1>", "<highlight 2>", "<highlight 3>"],\n'
            '  "suggested_roles": ["<role 1>", "<role 2>"]\n'
            "}\n\n"
            f"{role_clause}Resume Text:\n{resume_text}\n"
        )

    @staticmethod
    def get_rewrite_bullet_prompt(original_text: str, target_jd: Optional[str] = None) -> str:
        jd_clause = f"Target Job Description:\n{target_jd}\n\n" if target_jd else ""
        return (
            "You are an elite ATS resume writer. Rewrite the following bullet point using strong action verbs, quantifiable metrics, and clear impact. Return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "original_text": "<original text>",\n'
            '  "rewritten_bullet": "<action-oriented metric-driven bullet>",\n'
            '  "action_verbs_used": ["<verb1>", "<verb2>"],\n'
            '  "metrics_highlighted": ["<metric1>"],\n'
            '  "ats_optimization_notes": "<notes on ATS improvement>"\n'
            "}\n\n"
            f"{jd_clause}Original Bullet:\n{original_text}\n"
        )

    @staticmethod
    def get_cover_letter_prompt(resume_text: str, job_text: str, company_name: str, job_title: str) -> str:
        return (
            "You are an expert executive cover letter writer. Draft a compelling cover letter tailored to the job description. Return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "salutation": "Dear Hiring Manager,",\n'
            '  "executive_intro": "<opening hook>",\n'
            '  "body_paragraphs": ["<paragraph 1>", "<paragraph 2>"],\n'
            '  "closing": "<professional closing>",\n'
            '  "full_cover_letter": "<complete formatted cover letter text>"\n'
            "}\n\n"
            f"Company: {company_name}\nJob Title: {job_title}\n\nJob Description:\n{job_text}\n\nResume:\n{resume_text}\n"
        )

    @staticmethod
    def get_interview_prep_prompt(job_title: str, job_text: str, skills: list) -> str:
        skills_str = ", ".join(skills) if skills else "General Software"
        return (
            "You are an executive hiring manager and technical interviewer. Generate grounded interview preparation questions across 5 categories: Technical, Behavioral, HR, Project, and Role-specific. Return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "questions": [\n'
            '    {\n'
            '      "question": "Explain how you would deploy a machine learning model.",\n'
            '      "category": "Technical",\n'
            '      "difficulty": "Intermediate",\n'
            '      "why_this_question": "The JD requires ML deployment experience.",\n'
            '      "suggested_topics": ["Docker", "REST API", "Cloud", "Model serving"],\n'
            '      "recommended_answer_framework": "Discuss containerization with Docker, API wrapping with FastAPI, and cloud deployment."\n'
            '    }\n'
            '  ],\n'
            '  "star_tips": ["Use quantifiable metrics in your STAR responses.", "Focus on your individual contributions in team projects."]\n'
            "}\n\n"
            f"Target Role: {job_title}\nCandidate Skills: {skills_str}\nJob Description Context:\n{job_text[:1000]}\n"
        )

    @staticmethod
    def get_skill_gap_roadmap_prompt(cand_skills: list, req_skills: list, role: str) -> str:
        return (
            "You are a senior technical career mentor. Analyze candidate skill gaps against target role requirements and construct a 4-week step-by-step learning roadmap. Return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "current_skills_proficiency": [{"skill": "Python", "proficiency_percentage": 100, "status": "Mastered"}],\n'
            '  "missing_skills_proficiency": [{"skill": "Docker", "proficiency_percentage": 30, "status": "Gap"}],\n'
            '  "missing_skills": ["Docker", "AWS", "Kubernetes"],\n'
            '  "weekly_roadmap": [\n'
            '    {\n'
            '      "week_number": 1,\n'
            '      "title": "Docker Fundamentals",\n'
            '      "focus_skills": ["Docker", "Containers"],\n'
            '      "action_items": ["Learn Dockerfile syntax", "Containerize Python FastAPI app"],\n'
            '      "project_milestone": "Dockerize microservice"\n'
            '    }\n'
            '  ],\n'
            '  "learning_milestones": [{"skill": "Docker", "priority": "High", "estimated_weeks": 1, "recommended_projects": ["Dockerized ML API"], "free_resources": ["Docker Docs"]}],\n'
            '  "total_estimated_weeks": 4\n'
            "}\n\n"
            f"Target Role: {role}\nCandidate Skills: {', '.join(cand_skills)}\nRequired Skills: {', '.join(req_skills)}\n"
        )

    @staticmethod
    def get_career_recommendations_prompt(cand_skills: list, yoe: float, current_title: str) -> str:
        return (
            "You are an executive career coach. Generate top career path recommendations. Return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "recommended_roles": [{"role_title": "<title>", "fit_percentage": 88.0, "salary_range_estimate": "$120,000 - $150,000", "key_reasons": ["<reason1>"]}],\n'
            '  "industry_insights": ["<insight1>"]\n'
            "}\n\n"
            f"Current Title: {current_title}\nExperience Years: {yoe}\nSkills: {', '.join(cand_skills)}\n"
        )


prompt_manager = PromptManager()
