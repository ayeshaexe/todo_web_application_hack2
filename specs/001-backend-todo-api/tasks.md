# Tasks: Phase II – Backend Implementation (Frontend-Integrated)

**Feature**: 001-backend-todo-api
**Created**: 2026-01-08
**Status**: Draft
**Author**: Claude Code Assistant

## Implementation Strategy

Build the backend in priority order of user stories, starting with core authentication and todo functionality. Each user story should be independently testable and provide value. Focus on getting a minimal working version first, then enhance with additional features.

## Phase 1: Setup (Project Initialization)

**Goal**: Initialize the project structure and configure dependencies.

- [X] T001 Create project directory structure with all required files
- [X] T002 Install and configure dependencies: fastapi, uvicorn, sqlmodel, python-jose, psycopg2-binary, python-dotenv
- [X] T003 Set up .env file with required environment variables (NEON_DB_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL)
- [X] T004 Create requirements.txt with all project dependencies

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Implement foundational components that all user stories depend on.

- [X] T005 [P] Create database configuration module (database.py) with async engine and session setup
- [X] T006 [P] Create configuration module (config.py) to manage environment variables
- [X] T007 [P] Create JWT authentication utility functions (auth.py) for token verification
- [X] T008 [P] Create Pydantic schemas for request/response validation (schemas.py)
- [X] T009 [P] Create SQLModel models (models.py) with Todo entity as specified
- [X] T010 [P] Create main FastAPI application (main.py) with basic configuration
- [X] T011 [P] Implement CORS middleware to allow frontend integration
- [X] T012 [P] Set up logging configuration for error tracking

## Phase 3: User Story 1 - Authenticate and Manage Todos (P1)

**Goal**: Enable users to authenticate with JWT tokens and perform basic todo CRUD operations.

**Independent Test Criteria**: Can authenticate with a JWT token and create, read, update, delete todos, delivering the complete user experience for todo management.

- [X] T013 [P] [US1] Create JWTBearer class for FastAPI Security dependency
- [X] T014 [P] [US1] Implement get_current_user dependency to extract user info from JWT
- [X] T015 [US1] Create CRUD operations for Todo entity (crud.py) with proper ownership checks
- [X] T016 [US1] Implement GET /api/todos endpoint to fetch all user's todos
- [X] T017 [US1] Implement POST /api/todos endpoint to create new todo
- [X] T018 [US1] Implement GET /api/todos/{id} endpoint to fetch specific todo
- [X] T019 [US1] Implement PUT /api/todos/{id} endpoint to update todo
- [X] T020 [US1] Implement DELETE /api/todos/{id} endpoint to delete todo
- [X] T021 [US1] Add proper error handling for all endpoints (401, 403, 404, 422)
- [X] T022 [US1] Add input validation using Pydantic schemas for all endpoints
- [X] T023 [US1] Implement ownership verification in all todo operations

## Phase 4: User Story 2 - Secure Todo Operations (P1)

**Goal**: Ensure users cannot access or modify todos belonging to other users.

**Independent Test Criteria**: Can attempt cross-user access with different JWT tokens, ensuring the system properly enforces ownership checks and returns 401 or 403 errors when appropriate.

- [X] T024 [US2] Enhance CRUD operations with comprehensive ownership validation
- [X] T025 [US2] Implement detailed error responses for unauthorized access attempts
- [X] T026 [US2] Add logging for unauthorized access attempts
- [X] T027 [US2] Test cross-user access scenarios and verify proper rejection
- [X] T028 [US2] Add additional security checks for all endpoints to prevent IDOR attacks

## Phase 5: User Story 3 - JWT Token Validation (P2)

**Goal**: Ensure the system properly validates JWT tokens and rejects unauthorized requests.

**Independent Test Criteria**: Can make requests with no token, invalid tokens, and expired tokens, ensuring the system consistently rejects unauthorized access.

- [X] T029 [US3] Enhance JWT verification to handle expired tokens properly
- [X] T030 [US3] Add validation for malformed JWT tokens
- [X] T031 [US3] Implement proper error responses for all JWT validation failures
- [X] T032 [US3] Test authentication flow with various invalid token scenarios
- [X] T033 [US3] Add token refresh considerations to authentication logic

## Phase 6: User Story 4 - Todo Lifecycle Management (P2)

**Goal**: Ensure todos maintain proper timestamps and state changes throughout their lifecycle.

**Independent Test Criteria**: Can create todos, update them, and verify that createdAt and updatedAt timestamps are properly maintained throughout the todo lifecycle.

- [X] T034 [US4] Enhance Todo model to properly handle createdAt and updatedAt timestamps
- [X] T035 [US4] Implement automatic timestamp updates in CRUD operations
- [X] T036 [US4] Add PATCH /api/todos/{id}/toggle endpoint to toggle completion status
- [X] T037 [US4] Ensure updatedAt is updated whenever a todo is modified
- [X] T038 [US4] Add validation to prevent modification of createdAt field

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Complete the application with proper error handling, documentation, and production readiness.

- [X] T039 Add comprehensive error handling middleware
- [X] T040 Implement request/response logging for debugging
- [X] T041 Add input sanitization to prevent injection attacks
- [X] T042 Create API documentation using FastAPI's built-in documentation
- [X] T043 Add health check endpoint at /health
- [X] T044 Optimize database queries with proper indexing
- [X] T045 Add rate limiting to prevent abuse
- [X] T046 Perform security audit of all endpoints
- [X] T047 Test complete user flow from authentication to todo management
- [X] T048 Verify frontend compatibility with backend API
- [X] T049 Update README with setup and deployment instructions
- [X] T050 Run final tests to ensure error-free application

## Dependencies

- User Story 1 (P1) requires: Phase 1 (Setup) and Phase 2 (Foundational)
- User Story 2 (P1) requires: User Story 1 (P1) components
- User Story 3 (P2) requires: Phase 2 (Foundational)
- User Story 4 (P2) requires: User Story 1 (P1) components

## Parallel Execution Examples

- **Within User Story 1**: T013-T014 (auth) can run in parallel with T015 (CRUD), T016-T020 (endpoints)
- **Across Stories**: T029-T033 (JWT validation) can run in parallel with T034-T038 (lifecycle management)
- **Foundational Phase**: T005-T012 can largely run in parallel as they create independent modules

## MVP Scope

For a minimal viable product, focus on Phase 1 (Setup), Phase 2 (Foundational), and User Story 1 (Core authentication and CRUD). This delivers the essential functionality of JWT-authenticated todo management.