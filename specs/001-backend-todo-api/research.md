# Research Findings: Phase II Backend Implementation

## JWT Token Structure from Better Auth

### Decision
Using python-jose library to decode and verify JWT tokens from Better Auth, extracting the `sub` claim as the user ID.

### Rationale
Better Auth follows standard JWT practices where the `sub` (subject) claim contains the user ID. The python-jose library is well-maintained and integrates well with FastAPI applications.

### Claims Structure
- `sub`: User ID (primary identifier)
- `email`: User email address
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp
- Additional claims may be present but `sub` is guaranteed

## API Endpoint Design for Frontend Compatibility

### Decision
Designing endpoints following RESTful patterns that align with typical frontend API client expectations.

### Rationale
Most frontend API clients expect standard REST endpoints with predictable patterns. Using `/api/todos` as the base path with standard HTTP methods ensures compatibility.

### Endpoint Patterns
- `GET /api/todos` - Fetch all user's todos
- `POST /api/todos` - Create new todo
- `GET /api/todos/{id}` - Fetch specific todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `PATCH /api/todos/{id}/toggle` - Toggle completion status

## FastAPI Security Patterns

### Decision
Using FastAPI's dependency injection system with custom authentication dependencies.

### Rationale
FastAPI's Depends system provides clean separation of authentication logic while making it reusable across endpoints.

### Pattern Implementation
```python
def get_current_user(token: str = Security(JWTBearer())) -> dict:
    # Verify JWT and return user info
    pass
```

## Neon PostgreSQL Connection Best Practices

### Decision
Using async SQLModel engine with connection pooling and proper disposal.

### Rationale
Async operations are essential for FastAPI performance, and connection pooling optimizes database resource usage.

### Configuration
- Async engine for non-blocking operations
- Connection pooling parameters tuned for Neon
- Proper session management with context managers