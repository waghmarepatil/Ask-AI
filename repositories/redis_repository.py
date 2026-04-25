import json

import redis.asyncio as redis


class RedisRepository:
    def __init__(self):
        self.redis = redis.Redis(
            host="localhost", #default host
            port=6379, #default port
            decode_responses=True #decode else it will return bytes if tru return as string
        )

    async def get(self, key: str):
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(self, key: str, value, ttl: int = 60):
        await self.redis.set(
            key,
            json.dumps(value),
            ex=ttl
        )
