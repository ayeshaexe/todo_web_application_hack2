# from sqlmodel import select
# from sqlmodel.ext.asyncio.session import AsyncSession
# from typing import Optional
# from user_models import User, UserCreate, UserLogin, hash_password
# from passlib.context import CryptContext
# from auth import verify_jwt, create_jwt_token
# import uuid

# # Using bcrypt which is the standard for password hashing - with proper configuration
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     # Truncate password to 72 bytes to comply with bcrypt limits
#     truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
#     return pwd_context.verify(truncated_password, hashed_password)

# async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
#     statement = select(User).where(User.email == email)
#     result = await session.exec(statement)
#     user = result.first()
#     if not user or not verify_password(password, user.hashed_password):
#         return None
#     return user

# async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
#     statement = select(User).where(User.email == email)
#     result = await session.exec(statement)
#     return result.first()

# async def get_user_by_id(session: AsyncSession, user_id: str) -> Optional[User]:
#     statement = select(User).where(User.id == user_id)
#     result = await session.exec(statement)
#     return result.first()


# async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
#     hashed_password = hash_password(user_create.password)
#     db_user = User(
#         name=user_create.name,
#         email=user_create.email,
#         hashed_password=hashed_password
#     )
#     session.add(db_user)
#     await session.commit()
#     await session.refresh(db_user)
#     return db_user

from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from user_models import (
    User,
    UserCreate,
    verify_password,
    hash_password
)

async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str
) -> Optional[User]:
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    user = result.first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


async def get_user_by_email(
    session: AsyncSession,
    email: str
) -> Optional[User]:
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    return result.first()


async def get_user_by_id(
    session: AsyncSession,
    user_id: str
) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    return result.first()


async def create_user(
    session: AsyncSession,
    user_create: UserCreate
) -> User:
    hashed_password = hash_password(user_create.password)

    db_user = User(
        name=user_create.name,
        email=user_create.email,
        hashed_password=hashed_password
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user
