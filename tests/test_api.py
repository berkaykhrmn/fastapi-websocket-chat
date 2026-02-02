import pytest
from fastapi import status
from models import User, Chat, Message


def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "pass123",
        "password_confirm": "pass123"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"


def test_register_duplicate_user(client):
    client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "pass",
        "password_confirm": "pass"
    })
    response = client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "pass",
        "password_confirm": "pass"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login(client, test_user):
    response = client.post("/auth/login", data={
        "username": test_user.username,          # ← BURAYI DÜZELTTİK
        "password": "testpass"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_get_users(client, auth_token, test_user):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/users", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) == 0


def test_create_chat(client, auth_token, db_session):
    other_user = User(username="other", email="other@example.com", hashed_password="hash")
    db_session.add(other_user)
    db_session.commit()
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(f"/chats/{other_user.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert "chat_id" in response.json()


def test_get_chat_messages(client, auth_token, db_session, test_user):
    other_user = User(username="other", email="other@example.com", hashed_password="hash")
    db_session.add(other_user)
    db_session.commit()
    chat = Chat()
    chat.users.append(test_user)
    chat.users.append(other_user)
    db_session.add(chat)
    db_session.commit()
    message = Message(chat_id=chat.id, user_id=test_user.id, content="Hello")
    db_session.add(message)
    db_session.commit()
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/chats/{chat.id}/messages", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    messages = response.json()
    assert len(messages) == 1
    assert messages[0]["message"] == "Hello"