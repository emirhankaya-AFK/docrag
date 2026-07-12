from typing import Dict, Any
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService

class ExampleAgent:
    def __init__(self, llm_service: LLMService, rag_service: RAGService):
        self.llm = llm_service
        self.rag = rag_service

    def generate_example(self, task: str, framework_id: str = None) -> str:
        """
        Generates copy-paste ready code examples using documentation context.
        """
        chunks = self.rag.query_docs(query_text=task, framework_id=framework_id, n_results=3)
        context = "\n\n".join([c["text"] for c in chunks]) if chunks else "No relevant context found."
        
        variables = {
            "task": task,
            "context": context
        }
        
        return self.llm.generate_text("code_gen", variables)
