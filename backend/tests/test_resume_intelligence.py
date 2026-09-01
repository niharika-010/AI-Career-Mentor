import pytest
from app.services.resume_intelligence import resume_intelligence_engine
from app.schemas.resume_intelligence import ParsedResumeIntelligence
from tests.test_parsers import create_sample_pdf_bytes, create_sample_docx_bytes


SAMPLE_RESUME_TEXT_1 = """
Sarah Connor
San Francisco, CA | sarah.connor@example.com | +1 (555) 234-5678
linkedin.com/in/sarah-connor-dev | github.com/sarahconnor

PROFESSIONAL SUMMARY
Innovative Senior Software Engineer with 6+ years of experience building scalable distributed systems and cloud platforms. Skilled in Python, FastAPI, React, and AWS.

TECHNICAL SKILLS
Languages: Python, TypeScript, JavaScript, SQL, C++
Frameworks: FastAPI, React, Next.js, Node.js, Django
Databases & Cloud: PostgreSQL, Redis, AWS, Docker, Kubernetes, Terraform
Tools & Practices: Git, CI/CD, REST API, System Design, Microservices

SOFT SKILLS
Leadership, Cross-Functional Collaboration, Problem Solving, Agile

WORK EXPERIENCE
Senior Software Engineer | Cyberdyne Systems
Jan 2021 - Present | San Francisco, CA
• Architected microservices platform handling 10M+ daily requests using Python and FastAPI.
• Managed a team of 4 engineers and improved CI/CD deployment frequency by 40%.

Software Engineer | Skynet Innovations
Jun 2018 - Dec 2020 | San Jose, CA
• Developed React and Node.js frontend dashboards for real-time data analytics.
• Optimized PostgreSQL query performance, reducing p99 latency by 35%.

EDUCATION
Bachelor of Science in Computer Science | Stanford University
2014 - 2018 | GPA: 3.9/4.0

PROJECTS
AI Career Mentor Platform | github.com/sarahconnor/career-mentor
• Built full-stack AI career mentor web application using Next.js and FastAPI.

CERTIFICATIONS
AWS Certified Solutions Architect - Associate | AWS | 2022

ACHIEVEMENTS
1st Place Winner - Bay Area AI Hackathon 2023

LANGUAGES
English (Native), Spanish (Fluent)
"""


SAMPLE_RESUME_TEXT_2 = """
Dr. Marcus Vance
Boston, MA | marcus.vance@ai-lab.io | (617) 555-9012
linkedin.com/in/marcus-vance | github.com/marcusvance

SUMMARY
Senior Data Scientist and Machine Learning Researcher specializing in Deep Learning and Natural Language Processing.

SKILLS
PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, Python, R, SQL, NLP, Transformers, LLMs, Docker, GCP

WORK EXPERIENCE
Lead AI Researcher | OpenAI Labs
2020 - Present
• Fine-tuned large language models resulting in 15% benchmark accuracy improvement.
• Led research on automated retrieval augmented generation (RAG) architectures.

EDUCATION
Doctor of Philosophy (Ph.D.) in Computer Science | Massachusetts Institute of Technology (MIT)
2015 - 2020

CERTIFICATIONS
Google Cloud Professional Data Engineer | GCP | 2021

LANGUAGES
English, German (Professional)
"""


SAMPLE_RESUME_TEXT_3 = """
Alex Mercer
alex.mercer@techgrad.org | github.com/alexmercer-dev

EDUCATION
Bachelor of Technology in Computer Engineering | Indian Institute of Technology
2020 - 2024 | GPA: 3.8

SKILLS
Python, JavaScript, React, PostgreSQL, Git, Docker, Problem Solving, Communication

PROJECTS
Open Source ATS Checker
• Created lightweight open source ATS checker tool using Python and React.

LANGUAGES
English, Hindi
"""


def test_resume_intelligence_sarah_connor():
    parsed: ParsedResumeIntelligence = resume_intelligence_engine.parse_text(SAMPLE_RESUME_TEXT_1)

    # 1. Contact Info Verification
    assert parsed.contact.name.value == "Sarah Connor"
    assert parsed.contact.name.confidence >= 0.80
    assert parsed.contact.email.value == "sarah.connor@example.com"
    assert parsed.contact.email.confidence == 0.99
    assert parsed.contact.phone.value == "+1 (555) 234-5678"
    assert "linkedin.com/in/sarah-connor-dev" in parsed.contact.linkedin_url.value
    assert "github.com/sarahconnor" in parsed.contact.github_url.value

    # 2. Summary
    assert parsed.summary.value is not None
    assert "Senior Software Engineer" in parsed.summary.value

    # 3. Skills Taxonomy
    skill_names = [s.name for s in parsed.skills]
    assert "Python" in skill_names
    assert "FastAPI" in skill_names
    assert "React" in skill_names
    assert "PostgreSQL" in skill_names
    assert "Docker" in skill_names
    assert "Leadership" in skill_names

    # Check skill confidence structure
    python_skill = next(s for s in parsed.skills if s.name == "Python")
    assert python_skill.confidence > 0.80
    assert python_skill.source in ["skills_section", "experience_section", "full_text_heuristic"]

    # 4. Education
    assert len(parsed.education) >= 1
    edu = parsed.education[0]
    assert edu.degree == "Bachelor's Degree"
    assert edu.field_of_study == "Computer Science"
    assert edu.gpa == "3.9"

    # 5. Experience
    assert len(parsed.experience) >= 1
    exp = parsed.experience[0]
    assert exp.job_title == "Senior Software Engineer"
    assert exp.is_current is True
    assert len(exp.responsibilities) > 0

    # 6. Certifications & Achievements & Languages
    assert len(parsed.certifications) >= 1
    assert "AWS Certified Solutions Architect" in parsed.certifications[0].name

    assert len(parsed.achievements) >= 1
    assert "Hackathon" in parsed.achievements[0].title

    assert len(parsed.languages) >= 1
    lang_names = [l.language for l in parsed.languages]
    assert "English" in lang_names

    # 7. Overall Confidence
    assert parsed.overall_confidence > 0.80


def test_resume_intelligence_marcus_vance():
    parsed = resume_intelligence_engine.parse_text(SAMPLE_RESUME_TEXT_2)
    assert "Marcus Vance" in parsed.contact.name.value
    assert parsed.contact.email.value == "marcus.vance@ai-lab.io"

    skill_names = [s.name for s in parsed.skills]
    assert "PyTorch" in skill_names
    assert "TensorFlow" in skill_names

    assert len(parsed.education) >= 1
    assert parsed.education[0].degree == "Ph.D."

    assert len(parsed.experience) >= 1
    assert parsed.experience[0].job_title == "Lead AI Researcher"


def test_resume_intelligence_alex_mercer():
    parsed = resume_intelligence_engine.parse_text(SAMPLE_RESUME_TEXT_3)
    assert parsed.contact.name.value == "Alex Mercer"
    assert parsed.contact.email.value == "alex.mercer@techgrad.org"
    assert "github.com/alexmercer-dev" in parsed.contact.github_url.value

    assert len(parsed.education) >= 1
    assert parsed.education[0].degree == "Bachelor's Degree"
    assert len(parsed.projects) >= 1
    assert "ATS Checker" in parsed.projects[0].title
