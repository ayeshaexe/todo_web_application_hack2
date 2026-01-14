#!/usr/bin/env python3
"""
Script to initialize the database tables
"""
import asyncio
from sqlmodel import SQLModel
from database import async_engine
from models import Todo
from user_models import User

async def create_tables():
    print("Creating database tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())