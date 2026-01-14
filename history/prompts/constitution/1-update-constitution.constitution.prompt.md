---
id: 1
title: Update Constitution
stage: constitution
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-multi-user-todo
user: NBK COMPUTER
command: /sp.constitution
labels: [constitution,spec-driven,todo-app,security]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: Phase II – Spec-Driven Full-Stack Todo Web Application

Core principles:
- Spec-driven development as the single source of truth
- Security-first architecture with Better Auth–issued JWTs
- Strict user isolation enforced at API and database levels
- Deterministic, production-grade behavior across the stack

Key standards:
- All implementations must reference and comply with Spec-Kit specifications
- Authentication must be implemented using Better Auth (Next.js) with JWT tokens
- FastAPI must verify JWTs using the shared BETTER_AUTH_SECRET
- Backend must never trust client input for user identity
- Every task operation must enforce ownership via authenticated user ID
- Code must be idiomatic, readable, and maintainable

Constraints:
- Phase II scope only (no Phase III or chatbot features)
- Technology stack:
  - Frontend: Next.js 16+ (App Router, TypeScript, Tailwind CSS)
  - Backend: FastAPI, SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth with JWT
- Monorepo with Spec-Kit Plus and layered CLAUDE.md files
- Secrets managed via environment variables only

Success criteria:
- All API endpoints reject unauthenticated requests (401)
- JWT tokens are issued by Better Auth and verified by FastAPI
- Users can only view or modify their own tasks
- Implementation matches specs with no unauthorized deviations
- Project passes security, functionality, and spec-compliance review
```

## Response snapshot

Updated the constitution file at .specify/memory/constitution.md with specific principles for the Phase II Todo Web Application project. The new constitution includes core principles around spec-driven development, security-first architecture with JWTs, user isolation, production-grade behavior, and code maintainability. It also includes additional constraints and development workflow sections.

## Outcome

- ✅ Impact: Constitution file updated with project-specific principles
- 🧪 Tests: No tests required for this change
- 📁 Files: Updated .specify/memory/constitution.md with new project constitution
- 🔁 Next prompts: Implementation can now proceed following the defined constitution
- 🧠 Reflection: Constitution now properly defines the project's guiding principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing features according to the new constitution