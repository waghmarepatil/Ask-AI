from sqlalchemy.ext.asyncio import AsyncSession
from models.question import Question
from utils.logger import get_logger

logger = get_logger(__name__)


class DBRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, question: str, answer: str):
        try:
            logger.info(f"DB SAVE START | question_length={len(question)}")

            obj = Question(
                question=question,
                answer=answer
            )

            self.db.add(obj)
            await self.db.commit()

            logger.info("DB SAVE SUCCESS")

        except Exception as e:
            logger.error(f"DB SAVE FAILED: {e}", exc_info=True)
            raise