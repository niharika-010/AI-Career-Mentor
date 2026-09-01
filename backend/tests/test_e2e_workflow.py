import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.test_parsers import create_sample_pdf_bytes

@pytest.mark.asyncio
async def test_full_end_to_end_user_lifecycle(async_client: AsyncClient, db_session: AsyncSession):
    """Full End-to-End User Lifecycle Integration Test:
    1. Register Candidate
    2. Login Candidate
    3. Upload Resume
    4. Create Job Description
    5. Execute Match Analysis
    6. Compute Explainable AI Match
    7. Generate AI Guidance (Bullet Rewrite & Interview Prep)
    8. Export PDF Report
    9. Retrieve Analysis History Log
    """
    user_email = f"candidate_e2e_{uuid.uuid4().hex[:6]}@example.com"
    password = "SecurePassword123!"

    # 1. Register Candidate
    reg_res = await async_client.post(
        "/api/v1/auth/register",
        json={"email": user_email, "password": password, "full_name": "E2E Candidate", "role": "CANDIDATE"}
    )
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    access_token = reg_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 2. Login Candidate
    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": user_email, "password": password}
    )
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data

    # 3. Upload Resume (PDF)
    pdf_bytes = create_sample_pdf_bytes("E2E Candidate Resume Python FastAPI SQL Docker")
    files = {"file": ("resume_e2e.pdf", pdf_bytes, "application/pdf")}
    upload_res = await async_client.post("/api/v1/resumes", headers=headers, files=files)
    assert upload_res.status_code == 201
    resume_data = upload_res.json()
    resume_id = resume_data["id"]

    # 4. Create Job Description
    job_payload = {
        "title": "Machine Learning Engineer",
        "company_name": "AI Tech Corp",
        "raw_text": "We are seeking a Machine Learning Engineer with strong Python, FastAPI, Docker, and PyTorch experience."
    }
    job_res = await async_client.post("/api/v1/job-descriptions", headers=headers, data=job_payload)
    assert job_res.status_code == 201
    job_data = job_res.json()
    job_id = job_data["id"]

    # 5. Execute Match Analysis
    match_payload = {
        "resume_id": resume_id,
        "job_description_id": job_id,
    }
    analysis_res = await async_client.post("/api/v1/analysis/match", headers=headers, json=match_payload)
    assert analysis_res.status_code == 200
    analysis_data = analysis_res.json()
    assert "overall_score" in analysis_data
    assert analysis_data["overall_score"] >= 50.0

    # 6. Compute Explainable AI Match
    explain_res = await async_client.post("/api/v1/analysis/explain", headers=headers, json=match_payload)
    assert explain_res.status_code == 200
    explain_data = explain_res.json()
    assert "matched_skills_explanation" in explain_data
    assert "overall_score" in explain_data

    # 7. Generate AI Guidance (Bullet Rewrite & Interview Prep)
    rewrite_res = await async_client.post(
        "/api/v1/guidance/rewrite-project",
        headers=headers,
        json={"original_text": "Built ML model with Python."}
    )
    assert rewrite_res.status_code == 200
    assert "rewritten_bullet" in rewrite_res.json()

    interview_res = await async_client.post(
        "/api/v1/guidance/interview-prep",
        headers=headers,
        json={"job_title": "ML Engineer", "candidate_skills": ["Python", "Docker"]}
    )
    assert interview_res.status_code == 200
    assert "questions" in interview_res.json()

    # 8. Export PDF Report
    pdf_res = await async_client.post(
        "/api/v1/analysis/pdf",
        headers=headers,
        json={
            "candidate_name": "E2E Candidate",
            "target_role": "Machine Learning Engineer",
            "overall_score": 88.0,
            "ats_score": 92.0,
        }
    )
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert pdf_res.content.startswith(b"%PDF-")

    # 9. Retrieve Analysis History Log
    history_res = await async_client.get("/api/v1/analysis/history", headers=headers)
    assert history_res.status_code == 200
    assert isinstance(history_res.json(), list)
