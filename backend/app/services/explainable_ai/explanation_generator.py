from datetime import datetime, timezone
from typing import Dict, Any, List
from app.schemas.explainable_ai import (
    MatchedSkillsExplanation,
    MissingSkillsExplanation,
    ExperienceExplanation,
    ProjectExplanation,
    EducationExplanation,
    CertificationExplanation,
    ATSExplanation,
    KeywordExplanation,
    ExplainableMatchResponse,
)
from app.services.match_scoring.scoring_engine import deterministic_scoring_engine
from app.services.explainable_ai.evidence_collector import evidence_collector
from app.services.explainable_ai.claim_validator import claim_validator


class ExplanationGenerator:
    """Generates machine-grounded explanations for all 8 scoring components.
    Ensures zero contradictions with calculated scores and blocks unsupported claims via ClaimValidator.
    """

    def generate_explainable_match(
        self,
        resume_intelligence: Dict[str, Any],
        job_intelligence: Dict[str, Any],
        raw_resume_text: str = "",
        raw_job_text: str = "",
    ) -> ExplainableMatchResponse:
        # 1. Compute Deterministic Match & Component Scores
        match_resp = deterministic_scoring_engine.calculate_match(
            resume_intelligence=resume_intelligence,
            job_intelligence=job_intelligence,
            raw_resume_text=raw_resume_text,
            raw_job_text=raw_job_text,
        )

        scores = match_resp.component_scores

        # 2. Collect Machine-Generated Evidence
        evidence_dict = evidence_collector.collect_evidence(
            resume_intelligence=resume_intelligence,
            job_intelligence=job_intelligence,
            raw_resume_text=raw_resume_text,
            raw_job_text=raw_job_text,
        )

        cand_skills = [s.get("name", "") for s in resume_intelligence.get("skills", []) if s.get("name")]

        # 3. Build Matched Skills Explanation
        matched_items = match_resp.matched_skills
        raw_matched_text = f"Matched {len(matched_items)} skills ({', '.join(matched_items[:4])}) with a skill match score of {scores.skills:.1f}/100."
        _, clean_matched_text, _ = claim_validator.validate_explanation(raw_matched_text, scores.skills, evidence_dict["matched_skills"], cand_skills)

        exp_matched_skills = MatchedSkillsExplanation(
            score=scores.skills,
            evidence=evidence_dict["matched_skills"],
            explanation=clean_matched_text,
            matched_items=matched_items,
        )

        # 4. Build Missing Skills Explanation
        missing_items = match_resp.missing_skills
        raw_missing_text = f"Missing {len(missing_items)} required skills ({', '.join(missing_items[:4])}). Skill gap impact reflected in score {scores.skills:.1f}/100." if missing_items else "No critical skills missing from candidate profile."
        _, clean_missing_text, _ = claim_validator.validate_explanation(raw_missing_text, scores.skills, evidence_dict["missing_skills"], cand_skills)

        exp_missing_skills = MissingSkillsExplanation(
            score=scores.skills,
            evidence=evidence_dict["missing_skills"],
            explanation=clean_missing_text,
            missing_items=missing_items,
        )

        # 5. Build Experience Explanation
        cand_yoe = float(resume_intelligence.get("experience_years", 0.0) or 0.0)
        job_min_yoe = float(job_intelligence.get("experience_requirement", {}).get("min_years", 0.0) or 0.0)
        seniority = job_intelligence.get("experience_requirement", {}).get("seniority_level", "Unspecified")

        raw_exp_text = f"Experience score {scores.experience:.1f}/100. Candidate has {cand_yoe:.1f} YOE compared to job requirement of {job_min_yoe:.1f} YOE at {seniority} level."
        _, clean_exp_text, _ = claim_validator.validate_explanation(raw_exp_text, scores.experience, evidence_dict["experience"])

        exp_experience = ExperienceExplanation(
            score=scores.experience,
            evidence=evidence_dict["experience"],
            explanation=clean_exp_text,
            cand_yoe=cand_yoe,
            job_min_yoe=job_min_yoe,
            seniority_alignment=seniority,
        )

        # 6. Build Project Explanation
        cand_projs = [p.get("title", "Project") for p in resume_intelligence.get("projects", [])]
        raw_proj_text = f"Project relevance score {scores.projects:.1f}/100 based on practical project tech alignment across {len(cand_projs)} projects."
        _, clean_proj_text, _ = claim_validator.validate_explanation(raw_proj_text, scores.projects, evidence_dict["projects"])

        exp_project = ProjectExplanation(
            score=scores.projects,
            evidence=evidence_dict["projects"],
            explanation=clean_proj_text,
            relevant_projects=cand_projs,
        )

        # 7. Build Education Explanation
        cand_edu = resume_intelligence.get("education", [])
        job_edu_req = job_intelligence.get("education_requirement", {})
        cand_deg = cand_edu[0].get("degree", "Unspecified") if cand_edu else "Unspecified"
        job_deg = job_edu_req.get("degree_level", "Unspecified")

        raw_edu_text = f"Education score {scores.education:.1f}/100. Candidate degree '{cand_deg}' evaluated against job requirement '{job_deg}'."
        _, clean_edu_text, _ = claim_validator.validate_explanation(raw_edu_text, scores.education, evidence_dict["education"])

        exp_education = EducationExplanation(
            score=scores.education,
            evidence=evidence_dict["education"],
            explanation=clean_edu_text,
            cand_degree=cand_deg,
            job_degree=job_deg,
        )

        # 8. Build Certification Explanation
        raw_cert_text = f"Certification score {scores.certifications:.1f}/100 reflecting certification coverage."
        _, clean_cert_text, _ = claim_validator.validate_explanation(raw_cert_text, scores.certifications, evidence_dict["certifications"])

        exp_certification = CertificationExplanation(
            score=scores.certifications,
            evidence=evidence_dict["certifications"],
            explanation=clean_cert_text,
            matched_certs=[],
        )

        # 9. Build ATS Explanation
        raw_ats_text = f"ATS readability score {scores.ats:.1f}/100 based on standard section headers, contact completeness, and bullet formatting."
        _, clean_ats_text, _ = claim_validator.validate_explanation(raw_ats_text, scores.ats, evidence_dict["ats"])

        exp_ats = ATSExplanation(
            score=scores.ats,
            evidence=evidence_dict["ats"],
            explanation=clean_ats_text,
            readability_factors=evidence_dict["ats"],
        )

        # 10. Build Keyword Explanation
        raw_kw_text = f"Technical domain keyword score {scores.keywords:.1f}/100 based on keyword density and coverage."
        _, clean_kw_text, _ = claim_validator.validate_explanation(raw_kw_text, scores.keywords, evidence_dict["keywords"])

        exp_keyword = KeywordExplanation(
            score=scores.keywords,
            evidence=evidence_dict["keywords"],
            explanation=clean_kw_text,
            matched_keywords=[],
        )

        return ExplainableMatchResponse(
            overall_score=match_resp.overall_score,
            component_scores=match_resp.component_scores,
            matched_skills_explanation=exp_matched_skills,
            missing_skills_explanation=exp_missing_skills,
            experience_explanation=exp_experience,
            project_explanation=exp_project,
            education_explanation=exp_education,
            certification_explanation=exp_certification,
            ats_explanation=exp_ats,
            keyword_explanation=exp_keyword,
            analysis_confidence=match_resp.analysis_confidence,
            calculated_at=datetime.now(timezone.utc).isoformat(),
        )


explanation_generator = ExplanationGenerator()
