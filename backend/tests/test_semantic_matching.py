import pytest
from app.services.semantic_matching import semantic_matching_engine
from app.services.semantic_matching.similarity_calculator import similarity_calculator
from app.services.semantic_matching.skill_matcher import skill_matcher
from app.services.semantic_matching.experience_matcher import experience_matcher
from app.services.semantic_matching.project_matcher import project_matcher
from app.services.semantic_matching.education_matcher import education_matcher
from app.services.semantic_matching.certification_matcher import certification_matcher
from app.schemas.semantic_matching import SemanticMatchResponse


def test_non_exact_semantic_similarity_scikit_learn():
    """Verify non-exact semantic similarity between scikit-learn and machine learning."""
    resume_skill = "scikit-learn"
    job_req = "machine learning"

    similarity = similarity_calculator.compute_cosine_similarity(resume_skill, job_req)
    assert similarity >= 0.75  # High semantic similarity despite different exact text

    # Test via SkillMatcher
    result = skill_matcher.match_skills([resume_skill], [job_req])
    assert len(result.matched_items) >= 1
    match_item = result.matched_items[0]

    assert match_item.resume_item == "scikit-learn"
    assert match_item.job_requirement == "machine learning"
    assert match_item.similarity >= 0.75
    assert match_item.score >= 75.0
    assert match_item.match is True
    assert "machine learning" in match_item.explanation.lower()


def test_skill_matcher_multiple_domains():
    cand_skills = ["scikit-learn", "FastAPI", "React", "PostgreSQL", "Docker"]
    job_reqs = ["machine learning", "REST API", "Frontend", "Relational Database", "Containerization"]

    result = skill_matcher.match_skills(cand_skills, job_reqs)
    assert result.domain == "skills"
    assert result.score >= 80.0
    assert len(result.matched_items) >= 4

    for item in result.matched_items:
        assert 0.0 <= item.similarity <= 1.0
        assert 0.0 <= item.score <= 100.0
        assert item.match is True
        assert item.explanation != ""


def test_experience_matcher():
    cand_yoe = 5.0
    cand_exp = [
        {"job_title": "Senior Software Engineer", "responsibilities": ["Architected microservices API platform with FastAPI"]}
    ]
    job_min_yoe = 4.0
    job_seniority = "Senior"
    job_resps = ["Design and build scalable REST APIs and microservices platform."]

    result = experience_matcher.match_experience(cand_yoe, cand_exp, job_min_yoe, job_seniority, job_resps)
    assert result.domain == "experience"
    assert result.score >= 80.0
    assert len(result.matched_items) >= 1
    assert result.matched_items[0].match is True
    assert result.matched_items[0].explanation != ""


def test_project_matcher():
    cand_projects = [
        {
            "title": "ATS Resume Checker",
            "description": "Built AI powered resume checking system using Python and NLP.",
            "technologies": ["Python", "FastAPI", "spaCy"]
        }
    ]
    job_reqs = ["Develop natural language processing NLP algorithms for resume parsing."]

    result = project_matcher.match_projects(cand_projects, job_reqs)
    assert result.domain == "projects"
    assert result.score >= 70.0
    assert len(result.matched_items) >= 1
    assert result.matched_items[0].explanation != ""


def test_education_matcher():
    cand_edu = [{"degree": "Bachelor's Degree", "field_of_study": "Computer Science"}]
    job_edu = {"degree_level": "Bachelor's", "field_of_study": "Computer Science"}

    result = education_matcher.match_education(cand_edu, job_edu)
    assert result.domain == "education"
    assert result.score >= 90.0
    assert result.matched_items[0].match is True
    assert "meets or exceeds" in result.matched_items[0].explanation


def test_certification_matcher():
    cand_certs = [{"name": "AWS Certified Solutions Architect"}]
    job_certs = [{"name": "AWS Solutions Architect"}]

    result = certification_matcher.match_certifications(cand_certs, job_certs)
    assert result.domain == "certifications"
    assert result.score >= 90.0
    assert result.matched_items[0].match is True
    assert result.matched_items[0].explanation != ""


def test_full_semantic_matching_engine():
    resume_intel = {
        "skills": [{"name": "scikit-learn"}, {"name": "FastAPI"}, {"name": "Docker"}, {"name": "React"}],
        "experience_years": 5.5,
        "experience": [
            {
                "job_title": "Senior Software Engineer",
                "responsibilities": ["Developed predictive machine learning models using scikit-learn."]
            }
        ],
        "projects": [
            {
                "title": "ML Model Pipeline",
                "description": "Trained predictive models with scikit-learn and FastAPI.",
                "technologies": ["Python", "scikit-learn"]
            }
        ],
        "education": [{"degree": "Bachelor's Degree", "field_of_study": "Computer Science"}],
        "certifications": [{"name": "AWS Certified Solutions Architect"}],
    }

    job_intel = {
        "required_skills": [{"name": "machine learning"}, {"name": "REST API"}],
        "technologies": [{"name": "Docker"}, {"name": "React"}],
        "experience_requirement": {"min_years": 4.0, "seniority_level": "Senior"},
        "responsibilities": ["Build machine learning model pipelines and microservices."],
        "education_requirement": {"degree_level": "Bachelor's", "field_of_study": "Computer Science"},
        "certifications": [{"name": "AWS Certified"}],
    }

    response: SemanticMatchResponse = semantic_matching_engine.match_resume_and_job(resume_intel, job_intel)

    assert 0.0 <= response.overall_score <= 100.0
    assert response.overall_score >= 75.0
    assert response.match_grade in ["Excellent Match", "Strong Match", "Good Match"]

    # Verify every matched item in skill_match has explanation, match: bool, and similarity
    for item in response.skill_match.matched_items:
        assert item.resume_item != ""
        assert item.job_requirement != ""
        assert 0.0 <= item.similarity <= 1.0
        assert 0.0 <= item.score <= 100.0
        assert isinstance(item.match, bool)
        assert item.explanation != ""

    assert len(response.key_strengths) >= 1
