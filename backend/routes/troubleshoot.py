from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService
from ..services.error_database import ErrorDatabaseService
from ..agents.error_agent import ErrorAgent

router = APIRouter(prefix="/troubleshoot", tags=["troubleshoot"])

llm_service = LLMService()
rag_service = RAGService(llm_service)
err_db = ErrorDatabaseService()
error_agent = ErrorAgent(llm_service, rag_service, err_db)

class TroubleshootRequest(BaseModel):
    error_message: str
    framework_id: Optional[str] = None

@router.post("/")
async def troubleshoot_error(req: TroubleshootRequest):
    try:
        report = error_agent.troubleshoot_error(req.error_message, req.framework_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
