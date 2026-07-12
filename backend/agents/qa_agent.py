from typing import Dict, Any, List
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService

class QAAgent:
    def __init__(self, llm_service: LLMService, rag_service: RAGService):
        self.llm = llm_service
        self.rag = rag_service

    def answer_question(self, question: str, framework_id: str = None) -> Dict[str, Any]:
        """
        Answers a developer question using RAG docs.
        """
        chunks = self.rag.query_docs(query_text=question, framework_id=framework_id, n_results=4)
        
        if not chunks:
            return {
                "answer": "Not discussed in this documentation.",
                "sources": []
            }
            
        context_parts = []
        sources = []
        for idx, c in enumerate(chunks):
            filename = c["metadata"].get("file_name", "unknown")
            text_chunk = c["text"]
            context_parts.append(f"--- Chunk {idx+1} (File: {filename}) ---\n{text_chunk}")
            sources.append({
                "file_name": filename,
                "score": float(c["score"]),
                "snippet": text_chunk[:150] + "..."
            })
            
        context = "\n\n".join(context_parts)
        
        variables = {
            "context": context,
            "question": question
        }
        
        answer = self.llm.generate_text("qa", variables)
        
        return {
            "answer": answer,
            "sources": sources
        }
