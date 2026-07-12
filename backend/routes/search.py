from fastapi import APIRouter, HTTPException
from typing import Optional
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService
from ..agents.search_agent import SearchAgent

router = APIRouter(prefix="/search", tags=["search"])

llm_service = LLMService()
rag_service = RAGService(llm_service)
search_agent = SearchAgent(llm_service, rag_service)

@router.get("/")
async def semantic_search(query: str, framework_id: Optional[str] = None):
    try:
        results = search_agent.semantic_search(query, framework_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/details")
async def search_details(query: str, framework_id: Optional[str] = None):
    try:
        details = search_agent.extract_search_context(query, framework_id)
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
