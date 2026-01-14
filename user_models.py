from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from passlib.context import CryptContext
import uuid

# Using bcrypt which is the standard for password hashing - with proper configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

def hash_password(password: str) -> str:
    # Truncate password to 72 bytes to comply with bcrypt limits
    truncated_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(truncated_password)

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str = Field(max_length=100)

class User(UserBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

class UserCreate(UserBase):
    password: str

class UserLogin(SQLModel):
    email: str
    password: str

from pydantic import BaseModel
from pydantic.config import ConfigDict

class UserPublic(UserBase, BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: str
    name: str
    email: str
    createdAt: datetime
    updatedAt: datetime

class AuthResponse(SQLModel):
    success: bool = True
    user: UserPublic
    token: str