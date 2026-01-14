# Data Model: Phase II Frontend Implementation

## User Entity

**Description**: Represents an authenticated user with session state

**Fields**:
- `id: string` - Unique identifier for the user (UUID format)
- `name: string` - User's display name
- `email: string` - User's email address (unique, validated)
- `token: string` - JWT token for authentication (future backend integration)
- `createdAt: string` - ISO date string when user was created
- `updatedAt: string` - ISO date string when user was last updated

**Validation Rules**:
- Email must be a valid email format
- Name must be 1-50 characters
- Token must be a valid JWT format (when present)

## Todo Entity

**Description**: Represents a task item with completion status and metadata

**Fields**:
- `id: string` - Unique identifier for the todo (UUID format)
- `title: string` - Title of the task (required, 1-200 characters)
- `description: string` - Optional description of the task (0-1000 characters)
- `completed: boolean` - Whether the task is completed
- `userId: string` - Reference to the user who owns this todo
- `createdAt: string` - ISO date string when todo was created
- `updatedAt: string` - ISO date string when todo was last updated

**Validation Rules**:
- Title must be 1-200 characters
- Description must be 0-1000 characters if provided
- Completed must be a boolean value
- UserId must reference an existing user

## API Response Structures

### Auth Response
```typescript
interface AuthResponse {
  user: User;
  token: string;
  refreshToken?: string;
}
```

### Todo Response
```typescript
interface TodoResponse {
  todo: Todo;
}
```

### Todo List Response
```typescript
interface TodoListResponse {
  todos: Todo[];
  totalCount: number;
}
```

### Error Response
```typescript
interface ErrorResponse {
  error: string;
  message: string;
  statusCode: number;
}
```

## State Management Structures

### Auth State
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}
```

### Todo State
```typescript
interface TodoState {
  todos: Todo[];
  loading: boolean;
  error: string | null;
  currentTodo: Todo | null;
}
```

## Form Data Structures

### Login Form
```typescript
interface LoginForm {
  email: string;
  password: string;
}
```

### Signup Form
```typescript
interface SignupForm {
  name: string;
  email: string;
  password: string;
}
```

### Todo Form
```typescript
interface TodoForm {
  title: string;
  description?: string;
}
```