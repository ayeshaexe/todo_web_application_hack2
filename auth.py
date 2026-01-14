# from fastapi import HTTPException, Security, status, Request
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from jose import JWTError, jwt
# from datetime import datetime, timedelta, timezone
# from typing import Optional, Dict, Any
# from config import settings
# import os
# from dotenv import load_dotenv

# load_dotenv()

# security = HTTPBearer()

# def create_jwt_token(user_id: str) -> str:
#     """
#     Create a new JWT token for the user
#     """
#     expire = datetime.now(timezone.utc) + timedelta(hours=24)  # Token expires in 24 hours
#     to_encode = {
#         "sub": user_id,
#         "exp": expire.timestamp(),
#         "iat": datetime.now(timezone.utc).timestamp()
#     }
#     encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm=settings.jwt_algorithm)
#     return encoded_jwt


# def verify_jwt(token: str) -> Optional[Dict[str, Any]]:
#     """
#     Verify JWT token and return decoded payload if valid
#     """
#     try:
#         # Decode the JWT token using the secret
#         payload = jwt.decode(
#             token,
#             settings.better_auth_secret,
#             algorithms=[settings.jwt_algorithm]
#         )

#         # Check if token is expired
#         exp = payload.get("exp")
#         if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
#             return None

#         return payload
#     except JWTError:
#         return None

# async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
#     """
#     Get current user from JWT token in Authorization header
#     """
#     token = credentials.credentials

#     user_data = verify_jwt(token)
#     if not user_data:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     # Extract user ID from the 'sub' claim (standard for Better Auth)
#     user_id = user_data.get("sub")
#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     return {"user_id": user_id, "raw_payload": user_data}


# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super().__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super().__call__(request)
#         if credentials:
#             if not credentials.credentials:
#                 raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail="Invalid authentication credentials",
#                     headers={"WWW-Authenticate": "Bearer"},
#                 )

#             user_data = verify_jwt(credentials.credentials)
#             if not user_data:
#                 raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail="Invalid or expired token",
#                     headers={"WWW-Authenticate": "Bearer"},
#                 )

#             return user_data

#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )

from fastapi import HTTPException, Security, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from config import settings
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()


def now_utc() -> datetime:
    """Return current UTC time as timezone-aware datetime"""
    return datetime.now(timezone.utc)


def create_jwt_token(user_id: str, hours_valid: int = 24) -> str:
    """
    Create a JWT token for a user with expiry in UTC
    """
    current_time = now_utc()
    expire_time = current_time + timedelta(hours=hours_valid)
    
    payload = {
        "sub": user_id,
        "iat": int(current_time.timestamp()),   # issued at
        "exp": int(expire_time.timestamp())     # expiration
    }

    token = jwt.encode(payload, settings.better_auth_secret, algorithm=settings.jwt_algorithm)
    return token


def verify_jwt(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify JWT token.
    Returns payload if valid, None if expired or invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.jwt_algorithm]
        )

        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < now_utc():
            return None  # token expired

        return payload

    except JWTError:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """
    Extract the current user from the JWT token
    """
    token = credentials.credentials
    payload = verify_jwt(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {"user_id": user_id, "raw_payload": payload}


class JWTBearer(HTTPBearer):
    """
    Custom JWTBearer for dependency injection in FastAPI routes
    """
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Dict[str, Any]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials or not credentials.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

        payload = verify_jwt(credentials.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return payload
