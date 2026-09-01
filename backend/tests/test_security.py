import pytest
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


def test_password_hashing():
    raw_password = "SecretPassword123!"
    hashed = get_password_hash(raw_password)

    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_access_token():
    user_id = "test-user-uuid-1234"
    role = "RECRUITER"
    token = create_access_token(subject=user_id, role=role)

    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert payload["role"] == role
    assert payload["type"] == "access"
    assert "exp" in payload


def test_jwt_refresh_token():
    user_id = "test-user-uuid-5678"
    token = create_refresh_token(subject=user_id)

    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert payload["type"] == "refresh"
    assert "exp" in payload


def test_invalid_jwt_token():
    with pytest.raises(ValueError, match="Invalid JWT token"):
        decode_token("invalid.jwt.token.string")
