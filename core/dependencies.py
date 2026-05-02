from services.llm_service import LLMService
from services.rag.rag_service import RAGService
from repositories.redis_repository import RedisRepository
from clients.groq_client import GroqClient

cache = RedisRepository()
groq_client = GroqClient()


async def get_llm_service():
    rag_service = RAGService()
    return LLMService(
        rag_service=rag_service,
        cache=cache,
        llm_client=groq_client
    )