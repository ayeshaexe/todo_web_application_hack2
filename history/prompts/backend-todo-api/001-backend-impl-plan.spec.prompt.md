---
id: 001
title: backend-impl-plan
stage: plan
date_iso: 2026-01-08
surface: agent
model: Claude Sonnet 4.5
feature: backend-todo-api
branch: 001-backend-todo-api
user: Claude Code User
command: /sp.plan
labels: ["backend", "api", "jwt", "authentication", "todo", "fastapi"]
links:
  spec: ../specs/001-backend-todo-api/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/001-backend-todo-api/plan.md
  - specs/001-backend-todo-api/research.md
  - specs/001-backend-todo-api/data-model.md
  - specs/001-backend-todo-api/contracts/api-contract.yaml
  - specs/001-backend-todo-api/quickstart.md
tests_yaml: []
---

# Backend Implementation Plan for Todo API

## User Input

```
/sp.plan

Project: Phase II – Backend Implementation (Frontend-Integrated)

Context:
The frontend for Phase II is fully implemented (Next.js, TypeScript, Tailwind CSS). The backend will provide user authentication (via Better Auth JWT tokens) and persistent, user-specific todo management. The backend must integrate seamlessly with the frontend without requiring any UI changes.

Objective:
Generate a complete, step-by-step **backend implementation plan** for Phase II that ensures:
- JWT authentication is correctly verified
- Todos are persistent and user-specific
- Frontend API calls work without modification
- Backend is structured, maintainable, and production-ready

Scope:
- FastAPI backend
- SQLModel ORM
- Neon Serverless PostgreSQL
- Better Auth JWT authentication verification
- RESTful API endpoints for todos
- Error handling, input validation, and security

Step-by-Step Plan:

1. **Project Setup**
   - Initialize FastAPI project
   - Create a virtual environment
   - Install required dependencies:
     - `fastapi`, `uvicorn`, `sqlmodel`, `psycopg2-binary`, `python-jose` (for JWT)
   - Set up `.env` with:
     - `NEON_DB_URL`
     - `BETTER_AUTH_SECRET`
     - `BETTER_AUTH_URL`

2. **Database Setup**
   - Configure SQLModel to connect to Neon PostgreSQL via `NEON_DB_URL`
   - Create `User` and `Todo` models:
     - `User`: id (str, primary key), email, createdAt
     - `Todo`: id (int, primary key), userId (foreign key), title, description, completed, createdAt, updatedAt
   - Add indexes on `userId` and `completed` fields
   - Run initial migrations

3. **JWT Authentication Middleware**
   - Implement a middleware that:
     - Extracts the JWT from `Authorization: Bearer <token>` header
     - Verifies JWT using `BETTER_AUTH_SECRET`
     - Decodes user information (userId, email)
     - Rejects requests with invalid or missing token (HTTP 401)
   - Ensure token claims are available to all route handlers

4. **Todo API Endpoints**
   - `GET /api/{user_id}/tasks` → Fetch all todos for authenticated user
   - `POST /api/{user_id}/tasks` → Create a new todo (title required, description optional)
   - `GET /api/{user_id}/tasks/{id}` → Fetch a single todo
   - `PUT /api/{user_id}/tasks/{id}` → Update todo (title, description, completed)
   - `DELETE /api/{user_id}/tasks/{id}` → Delete todo
   - `PATCH /api/{user_id}/tasks/{id}/complete` → Toggle completion
   - Ensure all endpoints:
     - Enforce **ownership**: only return or modify user's own todos
     - Validate inputs with Pydantic
     - Return consistent JSON responses with proper HTTP status codes
     - Handle errors gracefully

5. **Integration with Frontend**
   - Align API routes exactly with frontend expectations
   - Test endpoints with frontend API client
   - Provide placeholder responses if needed during development

6. **Security and Validation**
   - Ensure JWT is required on all todo endpoints
   - Validate input data for length and type
   - Prevent cross-user data access
   - Handle errors: 401 (unauthorized), 403 (forbidden), 404 (not found), 422 (validation error)
   - Configure CORS to allow frontend origin

7. **Testing**
   - Test backend standalone using Postman or REST client
   - Verify JWT authentication works with frontend login
   - Test CRUD operations for todos
   - Ensure todos persist across logout/login cycles

8. **Documentation**
   - Document all endpoints with request/response contracts
   - Provide instructions for `.env` setup
   - Include backend startup instructions (`uvicorn main:app --reload --port 8000`)

9. **Deployment Preparation (Optional)**
   - Ensure NEON_DB_URL works in production
   - Verify Better Auth URL works for deployed frontend
   - Confirm JWT verification in deployed environment

Success Criteria:
- Backend starts without errors
- JWT authentication works end-to-end
- Todos persist correctly per user
- Frontend integrates without modification
- All endpoints tested and documented
- Backend is secure, stable, and production-ready
```

## Response Summary

Successfully created a comprehensive implementation plan for the Phase II backend. The plan includes:

- **Technical Context**: Architecture overview with FastAPI, SQLModel, Neon PostgreSQL, and JWT authentication
- **Research Findings**: JWT token structure, API endpoint patterns, security best practices
- **Data Model**: Detailed Todo entity with validation rules and relationships
- **API Contracts**: Complete OpenAPI-style contract defining all endpoints and responses
- **Quick Start Guide**: Step-by-step instructions for setting up and running the backend
- **Implementation Steps**: Structured approach to building the backend components

The plan addresses all requirements from the user input, including JWT authentication, user-specific todos, database persistence, and frontend integration compatibility.

## Outcome

The implementation plan is complete with all Phase 1 deliverables created. The backend is ready for development with clear specifications for data models, API contracts, and implementation steps. The next step would be to begin development following the outlined architecture and requirements.