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

            system_prompt = """
            You are a helpful and intelligent AI assistant.

            - Answer any user question clearly and accurately.
            - Keep responses natural and easy to understand.
            - Adapt your style based on the question:
              - Technical → detailed with examples/code
              - Casual → friendly and conversational
            - Use structured formatting (bullet points/steps) when helpful.
            - Do not hallucinate facts. If unsure, say you don’t know.
            - Do not assume missing details—ask clarifying questions if needed.
            - Keep responses concise unless more detail is requested.
            - Be polite, neutral, and helpful at all times.
            """

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