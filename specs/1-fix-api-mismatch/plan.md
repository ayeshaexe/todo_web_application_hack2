# Implementation Plan: Fix API Response Format Mismatch

## Technical Architecture

### Tech Stack
- Backend: FastAPI with Python 3.12
- Database: PostgreSQL with SQLModel/SQLAlchemy
- Authentication: JWT tokens with python-jose
- Frontend: Next.js (existing, to be integrated with fixed backend)
- Serialization: Pydantic v2 for data validation and serialization

### File Structure
```
/mnt/c/Users/NBK COMPUTER/Desktop/hackathon2/phase2part2/
├── main.py                 # FastAPI application with endpoints
├── models.py              # SQLModel database models
├── schemas.py             # Pydantic response/request schemas
├── user_models.py         # User-related models and AuthResponse
├── crud.py               # Database operations
├── auth.py               # Authentication utilities
├── database.py           # Database configuration
└── specs/1-fix-api-mismatch/
    ├── spec.md           # Feature specification
    ├── plan.md           # This implementation plan
    └── tasks.md          # Task breakdown
```

## Implementation Approach

### 1. Response Format Standardization
- Update all Pydantic response models to use proper configuration
- Ensure `from_attributes=True` for SQLModel compatibility
- Add `arbitrary_types_allowed=True` where needed for datetime handling
- Verify all datetime fields serialize to ISO format

### 2. Backend API Endpoint Fixes
- Update toggle endpoint with comprehensive error handling
- Ensure all task operations return consistent object structure
- Add proper datetime serialization for all response objects
- Maintain id field presence in all responses

### 3. Datetime Handling Consistency
- Replace deprecated `datetime.utcnow()` with `datetime.now(timezone.utc)`
- Update all models, CRUD operations, and auth functions
- Ensure proper timezone-aware datetime objects throughout

### 4. Frontend Integration Readiness
- Ensure API responses match frontend expectations exactly
- Maintain field naming consistency (id, completed, title, createdAt, updatedAt)
- Provide proper error responses that frontend can handle gracefully

## Critical Files to Modify

### Primary Files
1. `schemas.py` - Update response model configurations
2. `models.py` - Update datetime field configurations
3. `user_models.py` - Update UserPublic and AuthResponse configurations
4. `main.py` - Update toggle endpoint with error handling
5. `crud.py` - Update datetime usage in operations
6. `auth.py` - Update datetime usage in authentication

### Secondary Files
- `database.py` - Ensure proper asyncpg configuration remains intact

## Risk Mitigation

### High Priority Risks
1. **Datetime Serialization Issues** - Could cause "invalid date" errors in frontend
2. **Response Format Inconsistency** - Could cause undefined property access errors
3. **Missing Required Fields** - Could break frontend mapping operations

### Mitigation Strategies
1. Test all datetime serialization with comprehensive unit tests
2. Verify all API responses match expected frontend format
3. Add comprehensive error handling to prevent undefined responses
4. Use proper Pydantic configuration for SQLModel compatibility