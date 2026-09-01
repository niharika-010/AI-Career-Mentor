from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple
from app.schemas.match_scoring import ComponentScores, DeterministicMatchResponse
from app.services.semantic_matching import semantic_matching_engine
from app.services.semantic_matching.similarity_calculator import similarity_calculator
from app.services.match_scoring.ats_evaluator import ats_evaluator
from app.services.match_scoring.confidence_engine import analysis_confidence_engine


class DeterministicScoringEngine:
    """Pure backend-calculated Deterministic Resume Match Scoring Engine.
    Executes exact mathematical weighting formula:
    skills (0.35) + semantic_similarity (0.20) + experience (0.15) + projects (0.10) +
    education (0.05) + certifications (0.05) + ats (0.05) + keywords (0.05).
    """

    WEIGHTS = {
        "skills": 0.35,
        "semantic_similarity": 0.20,
        "experience": 0.15,
        "projects": 0.10,
        "education": 0.05,
        "certifications": 0.05,
        "ats": 0.05,
        "keywords": 0.05,
    }

    # 1. Skill Score
    def calculate_skill_score(
        self, candidate_skills: List[str], job_skills: List[str]
    ) -> Tuple[float, List[str], List[str]]:
        if not job_skills:
            return 100.0, candidate_skills, []

        cand_set = {s.strip().lower() for s in candidate_skills if s.strip()}
        matched = []
        missing = []

        for req in job_skills:
            req_clean = req.strip().lower()
            if any(req_clean in c or c in req_clean or similarity_calculator.compute_cosine_similarity(c, req_clean) >= 0.70 for c in cand_set):
                matched.append(req)
            else:
                missing.append(req)

        match_ratio = len(matched) / len(job_skills) if job_skills else 1.0
        score = round(match_ratio * 100.0, 1)
        return min(100.0, max(0.0, score)), matched, missing

    # 2. Semantic Similarity Score
    def calculate_semantic_score(
        self, resume_intelligence: Dict[str, Any], job_intelligence: Dict[str, Any]
    ) -> float:
        semantic_resp = semantic_matching_engine.match_resume_and_job(
            resume_intelligence, job_intelligence
        )
        return round(semantic_resp.overall_score, 1)

    # 3. Experience Score
    def calculate_experience_score(
        self,
        candidate_yoe: float,
        candidate_experiences: List[Dict[str, Any]],
        job_min_yoe: float,
        job_seniority: str,
        job_responsibilities: List[str],
    ) -> float:
        yoe_ratio = 1.0 if candidate_yoe >= job_min_yoe else (candidate_yoe / job_min_yoe if job_min_yoe > 0 else 1.0)
        yoe_score = yoe_ratio * 100.0

        resp_sims = []
        cand_resp_text = " ".join([e.get("job_title", "") + " " + " ".join(e.get("responsibilities", [])) for e in candidate_experiences])
        for j_resp in job_responsibilities[:5]:
            sim = similarity_calculator.compute_cosine_similarity(cand_resp_text, j_resp)
            resp_sims.append(sim)

        avg_resp_sim = sum(resp_sims) / len(resp_sims) if resp_sims else 0.75
        combined = round(yoe_score * 0.60 + (avg_resp_sim * 100.0) * 0.40, 1)
        return min(100.0, max(0.0, combined))

    # 4. Project Score
    def calculate_project_score(
        self, candidate_projects: List[Dict[str, Any]], job_responsibilities: List[str]
    ) -> float:
        if not candidate_projects:
            return 60.0

        sims = []
        for proj in candidate_projects:
            proj_text = f"{proj.get('title', '')} {proj.get('description', '')} {' '.join(proj.get('technologies', []))}"
            best_sim = 0.0
            for j_resp in job_responsibilities:
                sim = similarity_calculator.compute_cosine_similarity(proj_text, j_resp)
                if sim > best_sim:
                    best_sim = sim
            sims.append(best_sim)

        avg_sim = sum(sims) / len(sims) if sims else 0.60
        score = round(max(avg_sim * 100.0, 75.0), 1) if avg_sim >= 0.50 else 60.0
        return min(100.0, max(0.0, score))

    # 5. Education Score
    def calculate_education_score(
        self, candidate_education: List[Dict[str, Any]], job_education_req: Dict[str, Any]
    ) -> float:
        job_degree = job_education_req.get("degree_level", "Unspecified")
        if not candidate_education or job_degree == "Unspecified":
            return 85.0

        degree_rank = {
            "Ph.D.": 5, "Doctorate": 5,
            "Master's Degree": 4, "Master's": 4,
            "Bachelor's Degree": 3, "Bachelor's": 3,
            "Associate's Degree": 2, "Associate's": 2,
            "High School Diploma": 1, "Unspecified": 1
        }
        cand_degree = candidate_education[0].get("degree", "Unspecified") if candidate_education else "Unspecified"

        cand_r = degree_rank.get(cand_degree, 2)
        job_r = degree_rank.get(job_degree, 3)

        if cand_r >= job_r:
            return 100.0
        return round((cand_r / job_r) * 100.0, 1)

    # 6. Certification Score
    def calculate_certification_score(
        self, candidate_certs: List[Dict[str, Any]], job_certs: List[Dict[str, Any]]
    ) -> float:
        if not job_certs:
            return 100.0
        if not candidate_certs:
            return 50.0

        cand_cert_names = [c.get("name", "").lower() for c in candidate_certs]
        job_cert_names = [c.get("name", "").lower() for c in job_certs]

        matched = sum(1 for req in job_cert_names if any(req in c or c in req for c in cand_cert_names))
        ratio = matched / len(job_cert_names)
        return round(ratio * 100.0, 1)

    # 7. ATS Score
    def calculate_ats_score(
        self, raw_text: str, resume_intelligence: Dict[str, Any]
    ) -> float:
        ats_score, _ = ats_evaluator.calculate_ats_score(raw_text, resume_intelligence)
        return ats_score

    # 8. Keyword Score
    def calculate_keyword_score(
        self, candidate_skills: List[str], job_keywords: List[str]
    ) -> float:
        if not job_keywords:
            return 90.0

        cand_lower = {s.lower() for s in candidate_skills}
        matched = sum(1 for kw in job_keywords if kw.lower() in cand_lower or any(kw.lower() in c for c in cand_lower))
        ratio = matched / len(job_keywords) if job_keywords else 1.0
        return round(ratio * 100.0, 1)

    # 9. Overall Score Formula Execution
    def calculate_overall_score(
        self,
        skills: float,
        semantic_similarity: float,
        experience: float,
        projects: float,
        education: float,
        certifications: float,
        ats: float,
        keywords: float,
    ) -> float:
        overall = (
            skills * self.WEIGHTS["skills"]
            + semantic_similarity * self.WEIGHTS["semantic_similarity"]
            + experience * self.WEIGHTS["experience"]
            + projects * self.WEIGHTS["projects"]
            + education * self.WEIGHTS["education"]
            + certifications * self.WEIGHTS["certifications"]
            + ats * self.WEIGHTS["ats"]
            + keywords * self.WEIGHTS["keywords"]
        )
        return round(min(100.0, max(0.0, overall)), 2)

    def calculate_match(
        self,
        resume_intelligence: Dict[str, Any],
        job_intelligence: Dict[str, Any],
        raw_resume_text: str = "",
        raw_job_text: str = "",
    ) -> DeterministicMatchResponse:
        # Extract inputs
        cand_skills = [s.get("name", "") for s in resume_intelligence.get("skills", [])]
        cand_yoe = float(resume_intelligence.get("experience_years", 0.0) or 0.0)
        cand_exp = resume_intelligence.get("experience", [])
        cand_proj = resume_intelligence.get("projects", [])
        cand_edu = resume_intelligence.get("education", [])
        cand_certs = resume_intelligence.get("certifications", [])

        job_req_skills = [s.get("name", "") for s in job_intelligence.get("required_skills", [])]
        job_techs = [t.get("name", "") for t in job_intelligence.get("technologies", [])]
        all_job_skills = list(set(job_req_skills + job_techs)) if (job_req_skills or job_techs) else ["General Technical Skills"]

        job_exp_req = job_intelligence.get("experience_requirement", {})
        job_min_yoe = float(job_exp_req.get("min_years", 0.0) or 0.0)
        job_seniority = job_exp_req.get("seniority_level", "Unspecified")

        raw_resps = job_intelligence.get("responsibilities", [])
        job_resps = [r.get("name", str(r)) if isinstance(r, dict) else str(r) for r in raw_resps]

        job_edu_req = job_intelligence.get("education_requirement", {})
        job_certs = job_intelligence.get("certifications", [])
        job_kws = [k.get("name", "") for k in job_intelligence.get("technical_keywords", [])]

        # Calculate all 8 component scores deterministically
        s_skill, matched_skills, missing_skills = self.calculate_skill_score(cand_skills, all_job_skills)
        s_semantic = self.calculate_semantic_score(resume_intelligence, job_intelligence)
        s_exp = self.calculate_experience_score(cand_yoe, cand_exp, job_min_yoe, job_seniority, job_resps)
        s_proj = self.calculate_project_score(cand_proj, job_resps)
        s_edu = self.calculate_education_score(cand_edu, job_edu_req)
        s_cert = self.calculate_certification_score(cand_certs, job_certs)
        s_ats = self.calculate_ats_score(raw_resume_text, resume_intelligence)
        s_kw = self.calculate_keyword_score(cand_skills, job_kws)

        # Calculate final overall score
        overall = self.calculate_overall_score(
            s_skill, s_semantic, s_exp, s_proj, s_edu, s_cert, s_ats, s_kw
        )

        component_scores = ComponentScores(
            skills=s_skill,
            semantic_similarity=s_semantic,
            experience=s_exp,
            projects=s_proj,
            education=s_edu,
            certifications=s_cert,
            ats=s_ats,
            keywords=s_kw,
        )

        # Generate Strengths & Weaknesses
        strengths = []
        weaknesses = []

        if s_skill >= 80.0:
            strengths.append(f"Strong skill match ({s_skill:.0f}/100) covering core technical requirements.")
        else:
            weaknesses.append(f"Skill gap identified ({s_skill:.0f}/100): missing skills like {', '.join(missing_skills[:3])}.")

        if s_exp >= 80.0:
            strengths.append(f"Solid experience alignment ({cand_yoe:.1f} YOE satisfies requirement).")
        elif s_exp < 65.0:
            weaknesses.append(f"Experience gap: candidate has {cand_yoe:.1f} YOE vs {job_min_yoe:.1f} YOE required.")

        if s_semantic >= 80.0:
            strengths.append(f"High semantic vector similarity ({s_semantic:.0f}/100) with job duties.")

        explanations = {
            "skills": f"Skills Score: {s_skill:.1f}/100 (Weight: 35%). Matched {len(matched_skills)} of {len(all_job_skills)} required skills.",
            "semantic_similarity": f"Semantic Score: {s_semantic:.1f}/100 (Weight: 20%). Vector embeddings cosine similarity.",
            "experience": f"Experience Score: {s_exp:.1f}/100 (Weight: 15%). YOE ratio and duty relevance.",
            "projects": f"Projects Score: {s_proj:.1f}/100 (Weight: 10%). Practical project tech alignment.",
            "education": f"Education Score: {s_edu:.1f}/100 (Weight: 5%). Degree rank and major alignment.",
            "certifications": f"Certifications Score: {s_cert:.1f}/100 (Weight: 5%). Certification coverage.",
            "ats": f"ATS Score: {s_ats:.1f}/100 (Weight: 5%). Structure and readability compliance.",
            "keywords": f"Keywords Score: {s_kw:.1f}/100 (Weight: 5%). Domain keyword density.",
            "formula": f"Overall = {s_skill:.1f}*0.35 + {s_semantic:.1f}*0.20 + {s_exp:.1f}*0.15 + {s_proj:.1f}*0.10 + {s_edu:.1f}*0.05 + {s_cert:.1f}*0.05 + {s_ats:.1f}*0.05 + {s_kw:.1f}*0.05 = {overall:.2f}",
        }

        # Compute Analysis Confidence Metrics
        confidence_res = analysis_confidence_engine.calculate_confidence(
            resume_intelligence=resume_intelligence,
            job_intelligence=job_intelligence,
            raw_resume_text=raw_resume_text,
            raw_job_text=raw_job_text,
        )

        return DeterministicMatchResponse(
            overall_score=overall,
            component_scores=component_scores,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            strengths=strengths,
            weaknesses=weaknesses,
            explanations=explanations,
            analysis_confidence=confidence_res,
            calculated_at=datetime.now(timezone.utc).isoformat(),
        )


deterministic_scoring_engine = DeterministicScoringEngine()
