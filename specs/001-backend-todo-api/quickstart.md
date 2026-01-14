# Quick Start Guide: Todo Backend API

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Access to Neon PostgreSQL database
- Better Auth configured for JWT issuance

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
# If you have a repository
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn sqlmodel python-jose[cryptography] psycopg2-binary python-dotenv httpx
```

### 4. Create Environment File
Create a `.env` file in your project root:

```env
NEON_DB_URL="postgresql://neondb_owner:npg_rMyO3sjlSd4N@ep-blue-feather-a7ijzr38-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
BETTER_AUTH_SECRET="4wlEH3RGr/PlI1Qruzx2ZwiZ3mDOO6Vx1nJsvRf3wJM="
BETTER_AUTH_URL="http://localhost:3000"
ENVIRONMENT="development"
```

### 5. Create Project Structure
```
todo-backend/
├── main.py
├── models.py
├── database.py
├── auth.py
├── crud.py
├── schemas.py
├── config.py
└── requirements.txt
```

## Running the Application

### 1. Start the Development Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Access the API
- API endpoints: `http://localhost:8000/api/`
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Testing the API

### 1. Get Your JWT Token
First, authenticate through your frontend application using Better Auth to obtain a JWT token.

### 2. Test with curl
```bash
# Replace YOUR_JWT_TOKEN with your actual token
export JWT_TOKEN="YOUR_JWT_TOKEN"

# Get all todos
curl -H "Authorization: Bearer $JWT_TOKEN" \
     http://localhost:8000/api/todos

# Create a new todo
curl -X POST -H "Authorization: Bearer $JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test todo","description":"This is a test"}' \
     http://localhost:8000/api/todos
```

### 3. Test with Python
```python
import requests

headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
}

# Create a todo
response = requests.post(
    "http://localhost:8000/api/todos",
    json={"title": "Test from Python", "description": "Testing API"},
    headers=headers
)

print(response.json())
```

## Configuration Details

### Environment Variables
- `NEON_DB_URL`: PostgreSQL connection string for Neon database
- `BETTER_AUTH_SECRET`: Secret key for verifying JWT tokens from Better Auth
- `BETTER_AUTH_URL`: Base URL of your Better Auth instance
- `ENVIRONMENT`: Set to "development" or "production"

### Default Port
The application runs on port 8000 by default. Change in uvicorn command if needed.

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify NEON_DB_URL is correct
   - Check network connectivity to Neon
   - Ensure SSL settings are properly configured

2. **JWT Authentication Failure**
   - Verify BETTER_AUTH_SECRET matches Better Auth configuration
   - Check that JWT token is valid and not expired
   - Ensure token format is "Bearer <token>"

3. **CORS Issues**
   - If integrating with frontend, ensure proper CORS configuration
   - Add frontend domain to allowed origins

### Health Check
Visit `http://localhost:8000/health` to check if the API is running properly.

## Next Steps

1. Implement the data models as defined in `data-model.md`
2. Set up the database connection using the patterns in `database.py`
3. Implement JWT authentication in `auth.py`
4. Create CRUD operations in `crud.py`
5. Define Pydantic schemas in `schemas.py`
6. Build the API endpoints in `main.py`