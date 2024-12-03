from app.database.redis_client import redis_client


class RedisCacheController:
    async def get_data(self, key: str):
        value = await redis_client.redis.get(key)
        return value.decode('utf-8') if value else None

    async def set_data(self, key: str, value: str, expire: int = 3600):
        await redis_client.redis.set(key, value, ex=expire)

    async def delete_data(self, key: str):
        await redis_client.redis.delete(key)
