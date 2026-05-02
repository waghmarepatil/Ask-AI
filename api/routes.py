from fastapi import APIRouter, HTTPException, Depends, UploadFile, File

from core.dependencies import get_llm_service
from db.dependency import get_db
from repositories.db_repository import DBRepository
from schemas.request import AskRequest
from schemas.response import AskResponse
from services.llm_service import LLMService

from utils.logger import get_logger



router = APIRouter()

logger = get_logger(__name__)

@router.get("/health")
def health():
    logger.info("Health check API called")
    return {"status":"ok"}

@router.post("/chat", response_model=AskResponse)
async def ask(
        req: AskRequest = Depends(AskRequest.as_form),
        file: UploadFile = File(None),
        db= Depends(get_db),
        llm_service: LLMService = Depends(get_llm_service)
):
    #Injecting DB here
    logger.info(f"Incoming request | question={req.question}")
    try:

        db_repo = DBRepository(db=db)

        if file:
            pdf_bytes = await file.read()
            answer = await llm_service.get_answer_from_pdf(
                question=req.question,
                pdf_bytes=pdf_bytes,
                db_repo=db_repo
            )
        else:

            logger.info("Calling LLMService.get_answer")
            answer = await llm_service.get_answer(req.question, db_repo)

        logger.info(f"Response generated successfully : {answer}")

        return AskResponse(question=req.question, answer=answer)

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
