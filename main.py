from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import os
from dotenv import load_dotenv

from models import Todo, TodoCreate, TodoUpdate
from user_models import UserCreate, UserLogin, AuthResponse, UserPublic
from schemas import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoResponse,
    TodoItemResponse,
    TodoListResponse,
    SuccessResponse,
    ErrorResponse,
    HealthResponse,
    TodoToggleRequest
)
from auth import get_current_user, JWTBearer, create_jwt_token
from database import get_async_session
from crud import (
    create_todo,
    get_todo_by_id,
    get_todos_for_user,
    update_todo,
    delete_todo,
    toggle_todo_completion
)
from user_service import authenticate_user, get_user_by_email, create_user, get_user_by_id
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="Backend API for todo management with JWT authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Authentication endpoints
@app.post("/api/auth/signup", response_model=AuthResponse)
async def signup(
    user_create: UserCreate,
    session=Depends(get_async_session)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = await get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    db_user = await create_user(session, user_create)

    # Create JWT token
    token = create_jwt_token(db_user.id)

    # Return success response with user data and token
    return AuthResponse(
        user=UserPublic(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            createdAt=db_user.created_at,
            updatedAt=db_user.updated_at
        ),
        token=token
    )


@app.post("/api/auth/login", response_model=AuthResponse)
async def login(
    user_login: UserLogin,
    session=Depends(get_async_session)
):
    """Authenticate user and return JWT token"""
    user = await authenticate_user(session, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create JWT token
    token = create_jwt_token(user.id)

    # Return success response with user data and token
    return AuthResponse(
        user=UserPublic(
            id=user.id,
            name=user.name,
            email=user.email,
            createdAt=user.created_at,
            updatedAt=user.updated_at
        ),
        token=token
    )


@app.get("/api/auth/me", response_model=AuthResponse)
async def get_current_user_details(current_user: dict = Depends(get_current_user), session=Depends(get_async_session)):
    """Get current user details from the token"""

    # Get user details from database
    user = await get_user_by_id(session, current_user["user_id"])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create JWT token (same as login)
    token = create_jwt_token(user.id)

    # Return success response with user data and token
    return AuthResponse(
        user=UserPublic(
            id=user.id,
            name=user.name,
            email=user.email,
            createdAt=user.created_at,
            updatedAt=user.updated_at
        ),
        token=token
    )


@app.post("/api/auth/logout", response_model=SuccessResponse)
async def logout():
    """Logout endpoint - client should clear the token"""
    # In a real app, you might want to add the token to a blacklist
    # For now, we just return success and let the client handle token removal
    return SuccessResponse(success=True)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API is running"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat()
    )

@app.get("/api/todos", response_model=TodoListResponse)
async def get_todos(
    current_user: dict = Depends(get_current_user),
    session=Depends(get_async_session)
):
    """Get all todos for the authenticated user"""
    user_id = current_user["user_id"]
    todos = await get_todos_for_user(session, user_id)

    # Convert SQLModel objects to response models
    todo_responses = [
        TodoResponse(
            todo=TodoItemResponse(
                id=str(todo.id),
                user_id=todo.user_id,
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
        )
        for todo in todos
    ]

    return TodoListResponse(todos=todo_responses)


@app.post("/api/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_new_todo(
    todo_request: TodoCreateRequest,
    current_user: dict = Depends(get_current_user),
    session=Depends(get_async_session)
):
    """Create a new todo for the authenticated user"""
    user_id = current_user["user_id"]

    # Create TodoCreate object
    todo_create = TodoCreate(
        title=todo_request.title,
        description=todo_request.description,
        completed=False
    )

    # Create the todo in the database
    new_todo = await create_todo(session, user_id, todo_create)

    # Return response model
    return TodoResponse(
        todo=TodoItemResponse(
            id=str(new_todo.id),
            user_id=new_todo.user_id,
            title=new_todo.title,
            description=new_todo.description,
            completed=new_todo.completed,
            created_at=new_todo.created_at,
            updated_at=new_todo.updated_at
        )
    )


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    current_user: dict = Depends(get_current_user),
    session=Depends(get_async_session)
):
    """Get a specific todo by ID for the authenticated user"""
    user_id = current_user["user_id"]
    todo = await get_todo_by_id(session, todo_id, user_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return TodoResponse(
        todo=TodoItemResponse(
            id=str(todo.id),
            user_id=todo.user_id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )
    )


@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
async def update_existing_todo(
    todo_id: str,
    todo_request: TodoUpdateRequest,
    current_user: dict = Depends(get_current_user),
    session=Depends(get_async_session)
):
    """Update an existing todo for the authenticated user"""
    user_id = current_user["user_id"]

    # Check if the todo exists and belongs to the user
    existing_todo = await get_todo_by_id(session, todo_id, user_id)
    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Prepare update data
    todo_update = TodoUpdate(
        title=todo_request.title,
        description=todo_request.description,
        completed=todo_request.completed
    )

    # Update the todo
    updated_todo = await update_todo(session, todo_id, user_id, todo_update)

    return TodoResponse(
        todo=TodoItemResponse(
            id=str(updated_todo.id),
            user_id=updated_todo.user_id,
            title=updated_todo.title,
            description=updated_todo.description,
            completed=updated_todo.completed,
            created_at=updated_todo.created_at,
            updated_at=updated_todo.updated_at
        )
    )


@app.delete("/api/todos/{todo_id}", response_model=SuccessResponse)
async def delete_existing_todo(
    todo_id: str,
    current_user: dict = Depends(get_current_user),
    session=Depends(get_async_session)
):
    """Delete a specific todo for the authenticated user"""
    user_id = current_user["user_id"]

    # Check if the todo exists and belongs to the user
    existing_todo = await get_todo_by_id(session, todo_id, user_id)
    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Delete the todo
    await delete_todo(session, todo_id, user_id)

    return SuccessResponse(success=True)


from fastapi import Body

@app.patch("/api/todos/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_todo_status(
    todo_id: str,
    request_data: dict = Body({}),  # Accept any dictionary as body, default to empty dict
    current_user: dict = Depends(get_current_user),
    session=Depends(get_async_session)
):
    """Toggle the completion status of a specific todo for the authenticated user"""
    try:
        user_id = current_user["user_id"]

        # Check if the todo exists and belongs to the user
        existing_todo = await get_todo_by_id(session, todo_id, user_id)
        if not existing_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )

        # Determine the new completion status
        # If request_data has a completed value, use that
        # Otherwise, just toggle the current status
        new_completed_status = request_data.get('completed')
        if new_completed_status is not None:
            new_completed_status = bool(new_completed_status)
        else:
            # Toggle the current completion status
            new_completed_status = not existing_todo.completed

        # Toggle the completion status
        updated_todo = await toggle_todo_completion(
            session,
            todo_id,
            user_id,
            new_completed_status
        )

        # Ensure updated_todo exists before creating response
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update todo completion status"
            )

        # Create and return response ensuring all fields are properly set
        # Convert integer ID to string to match frontend expectations
        response = TodoResponse(
            todo=TodoItemResponse(
                id=str(updated_todo.id),
                user_id=updated_todo.user_id,
                title=updated_todo.title,
                description=updated_todo.description,
                completed=updated_todo.completed,
                created_at=updated_todo.created_at,
                updated_at=updated_todo.updated_at
            )
        )

        return response
    except HTTPException:
        # Re-raise HTTP exceptions to be handled by the global error handlers
        raise
    except Exception as e:
        # Log the error and raise an internal server error
        logger.error(f"Error in toggle_todo_status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the todo completion status"
        )


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            success=False,
            error={"code": "NOT_FOUND", "message": "Resource not found"}
        ).dict()
    )


@app.exception_handler(401)
async def unauthorized_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content=ErrorResponse(
            success=False,
            error={"code": "UNAUTHORIZED", "message": "Not authenticated"}
        ).dict()
    )


@app.exception_handler(403)
async def forbidden_handler(request, exc):
    return JSONResponse(
        status_code=403,
        content=ErrorResponse(
            success=False,
            error={"code": "FORBIDDEN", "message": "Access denied"}
        ).dict()
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": "Internal server error occurred"}
        ).dict()
    )