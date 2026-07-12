from typing import Dict, Any, List
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService

class SearchAgent:
    def __init__(self, llm_service: LLMService, rag_service: RAGService):
        self.llm = llm_service
        self.rag = rag_service

    def semantic_search(self, query: str, framework_id: str = None) -> List[Dict[str, Any]]:
        """
        Retrieves matching documentation chunks from ChromaDB.
        """
        return self.rag.query_docs(query_text=query, framework_id=framework_id, n_results=4)

    def extract_search_context(self, query: str, framework_id: str = None) -> Dict[str, Any]:
        """
        Retrieves relevant docs and extracts structural details like signature and parameters.
        """
        chunks = self.semantic_search(query, framework_id)
        if not chunks:
            return {
                "name": "No match found",
                "parameters": "None",
                "description": "No relevant section found in documentation.",
                "code_example": "# N/A"
            }
            
        context = "\n\n".join([c["text"] for c in chunks])
        
        variables = {
            "query": query,
            "text": context  # prompts.yaml might expect the text payload
        }
        
        return self.llm.generate_json("search_context", variables)
