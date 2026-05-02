from fastapi import Form
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)

    @classmethod
    def as_form(cls,
                question: str = Form()
                ):
        return cls(question=question)
