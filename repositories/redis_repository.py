import json
import redis.asyncio as redis
from utils.logger import get_logger

logger = get_logger(__name__)


class RedisRepository:
    def __init__(self):
        self.redis = redis.Redis(
            host="localhost",   # default host
            port=6379,          # default port
            decode_responses=True  # return string instead of bytes
        )

    async def get(self, key: str):
        try:
            data = await self.redis.get(key)

            if data:
                logger.info(f"Redis HIT | key={key}")
                return json.loads(data)

            logger.info(f"Redis MISS | key={key}")
            return None

        except Exception as e:
            logger.error(f"Redis GET failed | key={key} | error={e}", exc_info=True)
            return None  # fail-safe (don’t break app)

    async def set(self, key: str, value, ttl: int = 60):
        try:
            await self.redis.set(
                key,
                json.dumps(value),
                ex=ttl
            )

            logger.info(f"Redis SET | key={key} | ttl={ttl}")

        except Exception as e:
            logger.error(f"Redis SET failed | key={key} | error={e}", exc_info=True)