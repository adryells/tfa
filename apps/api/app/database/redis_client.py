import aioredis

from app.config import settings


class RedisClient:
    def __init__(self, redis_url=settings.REDIS_URL):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

redis_client = RedisClient()
