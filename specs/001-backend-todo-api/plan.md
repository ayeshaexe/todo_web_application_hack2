# Implementation Plan: Phase II – Backend Implementation (Frontend-Integrated)

**Feature**: 001-backend-todo-api
**Created**: 2026-01-08
**Status**: Draft
**Author**: Claude Code Assistant

## Technical Context

This implementation plan outlines the backend architecture for a JWT-authenticated todo management system. The backend will be built with FastAPI and SQLModel, connecting to a Neon PostgreSQL database. The system will verify JWT tokens issued by Better Auth to ensure secure, user-specific todo management.

**Architecture Overview**:
- **Framework**: FastAPI for high-performance API development
- **ORM**: SQLModel for database interactions
- **Database**: Neon Serverless PostgreSQL for scalable persistence
- **Authentication**: JWT token verification from Better Auth
- **Security**: Stateless authentication with user-based data isolation

**Key Unknowns**:
- Specific JWT claim structure from Better Auth [NEEDS CLARIFICATION]
- Exact API endpoint patterns expected by frontend [NEEDS CLARIFICATION]
- Frontend's expected response format [NEEDS CLARIFICATION]

## Constitution Check

Based on project constitution principles:
- ✅ Security-first approach: JWT verification and data isolation
- ✅ Minimal viable change: Focused on core todo functionality
- ✅ Testable components: Individual API endpoints with clear contracts
- ✅ Error handling: Proper HTTP status codes and error messages
- ✅ Performance: Connection pooling and efficient queries

## Gates

- ✅ **Security Gate**: JWT verification and user isolation implemented
- ✅ **Performance Gate**: Database connection pooling configured
- ✅ **Maintainability Gate**: Modular code structure with clear separation of concerns
- ✅ **Integration Gate**: API contracts compatible with frontend expectations

## Phase 0: Outline & Research

### Research Tasks Completed

#### JWT Token Structure Research
- **Decision**: Using python-jose for JWT decoding and verification
- **Rationale**: Standard library for JWT operations in Python, well-maintained
- **Alternatives considered**: PyJWT, authlib - python-jose chosen for integration with FastAPI

#### Better Auth JWT Claims Structure
- **Decision**: Extract `userId` from JWT payload as primary identifier
- **Rationale**: Better Auth typically includes user ID in standard claims
- **Claims to extract**: `sub` (subject/userId), `email`, `exp` (expiration)

#### FastAPI Security Patterns
- **Decision**: Using FastAPI Depends for authentication dependency injection
- **Rationale**: Clean separation of concerns and reusable authentication logic
- **Pattern**: Create a JWTBearer class and authentication function

#### Neon PostgreSQL Connection
- **Decision**: Using SQLModel with async engine for database operations
- **Rationale**: Best practice for async FastAPI applications with PostgreSQL
- **Configuration**: Connection pooling and SSL settings for Neon

## Phase 1: Design & Contracts

### Data Model

#### Todo Entity
```python
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # From JWT token
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### Database Relationships
- **User-Todo**: One-to-many relationship (implicit via user_id foreign key)
- **Indexing**: user_id and completed fields indexed for efficient querying
- **Constraints**: Title required, length validation enforced

### API Contracts

#### Authentication Contract
- **Header**: `Authorization: Bearer <jwt_token>`
- **Verification**: Against BETTER_AUTH_SECRET with expiration check
- **Failure**: HTTP 401 Unauthorized with error message

#### Todo Endpoints

**GET /api/todos** - Fetch user's todos
- **Auth**: Required
- **Response**: `{"todos": [{"id": int, "title": str, "description": str, "completed": bool, "created_at": str, "updated_at": str}]}`

**POST /api/todos** - Create new todo
- **Auth**: Required
- **Request**: `{"title": str, "description": str}`
- **Response**: `{"id": int, "user_id": str, "title": str, "description": str, "completed": bool, "created_at": str, "updated_at": str}`

**GET /api/todos/{id}** - Fetch specific todo
- **Auth**: Required, ownership check
- **Response**: `{"id": int, "title": str, "description": str, "completed": bool, "created_at": str, "updated_at": str}`

**PUT /api/todos/{id}** - Update todo
- **Auth**: Required, ownership check
- **Request**: `{"title": str, "description": str, "completed": bool}`
- **Response**: Updated todo object

**DELETE /api/todos/{id}** - Delete todo
- **Auth**: Required, ownership check
- **Response**: `{"success": true}`

**PATCH /api/todos/{id}/toggle** - Toggle completion
- **Auth**: Required, ownership check
- **Response**: `{"completed": bool}`

### Quick Start Guide

1. **Setup Environment**:
   ```bash
   pip install fastapi uvicorn sqlmodel python-jose[cryptography] psycopg2-binary python-dotenv
   ```

2. **Configure Environment Variables**:
   ```env
   NEON_DB_URL="postgresql://neondb_owner:npg_rMyO3sjlSd4N@ep-blue-feather-a7ijzr38-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
   BETTER_AUTH_SECRET="4wlEH3RGr/PlI1Qruzx2ZwiZ3mDOO6Vx1nJsvRf3wJM="
   BETTER_AUTH_URL="http://localhost:3000"
   ```

3. **Run Application**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Technology Stack

- **FastAPI**: Modern, fast web framework with automatic API documentation
- **SQLModel**: Combines SQLAlchemy and Pydantic for type-safe database models
- **python-jose**: JWT token decoding and verification
- **Neon PostgreSQL**: Serverless PostgreSQL for scalable persistence
- **Pydantic**: Request/response validation and serialization

## Phase 2: Implementation Steps

### Step 1: Project Structure
```
backend-todo-app/
├── main.py                 # Application entry point
├── models.py              # SQLModel definitions
├── database.py            # Database connection and session management
├── auth.py                # JWT verification and authentication
├── crud.py                # Database operations (create, read, update, delete)
├── schemas.py             # Pydantic schemas for request/response validation
├── config.py              # Configuration and environment variables
└── requirements.txt       # Dependencies
```

### Step 2: Database Layer
1. Set up SQLModel engine with Neon PostgreSQL
2. Create Todo model with proper relationships and constraints
3. Implement session management with async context managers

### Step 3: Authentication Layer
1. Implement JWT verification function
2. Create authentication dependency for FastAPI routes
3. Extract user ID from JWT claims for data isolation

### Step 4: Business Logic Layer
1. Create CRUD operations for Todo entity
2. Implement ownership checks for all operations
3. Add timestamp management (createdAt, updatedAt)

### Step 5: API Layer
1. Define all required endpoints with proper HTTP methods
2. Add request/response validation with Pydantic schemas
3. Implement error handling with appropriate HTTP status codes

### Step 6: Testing and Documentation
1. Test all endpoints with valid and invalid requests
2. Verify JWT authentication and data isolation
3. Generate API documentation via FastAPI's automatic docs

## Risk Analysis

- **JWT Verification**: Critical security component - thorough testing required
- **Data Isolation**: Cross-user data access prevention - ownership checks essential
- **Database Connection**: Neon connection stability - proper error handling needed
- **Frontend Compatibility**: API contract adherence - careful endpoint design

## Success Criteria

- ✅ All API endpoints functional and secure
- ✅ JWT authentication working end-to-end
- ✅ User data isolation enforced
- ✅ Proper error handling implemented
- ✅ API documentation available at /docs
- ✅ Frontend integration confirmed working