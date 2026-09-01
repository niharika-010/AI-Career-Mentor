import pytest
from app.services.match_scoring import deterministic_scoring_engine, DeterministicScoringEngine
from app.schemas.match_scoring import DeterministicMatchResponse, ComponentScores


def test_individual_component_scoring_functions():
    engine = DeterministicScoringEngine()

    # 1. Skill score test
    s_skill, matched, missing = engine.calculate_skill_score(
        candidate_skills=["Python", "FastAPI", "Docker", "PostgreSQL"],
        job_skills=["Python", "FastAPI", "Docker", "AWS"]
    )
    assert s_skill == 75.0  # 3 of 4 matched
    assert "Python" in matched
    assert "AWS" in missing

    # 2. Experience score test
    s_exp = engine.calculate_experience_score(
        candidate_yoe=5.0,
        candidate_experiences=[{"job_title": "Senior Software Engineer", "responsibilities": ["Architected microservices"]}],
        job_min_yoe=5.0,
        job_seniority="Senior",
        job_responsibilities=["Architect microservices APIs."]
    )
    assert 80.0 <= s_exp <= 100.0

    # 3. Project score test
    s_proj = engine.calculate_project_score(
        candidate_projects=[{"title": "ATS Engine", "description": "Built AI scoring system", "technologies": ["Python"]}],
        job_responsibilities=["Develop AI scoring engines."]
    )
    assert s_proj >= 70.0

    # 4. Education score test
    s_edu = engine.calculate_education_score(
        candidate_education=[{"degree": "Bachelor's Degree", "field_of_study": "Computer Science"}],
        job_education_req={"degree_level": "Bachelor's"}
    )
    assert s_edu == 100.0

    # 5. Certification score test
    s_cert = engine.calculate_certification_score(
        candidate_certs=[{"name": "AWS Certified Solutions Architect"}],
        job_certs=[{"name": "AWS Certified"}]
    )
    assert s_cert == 100.0

    # 6. Keyword score test
    s_kw = engine.calculate_keyword_score(
        candidate_skills=["Python", "FastAPI", "PostgreSQL"],
        job_keywords=["Python", "PostgreSQL"]
    )
    assert s_kw == 100.0


def test_formula_weighted_sum_exactness():
    engine = DeterministicScoringEngine()

    skills = 80.0
    semantic = 90.0
    experience = 70.0
    projects = 85.0
    education = 100.0
    certifications = 50.0
    ats = 90.0
    keywords = 80.0

    # Formula:
    # 80*0.35 (28.0) + 90*0.20 (18.0) + 70*0.15 (10.5) + 85*0.10 (8.5) +
    # 100*0.05 (5.0) + 50*0.05 (2.5) + 90*0.05 (4.5) + 80*0.05 (4.0) = 81.00

    expected_overall = (
        80.0 * 0.35 + 90.0 * 0.20 + 70.0 * 0.15 + 85.0 * 0.10 +
        100.0 * 0.05 + 50.0 * 0.05 + 90.0 * 0.05 + 80.0 * 0.05
    )

    actual_overall = engine.calculate_overall_score(
        skills, semantic, experience, projects, education, certifications, ats, keywords
    )

    assert actual_overall == round(expected_overall, 2)
    assert actual_overall == 81.00


