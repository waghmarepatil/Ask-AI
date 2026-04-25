import asyncio
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GroqClient:
    def __init__(self):
        self.client = Groq()

    def _sync_generate(self, question: str) -> str:
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
            return result

    async def generate(self, question: str) -> str:
        return await asyncio.to_thread(self._sync_generate,question)