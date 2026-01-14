from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    neon_db_url: str = os.getenv("NEON_DB_URL", "")

    # Auth settings
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "")

    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")

    # JWT settings
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()