import pytest
from app.services.job_intelligence import job_intelligence_engine
from app.schemas.job_intelligence import ParsedJobIntelligence


SAMPLE_JD_TEXT_1 = """
Senior Backend Engineer
Company: Quantum Innovations | Location: San Francisco, CA

ABOUT THE ROLE
We are seeking a Senior Backend Engineer to design and build high-throughput microservices for our cloud platform.

RESPONSIBILITIES
• Architect scalable REST APIs and microservices using Python and FastAPI.
• Lead backend code reviews and mentor junior developers.
• Optimize PostgreSQL database queries and data pipelines.

REQUIRED QUALIFICATIONS
• Must have at least 5+ years of professional experience in backend software development.
• Strong experience with Python, FastAPI, PostgreSQL, Docker, and AWS.
• Solid background in System Design, Microservices, and REST API architecture.
• Bachelor's Degree in Computer Science or Software Engineering required.

PREFERRED QUALIFICATIONS
• Experience with Kubernetes and Redis is a plus.
• Familiarity with GraphQL and Serverless architecture is preferred.
• AWS Certified Solutions Architect certification is a bonus.

TOOLS & ENVIRONMENT
Git, Jira, Postman, Docker, AWS
"""


SAMPLE_JD_TEXT_2 = """
Lead AI Engineer (Machine Learning)
Location: Boston, MA | Industry: Artificial Intelligence

ROLE OVERVIEW
Join our AI Research team to build cutting-edge Generative AI and LLM solutions.

REQUIREMENTS
• Minimum 6 years of experience in Machine Learning and AI engineering.
• Deep proficiency with PyTorch, TensorFlow, Scikit-Learn, and Python.
• Strong experience with Natural Language Processing (NLP), Transformers, and RAG architectures.
• Ph.D. or Master's Degree in Computer Science, Data Science, or Artificial Intelligence preferred.

DESIRED SKILLS
• Experience with GCP and Kubernetes is desirable.
• Google Cloud Certified Data Engineer is a plus.
"""


SAMPLE_JD_TEXT_3 = """
Frontend Developer
Location: Remote

REQUIREMENTS
• 3+ years of experience with React, TypeScript, HTML, CSS, and Tailwind CSS.
• Experience with Git, GitHub, and Jira.
• Good communication and problem solving skills.
"""


def test_job_intelligence_senior_backend_engineer():
    parsed: ParsedJobIntelligence = job_intelligence_engine.parse_text(
        SAMPLE_JD_TEXT_1, title="Senior Backend Engineer", company_name="Quantum Innovations"
    )

    # 1. Title & Industry Normalization
    assert parsed.job_title == "Senior Backend Engineer"
    assert parsed.company_name == "Quantum Innovations"
    assert parsed.industry in ["Cloud & Infrastructure", "Software & SaaS", "Technology & Software"]

    # 2. Required vs Preferred Skills
    req_names = [s.name for s in parsed.required_skills]
    assert "Python" in req_names
    assert "FastAPI" in req_names
    assert "PostgreSQL" in req_names
    assert "Docker" in req_names
    assert "AWS" in req_names

    pref_names = [s.name for s in parsed.preferred_skills]
    assert "Kubernetes" in pref_names or "Redis" in pref_names

    # 3. Source Text & Confidence Verification for every requirement item
    for req in parsed.required_skills:
        assert req.name is not None
        assert req.category in ["technology", "tool", "keyword", "soft_skill", "required_skill"]
        assert req.requirement_type == "required"
        assert 0.0 <= req.confidence <= 1.0
        assert req.source_text != ""  # Non-empty source_text attribution

    for pref in parsed.preferred_skills:
        assert pref.requirement_type == "preferred"
        assert pref.source_text != ""

    # 4. Responsibilities
    assert len(parsed.responsibilities) >= 2
    for resp in parsed.responsibilities:
        assert resp.source_text != ""

    # 5. Experience Requirements
    assert parsed.experience_requirement.min_years == 5.0
    assert parsed.experience_requirement.seniority_level == "Senior"
    assert parsed.experience_requirement.source_text != ""

    # 6. Education Requirements
    assert parsed.education_requirement.degree_level == "Bachelor's"
    assert parsed.education_requirement.field_of_study in ["Computer Science", "Software Engineering"]

    # 7. Certifications
    assert len(parsed.certifications) >= 1
    assert "AWS Certified" in parsed.certifications[0].name
    assert parsed.certifications[0].source_text != ""

    # 8. Overall Confidence
    assert parsed.overall_confidence > 0.80


def test_job_intelligence_lead_ai_engineer():
    parsed = job_intelligence_engine.parse_text(
        SAMPLE_JD_TEXT_2, title="Lead AI Engineer", company_name="AI Research Corp"
    )

    assert parsed.job_title == "Lead AI Engineer"
    assert parsed.industry == "AI & Machine Learning"

    req_names = [s.name for s in parsed.required_skills]
    assert "PyTorch" in req_names
    assert "TensorFlow" in req_names

    assert parsed.experience_requirement.min_years == 6.0
    assert parsed.experience_requirement.seniority_level == "Lead"

    assert parsed.education_requirement.degree_level in ["Master's", "Ph.D."]
    assert parsed.education_requirement.requirement_type == "preferred"


def test_job_intelligence_frontend_developer():
    parsed = job_intelligence_engine.parse_text(SAMPLE_JD_TEXT_3, title="Frontend Developer")

    assert parsed.job_title == "Frontend Developer"
    req_names = [s.name for s in parsed.required_skills]
    assert "React" in req_names
    assert "TypeScript" in req_names

    tool_names = [t.name for t in parsed.tools]
    assert "Git" in tool_names or "GitHub" in tool_names

    assert parsed.experience_requirement.min_years == 3.0
    assert parsed.experience_requirement.seniority_level == "Mid-Level"
