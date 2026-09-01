import pytest
from httpx import AsyncClient
from tests.test_parsers import create_sample_pdf_bytes, create_sample_docx_bytes


async def get_auth_token(async_client: AsyncClient, email: str = "jdtest@example.com") -> str:
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": "JD Tester",
        "role": "RECRUITER",
    }
    resp = await async_client.post("/api/v1/auth/register", json=reg_payload)
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_create_jd_json_success(async_client: AsyncClient):
    token = await get_auth_token(async_client, "json_jd@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "title": "Senior Backend Developer",
        "company_name": "Acme Corp",
        "raw_text": "We are seeking a Senior Backend Engineer with 5+ years of experience in Python, FastAPI, Docker, and PostgreSQL.",
    }

    response = await async_client.post("/api/v1/job-descriptions/text", headers=headers, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Senior Backend Developer"
    assert data["company_name"] == "Acme Corp"
    assert "parsed_requirements" in data
    assert "Python" in data["parsed_requirements"]["extracted_skills"]


@pytest.mark.asyncio
async def test_upload_jd_file_success(async_client: AsyncClient):
    token = await get_auth_token(async_client, "file_jd@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    pdf_bytes = create_sample_pdf_bytes("Staff Cloud Architect Job Posting")

    data = {
        "title": "Staff Cloud Architect",
        "company_name": "CloudTech",
    }
    files = {
        "file": ("architect_jd.pdf", pdf_bytes, "application/pdf")
    }

    response = await async_client.post("/api/v1/job-descriptions", headers=headers, data=data, files=files)
    assert response.status_code == 201
    res_data = response.json()
    assert res_data["title"] == "Staff Cloud Architect"
    assert res_data["file_name"] == "architect_jd.pdf"
    assert res_data["scan_status"] == "CLEAN"


@pytest.mark.asyncio
async def test_list_and_get_and_delete_jds(async_client: AsyncClient):
    token = await get_auth_token(async_client, "crud_jd@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "title": "Frontend Lead",
        "company_name": "NextGen UI",
        "raw_text": "Looking for a Frontend Lead with React, TypeScript, and Next.js skills.",
    }

    # 1. Create
    create_resp = await async_client.post("/api/v1/job-descriptions/text", headers=headers, json=payload)
    assert create_resp.status_code == 201
    job_id = create_resp.json()["id"]

    # 2. List
    list_resp = await async_client.get("/api/v1/job-descriptions", headers=headers)
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert list_data["total"] >= 1
    assert any(j["id"] == job_id for j in list_data["items"])

    # 3. Get single
    get_resp = await async_client.get(f"/api/v1/job-descriptions/{job_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == job_id

    # 4. Delete
    del_resp = await async_client.delete(f"/api/v1/job-descriptions/{job_id}", headers=headers)
    assert del_resp.status_code == 200

    # 5. Verify deleted
    get_after_del = await async_client.get(f"/api/v1/job-descriptions/{job_id}", headers=headers)
    assert get_after_del.status_code == 404
