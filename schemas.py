from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import Field
from pydantic.config import ConfigDict

# Request Schemas
class TodoCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoToggleRequest(BaseModel):
    completed: Optional[bool] = None

# Response Schemas
class TodoItemResponse(BaseModel):  # Individual todo item
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime


class TodoResponse(BaseModel):  # Response wrapper with todo property
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    todo: TodoItemResponse

class TodoListResponse(BaseModel):
    todos: list[TodoResponse]

class SuccessResponse(BaseModel):
    success: bool = True

class ErrorResponse(BaseModel):
    success: bool = False
    error: dict

# Health Check Response
class HealthResponse(BaseModel):
    status: str
    timestamp: str