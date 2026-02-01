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
