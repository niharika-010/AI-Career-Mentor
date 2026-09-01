from typing import List, Dict, Any
from app.schemas.semantic_matching import MatchItem, DomainMatchResult
from app.services.semantic_matching.similarity_calculator import similarity_calculator


class CertificationMatcher:
    """Evaluates candidate certifications against job certification requirements."""

    def match_certifications(
        self, candidate_certs: List[Dict[str, Any]], job_certs: List[Dict[str, Any]]
    ) -> DomainMatchResult:
        if not job_certs:
            return DomainMatchResult(
                domain="certifications",
                score=100.0,
                weight=0.10,
                matched_items=[],
                unmatched_requirements=[],
                summary="No required certifications specified in job description.",
            )

        cand_cert_names = [c.get("name", "") if isinstance(c, dict) else str(c) for c in candidate_certs]
        job_cert_names = [c.get("name", "") if isinstance(c, dict) else str(c) for c in job_certs]

        matched_items: List[MatchItem] = []
        unmatched_reqs: List[str] = []

        for req in job_cert_names:
            best_sim = 0.0
            best_cand_cert = None

            for cand_c in cand_cert_names:
                sim = similarity_calculator.compute_cosine_similarity(cand_c, req)
                if sim > best_sim:
                    best_sim = sim
                    best_cand_cert = cand_c

            is_match = best_sim >= 0.70
            score_100 = round(best_sim * 100, 1)

            if is_match and best_cand_cert:
                expl = f"Candidate certification '{best_cand_cert}' matches job requirement '{req}'."
                matched_items.append(
                    MatchItem(
                        resume_item=best_cand_cert,
                        job_requirement=req,
                        similarity=round(best_sim, 4),
                        score=score_100,
                        match=True,
                        explanation=expl,
                    )
                )
            else:
                unmatched_reqs.append(req)

        match_rate = len(matched_items) / len(job_cert_names) if job_cert_names else 1.0
        domain_score = round(match_rate * 100, 1)

        return DomainMatchResult(
            domain="certifications",
            score=domain_score,
            weight=0.10,
            matched_items=matched_items,
            unmatched_requirements=unmatched_reqs,
            summary=f"Matched {len(matched_items)} out of {len(job_cert_names)} certification requirements.",
        )


certification_matcher = CertificationMatcher()
