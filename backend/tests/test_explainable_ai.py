import pytest
from app.services.explainable_ai import explanation_generator, evidence_collector, claim_validator
from app.schemas.explainable_ai import ExplainableMatchResponse


def test_evidence_collector():
    resume_intel = {
        "skills": [{"name": "Python"}, {"name": "FastAPI"}, {"name": "Docker"}],
        "experience_years": 5.0,
        "experience": [{"job_title": "Senior Engineer"}],
        "projects": [{"title": "Cloud API", "technologies": ["Python"]}],
        "education": [{"degree": "Master's Degree", "field_of_study": "Computer Science"}],
        "certifications": [{"name": "AWS Certified"}],
        "contact": {"name": {"value": "John"}, "email": {"value": "john@example.com"}}
    }

    job_intel = {
        "required_skills": [{"name": "Python"}, {"name": "FastAPI"}],
        "experience_requirement": {"min_years": 4.0, "seniority_level": "Senior"},
        "education_requirement": {"degree_level": "Master's"},
        "certifications": [],
        "technical_keywords": [{"name": "Python"}]
    }

    evidence = evidence_collector.collect_evidence(resume_intel, job_intel)

    assert len(evidence["matched_skills"]) >= 1
    assert "Requirement 'Python' matched" in evidence["matched_skills"][0] or "Requirement 'FastAPI' matched" in evidence["matched_skills"][0]
    assert "Candidate has 5.0 YOE" in evidence["experience"][0]
    assert "Master's Degree" in evidence["education"][0]


def test_claim_validator_blocks_contradictions_and_unsupported_claims():
    # 1. Test High Score Contradiction (High score cannot say "poor fit" or "unqualified")
    is_valid, sanitized, violations = claim_validator.validate_explanation(
        explanation_text="Candidate is an unqualified poor fit for the role.",
        score=95.0,
        evidence_list=["Requirement 'Python' matched."],
    )
    assert is_valid is False
    assert len(violations) >= 1
    assert "Contradiction" in violations[0]
    assert "Evaluated Score: 95.0/100" in sanitized

    # 2. Test Low Score Contradiction (Low score cannot say "perfect candidate")
    is_valid_low, sanitized_low, violations_low = claim_validator.validate_explanation(
        explanation_text="This candidate is a perfect candidate and flawless fit.",
        score=30.0,
        evidence_list=["Missing skill 'AWS'."],
    )
    assert is_valid_low is False
    assert len(violations_low) >= 1
    assert "Contradiction" in violations_low[0]

    # 3. Test Unsupported Technical Skill Claim (Skill mentioned in prose but missing from evidence)
    is_valid_claim, _, violations_claim = claim_validator.validate_explanation(
        explanation_text="Candidate demonstrates extensive experience with Kubernetes.",
        score=75.0,
        evidence_list=["Requirement 'Python' matched."],
        allowed_tokens=["Python", "FastAPI"]
    )
    assert is_valid_claim is False
    assert any("Kubernetes" in v for v in violations_claim)


def test_explainable_match_generation():
    resume_intel = {
        "skills": [{"name": "Python"}, {"name": "FastAPI"}, {"name": "Docker"}, {"name": "PostgreSQL"}],
        "experience_years": 5.0,
        "experience": [{"job_title": "Senior Engineer", "responsibilities": ["Built APIs"]}],
        "projects": [{"title": "API Gateway", "description": "Routing service", "technologies": ["Python"]}],
        "education": [{"degree": "Bachelor's Degree", "field_of_study": "Computer Science"}],
        "certifications": [{"name": "AWS Certified"}],
        "contact": {"name": {"value": "Jane"}, "email": {"value": "jane@example.com"}}
    }

    job_intel = {
        "required_skills": [{"name": "Python"}, {"name": "FastAPI"}, {"name": "Docker"}],
        "technologies": [{"name": "PostgreSQL"}],
        "experience_requirement": {"min_years": 4.0, "seniority_level": "Senior"},
        "responsibilities": ["Build REST APIs with FastAPI."],
        "education_requirement": {"degree_level": "Bachelor's"},
        "certifications": [],
        "technical_keywords": [{"name": "Python"}]
    }

    res = explanation_generator.generate_explainable_match(resume_intel, job_intel)

    assert isinstance(res, ExplainableMatchResponse)
    assert res.overall_score >= 80.0

    # Verify all 8 explanation models are populated with non-empty evidence and explanations
    assert res.matched_skills_explanation.score >= 80.0
    assert len(res.matched_skills_explanation.evidence) >= 1
    assert "Python" in res.matched_skills_explanation.matched_items

    assert res.missing_skills_explanation.score >= 80.0

    assert res.experience_explanation.cand_yoe == 5.0
    assert res.experience_explanation.job_min_yoe == 4.0

    assert len(res.project_explanation.relevant_projects) >= 1

    assert res.education_explanation.cand_degree == "Bachelor's Degree"

    assert len(res.certification_explanation.evidence) >= 1

    assert len(res.ats_explanation.evidence) >= 1

    assert len(res.keyword_explanation.evidence) >= 1
