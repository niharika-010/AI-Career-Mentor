from typing import List, Dict, Any
from app.schemas.semantic_matching import MatchItem, DomainMatchResult
from app.services.semantic_matching.similarity_calculator import similarity_calculator
from app.services.semantic_matching.explanation_generator import explanation_generator


class ExperienceMatcher:
    """Evaluates candidate YOE, Seniority Level, and Work Responsibilities against Job Requirements."""

    def match_experience(
        self,
        candidate_yoe: float,
        candidate_experiences: List[Dict[str, Any]],
        job_min_yoe: float,
        job_seniority: str,
        job_responsibilities: List[str],
    ) -> DomainMatchResult:
        matched_items: List[MatchItem] = []
        unmatched_reqs: List[str] = []

        # 1. YOE & Seniority Alignment
        yoe_sim = 1.0 if candidate_yoe >= job_min_yoe else (candidate_yoe / job_min_yoe if job_min_yoe > 0 else 1.0)
        yoe_score = round(yoe_sim * 100, 1)
        yoe_match = candidate_yoe >= job_min_yoe

        yoe_expl = (
            f"Candidate meets YOE requirement ({candidate_yoe:.1f} years vs {job_min_yoe:.1f} years required)."
            if yoe_match
            else f"Candidate has {candidate_yoe:.1f} years experience vs {job_min_yoe:.1f} years required."
        )

        matched_items.append(
            MatchItem(
                resume_item=f"{candidate_yoe:.1f} Years Professional Experience",
                job_requirement=f"{job_min_yoe:.1f}+ Years Required Experience ({job_seniority})",
                similarity=round(yoe_sim, 4),
                score=yoe_score,
                match=yoe_match,
                explanation=yoe_expl,
            )
        )

        # 2. Work Responsibilities Semantic Similarity
        cand_resp_texts = []
        for exp in candidate_experiences:
            title = exp.get("job_title", "")
            bullets = exp.get("responsibilities", [])
            cand_resp_texts.append(f"{title}: " + " ".join(bullets[:3]))

        for job_resp in job_responsibilities[:5]:
            best_sim = 0.0
            best_cand_text = None

            for cand_text in cand_resp_texts:
                sim = similarity_calculator.compute_cosine_similarity(cand_text, job_resp)
                if sim > best_sim:
                    best_sim = sim
                    best_cand_text = cand_text

            is_match = best_sim >= 0.60
            score_100 = round(best_sim * 100, 1)

            if is_match and best_cand_text:
                expl = f"Candidate role responsibility shows {score_100:.0f}% semantic alignment with job duty '{job_resp[:60]}...'."
                matched_items.append(
                    MatchItem(
                        resume_item=best_cand_text[:100],
                        job_requirement=job_resp[:100],
                        similarity=round(best_sim, 4),
                        score=score_100,
                        match=True,
                        explanation=expl,
                    )
                )
            else:
                unmatched_reqs.append(job_resp[:100])

        # Overall domain score
        avg_score = sum(m.score for m in matched_items) / len(matched_items) if matched_items else yoe_score
        domain_score = min(100.0, max(0.0, round(avg_score, 1)))

        summary = f"Experience score {domain_score:.0f}/100 based on {candidate_yoe:.1f} YOE and job duties relevance."

        return DomainMatchResult(
            domain="experience",
            score=domain_score,
            weight=0.25,
            matched_items=matched_items,
            unmatched_requirements=unmatched_reqs,
            summary=summary,
        )


experience_matcher = ExperienceMatcher()
