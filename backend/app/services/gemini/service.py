import logging
from typing import Dict, Any, List, Optional
from app.schemas.ai_guidance import (
    ResumeSummaryResponse,
    RewriteBulletResponse,
    CoverLetterResponse,
    InterviewPrepResponse,
    InterviewQuestionItem,
    SkillGapRoadmapResponse,
    LearningMilestone,
    SkillProficiencyItem,
    WeeklyRoadmapStepItem,
    CareerRecommendationsResponse,
    CareerRoleRecommendation,
)
from app.services.gemini.client import gemini_client
from app.services.gemini.prompts import prompt_manager
from app.services.gemini.validator import structured_output_validator
from app.services.gemini.cache import ai_response_cache

logger = logging.getLogger("app.services.gemini.service")


class GeminiService:
    """Centralized Gemini AI Service abstraction.
    All LLM interactions pass through this service. Never calls Gemini directly elsewhere.
    Does NOT calculate numerical ATS or match scores.
    """

    # 1. Resume Summary
    def generate_resume_summary(
        self, resume_text: str, target_role: Optional[str] = None
    ) -> ResumeSummaryResponse:
        cache_key = f"{resume_text}:{target_role}"
        cached = ai_response_cache.get("summary", cache_key)
        if cached:
            return cached

        prompt = prompt_manager.get_resume_summary_prompt(resume_text, target_role)
        raw_text = gemini_client.generate_content(prompt)
        validated = structured_output_validator.validate_and_parse(raw_text, ResumeSummaryResponse) if raw_text else None

        if not validated:
            # Deterministic Fallback
            words = resume_text.split()
            preview = " ".join(words[:30]) + "..." if len(words) > 30 else resume_text
            role_title = target_role or "Software Professional"
            validated = ResumeSummaryResponse(
                executive_summary=f"Results-oriented {role_title} with demonstrated experience across key technical initiatives. {preview}",
                key_highlights=["Engineered high-performance software solutions.", "Optimized system architecture and workflows."],
                suggested_roles=[role_title, "Senior Software Engineer"]
            )

        ai_response_cache.set("summary", cache_key, validated)
        return validated

    # 2. Rewrite Project
    def rewrite_project(
        self, original_text: str, target_jd: Optional[str] = None
    ) -> RewriteBulletResponse:
        cache_key = f"{original_text}:{target_jd}"
        cached = ai_response_cache.get("rewrite_project", cache_key)
        if cached:
            return cached

        prompt = prompt_manager.get_rewrite_bullet_prompt(original_text, target_jd)
        raw_text = gemini_client.generate_content(prompt)
        validated = structured_output_validator.validate_and_parse(raw_text, RewriteBulletResponse) if raw_text else None

        if not validated:
            # Fallback
            validated = RewriteBulletResponse(
                original_text=original_text,
                rewritten_bullet=f"Architected and deployed {original_text.strip()}, delivering 35% performance enhancement and sub-100ms API latency.",
                action_verbs_used=["Architected", "Deployed", "Delivering"],
                metrics_highlighted=["35% performance enhancement", "sub-100ms API latency"],
                ats_optimization_notes="Transformed passive project description into metric-driven action statement."
            )

        ai_response_cache.set("rewrite_project", cache_key, validated)
        return validated

    # 3. Rewrite Experience
    def rewrite_experience(
        self, original_text: str, target_jd: Optional[str] = None
    ) -> RewriteBulletResponse:
        cache_key = f"{original_text}:{target_jd}"
        cached = ai_response_cache.get("rewrite_experience", cache_key)
        if cached:
            return cached

        prompt = prompt_manager.get_rewrite_bullet_prompt(original_text, target_jd)
        raw_text = gemini_client.generate_content(prompt)
        validated = structured_output_validator.validate_and_parse(raw_text, RewriteBulletResponse) if raw_text else None

        if not validated:
            validated = RewriteBulletResponse(
                original_text=original_text,
                rewritten_bullet=f"Spearheaded core development for {original_text.strip()}, reducing system downtime by 40% across production clusters.",
                action_verbs_used=["Spearheaded", "Reducing"],
                metrics_highlighted=["40% reduction in system downtime"],
                ats_optimization_notes="Enriched with quantifiable metrics and active leadership verbs for ATS ranking."
            )

        ai_response_cache.set("rewrite_experience", cache_key, validated)
        return validated

    # 4. Generate Cover Letter
    def generate_cover_letter(
        self,
        resume_text: str,
        job_description_text: str,
        company_name: Optional[str] = "Hiring Manager",
        job_title: Optional[str] = "Target Position",
    ) -> CoverLetterResponse:
        c_name = company_name or "Hiring Manager"
        j_title = job_title or "Target Position"
        cache_key = f"{resume_text[:200]}:{job_description_text[:200]}:{c_name}:{j_title}"
        cached = ai_response_cache.get("cover_letter", cache_key)
        if cached:
            return cached

        prompt = prompt_manager.get_cover_letter_prompt(resume_text, job_description_text, c_name, j_title)
        raw_text = gemini_client.generate_content(prompt)
        validated = structured_output_validator.validate_and_parse(raw_text, CoverLetterResponse) if raw_text else None

        if not validated:
            intro = f"I am writing to express my strong enthusiasm for the {j_title} position at {c_name}."
            p1 = "With a proven track record of designing scalable technical solutions and driving high-impact projects, I am confident in my ability to make an immediate contribution to your team."
            closing = "Thank you for your time and consideration. I look forward to the opportunity to discuss how my experience aligns with your team's goals."
            full_text = f"Dear {c_name},\n\n{intro}\n\n{p1}\n\n{closing}\n\nSincerely,\nCandidate"

            validated = CoverLetterResponse(
                salutation=f"Dear {c_name},",
                executive_intro=intro,
                body_paragraphs=[p1],
                closing=closing,
                full_cover_letter=full_text,
            )

        ai_response_cache.set("cover_letter", cache_key, validated)
        return validated

    # 5. Interview Questions
    def generate_interview_questions(
        self, job_title: str, job_description_text: Optional[str] = None, candidate_skills: Optional[List[str]] = None
    ) -> InterviewPrepResponse:
        skills = candidate_skills or ["Software Development"]
        cache_key = f"{job_title}:{','.join(skills)}"
        cached = ai_response_cache.get("interview", cache_key)
        if cached:
            return cached

        prompt = prompt_manager.get_interview_prep_prompt(job_title, job_description_text or "", skills)
        raw_text = gemini_client.generate_content(prompt)
        validated = structured_output_validator.validate_and_parse(raw_text, InterviewPrepResponse) if raw_text else None

        if not validated or not validated.questions:
            sk_primary = skills[0] if skills else "Software Engineering"
            q_list = [
                InterviewQuestionItem(
                    question=f"Explain how you would deploy a high-throughput machine learning model or API using {sk_primary}.",
                    category="Technical",
                    difficulty="Intermediate",
                    why_this_question=f"The JD requires practical proficiency and production deployment experience in {sk_primary}.",
                    suggested_topics=["Docker", "REST API", "Cloud Infrastructure", "Model Serving"],
                    recommended_answer_framework="Discuss containerization with Docker, API routing via FastAPI/Flask, caching layers, and CI/CD pipelines."
                ),
                InterviewQuestionItem(
                    question="Describe a situation where you resolved a critical production bug under tight deadline pressure.",
                    category="Behavioral",
                    difficulty="Intermediate",
                    why_this_question="Assesses leadership, crisis mitigation, and communication under pressure.",
                    suggested_topics=["STAR Method", "Incident Response", "Post-mortem", "Stakeholder Communication"],
                    recommended_answer_framework="STAR Method: Situation (incident details), Task (resolution goal), Action (debugging & patch), Result (uptime restored)."
                ),
                InterviewQuestionItem(
                    question=f"What motivates you to pursue the {job_title} role at our organization?",
                    category="HR",
                    difficulty="Beginner",
                    why_this_question="Evaluates cultural alignment, career growth goals, and company research.",
                    suggested_topics=["Career Goals", "Company Culture", "Technical Value Add"],
                    recommended_answer_framework="Connect your past achievements to the company's mission and team growth objectives."
                ),
                InterviewQuestionItem(
                    question="Walk me through your architecture decisions and trade-offs on your most complex project.",
                    category="Project",
                    difficulty="Advanced",
                    why_this_question="Evaluates system design depth, technical trade-off evaluation, and ownership.",
                    suggested_topics=["System Design", "Scalability Trade-offs", "Database Selection", "API Design"],
                    recommended_answer_framework="Highlight problem statement, architecture diagram/flow, database choice, and performance bottlenecks overcome."
                ),
                InterviewQuestionItem(
                    question=f"How do you stay updated with emerging industry standards and best practices as a {job_title}?",
                    category="Role-specific",
                    difficulty="Intermediate",
                    why_this_question=f"Determines continuous learning habits required for modern {job_title} positions.",
                    suggested_topics=["Continuous Learning", "Open Source", "Tech Blogs", "Certifications"],
                    recommended_answer_framework="Mention specific tech publications, open-source projects, and recent skills mastered."
                )
            ]

            tech_q = [q for q in q_list if q.category == "Technical"]
            beh_q = [q for q in q_list if q.category == "Behavioral"]

            validated = InterviewPrepResponse(
                questions=q_list,
                technical_questions=tech_q,
                behavioral_questions=beh_q,
                star_tips=["Quantify your results with metrics (e.g. +35% speed, -40% downtime).", "Keep problem descriptions concise."],
                total_questions=len(q_list)
            )
        else:
            validated.total_questions = len(validated.questions)
            if not validated.technical_questions:
                validated.technical_questions = [q for q in validated.questions if q.category == "Technical"]
            if not validated.behavioral_questions:
                validated.behavioral_questions = [q for q in validated.questions if q.category == "Behavioral"]

        ai_response_cache.set("interview", cache_key, validated)
        return validated

    # 6. Skill Gap Roadmap
    def generate_skill_gap_roadmap(
        self, candidate_skills: List[str], required_skills: List[str], target_role: Optional[str] = "Target Role"
    ) -> SkillGapRoadmapResponse:
        missing = [s for s in required_skills if s.lower() not in {c.lower() for c in candidate_skills}]
        cache_key = f"{','.join(candidate_skills)}:{','.join(required_skills)}"
        cached = ai_response_cache.get("skill_gap", cache_key)
        if cached:
            return cached

        prompt = prompt_manager.get_skill_gap_roadmap_prompt(candidate_skills, required_skills, target_role or "Target Role")
        raw_text = gemini_client.generate_content(prompt)
        validated = structured_output_validator.validate_and_parse(raw_text, SkillGapRoadmapResponse) if raw_text else None

        if not validated or not validated.weekly_roadmap:
            # Build current skills proficiency (80% - 100%)
            current_prof = []
            percentages = [100, 90, 80, 85, 95]
            for idx, sk in enumerate(candidate_skills or ["Python", "Machine Learning", "SQL"]):
                pct = percentages[idx % len(percentages)]
                current_prof.append(SkillProficiencyItem(skill=sk, proficiency_percentage=pct, status="Mastered"))

            # Build missing skills proficiency (10% - 30%)
            missing_list = missing or ["Docker", "AWS", "Kubernetes"]
            missing_prof = []
            gap_pcts = [30, 20, 10, 15, 25]
            for idx, sk in enumerate(missing_list):
                pct = gap_pcts[idx % len(gap_pcts)]
                missing_prof.append(SkillProficiencyItem(skill=sk, proficiency_percentage=pct, status="Gap"))

            # Build 4-week learning roadmap
            m_primary = missing_list[0] if missing_list else "Docker"
            m_secondary = missing_list[1] if len(missing_list) > 1 else "AWS"
            m_tertiary = missing_list[2] if len(missing_list) > 2 else "Kubernetes"

            weekly_steps = [
                WeeklyRoadmapStepItem(
                    week_number=1,
                    title=f"{m_primary} Fundamentals",
                    focus_skills=[m_primary],
                    action_items=[f"Study {m_primary} containerization & core concepts.", f"Build initial local {m_primary} setup."],
                    project_milestone=f"{m_primary} Sandbox Environment"
                ),
                WeeklyRoadmapStepItem(
                    week_number=2,
                    title=f"{m_secondary} Basics",
                    focus_skills=[m_secondary],
                    action_items=[f"Learn {m_secondary} core services and configuration.", "Implement cloud networking & storage."],
                    project_milestone=f"{m_secondary} Cloud Staging Environment"
                ),
                WeeklyRoadmapStepItem(
                    week_number=3,
                    title=f"Deploy ML API with {m_primary}",
                    focus_skills=[m_primary, m_secondary],
                    action_items=[f"Package ML model inside {m_primary} container.", f"Deploy container to {m_secondary}."],
                    project_milestone="Automated Production Deployment API"
                ),
                WeeklyRoadmapStepItem(
                    week_number=4,
                    title=f"{m_primary} + {m_secondary} Capstone Project",
                    focus_skills=[m_primary, m_secondary, m_tertiary],
                    action_items=["Integrate full CI/CD pipeline.", "Conduct performance & load testing."],
                    project_milestone=f"Complete {m_primary} + {m_secondary} Capstone Project"
                )
            ]

            milestones = []
            for sk in missing_list:
                milestones.append(
                    LearningMilestone(
                        skill=sk,
                        priority="High",
                        estimated_weeks=1,
                        recommended_projects=[f"Build a hands-on microservice using {sk}."],
                        free_resources=[f"Official {sk} Documentation & Tutorials."]
                    )
                )

            validated = SkillGapRoadmapResponse(
                current_skills_proficiency=current_prof,
                missing_skills_proficiency=missing_prof,
                missing_skills=missing_list,
                weekly_roadmap=weekly_steps,
                learning_milestones=milestones,
                total_estimated_weeks=4
            )

        ai_response_cache.set("skill_gap", cache_key, validated)
        return validated

    # 7. Career Recommendations
    def generate_career_recommendations(
        self,
        candidate_skills: List[str],
        interests: Optional[List[str]] = None,
        education_degree: Optional[str] = None,
        projects: Optional[List[str]] = None,
        experience_years: float = 0.0,
        preferred_industry: Optional[str] = None,
        current_title: Optional[str] = None,
    ) -> CareerRecommendationsResponse:
        from app.services.career_knowledge.career_ranking_engine import career_ranking_engine

        cache_key = f"{','.join(candidate_skills)}:{experience_years}:{education_degree}:{preferred_industry}"
        cached = ai_response_cache.get("career_rec", cache_key)
        if cached:
            return cached

        # Use deterministic Career Ranking Engine grounded in Career Knowledge Base
        ranked_res = career_ranking_engine.rank_careers(
            candidate_skills=candidate_skills,
            interests=interests,
            education_degree=education_degree,
            projects=projects,
            experience_years=experience_years,
            preferred_industry=preferred_industry,
        )

        ai_response_cache.set("career_rec", cache_key, ranked_res)
        return ranked_res

    # 8. Generate Explanation Polish
    def generate_explanation(self, evidence_summary: str, score: float) -> str:
        prompt = f"Summarize this evidence cleanly for a candidate matching score of {score:.1f}/100: {evidence_summary}"
        raw_text = gemini_client.generate_content(prompt)
        return raw_text.strip() if raw_text else f"Score {score:.1f}/100 based on extracted evidence: {evidence_summary}"


gemini_service = GeminiService()
