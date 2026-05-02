import asyncio
import hashlib
from utils.logger import get_logger

logger = get_logger(__name__)


class LLMService:
    def __init__(self, rag_service, cache, llm_client):
        self.rag_service = rag_service
        self.cache = cache
        self.llm_client = llm_client
        self.semaphore = asyncio.Semaphore(3)

    def _key(self, value: str):
        return f"llm:{hashlib.md5(value.encode()).hexdigest()}"

    async def get_answer(self, question: str, db_repo):
        key = self._key(question)

        logger.info(f"Processing request | key={key[:10]}...")

        cached = await self.cache.get(key)
        if cached:
            logger.info("Cache HIT")
            return cached

        logger.info("Cache MISS → calling LLM")

        for attempt in range(3):
            try:
                async with self.semaphore:
                    result = await asyncio.wait_for(
                        self.llm_client.generate(question),
                        timeout=5
                    )

                await self.cache.set(key, result)

                try:
                    await db_repo.save(question=question, answer=result)
                except Exception as e:
                    logger.error(f"DB save failed: {e}", exc_info=True)

                return result

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(2 ** attempt)

        raise Exception("LLM failed after retries")

    async def get_answer_from_pdf(self, question: str, pdf_bytes: bytes, db_repo):
        key = self._key(f"pdf:{question}:{len(pdf_bytes)}")
        context_key = self._key(f"context:{len(pdf_bytes)}")

        logger.info(f"Processing PDF request | key={key[:10]}...")

        # Final answer cache
        cached = await self.cache.get(key)
        if cached:
            logger.info("Answer cache HIT")
            return cached

        try:
            # Context cache (IMPORTANT OPTIMIZATION)
            context = await self.cache.get(context_key)

            if not context:
                logger.info("Context cache MISS → building RAG context")

                context = self.rag_service.build_context_from_pdf(
                    pdf_bytes=pdf_bytes,
                    question=question
                )

                await self.cache.set(context_key, context)

            else:
                logger.info("Context cache HIT")

        except Exception as e:
            logger.warning(f"RAG failed: {e} → fallback to normal LLM")

            return await self.get_answer(question, db_repo)

        # LLM call
        for attempt in range(3):
            try:
                async with self.semaphore:
                    result = await asyncio.wait_for(
                        self.llm_client.generate_with_context(
                            question=question,
                            context=context
                        ),
                        timeout=5
                    )

                await self.cache.set(key, result)

                try:
                    await db_repo.save(question=question, answer=result)
                except Exception as e:
                    logger.error(f"DB save failed: {e}", exc_info=True)

                return result

            except Exception as e:
                logger.warning(f"RAG attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(2 ** attempt)

        raise Exception("RAG failed after retries")