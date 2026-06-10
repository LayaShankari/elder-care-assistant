from datetime import timedelta

from app.utils.security import create_access_token, decode_token, hash_password, verify_password


def test_password_hash_and_verify():
    hashed_password = hash_password("safe-password")

    assert hashed_password != "safe-password"
    assert verify_password("safe-password", hashed_password)
    assert not verify_password("wrong-password", hashed_password)


def test_create_and_decode_access_token():
    token = create_access_token(
        {"sub": "user-123"},
        expires_delta=timedelta(minutes=5),
    )

    payload = decode_token(token)

    assert payload is not None
    assert payload["sub"] == "user-123"


def test_decode_invalid_token_returns_none():
    assert decode_token("not-a-valid-token") is None
