from utils.logger import get_logger

logger = get_logger(__name__)


class CacheRepository:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        value = self.store.get(key)

        if value is not None:
            logger.info(f"Cache HIT | key={key}")
        else:
            logger.info(f"Cache MISS | key={key}")

        return value

    async def set(self, key, value):
        self.store[key] = value

        logger.info(f"Cache SET | key={key}")