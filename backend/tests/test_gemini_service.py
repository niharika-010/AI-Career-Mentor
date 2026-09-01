import pytest
from app.services.gemini import (
    gemini_service,
    gemini_client,
    prompt_manager,
    structured_output_validator,
    ai_response_cache,
)
from app.schemas.ai_guidance import (
    ResumeSummaryResponse,
    RewriteBulletResponse,
    CoverLetterResponse,
    InterviewPrepResponse,
    SkillGapRoadmapResponse,
    CareerRecommendationsResponse,
)


def test_gemini_client_configuration_and_isolation():
    assert hasattr(gemini_client, "is_configured")
    assert hasattr(gemini_client, "generate_content")
    # API key is never exposed on client representation
    assert not hasattr(gemini_client, "frontend_key")


def test_structured_output_validator():
    raw_json_str = '```json\n{"executive_summary": "Test Summary", "key_highlights": ["Highlight 1"], "suggested_roles": ["Engineer"]}\n```'
    parsed = structured_output_validator.validate_and_parse(raw_json_str, ResumeSummaryResponse)
    assert parsed is not None
    assert parsed.executive_summary == "Test Summary"
    assert parsed.key_highlights == ["Highlight 1"]

    # Invalid JSON string handles gracefully without throwing
    invalid_parsed = structured_output_validator.validate_and_parse("Not a JSON string", ResumeSummaryResponse)
    assert invalid_parsed is None


def test_ai_response_cache():
    ai_response_cache.clear()
    ai_response_cache.set("test_task", "test_payload", "test_result")
    assert ai_response_cache.get("test_task", "test_payload") == "test_result"
    assert ai_response_cache.get("test_task", "different_payload") is None


def test_all_eight_generation_methods():
    # 1. Resume Summary
    summary = gemini_service.generate_resume_summary("Senior Software Engineer with 5 years experience in Python and FastAPI.")
    assert isinstance(summary, ResumeSummaryResponse)
    assert len(summary.executive_summary) > 10

    # 2. Rewrite Project
    proj_rewrite = gemini_service.rewrite_project("Built a user login feature.")
    assert isinstance(proj_rewrite, RewriteBulletResponse)
    assert len(proj_rewrite.rewritten_bullet) > 10

    # 3. Rewrite Experience
    exp_rewrite = gemini_service.rewrite_experience("Managed backend database tables.")
    assert isinstance(exp_rewrite, RewriteBulletResponse)
    assert len(exp_rewrite.rewritten_bullet) > 10

    # 4. Cover Letter
    cover_letter = gemini_service.generate_cover_letter("Resume content", "Job description content", "Acme Corp", "Senior Developer")
    assert isinstance(cover_letter, CoverLetterResponse)
    assert "Acme Corp" in cover_letter.salutation or "Acme Corp" in cover_letter.full_cover_letter or "Hiring" in cover_letter.salutation

    # 5. Interview Questions
    interview = gemini_service.generate_interview_questions("Python Developer", "Need Python experience", ["Python", "FastAPI"])
    assert isinstance(interview, InterviewPrepResponse)
    assert len(interview.questions) >= 5
    categories = {q.category for q in interview.questions}
    assert "Technical" in categories
    assert "Behavioral" in categories
    assert "HR" in categories
    assert "Project" in categories
    assert "Role-specific" in categories
    first_q = interview.questions[0]
    assert first_q.difficulty in ["Beginner", "Intermediate", "Advanced"]
    assert len(first_q.why_this_question) > 5
    assert len(first_q.suggested_topics) >= 1

    # 6. Skill Gap Roadmap
    roadmap = gemini_service.generate_skill_gap_roadmap(["Python"], ["Python", "Kubernetes", "AWS"])
    assert isinstance(roadmap, SkillGapRoadmapResponse)
    assert "Kubernetes" in roadmap.missing_skills or "AWS" in roadmap.missing_skills
    assert len(roadmap.current_skills_proficiency) >= 1
    assert len(roadmap.missing_skills_proficiency) >= 1
    assert len(roadmap.weekly_roadmap) == 4

    # 7. Career Recommendations
    career_recs = gemini_service.generate_career_recommendations(["Python", "FastAPI"], 5.0, "Software Developer")
    assert isinstance(career_recs, CareerRecommendationsResponse)
    assert len(career_recs.recommended_roles) >= 1

    # 8. Explanation Polish
    exp_text = gemini_service.generate_explanation("Candidate has 5 YOE matching requirements.", 85.0)
    assert len(exp_text) > 5
