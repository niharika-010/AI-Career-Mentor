import pytest
from app.services.match_scoring.confidence_engine import analysis_confidence_engine, AnalysisConfidenceEngine


def test_high_confidence_analysis():
    resume_intel = {
        "contact": {
            "name": {"value": "Jane Doe", "confidence": 0.95},
            "email": {"value": "jane@example.com", "confidence": 0.98},
            "phone": {"value": "+1-555-0199", "confidence": 0.90}
        },
        "skills": [{"name": "Python"}, {"name": "FastAPI"}, {"name": "Docker"}, {"name": "PostgreSQL"}, {"name": "AWS"}, {"name": "React"}],
        "experience_years": 6.0,
        "experience": [{"job_title": "Senior Backend Developer", "responsibilities": ["Designed microservices"]}],
        "education": [{"degree": "Master's Degree", "field_of_study": "Computer Science"}],
        "sections": {"summary": True, "skills": True, "experience": True, "education": True}
    }

    job_intel = {
        "job_title": "Senior Python Backend Engineer",
        "required_skills": [{"name": "Python"}, {"name": "FastAPI"}, {"name": "Docker"}],
        "technologies": [{"name": "PostgreSQL"}],
        "experience_requirement": {"min_years": 5.0, "seniority_level": "Senior"},
        "responsibilities": ["Architect microservices APIs.", "Lead backend optimization."],
        "education_requirement": {"degree_level": "Bachelor's"}
    }

    res = analysis_confidence_engine.calculate_confidence(resume_intel, job_intel)
    assert res.confidence_score >= 80.0
    assert res.confidence_level == "High"
    assert len(res.confidence_reasons) >= 5


def test_low_confidence_due_to_missing_data():
    resume_intel = {
        "contact": {},
        "skills": [],
        "experience_years": 0.0,
        "experience": [],
        "education": [],
        "sections": {}
    }

    job_intel = {
        "job_title": "Unspecified Title",
        "required_skills": [],
        "experience_requirement": {},
        "responsibilities": []
    }

    res = analysis_confidence_engine.calculate_confidence(resume_intel, job_intel)
    assert res.confidence_score < 60.0
    assert res.confidence_level == "Low"
    assert any("Ambiguity Penalty" in r for r in res.confidence_reasons)


def test_confidence_reproducibility():
    resume_intel = {
        "contact": {"name": {"value": "Alice"}, "email": {"value": "alice@example.com"}},
        "skills": [{"name": "Python"}, {"name": "Django"}, {"name": "SQL"}],
        "experience_years": 3.0,
        "experience": [{"job_title": "Software Developer"}],
        "education": [{"degree": "Bachelor's Degree"}],
    }
    job_intel = {
        "job_title": "Full Stack Engineer",
        "required_skills": [{"name": "Python"}],
        "experience_requirement": {"min_years": 2.0},
        "responsibilities": ["Develop web applications."]
    }

    res1 = analysis_confidence_engine.calculate_confidence(resume_intel, job_intel)
    res2 = analysis_confidence_engine.calculate_confidence(resume_intel, job_intel)

    assert res1.confidence_score == res2.confidence_score
    assert res1.confidence_level == res2.confidence_level
    assert res1.confidence_reasons == res2.confidence_reasons
