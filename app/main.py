from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from pathlib import Path

from core.database import engine, Base, SessionLocal
from schemas import UserCreate, UserResponse, Token
from core.security import hash_password, verify_password, create_access_token, decode_access_token
from models import User, Message, Chat, chat_users
from core.dependencies import get_db, get_current_user

import json

app = FastAPI()

active_connections = {}

@app.post("/auth/register", response_model=UserResponse, tags=["authentication"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        or_(
            User.username == user.username,
            User.email == user.email
        )
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/auth/login", response_model=Token, tags=["authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        or_(
            User.username == form_data.username,
            User.email == form_data.username,
        )
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users")
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).filter(User.id != current_user.id).all()
    return [
        {
            "id": u.id,
            "username": u.username
        }
        for u in users
    ]

@app.get("/chats")
def get_chats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chats = current_user.chats
    result = []

    for chat in chats:
        other_user = next(u for u in chat.users if u.id != current_user.id)
        result.append({
            "chat_id": chat.id,
            "username": other_user.username
        })

    return result


@app.post("/chats/{user_id}")
def get_or_create_chat(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = (
        db.query(Chat)
        .join(chat_users)
        .filter(chat_users.c.user_id.in_([current_user.id, user_id]))
        .group_by(Chat.id)
        .having(func.count(Chat.id) == 2)
        .first()
    )

    if chat:
        return {"chat_id": chat.id}

    other_user = db.query(User).filter(User.id == user_id).first()
    if not other_user:
        raise HTTPException(status_code=404, detail="User not found")

    chat = Chat()
    chat.users.append(current_user)
    chat.users.append(other_user)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return {"chat_id": chat.id}


@app.get("/chats/{chat_id}/messages")
def get_chat_messages(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if current_user not in chat.users:
        raise HTTPException(status_code=403, detail="Forbidden")

    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc(), Message.id.asc())
        .all()
    )

    return [
        {
            "username": m.user.username,
            "message": m.content,
            "time": m.created_at.strftime("%H:%M"),
        }
        for m in messages
    ]


BASE_DIR = Path(__file__).resolve().parent.parent
@app.get("/")
async def get():
    html_path = BASE_DIR / "templates" / "index.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=1008)
        return

    user_id = payload.get("sub")
    if not user_id:
        await websocket.close(code=1008)
        return

    db = SessionLocal()
    user = db.query(User).filter(User.id == int(user_id)).first()
    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    if not user or not chat or user not in chat.users:
        db.close()
        await websocket.close(code=1008)
        return

    await websocket.accept()

    user.is_online = True
    user.last_seen = datetime.now()
    db.commit()

    for u_chat in user.chats:
        for client in active_connections.get(u_chat.id, []):
            await client["ws"].send_text(json.dumps({
                "action": "user_status",
                "username": user.username,
                "is_online": True,
                "last_seen": user.last_seen.isoformat()
            }))

    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append({"ws": websocket, "user": user})

    try:
        while True:
            data = json.loads(await websocket.receive_text())
            action = data.get("action")

            if action == "typing":
                for client in active_connections.get(chat_id, []):
                    if client["ws"] != websocket:
                        await client["ws"].send_text(json.dumps({
                            "action": "typing",
                            "username": user.username,
                        }))
                continue
            elif action == "stop_typing":
                for client in active_connections.get(chat_id, []):
                    if client["ws"] != websocket:
                        await client["ws"].send_text(json.dumps({
                            "action": "stop_typing",
                            "username": user.username,
                        }))
                continue
            else:
                new_message = Message(
                    chat_id=chat_id,
                    user_id=user.id,
                    content=data["message"]
                )
                db.add(new_message)
                db.commit()
                db.refresh(new_message)

                response = {
                    "username": user.username,
                    "message": new_message.content,
                    "time": new_message.created_at.strftime("%H:%M"),
                }
                for client in active_connections.get(chat_id, []):
                    await client["ws"].send_text(json.dumps(response))

    except WebSocketDisconnect:
        active_connections[chat_id] = [
            c for c in active_connections[chat_id] if c["ws"] != websocket
        ]
        if not active_connections[chat_id]:
            del active_connections[chat_id]

        user.is_online = False
        user.last_seen = datetime.now()
        db.commit()

        for u_chat in user.chats:
            for client in active_connections.get(u_chat.id, []):
                await client["ws"].send_text(json.dumps({
                    "action": "user_status",
                    "username": user.username,
                    "is_online": False,
                    "last_seen": user.last_seen.isoformat()
                }))
        db.close()