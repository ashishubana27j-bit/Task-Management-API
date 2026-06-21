# Task Management API

A production-ready Task Management REST API built with FastAPI, PostgreSQL, SQLAlchemy, Docker, and JWT Authentication.

## Features

- User Registration & Login
- JWT Authentication
- CRUD Operations for Tasks
- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Database Migrations
- Docker Support
- Swagger API Documentation
- Environment Variable Configuration
- Async API Endpoints

## Tech Stack

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Docker & Docker Compose
- Pydantic

## Project Structure

```text
task-management-api/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── alembic/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

## API Features

### Authentication

- User Registration
- User Login
- JWT Token Generation
- Protected Routes

### Task Management

- Create Task
- Get All Tasks
- Get Task By ID
- Update Task
- Delete Task
- Mark Task Complete

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskdb
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Migration

```bash
alembic upgrade head
```

## Run Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

ReDoc Documentation:

```text
http://localhost:8000/redoc
```

## Docker Setup

### Build Docker Image

```bash
docker build -t task-management-api .
```

### Run Container

```bash
docker run -p 8000:8000 task-management-api
```

### Docker Compose

```bash
docker-compose up --build
```

## Example API Requests

### Register User

```http
POST /auth/register
```

Request Body:

```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

### Login

```http
POST /auth/login
```

Request Body:

```json
{
  "username": "user@example.com",
  "password": "Password123"
}
```

### Create Task

```http
POST /tasks
Authorization: Bearer <token>
```

Request Body:

```json
{
  "title": "Learn Docker",
  "description": "Practice Docker deployment",
  "completed": false
}
```

### Get Tasks

```http
GET /tasks
Authorization: Bearer <token>
```

## Running Tests

```bash
pytest
```

## Future Enhancements

- Role-Based Access Control (RBAC)
- Task Categories
- Task Priorities
- Due Dates & Reminders
- Email Notifications
- Redis Caching
- CI/CD Pipeline with GitHub Actions
- Deployment on Render/AWS

## Deployment

The API can be deployed using:

- Render
- Railway
- Fly.io
- AWS ECS
- DigitalOcean

## Author

**Ashish Ubana**

Tech Lead | Unity Developer | AR/VR | Multiplayer Systems | FastAPI Enthusiast

LinkedIn: https://www.linkedin.com/in/ashish-ubana-7243503b5/

