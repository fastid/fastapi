from contextlib import asynccontextmanager
from typing import AsyncGenerator

import redis.asyncio as redis

from .settings import settings


@asynccontextmanager
async def redis_client() -> AsyncGenerator[redis.Redis, None]:
    client = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
        username=settings.redis_username,
        password=settings.redis_password.get_secret_value() if settings.redis_password else None,
    )

    yield client
    await client.close()
