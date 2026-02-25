import os
from typing import Optional

from fastapi import FastAPI
from redis.asyncio import Redis


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client: Optional[Redis] = None


async def connect_redis():
    global redis_client
    if redis_client is None:
        redis_client = Redis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )


async def close_redis():
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None


def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis client not initialized. Call connect_redis() first.")
    return redis_client