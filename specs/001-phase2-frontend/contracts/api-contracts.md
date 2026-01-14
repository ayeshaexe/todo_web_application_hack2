# API Contracts: Phase II Frontend Implementation

## Authentication Endpoints

### POST /api/auth/login
**Description**: Authenticate user and return JWT token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK)**:
```json
{
  "user": {
    "id": "uuid-string",
    "name": "John Doe",
    "email": "user@example.com"
  },
  "token": "jwt-token-string",
  "refreshToken": "refresh-token-string"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Invalid credentials",
  "message": "Email or password is incorrect"
}
```

### POST /api/auth/signup
**Description**: Register new user

**Request**:
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created)**:
```json
{
  "user": {
    "id": "uuid-string",
    "name": "John Doe",
    "email": "user@example.com"
  },
  "token": "jwt-token-string"
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Validation error",
  "message": "Email already exists"
}
```

### POST /api/auth/logout
**Description**: Logout user and invalidate session

**Request**: (No body required, uses Authorization header)

**Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

## Todo Endpoints

### GET /api/todos
**Description**: Get all todos for authenticated user

**Request**: (Uses Authorization header)

**Response (200 OK)**:
```json
{
  "todos": [
    {
      "id": "uuid-string",
      "title": "Complete project",
      "description": "Finish the frontend implementation",
      "completed": false,
      "userId": "user-uuid-string",
      "createdAt": "2026-01-07T10:00:00Z",
      "updatedAt": "2026-01-07T10:00:00Z"
    }
  ],
  "totalCount": 1
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized",
  "message": "Authentication token is required"
}
```

### POST /api/todos
**Description**: Create a new todo

**Request**:
```json
{
  "title": "New task",
  "description": "Task description (optional)"
}
```

**Response (201 Created)**:
```json
{
  "todo": {
    "id": "uuid-string",
    "title": "New task",
    "description": "Task description (optional)",
    "completed": false,
    "userId": "user-uuid-string",
    "createdAt": "2026-01-07T10:00:00Z",
    "updatedAt": "2026-01-07T10:00:00Z"
  }
}
```

### PUT /api/todos/{id}
**Description**: Update an existing todo

**Request**:
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "todo": {
    "id": "uuid-string",
    "title": "Updated task title",
    "description": "Updated description",
    "completed": true,
    "userId": "user-uuid-string",
    "createdAt": "2026-01-07T10:00:00Z",
    "updatedAt": "2026-01-07T11:00:00Z"
  }
}
```

### PATCH /api/todos/{id}/toggle
**Description**: Toggle completion status of a todo

**Request**: (No body required)

**Response (200 OK)**:
```json
{
  "todo": {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": true,
    "userId": "user-uuid-string",
    "createdAt": "2026-01-07T10:00:00Z",
    "updatedAt": "2026-01-07T11:00:00Z"
  }
}
```

### DELETE /api/todos/{id}
**Description**: Delete a todo

**Request**: (No body required, uses Authorization header)

**Response (200 OK)**:
```json
{
  "message": "Todo deleted successfully"
}
```

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Error type",
  "message": "Human-readable error message",
  "statusCode": 400
}
```

## Common Headers

- `Authorization: Bearer <jwt-token>` - Required for authenticated endpoints
- `Content-Type: application/json` - For requests with JSON body
- `Accept: application/json` - For JSON responses