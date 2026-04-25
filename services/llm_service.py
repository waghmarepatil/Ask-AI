import asyncio
import hashlib

from clients.groq_client import GroqClient
from repositories.redis_repository import RedisRepository
from utils.logger import get_logger

logger = get_logger(__name__)

class LLMService:
    def __init__(self):
        self.cache = RedisRepository()
        self.semaphore = asyncio.Semaphore(3)
        self.groq_client = GroqClient()

    def _key(self, question: str):
        return f"llm:{hashlib.md5(question.encode()).hexdigest()}"

    async def get_answer(self, question: str, db_repo):
        key = self._key(question)

        cached = await self.cache.get(key)
        if cached:
            logger.info("Cache hit")
            return cached

        for attempt in range(3):
            try:
                async with self.semaphore:
                    result = await asyncio.wait_for(
                        self.groq_client.generate(question),
                        timeout=5
                    )

                await self.cache.set(key, result, ttl=60)

                await db_repo.save(question=question, answer=result)

                return result

            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(2 ** attempt)

        raise Exception("LLM failed after retries")