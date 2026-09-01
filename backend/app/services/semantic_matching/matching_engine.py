from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.schemas.semantic_matching import SemanticMatchResponse, DomainMatchResult
from app.services.semantic_matching.skill_matcher import skill_matcher
from app.services.semantic_matching.experience_matcher import experience_matcher
from app.services.semantic_matching.project_matcher import project_matcher
from app.services.semantic_matching.education_matcher import education_matcher
from app.services.semantic_matching.certification_matcher import certification_matcher


class SemanticMatchingEngine:
    """Master Semantic Matching Engine.
    Executes vector similarity matching across Skills, Experience, Projects, Education, and Certifications.
    """

    def compute_match_grade(self, overall_score: float) -> str:
        if overall_score >= 85.0:
            return "Excellent Match"
        elif overall_score >= 75.0:
            return "Strong Match"
        elif overall_score >= 65.0:
            return "Good Match"
        elif overall_score >= 50.0:
            return "Moderate Match"
        else:
            return "Low Match"

    def match_resume_and_job(
        self,
        resume_intelligence: Dict[str, Any],
        job_intelligence: Dict[str, Any],
    ) -> SemanticMatchResponse:
        # Extract candidate inputs
        cand_skills = [s.get("name", "") for s in resume_intelligence.get("skills", [])]
        cand_yoe = float(resume_intelligence.get("experience_years", 0.0) or 0.0)
        cand_exp_list = resume_intelligence.get("experience", [])
        cand_proj_list = resume_intelligence.get("projects", [])
        cand_edu_list = resume_intelligence.get("education", [])
        cand_cert_list = resume_intelligence.get("certifications", [])

        # Extract job requirements
        job_req_skills = [s.get("name", "") for s in job_intelligence.get("required_skills", [])]
        job_pref_skills = [s.get("name", "") for s in job_intelligence.get("preferred_skills", [])]
        job_techs = [t.get("name", "") for t in job_intelligence.get("technologies", [])]
        all_job_skills = list(set(job_req_skills + job_techs)) if (job_req_skills or job_techs) else ["General Technical Skills"]

        job_exp_req = job_intelligence.get("experience_requirement", {})
        job_min_yoe = float(job_exp_req.get("min_years", 0.0) or 0.0)
        job_seniority = job_exp_req.get("seniority_level", "Unspecified")
        raw_resps = job_intelligence.get("responsibilities", [])
        job_resps = [r.get("name", str(r)) if isinstance(r, dict) else str(r) for r in raw_resps]

        job_edu_req = job_intelligence.get("education_requirement", {})
        job_certs = job_intelligence.get("certifications", [])

        # 1. Execute Sub-Matchers
        skill_res = skill_matcher.match_skills(cand_skills, all_job_skills)
        exp_res = experience_matcher.match_experience(
            cand_yoe, cand_exp_list, job_min_yoe, job_seniority, job_resps
        )
        proj_res = project_matcher.match_projects(cand_proj_list, job_resps)
        edu_res = education_matcher.match_education(cand_edu_list, job_edu_req)
        cert_res = certification_matcher.match_certifications(cand_cert_list, job_certs)

        # 2. Compute Weighted Overall Score
        domains = [skill_res, exp_res, proj_res, edu_res, cert_res]
        total_weight = sum(d.weight for d in domains)
        overall_score = round(
            sum(d.score * d.weight for d in domains) / total_weight, 1
        ) if total_weight > 0 else 0.0
        overall_score = min(100.0, max(0.0, overall_score))

        match_grade = self.compute_match_grade(overall_score)

        # 3. Generate Key Strengths & Missing Gaps
        key_strengths = []
        missing_gaps = []

        for item in skill_res.matched_items:
            key_strengths.append(f"Strong skill match: {item.resume_item} for {item.job_requirement}")

        for gap in skill_res.unmatched_requirements[:5]:
            missing_gaps.append(f"Missing required skill: {gap}")

        if exp_res.score >= 80.0:
            key_strengths.append(f"Sufficient experience: {cand_yoe:.1f} YOE satisfies job requirement.")
        elif exp_res.score < 60.0:
            missing_gaps.append(f"Experience gap: Candidate has {cand_yoe:.1f} YOE vs {job_min_yoe:.1f} required.")

        return SemanticMatchResponse(
            overall_score=overall_score,
            match_grade=match_grade,
            skill_match=skill_res,
            experience_match=exp_res,
            project_match=proj_res,
            education_match=edu_res,
            certification_match=cert_res,
            key_strengths=key_strengths[:5],
            missing_gaps=missing_gaps[:5],
            matched_at=datetime.now(timezone.utc).isoformat(),
        )


semantic_matching_engine = SemanticMatchingEngine()
