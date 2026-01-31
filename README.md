# FastAPI WebSocket Chat Application

A real-time chat application built with FastAPI, WebSockets, PostgreSQL, and modern web technologies. This project demonstrates a full-stack implementation of a messaging platform with user authentication, real-time communication, and online status tracking.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green)
![JWT](https://img.shields.io/badge/Auth-JWT-orange?logo=jsonwebtokens)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-orange)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **Note:**
> Note: The HTML–CSS–JS design of this project is based on a pre-made template. I integrated the FastAPI Websocket backend myself and customized the template to fit project structure. All backend logic, models, auth, and other content features were developed by me.

## 🚀 Features

- **Real-time Messaging**: WebSocket-based instant messaging between users
- **User Authentication**: Secure JWT-based authentication system with Argon2 password hashing
- **Online Status Tracking**: Real-time user online/offline status and last seen timestamps
- **Typing Indicators**: Live typing status updates during conversations
- **Chat Management**: Create and manage one-on-one chat sessions
- **Responsive UI**: Modern, gradient-styled interface with smooth animations
- **Database Persistence**: PostgreSQL database for storing users, chats, and messages
- **Docker Support**: Easy deployment with Docker and Docker Compose

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [WebSocket Protocol](#websocket-protocol)
- [Project Structure](#project-structure)

## 🛠️ Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 16 (or use Docker)
- pip package manager
- Docker and Docker Compose (optional, for containerized deployment)

### Docker Deployment

1. Clone the repository:
```bash
git clone https://github.com/berkaykhrmn/fastapi-websocket-chat
cd fastapi-websocket-chat
```

2. Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/chatdb
SECRET_KEY=your-super-secret-key-here
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/dbname` |
| `SECRET_KEY` | Secret key for JWT token generation | `your-secret-key-here` |

### Security Configuration

- **JWT Algorithm**: HS256
- **Token Expiration**: 30 minutes
- **Password Hashing**: Argon2

## 🎯 Usage

### Creating an Account

1. Navigate to `http://localhost:8000`
2. Click on "Register" 
3. Fill in username, email, password, and confirm password
4. Click "Register"

### Logging In

1. Enter your username or email
2. Enter your password
3. Click "Login"

### Starting a Chat

1. After logging in, click "New Chat" button
2. Select a user from the list
3. Start messaging in real-time
4. See online status and typing indicators

### Features in Chat

- **Send Messages**: Type and press Enter or click Send
- **Typing Indicators**: See when the other user is typing
- **Online Status**: Green "Online" badge or "Last seen" timestamp
- **Message History**: All messages are persisted in the database
- **Multiple Chats**: Switch between different conversations

## 📡 API Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "password_confirm": "string"
}
```

**Response**: `UserResponse` (201)

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=string&password=string
```

**Response**: 
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### User Management

#### Get Users
```http
GET /users
Authorization: Bearer <token>
```

**Response**: Array of users (excluding current user)
```json
[
  {
    "id": 1,
    "username": "string"
  }
]
```

### Chat Management

#### Get User's Chats
```http
GET /chats
Authorization: Bearer <token>
```

**Response**: Array of chats
```json
[
  {
    "chat_id": 1,
    "username": "string"
  }
]
```

#### Create or Get Chat
```http
POST /chats/{user_id}
Authorization: Bearer <token>
```

**Response**:
```json
{
  "chat_id": 1
}
```

#### Get Chat Messages
```http
GET /chats/{chat_id}/messages
Authorization: Bearer <token>
```

**Response**: Array of messages
```json
[
  {
    "username": "string",
    "message": "string",
    "time": "HH:MM"
  }
]
```

## 🔌 WebSocket Protocol

### Connection
```
ws://localhost:8000/ws/{chat_id}?token=<jwt_token>
```

### Message Types

#### Send Message
```json
{
  "message": "Hello, World!"
}
```

#### Typing Indicator
```json
{
  "action": "typing"
}
```

#### Stop Typing
```json
{
  "action": "stop_typing"
}
```

### Server Events

#### New Message
```json
{
  "username": "string",
  "message": "string",
  "time": "HH:MM"
}
```

#### Typing Status
```json
{
  "action": "typing",
  "username": "string"
}
```

#### User Status Update
```json
{
  "action": "user_status",
  "username": "string",
  "is_online": true,
  "last_seen": "2026-01-31T12:00:00"
}
```

## 📁 Project Structure

```
fastapi-websocket-chat/
├── main.py                 # FastAPI application and routes
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic schemas for validation
├── database.py            # Database configuration
├── security.py            # Authentication and password hashing
├── dependencies.py        # FastAPI dependencies (auth, db)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker Compose services
├── .env                   # Environment variables (create this)
└── templates/
    └── index.html         # Frontend HTML/CSS/JavaScript
```

