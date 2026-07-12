from typing import Dict, Any
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService

class BestPracticeAgent:
    def __init__(self, llm_service: LLMService, rag_service: RAGService):
        self.llm = llm_service
        self.rag = rag_service

    def analyze_practices(self, topic: str, framework_id: str = None) -> str:
        """
        Extracts documentation details and summarizes programming recommendations.
        """
        chunks = self.rag.query_docs(query_text=topic, framework_id=framework_id, n_results=3)
        context = "\n\n".join([c["text"] for c in chunks]) if chunks else "No relevant context found."
        
        variables = {
            "topic": topic,
            "context": context
        }
        
        return self.llm.generate_text("best_practice", variables)
