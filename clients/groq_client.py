import asyncio
from dotenv import load_dotenv
from groq import Groq
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class GroqClient:
    def __init__(self):
        self.client = Groq()

    def _sync_generate(self, question: str) -> str:
        try:
            logger.info(f"LLM request started | length={len(question)}")

            system_prompt = """You are a versatile AI text processor...
(keep your full prompt here)"""

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                model="openai/gpt-oss-20b",
            )

            result = chat_completion.choices[0].message.content

            logger.info("LLM response received successfully")

            return result

        except Exception as e:
            logger.error(f"LLM call failed: {e}", exc_info=True)
            raise

    async def generate(self, question: str) -> str:
        logger.debug("Dispatching LLM call to thread")

        return await asyncio.to_thread(self._sync_generate, question)