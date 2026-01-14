from sqlmodel import select, Session, update
from models import Todo, TodoCreate, TodoUpdate
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import HTTPException, status

async def create_todo(session, user_id: str, todo: TodoCreate) -> Todo:
    """Create a new todo for a user"""
    db_todo = Todo(
        user_id=user_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


async def get_todos_for_user(session, user_id: str) -> List[Todo]:
    """Get all todos for a specific user"""
    statement = select(Todo).where(Todo.user_id == user_id)
    result = await session.execute(statement)
    todos = result.scalars().all()
    return todos


async def get_todo_by_id(session, todo_id: str, user_id: str) -> Optional[Todo]:
    """Get a specific todo by ID for a specific user (enforcing ownership)"""
    # Convert string ID to integer for database query
    int_todo_id = int(todo_id)
    statement = select(Todo).where(Todo.id == int_todo_id, Todo.user_id == user_id)
    result = await session.execute(statement)
    todo = result.scalar_one_or_none()
    return todo


async def update_todo(session, todo_id: str, user_id: str, todo_update: TodoUpdate) -> Optional[Todo]:
    """Update a specific todo for a specific user (enforcing ownership)"""
    # First get the existing todo to ensure it exists and belongs to the user
    # Convert string ID to integer for database query
    int_todo_id = int(todo_id)
    existing_todo = await get_todo_by_id(session, int_todo_id, user_id)
    if not existing_todo:
        return None

    # Prepare update data
    update_data = todo_update.dict(exclude_unset=True)
    if "completed" in update_data and update_data["completed"] is None:
        del update_data["completed"]

    # Update the todo
    for field, value in update_data.items():
        setattr(existing_todo, field, value)

    # Update the updated_at timestamp
    existing_todo.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    await session.commit()
    await session.refresh(existing_todo)

    return existing_todo


async def delete_todo(session, todo_id: str, user_id: str) -> bool:
    """Delete a specific todo for a specific user (enforcing ownership)"""
    # First get the existing todo to ensure it exists and belongs to the user
    # Convert string ID to integer for database query
    int_todo_id = int(todo_id)
    existing_todo = await get_todo_by_id(session, int_todo_id, user_id)
    if not existing_todo:
        return False

    await session.delete(existing_todo)
    await session.commit()

    return True


async def toggle_todo_completion(session, todo_id: str, user_id: str, completed: Optional[bool] = None) -> Optional[Todo]:
    """Toggle the completion status of a specific todo for a specific user"""
    # First get the existing todo to ensure it exists and belongs to the user
    # Convert string ID to integer for database query
    int_todo_id = int(todo_id)
    existing_todo = await get_todo_by_id(session, int_todo_id, user_id)
    if not existing_todo:
        return None

    # Toggle the completion status if not specified
    if completed is None:
        existing_todo.completed = not existing_todo.completed
    else:
        existing_todo.completed = completed

    # Update the updated_at timestamp
    existing_todo.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    await session.commit()
    await session.refresh(existing_todo)

    return existing_todo