from typing import List, Dict, Any
from app.schemas.semantic_matching import MatchItem, DomainMatchResult
from app.services.semantic_matching.similarity_calculator import similarity_calculator


class ProjectMatcher:
    """Evaluates candidate technical projects against job responsibilities and domain requirements."""

    def match_projects(
        self, candidate_projects: List[Dict[str, Any]], job_requirements: List[str]
    ) -> DomainMatchResult:
        if not candidate_projects:
            return DomainMatchResult(
                domain="projects",
                score=60.0,
                weight=0.15,
                matched_items=[],
                unmatched_requirements=[],
                summary="No specific candidate projects listed for evaluation.",
            )

        matched_items: List[MatchItem] = []
        unmatched_reqs: List[str] = []

        for proj in candidate_projects:
            title = proj.get("title", "Project")
            desc = proj.get("description", "")
            techs = ", ".join(proj.get("technologies", []))
            full_proj_text = f"{title} - {desc} ({techs})"

            best_sim = 0.0
            best_req = None

            for req in job_requirements:
                sim = similarity_calculator.compute_cosine_similarity(full_proj_text, req)
                if sim > best_sim:
                    best_sim = sim
                    best_req = req

            is_match = best_sim >= 0.50
            score_100 = round(max(best_sim * 100, 75.0), 1) if is_match else 60.0

            expl = (
                f"Project '{title}' demonstrates relevant practical experience with '{best_req[:60]}...' ({score_100:.0f}% similarity)."
                if is_match and best_req
                else f"Project '{title}' provides general technical domain context."
            )

            matched_items.append(
                MatchItem(
                    resume_item=full_proj_text[:120],
                    job_requirement=best_req[:100] if best_req else "General Project Alignment",
                    similarity=round(best_sim, 4),
                    score=score_100 if is_match else 60.0,
                    match=is_match,
                    explanation=expl,
                )
            )

        avg_score = sum(m.score for m in matched_items) / len(matched_items) if matched_items else 70.0
        domain_score = min(100.0, max(0.0, round(avg_score, 1)))

        return DomainMatchResult(
            domain="projects",
            score=domain_score,
            weight=0.15,
            matched_items=matched_items,
            unmatched_requirements=unmatched_reqs,
            summary=f"Evaluated {len(candidate_projects)} projects with average relevance score {domain_score:.0f}/100.",
        )


project_matcher = ProjectMatcher()
