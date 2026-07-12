from fastapi import APIRouter, HTTPException
from typing import Optional
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService
from ..agents.best_practice_agent import BestPracticeAgent

router = APIRouter(prefix="/best-practices", tags=["best-practices"])

llm_service = LLMService()
rag_service = RAGService(llm_service)
bp_agent = BestPracticeAgent(llm_service, rag_service)

@router.get("/")
async def get_best_practices(topic: str, framework_id: Optional[str] = None):
    try:
        report = bp_agent.analyze_practices(topic, framework_id)
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
