import pytest
from app.services.career_knowledge.career_ranking_engine import career_ranking_engine
from app.schemas.ai_guidance import CareerRecommendationsResponse

def test_career_ranking_engine_deterministic_order():
    cand_skills = ["Python", "Machine Learning", "PyTorch", "FastAPI", "SQL"]
    interests = ["Artificial Intelligence", "Deep Learning"]
    degree = "Bachelor's in Computer Science & AI"
    projects = ["Deployed PyTorch ML API with Docker"]
    experience_years = 3.5
    preferred_industry = "Artificial Intelligence"

    res = career_ranking_engine.rank_careers(
        candidate_skills=cand_skills,
        interests=interests,
        education_degree=degree,
        projects=projects,
        experience_years=experience_years,
        preferred_industry=preferred_industry,
    )

    assert isinstance(res, CareerRecommendationsResponse)
    assert len(res.recommended_roles) >= 4

    top_role = res.recommended_roles[0]
    assert top_role.role_title in ["ML Engineer", "AI Engineer"]
    assert top_role.fit_percentage >= 85.0

    # Verify scores are strictly ordered descending
    fit_scores = [r.fit_percentage for r in res.recommended_roles]
    assert fit_scores == sorted(fit_scores, reverse=True)

    # Verify evidence bullets contain checkmark evidence
    assert len(top_role.evidence_bullets) >= 3
    assert any("Python" in b for b in top_role.evidence_bullets)
    assert any("industry" in b.lower() for b in top_role.evidence_bullets)


def test_career_ranking_engine_reproducibility():
    cand_skills = ["Python", "SQL", "Pandas", "Scikit-Learn"]
    res1 = career_ranking_engine.rank_careers(candidate_skills=cand_skills, preferred_industry="Analytics")
    res2 = career_ranking_engine.rank_careers(candidate_skills=cand_skills, preferred_industry="Analytics")

    assert res1.recommended_roles[0].role_title == res2.recommended_roles[0].role_title
    assert res1.recommended_roles[0].fit_percentage == res2.recommended_roles[0].fit_percentage
