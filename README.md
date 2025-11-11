# 🚀 Assignment 10 - FastAPI Authentication System

A comprehensive FastAPI application featuring user authentication, JWT token management, and secure password handling with PostgreSQL database integration.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Docker Deployment](#docker-deployment)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)


---

## ✨ Features

- 🔐 **User Authentication** - Secure JWT-based authentication system
- 👤 **User Management** - Register, login, and manage user accounts
- 🔑 **Password Security** - Bcrypt hashing with strong password validation
- 📊 **PostgreSQL Database** - Reliable data persistence
- 🧪 **Comprehensive Testing** - Unit and integration tests with pytest
- 🐳 **Docker Support** - Containerized deployment ready
- 📝 **API Documentation** - Auto-generated with FastAPI/Swagger

---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (Jose), Passlib
- **Validation**: Pydantic v2
- **Testing**: Pytest, Coverage
- **Containerization**: Docker

---

## 📁 Project Structure

```
assignment-10/
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── dependencies.py          # Authentication dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py                  # User database model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base.py                  # Base schemas and validators
│   │   └── user.py                  # User response schemas
│   ├── operations/
│   │   └── __init__.py              # Business logic operations
│   ├── config.py                    # Application configuration
│   ├── database.py                  # Database connection setup
│   └── database_init.py             # Database initialization
├── templates/
│   └── index.html                   # HTML template
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures and configuration
│   ├── e2e/
│   │   ├── __init__.py
│   │   └── test_e2e.py              # End-to-end tests
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_database.py         # Database integration tests
│   │   ├── test_dependencies.py     # Auth dependency tests
│   │   ├── test_fastapi_calculator.py  # Calculator API tests
│   │   ├── test_schema_base.py      # Schema validation tests
│   │   ├── test_user.py             # User model tests
│   │   └── test_user_auth.py        # User authentication tests
│   └── unit/
│       ├── __init__.py
│       └── test_calculator.py       # Calculator unit tests
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── docker-compose.yml               # Docker Compose setup
├── pytest.ini                       # Pytest configuration
├── LICENSE                          # License file
└── README.md                        # This file                      
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL 13+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Docker** (Optional) - [Download](https://www.docker.com/products/docker-desktop/)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/techy-Nik/assignment-10.git
cd assignment-10
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Database Setup

1. Create a PostgreSQL database:

```sql
CREATE DATABASE assignment10_db;
```

2. Update `app/config.py` or set environment variables:

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/assignment10_db"
export SECRET_KEY="your-secret-key-here"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/assignment10_db
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🏃 Running the Application

### Local Development

```bash
# Run with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

---

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t assignment10-app .

# Run the container
docker run -p 8000:8000 assignment10-app
```

### Using Docker Compose

```bash
# Start all services (app + database)
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag assignment10-app techynik/assignment10:latest

# Push to Docker Hub
docker push techynik/assignment10:latest
```
### Docker REPOSITORY
- REPO: https://hub.docker.com/repository/docker/techynik/module10/general


---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | User authentication | No |
| POST | `/token` | Get access token | No |

### User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/me` | Get current user info | Yes |
| PUT | `/users/me` | Update user profile | Yes |
| GET | `/users/{user_id}` | Get user by ID | Yes |

### Example Requests

**Register User:**
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alicesmith",
    "email": "alice.smith@email.com",
    "password": "MyPass456",
    "first_name": "Alice",
    "last_name": "Smith"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alicesmith",
    "password": "MyPass456"
  }'
```

**Access Protected Endpoint:**
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🧪 Testing

### Run All Tests

```bash
# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/auth/test_dependencies.py -v

# Run with verbose output
pytest -v
```

### View Coverage Report

```bash
# Open HTML coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

### Test Structure

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API endpoints and database interactions
- **Schema Tests**: Validate Pydantic models and data validation

---

### Authentication Flow

1. User registers with validated credentials
2. Password is hashed using bcrypt
3. User logs in with username/email and password
4. JWT token is generated with expiration
5. Token is used for subsequent authenticated requests

---

## 📚 Key Components

### Authentication System

- **JWT Tokens**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Token Validation**: Automatic token verification on protected routes

### Database Models

- **User Model**: Comprehensive user data with audit fields
- **SQLAlchemy ORM**: Type-safe database operations
- **UUID Primary Keys**: Secure and scalable identifiers

### Schema Validation

- **Pydantic V2**: Modern data validation
- **Custom Validators**: Password strength and format checks
- **Response Models**: Type-safe API responses

---

## 📝 License

This project is created for educational purposes as part of Assignment 10.

---

## 👤 Author

**Nikunj (techy-Nik)**
- GitHub: [@techy-Nik](https://github.com/techy-Nik)
- Repository: [assignment-10](https://github.com/techy-Nik/assignment-10)

---

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list               # macOS

# Verify DATABASE_URL in config
echo $DATABASE_URL
```

**Import Errors:**
```bash
# Ensure virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt
```

**Docker Permission Issues:**
```bash
# Restart Docker daemon
sudo systemctl restart docker

# Check Docker status
sudo docker info
```

---



