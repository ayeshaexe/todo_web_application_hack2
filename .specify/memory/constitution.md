<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: [PRINCIPLE_1_NAME] → Spec-driven development as the single source of truth
Modified principles: [PRINCIPLE_2_NAME] → Security-first architecture with Better Auth–issued JWTs
Modified principles: [PRINCIPLE_3_NAME] → Strict user isolation enforced at API and database levels
Modified principles: [PRINCIPLE_4_NAME] → Deterministic, production-grade behavior across the stack
Modified principles: [PRINCIPLE_5_NAME] → Idiomatic, readable, and maintainable code
Modified principles: [PRINCIPLE_6_NAME] → Authentication via Better Auth with JWT verification
Added sections: Additional Constraints, Development Workflow
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ✅ updated
Follow-up TODOs: None
-->
# Phase II – Spec-Driven Full-Stack Todo Web Application Constitution

## Core Principles

### Spec-driven development as the single source of truth
All implementations must reference and comply with Spec-Kit specifications. Development work must strictly follow the specifications as the authoritative source of requirements and behavior. This ensures deterministic outcomes and prevents unauthorized deviations from the planned functionality.

### Security-first architecture with Better Auth–issued JWTs
Authentication must be implemented using Better Auth (Next.js) with JWT tokens. FastAPI must verify JWTs using the shared BETTER_AUTH_SECRET. Backend must never trust client input for user identity. This creates a secure authentication chain from frontend to backend.

### Strict user isolation enforced at API and database levels
Every task operation must enforce ownership via authenticated user ID. Users can only view or modify their own tasks. This principle ensures data privacy and prevents unauthorized access to other users' information at both the API and database layers.

### Deterministic, production-grade behavior across the stack
Technology stack must follow the defined requirements: Frontend: Next.js 16+ (App Router, TypeScript, Tailwind CSS); Backend: FastAPI, SQLModel; Database: Neon Serverless PostgreSQL; Authentication: Better Auth with JWT. This ensures consistent, reliable behavior across all environments.

### Idiomatic, readable, and maintainable code
Code must be idiomatic to the respective technologies, readable for team collaboration, and maintainable for long-term project health. This principle ensures that the codebase remains accessible to developers and follows established best practices for each technology stack.

### Authentication via Better Auth with JWT verification
All API endpoints must reject unauthenticated requests (401). JWT tokens are issued by Better Auth and verified by FastAPI. This creates a consistent security posture across all API interactions and ensures that only authenticated users can access protected resources.

## Additional Constraints

Phase II scope only (no Phase III or chatbot features). Monorepo with Spec-Kit Plus and layered CLAUDE.md files. Secrets managed via environment variables only. All implementations must comply with the specified technology stack requirements and security standards.

## Development Workflow

All development must follow the Spec-Kit Plus workflow with proper specification, planning, and task generation. Every change must be traced back to the specification and validated for compliance. Code reviews must verify adherence to constitutional principles and security requirements.

## Governance

This constitution supersedes all other practices and development guidelines. All implementations must comply with these principles. Amendments require explicit documentation, approval, and migration plan. All PRs/reviews must verify constitutional compliance. Complexity must be justified against these principles. Use CLAUDE.md for runtime development guidance.

**Version**: 1.1.0 | **Ratified**: 2026-01-07 | **Last Amended**: 2026-01-07