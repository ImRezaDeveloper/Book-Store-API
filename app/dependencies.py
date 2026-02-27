import datetime
from typing import AsyncGenerator
from fastapi import Depends, HTTPException
from sqlalchemy import select
from app.db.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session