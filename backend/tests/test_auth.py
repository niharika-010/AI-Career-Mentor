import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(async_client: AsyncClient):
    payload = {
        "email": "newcandidate@example.com",
        "password": "SecurePassword123!",
        "full_name": "New Candidate",
        "role": "CANDIDATE",
    }
    response = await async_client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "newcandidate@example.com"
    assert data["user"]["role"] == "CANDIDATE"


@pytest.mark.asyncio
async def test_register_duplicate_email(async_client: AsyncClient):
    payload = {
        "email": "duplicate@example.com",
        "password": "SecurePassword123!",
        "full_name": "First User",
        "role": "CANDIDATE",
    }
    resp1 = await async_client.post("/api/v1/auth/register", json=payload)
    assert resp1.status_code == 201

    resp2 = await async_client.post("/api/v1/auth/register", json=payload)
    assert resp2.status_code == 400
    assert "already exists" in resp2.json()["detail"]


@pytest.mark.asyncio
async def test_register_weak_password(async_client: AsyncClient):
    payload = {
        "email": "weakpwd@example.com",
        "password": "123",  # Fails min length, uppercase, lowercase, special char
        "full_name": "Weak Pwd",
    }
    response = await async_client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    # Register
    reg_payload = {
        "email": "logintest@example.com",
        "password": "ValidPassword99!",
        "full_name": "Login User",
        "role": "RECRUITER",
    }
    await async_client.post("/api/v1/auth/register", json=reg_payload)

    # Login
    login_payload = {
        "email": "logintest@example.com",
        "password": "ValidPassword99!",
    }
    response = await async_client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["role"] == "RECRUITER"


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client: AsyncClient):
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "ValidPassword99!",
    }
    response = await async_client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_flow(async_client: AsyncClient):
    reg_payload = {
        "email": "refreshtest@example.com",
        "password": "ValidPassword99!",
    }
    reg_resp = await async_client.post("/api/v1/auth/register", json=reg_payload)
    refresh_token = reg_resp.json()["refresh_token"]

    refresh_resp = await async_client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 200
    data = refresh_resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_get_me_authenticated(async_client: AsyncClient):
    reg_payload = {
        "email": "metest@example.com",
        "password": "ValidPassword99!",
        "full_name": "Me User",
    }
    reg_resp = await async_client.post("/api/v1/auth/register", json=reg_payload)
    access_token = reg_resp.json()["access_token"]

    me_resp = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_resp.status_code == 200
    data = me_resp.json()
    assert data["email"] == "metest@example.com"
    assert data["full_name"] == "Me User"


@pytest.mark.asyncio
async def test_get_me_unauthorized(async_client: AsyncClient):
    me_resp = await async_client.get("/api/v1/auth/me")
    assert me_resp.status_code == 401


@pytest.mark.asyncio
async def test_forgot_and_reset_password_flow(async_client: AsyncClient):
    reg_payload = {
        "email": "recover@example.com",
        "password": "OriginalPassword1!",
    }
    await async_client.post("/api/v1/auth/register", json=reg_payload)

    # 1. Forgot password
    forgot_resp = await async_client.post("/api/v1/auth/forgot-password", json={"email": "recover@example.com"})
    assert forgot_resp.status_code == 200
    reset_token = forgot_resp.json()["reset_token"]
    assert reset_token is not None

    # 2. Reset password
    reset_resp = await async_client.post(
        "/api/v1/auth/reset-password",
        json={"token": reset_token, "new_password": "NewSecretPassword2!"},
    )
    assert reset_resp.status_code == 200

    # 3. Login with old password (should fail)
    fail_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "recover@example.com", "password": "OriginalPassword1!"},
    )
    assert fail_login.status_code == 401

    # 4. Login with new password (should succeed)
    succ_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "recover@example.com", "password": "NewSecretPassword2!"},
    )
    assert succ_login.status_code == 200
