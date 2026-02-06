# FastAPI WebSocket Chat Application

A real-time chat application built with FastAPI, WebSockets, PostgreSQL, and modern web technologies. This project demonstrates a full-stack implementation of a messaging platform with user authentication, real-time communication, and online status tracking.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green)
![JWT](https://img.shields.io/badge/Auth-JWT-orange?logo=jsonwebtokens)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Alembic](https://img.shields.io/badge/Migrations-Alembic-red)
![Pytest](https://img.shields.io/badge/Tests-Pytest-green)

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
- **Database Migrations**: Alembic for managing database schema changes
- **Automated Testing**: Comprehensive test suite with pytest
- **Docker Support**: Easy deployment with Docker and Docker Compose

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)

## 🛠️ Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL
- pip package manager
- Docker and Docker Compose

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


## 📁 Project Structure
```
fastapi-websocket-chat/
├── alembic/                    # Database migrations
│   ├── versions/               # Migration version files
│   ├── env.py                  # Alembic environment configuration
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest fixtures and configuration
│   ├── test_api.py             # Authentication tests
│   ├── test_security.py        # Chat functionality tests
├── templates/                  # Frontend templates
│   └── index.html              # Main HTML/CSS/JavaScript interface
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point and routes
├── core/
│   ├── database.py             # Database configuration and session management
│   ├── security.py             # JWT authentication and Argon2 password hashing
│   ├── dependencies.py         # FastAPI dependencies (auth, database session)
│   ├── __init__.py
├── models.py                   # SQLAlchemy ORM models (User, Chat, Message)
├── schemas.py                  # Pydantic schemas for request/response validation
├── requirements.txt            # Python package dependencies
├── alembic.ini                # Alembic configuration file
├── pytest.ini                 # Pytest configuration file
├── Dockerfile                 # Docker container configuration
├── docker-compose.yml         # Docker Compose services (app, db)
├── .env                       # Environment variables (not in git)
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
└── README.md                  # Project documentation
```
