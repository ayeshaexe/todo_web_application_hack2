# Todo Backend API

A secure, JWT-authenticated todo management backend built with FastAPI and SQLModel.

## Features

- JWT-based authentication using Better Auth tokens
- User-specific todo management with data isolation
- Full CRUD operations for todos
- Secure endpoints with proper error handling
- PostgreSQL database with Neon Serverless

## Prerequisites

- Python 3.8+
- PostgreSQL database (Neon recommended)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` file:
   ```
   NEON_DB_URL="your_postgres_connection_string"
   BETTER_AUTH_SECRET="your_better_auth_secret"
   BETTER_AUTH_URL="your_better_auth_url"
   ENVIRONMENT="development"
   ```

## Running the Application

```bash
python start_server.py
```

Or alternatively:
```bash
uvicorn main:app --reload --port 8000
```

## Troubleshooting

If you encounter the error "The asyncio extension requires an async driver to be used", ensure you have installed asyncpg:
```bash
pip install asyncpg
```

The database configuration automatically converts the PostgreSQL URL to use the async driver format for compatibility with async operations.

## API Documentation

Once the server is running, visit:
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Endpoints

- `GET /health` - Health check
- `GET /api/todos` - Get all user's todos
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get specific todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo
- `PATCH /api/todos/{id}/toggle` - Toggle completion status

All endpoints (except health check) require JWT authentication in the Authorization header:
`Authorization: Bearer <jwt_token>`