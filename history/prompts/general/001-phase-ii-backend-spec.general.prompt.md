---
id: 001
title: phase-ii-backend-spec
stage: spec
date_iso: 2026-01-08
surface: agent
model: Claude Sonnet 4.5
feature: backend-todo-api
branch: 001-backend-todo-api
user: Claude Code User
command: /sp.specify
labels: ["specification", "backend", "todo-api", "jwt-authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/001-backend-todo-api/spec.md
  - specs/001-backend-todo-api/checklists/requirements.md
tests_yaml: []
---

# Phase II Backend Implementation Specification

## User Input

```
/sp.specify

Project: Phase II – Backend Implementation (Frontend-Integrated)

Context:
The frontend for Phase II is already fully implemented using Next.js (App Router), TypeScript, Tailwind CSS, and a centralized API client. This task is to implement the BACKEND for Phase II so it integrates seamlessly with the existing frontend without requiring any frontend changes.

The backend must provide authentication and persistent todo management using JWT-based authentication issued by Better Auth.

Technology Stack:
- Python FastAPI
- SQLModel ORM
- PostgreSQL (Neon Serverless)
- Better Auth (JWT verification only)
- RESTful API architecture

Environment Configuration (MANDATORY):
Create and use a `.env` file with ONLY the following variables:

- NEON_DB_URL="postgresql://neondb_owner:npg_rMyO3sjlSd4N@ep-blue-feather-a7ijzr38-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
- BETTER_AUTH_SECRET="4wlEH3RGr/PlI1Qruzx2ZwiZ3mDOO6Vx1nJsvRf3wJM="
- BETTER_AUTH_URL="http://localhost:3000"

No additional secrets or keys should be introduced at this stage.

Authentication Requirements:
- Backend MUST verify JWT tokens issued by Better Auth
- Extract user identity from JWT
- Reject unauthenticated requests with 401
- Enforce user-based data isolation on all routes
- No session storage on backend (stateless JWT verification)

Todo Management (User-Scoped):
- Create todo
- Fetch all todos for authenticated user
- Fetch single todo
- Update todo (title, description, completed)
- Delete todo
- Toggle completion
- Persist createdAt and updatedAt timestamps
- Enforce ownership checks on every operation

API Rules:
- All routes under `/api/`
- JWT required via `Authorization: Bearer <token>`
- Consistent JSON responses
- Proper HTTP status codes
- Centralized error handling
- Input validation using Pydantic models

Database Requirements:
- Use SQLModel
- Connect via NEON_DB_URL
- Users identified ONLY via JWT claims
- Todos linked to user ID from token

Integration Constraints:
- API con
```

## Response Summary

Created comprehensive specification for the Phase II backend implementation featuring JWT-authenticated todo management API. The specification includes:

- User scenarios covering authentication, todo CRUD operations, and security requirements
- 21 functional requirements covering authentication, data isolation, API behavior, and data management
- Success criteria with measurable outcomes for performance and security
- Key entities (Todo and User) with proper relationships
- Edge cases for error handling and boundary conditions

The specification was refined to remove implementation details (like Python FastAPI, SQLModel, PostgreSQL) to maintain focus on user requirements and business needs, making it technology-agnostic while preserving all functional requirements.

## Outcome

Specification is complete and validated through quality checklist. Ready for the planning phase (/sp.plan) to design the technical implementation approach.