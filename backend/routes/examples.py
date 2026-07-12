from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..db import list_code_examples
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService
from ..agents.example_agent import ExampleAgent

router = APIRouter(prefix="/examples", tags=["examples"])

llm_service = LLMService()
rag_service = RAGService(llm_service)
example_agent = ExampleAgent(llm_service, rag_service)

class ExampleRequest(BaseModel):
    task: str
    framework_id: Optional[str] = None

@router.get("/")
async def get_examples(framework: Optional[str] = None):
    return list_code_examples(framework)

@router.post("/generate")
async def generate_example(req: ExampleRequest):
    try:
        code = example_agent.generate_example(req.task, req.framework_id)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
