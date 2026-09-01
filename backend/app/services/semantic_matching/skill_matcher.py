from typing import List, Dict, Any, Set
from app.schemas.semantic_matching import MatchItem, DomainMatchResult
from app.services.semantic_matching.similarity_calculator import similarity_calculator
from app.services.semantic_matching.explanation_generator import explanation_generator


class SkillMatcher:
    """Evaluates semantic similarity between candidate skills and job skill requirements."""

    MATCH_THRESHOLD = 0.65

    def match_skills(
        self, candidate_skills: List[str], job_requirements: List[str]
    ) -> DomainMatchResult:
        if not job_requirements:
            return DomainMatchResult(
                domain="skills",
                score=100.0,
                weight=0.35,
                matched_items=[],
                unmatched_requirements=[],
                summary="No specific skill requirements listed in job posting.",
            )

        if not candidate_skills:
            return DomainMatchResult(
                domain="skills",
                score=0.0,
                weight=0.35,
                matched_items=[],
                unmatched_requirements=job_requirements,
                summary="Candidate profile contains no extracted skills.",
            )

        matched_items: List[MatchItem] = []
        unmatched_reqs: List[str] = []
        matched_job_reqs: Set[str] = set()

        for req in job_requirements:
            best_sim = 0.0
            best_cand_skill = None

            for cand_skill in candidate_skills:
                sim = similarity_calculator.compute_cosine_similarity(cand_skill, req)
                if sim > best_sim:
                    best_sim = sim
                    best_cand_skill = cand_skill

            is_match = best_sim >= self.MATCH_THRESHOLD
            score_100 = round(best_sim * 100, 1)

            if is_match and best_cand_skill:
                matched_job_reqs.add(req)
                expl = explanation_generator.generate_match_explanation(
                    best_cand_skill, req, best_sim, is_match=True
                )
                matched_items.append(
                    MatchItem(
                        resume_item=best_cand_skill,
                        job_requirement=req,
                        similarity=best_sim,
                        score=score_100,
                        match=True,
                        explanation=expl,
                    )
                )
            else:
                unmatched_reqs.append(req)

        # Domain score calculation
        match_rate = len(matched_job_reqs) / len(job_requirements) if job_requirements else 0.0
        avg_match_sim = (
            sum(m.similarity for m in matched_items) / len(matched_items)
            if matched_items
            else 0.0
        )

        domain_score = round((match_rate * 0.70 + avg_match_sim * 0.30) * 100, 1)
        domain_score = min(100.0, max(0.0, domain_score))

        summary = f"Matched {len(matched_job_reqs)} out of {len(job_requirements)} required skills."

        return DomainMatchResult(
            domain="skills",
            score=domain_score,
            weight=0.35,
            matched_items=matched_items,
            unmatched_requirements=unmatched_reqs,
            summary=summary,
        )


skill_matcher = SkillMatcher()
