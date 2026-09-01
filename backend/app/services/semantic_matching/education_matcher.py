from typing import List, Dict, Any
from app.schemas.semantic_matching import MatchItem, DomainMatchResult
from app.services.semantic_matching.similarity_calculator import similarity_calculator


class EducationMatcher:
    """Evaluates candidate degree level and major field of study against job education requirements."""

    DEGREE_RANK = {
        "Ph.D.": 5,
        "Master's Degree": 4,
        "Master's": 4,
        "Bachelor's Degree": 3,
        "Bachelor's": 3,
        "Associate's Degree": 2,
        "Associate's": 2,
        "High School Diploma": 1,
        "Unspecified": 0,
    }

    def match_education(
        self,
        candidate_education: List[Dict[str, Any]],
        job_education_req: Dict[str, Any],
    ) -> DomainMatchResult:
        job_degree = job_education_req.get("degree_level", "Unspecified")
        job_field = job_education_req.get("field_of_study") or ""
        req_type = job_education_req.get("requirement_type", "required")

        if not candidate_education or job_degree == "Unspecified":
            return DomainMatchResult(
                domain="education",
                score=85.0,
                weight=0.15,
                matched_items=[],
                unmatched_requirements=[],
                summary="Education requirements satisfied or not specified.",
            )

        cand_degree = candidate_education[0].get("degree", "Unspecified") if candidate_education else "Unspecified"
        cand_field = candidate_education[0].get("field_of_study", "") if candidate_education else ""

        cand_rank = self.DEGREE_RANK.get(cand_degree, 2)
        job_rank = self.DEGREE_RANK.get(job_degree, 2)

        degree_match = cand_rank >= job_rank
        if degree_match:
            deg_sim = 1.0
            deg_score = 100.0
            deg_expl = f"Candidate degree ({cand_degree}) meets or exceeds required level ({job_degree})."
        else:
            deg_sim = round(cand_rank / job_rank, 2) if job_rank > 0 else 0.8
            deg_score = round(deg_sim * 100, 1)
            deg_expl = f"Candidate degree ({cand_degree}) is below job requirement ({job_degree})."

        field_sim = similarity_calculator.compute_cosine_similarity(cand_field, job_field) if job_field else 1.0
        field_score = round(field_sim * 100, 1)

        combined_score = round(deg_score * 0.70 + field_score * 0.30, 1)

        matched_item = MatchItem(
            resume_item=f"{cand_degree} in {cand_field}" if cand_field else cand_degree,
            job_requirement=f"{job_degree} in {job_field}" if job_field else job_degree,
            similarity=deg_sim,
            score=combined_score,
            match=degree_match,
            explanation=deg_expl,
        )

        return DomainMatchResult(
            domain="education",
            score=combined_score,
            weight=0.15,
            matched_items=[matched_item],
            unmatched_requirements=[] if degree_match else [job_degree],
            summary=f"Education match score {combined_score:.0f}/100.",
        )


education_matcher = EducationMatcher()
