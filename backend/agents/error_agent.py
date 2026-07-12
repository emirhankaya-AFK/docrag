from typing import Dict, Any
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService
from ..services.error_database import ErrorDatabaseService

class ErrorAgent:
    def __init__(self, llm_service: LLMService, rag_service: RAGService, err_db: ErrorDatabaseService):
        self.llm = llm_service
        self.rag = rag_service
        self.err_db = err_db

    def troubleshoot_error(self, error_message: str, framework_id: str = None) -> Dict[str, Any]:
        """
        Troubleshoots developer error message using database mappings and RAG documentation.
        """
        # 1. Check local catalog first
        local_match = self.err_db.lookup_error(error_message)
        if local_match:
            # Let's enrich it with a corrected code example using LLM
            return {
                "error_type": local_match["error_type"],
                "root_cause": local_match["explanation"],
                "fix_steps": local_match["solution"],
                "corrected_code": "See troubleshooting details."
            }
            
        # 2. RAG fallback
        chunks = self.rag.query_docs(query_text=error_message, framework_id=framework_id, n_results=3)
        context = "\n\n".join([c["text"] for c in chunks]) if chunks else "No relevant context found."
        
        variables = {
            "error_message": error_message,
            "context": context
        }
        
        narrative = self.llm.generate_text("error_explanation", variables)
        
        # Simple parser for markdown sections in response
        return {
            "error_type": "Parsed Exception",
            "root_cause": "Detailed analysis below.",
            "fix_steps": narrative,
            "corrected_code": ""
        }
