import pytest
from core.security import hash_password, verify_password, create_access_token, decode_access_token

def test_hash_password():
    password = "testpass"
    hashed = hash_password(password)
    assert hashed != password
    assert len(hashed) > 10

def test_verify_password():
    password = "testpass"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpass", hashed) is False

def test_create_and_decode_token():
    data = {"sub": "1"}
    token = create_access_token(data)
    decoded = decode_access_token(token)
    assert decoded["sub"] == "1"
    invalid_token = "invalid"
    assert decode_access_token(invalid_token) is None