def test_deterministic_reproducibility():
    """Verify that multiple executions with identical inputs produce 100% identical score payloads."""
    resume_intel = {
        "skills": [{"name": "Python"}, {"name": "FastAPI"}, {"name": "PostgreSQL"}, {"name": "Docker"}],
        "experience_years": 5.0,
        "experience": [{"job_title": "Software Engineer", "responsibilities": ["Built REST APIs"]}],
        "projects": [{"title": "API Gateway", "description": "Built API routing service", "technologies": ["Python"]}],
        "education": [{"degree": "Bachelor's Degree", "field_of_study": "Computer Science"}],
        "certifications": [],
        "contact": {"name": {"value": "John Doe"}, "email": {"value": "john@example.com"}, "phone": {"value": "+123456789"}}
    }

    job_intel = {
        "required_skills": [{"name": "Python"}, {"name": "FastAPI"}, {"name": "Docker"}],
        "technologies": [{"name": "PostgreSQL"}],
        "experience_requirement": {"min_years": 4.0, "seniority_level": "Senior"},
        "responsibilities": ["Build REST APIs with FastAPI."],
        "education_requirement": {"degree_level": "Bachelor's"},
        "certifications": [],
        "technical_keywords": [{"name": "Python"}, {"name": "PostgreSQL"}]
    }

    raw_text = "John Doe\njohn@example.com\nSUMMARY\nSenior Engineer with Python experience.\nEXPERIENCE\n• Built REST APIs using FastAPI and PostgreSQL."

    res1 = deterministic_scoring_engine.calculate_match(resume_intel, job_intel, raw_resume_text=raw_text)
    res2 = deterministic_scoring_engine.calculate_match(resume_intel, job_intel, raw_resume_text=raw_text)

    # Assert exact score identity across runs
    assert res1.overall_score == res2.overall_score
    assert res1.component_scores.skills == res2.component_scores.skills
    assert res1.component_scores.semantic_similarity == res2.component_scores.semantic_similarity
    assert res1.component_scores.experience == res2.component_scores.experience
    assert res1.component_scores.projects == res2.component_scores.projects
    assert res1.component_scores.education == res2.component_scores.education
    assert res1.component_scores.certifications == res2.component_scores.certifications
    assert res1.component_scores.ats == res2.component_scores.ats
    assert res1.component_scores.keywords == res2.component_scores.keywords

    # Assert explanations presence and non-LLM deterministic construction
    assert "formula" in res1.explanations
    assert f"Overall =" in res1.explanations["formula"]
    assert len(res1.strengths) >= 1


def test_deterministic_zero_variance_multi_iteration():
    """Verify that 10 consecutive evaluations on the same input yield 0.00 score variance."""
    resume_intel = {
        "skills": [{"name": "Python"}, {"name": "Machine Learning"}, {"name": "SQL"}],
        "experience_years": 3.0,
        "experience": [{"job_title": "ML Engineer", "responsibilities": ["Trained PyTorch models"]}],
        "projects": [{"title": "ML Model", "description": "Trained ML model", "technologies": ["Python"]}],
        "education": [{"degree": "Bachelor's Degree", "field_of_study": "Computer Science"}],
        "certifications": [],
        "contact": {"name": {"value": "Priya"}, "email": {"value": "priya@example.com"}}
    }

    job_intel = {
        "required_skills": [{"name": "Python"}, {"name": "Machine Learning"}, {"name": "Docker"}],
        "technologies": [{"name": "SQL"}],
        "experience_requirement": {"min_years": 3.0, "seniority_level": "Mid"},
        "responsibilities": ["Train PyTorch models and deploy API."],
        "education_requirement": {"degree_level": "Bachelor's"},
        "certifications": [],
        "technical_keywords": [{"name": "Python"}, {"name": "SQL"}]
    }

    scores = []
    for _ in range(10):
        res = deterministic_scoring_engine.calculate_match(resume_intel, job_intel, raw_resume_text="Priya priya@example.com ML Engineer Python SQL")
        scores.append(res.overall_score)

    # Calculate variance
    mean_score = sum(scores) / len(scores)
    variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)

    assert variance == 0.00
    assert len(set(scores)) == 1  # 100% exact numerical identity across all 10 runs


def test_deterministic_skill_permutation_invariance():
    """Verify that permuting skill order does not alter the canonical match score."""
    resume_intel_1 = {
        "skills": [{"name": "Python"}, {"name": "FastAPI"}, {"name": "PostgreSQL"}],
        "experience_years": 4.0,
        "experience": [],
        "projects": [],
        "education": [],
        "certifications": [],
    }

    resume_intel_2 = {
        "skills": [{"name": "PostgreSQL"}, {"name": "Python"}, {"name": "FastAPI"}],
        "experience_years": 4.0,
        "experience": [],
        "projects": [],
        "education": [],
        "certifications": [],
    }

    job_intel = {
        "required_skills": [{"name": "FastAPI"}, {"name": "Python"}, {"name": "PostgreSQL"}],
        "technologies": [],
        "experience_requirement": {"min_years": 3.0},
        "responsibilities": [],
        "education_requirement": {},
        "certifications": [],
        "technical_keywords": []
    }

    res1 = deterministic_scoring_engine.calculate_match(resume_intel_1, job_intel)
    res2 = deterministic_scoring_engine.calculate_match(resume_intel_2, job_intel)

    assert res1.overall_score == res2.overall_score
    assert res1.component_scores.skills == res2.component_scores.skills
