from typing import Dict, Any, List, Tuple
from app.schemas.match_scoring import AnalysisConfidence


class AnalysisConfidenceEngine:
    """Deterministic Analysis Confidence Engine.
    Evaluates analysis quality, data completeness, and extraction quality—NOT hiring probability.
    Uses 100% deterministic backend rules with zero random numbers or LLM outputs.
    """

    def calculate_confidence(
        self,
        resume_intelligence: Dict[str, Any],
        job_intelligence: Dict[str, Any],
        raw_resume_text: str = "",
        raw_job_text: str = "",
    ) -> AnalysisConfidence:
        score = 0.0
        reasons: List[str] = []

        # 1. Resume Extraction Completeness (20 pts)
        r_contact = resume_intelligence.get("contact", {})
        r_has_contact = bool(r_contact.get("email", {}).get("value") or r_contact.get("name", {}).get("value"))
        r_has_skills = bool(resume_intelligence.get("skills"))
        r_has_exp = bool(resume_intelligence.get("experience"))
        r_has_edu = bool(resume_intelligence.get("education"))

        r_comp_pts = (4.0 if r_has_contact else 0.0) + (6.0 if r_has_skills else 0.0) + (5.0 if r_has_exp else 0.0) + (5.0 if r_has_edu else 0.0)
        score += r_comp_pts
        reasons.append(f"Resume Extraction Completeness: {r_comp_pts:.0f}/20 pts")

        # 2. Job Description Extraction Completeness (20 pts)
        j_has_title = bool(job_intelligence.get("job_title") and job_intelligence.get("job_title") != "Unspecified Title")
        j_has_skills = bool(job_intelligence.get("required_skills") or job_intelligence.get("technologies"))
        j_has_exp = bool(job_intelligence.get("experience_requirement", {}).get("min_years", 0) > 0)
        j_has_resp = bool(job_intelligence.get("responsibilities"))

        j_comp_pts = (5.0 if j_has_title else 0.0) + (6.0 if j_has_skills else 0.0) + (4.0 if j_has_exp else 0.0) + (5.0 if j_has_resp else 0.0)
        score += j_comp_pts
        reasons.append(f"JD Extraction Completeness: {j_comp_pts:.0f}/20 pts")

        # 3. Number of Successfully Extracted Skills (15 pts)
        skills_count = len(resume_intelligence.get("skills", []))
        if skills_count >= 6:
            skill_pts = 15.0
        elif skills_count >= 3:
            skill_pts = 10.0
        elif skills_count >= 1:
            skill_pts = 5.0
        else:
            skill_pts = 0.0

        score += skill_pts
        reasons.append(f"Extracted Skills Count ({skills_count} skills): {skill_pts:.0f}/15 pts")

        # 4. Contact Extraction Quality (5 pts)
        name_conf = float(r_contact.get("name", {}).get("confidence", 0.0) or 0.0)
        email_conf = float(r_contact.get("email", {}).get("confidence", 0.0) or 0.0)
        if name_conf >= 0.80 and email_conf >= 0.80:
            contact_q_pts = 5.0
        elif name_conf >= 0.70 or email_conf >= 0.70:
            contact_q_pts = 3.0
        else:
            contact_q_pts = 1.0

        score += contact_q_pts
        reasons.append(f"Contact Extraction Quality: {contact_q_pts:.0f}/5 pts")

        # 5. Education Extraction Quality (5 pts)
        edu_list = resume_intelligence.get("education", [])
        if edu_list and edu_list[0].get("degree") != "Unspecified":
            edu_q_pts = 5.0
        elif edu_list:
            edu_q_pts = 3.0
        else:
            edu_q_pts = 1.0

        score += edu_q_pts
        reasons.append(f"Education Extraction Quality: {edu_q_pts:.0f}/5 pts")

        # 6. Experience Extraction Quality (10 pts)
        exp_list = resume_intelligence.get("experience", [])
        yoe = float(resume_intelligence.get("experience_years", 0.0) or 0.0)
        if exp_list and yoe > 0:
            exp_q_pts = 10.0
        elif exp_list or yoe > 0:
            exp_q_pts = 6.0
        else:
            exp_q_pts = 2.0

        score += exp_q_pts
        reasons.append(f"Experience Extraction Quality: {exp_q_pts:.0f}/10 pts")

        # 7. Semantic Embedding Quality (5 pts)
        from app.services.semantic_matching.similarity_calculator import _model
        emb_pts = 5.0 if _model is not None else 3.0
        score += emb_pts
        reasons.append(f"Semantic Embedding Engine: {emb_pts:.0f}/5 pts")

        # 8. Number of Analyzable Sections (10 pts)
        r_sections = resume_intelligence.get("sections", {})
        sec_count = len(r_sections) if r_sections else (4 if raw_resume_text and len(raw_resume_text) > 300 else 2)
        if sec_count >= 4:
            sec_pts = 10.0
        elif sec_count >= 2:
            sec_pts = 6.0
        else:
            sec_pts = 3.0

        score += sec_pts
        reasons.append(f"Analyzable Section Count: {sec_pts:.0f}/10 pts")

        # 9. Missing / Ambiguous Information Penalties (10 pts max deduction)
        penalties = 0.0
        if not j_has_exp:
            penalties += 4.0
            reasons.append("Ambiguity Penalty: Unspecified JD experience requirement (-4 pts)")
        if not r_has_skills:
            penalties += 4.0
            reasons.append("Ambiguity Penalty: Candidate profile missing extracted skills (-4 pts)")
        if not r_has_edu:
            penalties += 2.0
            reasons.append("Ambiguity Penalty: Missing education history (-2 pts)")

        final_score = min(100.0, max(0.0, round(score - penalties, 1)))

        # Determine confidence level
        if final_score >= 80.0:
            level = "High"
        elif final_score >= 60.0:
            level = "Medium"
        else:
            level = "Low"

        return AnalysisConfidence(
            confidence_score=final_score,
            confidence_level=level,
            confidence_reasons=reasons,
        )


analysis_confidence_engine = AnalysisConfidenceEngine()
