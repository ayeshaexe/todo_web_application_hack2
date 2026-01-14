# Data Model: Todo Backend System

## Entities

### Todo Entity
**Description**: Represents a user's task item with properties for tracking and management.

**Fields**:
- `id` (Integer, Primary Key, Auto-generated)
  - Unique identifier for the todo
  - Auto-incrementing integer

- `user_id` (String, Indexed)
  - Foreign key linking to the user who owns this todo
  - Extracted from JWT token during creation
  - Indexed for efficient queries

- `title` (String, Required, Min: 1, Max: 255)
  - Title or brief description of the todo
  - Required field with length validation

- `description` (String, Optional, Max: 1000)
  - Detailed description of the todo
  - Optional field with length validation

- `completed` (Boolean, Default: False)
  - Status indicating if the todo is completed
  - Boolean flag with default value of False

- `created_at` (DateTime, Auto-generated)
  - Timestamp when the todo was created
  - Automatically set to current time on creation

- `updated_at` (DateTime, Auto-generated)
  - Timestamp when the todo was last updated
  - Automatically updated to current time on modification

**Validation Rules**:
- Title is required and must be 1-255 characters
- Description, if provided, must be ≤ 1000 characters
- user_id must match the authenticated user's ID from JWT
- createdAt is set only on creation
- updatedAt is updated on every modification

**Relationships**:
- One-to-many relationship with User (via user_id foreign key)
- Each user can have multiple todos
- Todos are isolated by user_id for security

### User (Implicit Entity via JWT)
**Description**: User identity is derived from JWT token claims, not stored as a separate database entity.

**Attributes** (from JWT claims):
- `user_id` (String) - Extracted from `sub` claim
- `email` (String) - Extracted from `email` claim (optional)
- `expires_at` (DateTime) - Extracted from `exp` claim

## Indexes

### Database Indexes
- `idx_todo_user_id`: Index on user_id field for efficient user-specific queries
- `idx_todo_completed`: Index on completed field for filtering by completion status
- `idx_todo_user_completed`: Composite index on (user_id, completed) for common queries

## Constraints

### Data Integrity Constraints
- Foreign key constraint: user_id must correspond to a valid user (verified via JWT)
- Not null constraints: id, user_id, title, completed, created_at, updated_at
- Length constraints: title (1-255), description (≤1000)
- Ownership constraint: Operations restricted to authenticated user's todos only

## State Transitions

### Todo State Changes
- **Creation**: New todo with completed=False, created_at and updated_at set to current time
- **Update**: Existing todo with updated fields, updated_at updated to current time
- **Toggle Completion**: completed field flipped, updated_at updated to current time
- **Deletion**: Todo record removed from database
- **Read**: Access granted only to owner (based on user_id match)

## Audit Trail

### Timestamp Management
- `created_at`: Immutable timestamp set once at creation
- `updated_at`: Updated automatically on every modification
- Both timestamps stored in UTC for consistency