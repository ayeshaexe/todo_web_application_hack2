from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, urlunparse

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("NEON_DB_URL")

# Replace postgresql:// with postgresql+asyncpg:// for async operations
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    # Parse the URL to handle query parameters properly for asyncpg
    parsed = urlparse(DATABASE_URL)

    # Parse query parameters
    query_params = dict(parse_qsl(parsed.query))

    # Remove parameters that are not supported by asyncpg
    unsupported_params = ['sslmode', 'channel_binding']
    for param in unsupported_params:
        query_params.pop(param, None)

    # Reconstruct query string
    new_query = '&'.join([f'{k}={v}' for k, v in query_params.items()])

    # Reconstruct URL with asyncpg scheme
    DATABASE_URL = urlunparse((
        'postgresql+asyncpg',
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

# Create async engine with proper parameters for asyncpg
async_engine = create_async_engine(DATABASE_URL)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session