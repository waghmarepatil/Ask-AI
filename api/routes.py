from fastapi import APIRouter, HTTPException, Depends

from db.dependency import get_db
from repositories.db_repository import DBRepository
from schemas.request import AskRequest
from schemas.response import AskResponse
from services.llm_service import LLMService

from utils.logger import get_logger



router = APIRouter()
llm_service = LLMService()

logger = get_logger(__name__)

@router.get("/health")
def health():
    logger.info("Health check API called")
    return {"status":"ok"}

@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest, db= Depends(get_db)):
    #Injecting DB here
    logger.info(f"Incoming request | question={req.question}")
    try:

        db_repo = DBRepository(db=db)
        logger.info("Calling LLMService.get_answer")
        answer = await llm_service.get_answer(req.question, db_repo)
        logger.info(f"Response generated successfully : {answer}")
        return AskResponse(question=req.question, answer=answer)

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
