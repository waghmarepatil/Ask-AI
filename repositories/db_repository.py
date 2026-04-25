from sqlalchemy.ext.asyncio import AsyncSession

from models.question import Question


class DBRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, question: str, answer: str):
        obj = Question(
            question=question,
            answer=answer
        )
        self.db.add(obj)
        await self.db.commit()