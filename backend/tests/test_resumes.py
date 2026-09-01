import pytest
from httpx import AsyncClient
from tests.test_parsers import create_sample_pdf_bytes, create_sample_docx_bytes


async def get_auth_token(async_client: AsyncClient, email: str = "resumetest@example.com") -> str:
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": "Resume Tester",
        "role": "CANDIDATE",
    }
    resp = await async_client.post("/api/v1/auth/register", json=reg_payload)
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_upload_pdf_resume_success(async_client: AsyncClient):
    token = await get_auth_token(async_client, "pdf_test@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    pdf_bytes = create_sample_pdf_bytes("Alice Engineer Resume")

    files = {
        "file": ("alice_resume.pdf", pdf_bytes, "application/pdf")
    }

    response = await async_client.post("/api/v1/resumes", headers=headers, files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["file_name"] == "alice_resume.pdf"
    assert data["scan_status"] == "CLEAN"
    assert "parsed_data" in data
    assert data["parsed_data"]["metadata"]["preprocessed"] is True


@pytest.mark.asyncio
async def test_upload_docx_resume_success(async_client: AsyncClient):
    token = await get_auth_token(async_client, "docx_test@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    docx_bytes = create_sample_docx_bytes("Bob Engineer Resume")

    files = {
        "file": ("bob_resume.docx", docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    }

    response = await async_client.post("/api/v1/resumes", headers=headers, files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["file_name"] == "bob_resume.docx"
    assert "parsed_data" in data


@pytest.mark.asyncio
async def test_list_and_get_and_delete_resumes(async_client: AsyncClient):
    token = await get_auth_token(async_client, "crud_test@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    pdf_bytes = create_sample_pdf_bytes("Charlie Resume")

    # 1. Upload
    upload_resp = await async_client.post(
        "/api/v1/resumes",
        headers=headers,
        files={"file": ("charlie.pdf", pdf_bytes, "application/pdf")},
    )
    assert upload_resp.status_code == 201
    resume_id = upload_resp.json()["id"]

    # 2. List
    list_resp = await async_client.get("/api/v1/resumes", headers=headers)
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert list_data["total"] >= 1
    assert any(r["id"] == resume_id for r in list_data["items"])

    # 3. Get single
    get_resp = await async_client.get(f"/api/v1/resumes/{resume_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == resume_id

    # 4. Delete
    del_resp = await async_client.delete(f"/api/v1/resumes/{resume_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["id"] == resume_id

    # 5. Verify deleted
    get_after_del = await async_client.get(f"/api/v1/resumes/{resume_id}", headers=headers)
    assert get_after_del.status_code == 404
