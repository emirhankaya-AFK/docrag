import chromadb
from typing import List, Dict, Any
from ..config import settings
from .llm_service import LLMService

class RAGService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name="developer_docs",
            metadata={"hnsw:space": "cosine"}
        )

    def index_doc_file(self, doc_id: str, framework_id: str, text: str, metadata: Dict[str, Any]) -> None:
        """
        Chunks and indexes raw documentation texts.
        """
        chunks = self._chunk_text(text, chunk_size=900, overlap=90)
        
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_{idx}"
            chunk_metadata = {
                "doc_id": doc_id,
                "framework_id": framework_id,
                "file_name": metadata.get("file_name", ""),
                "topic": metadata.get("topic", "General")
            }
            
            embedding = self.llm.get_embedding(chunk)
            
            documents.append(chunk)
            embeddings.append(embedding)
            metadatas.append(chunk_metadata)
            ids.append(chunk_id)
            
        if documents:
            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )

    def query_docs(self, query_text: str, framework_id: str = None, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Conducts semantic search over indexed documents, optionally filtered by framework.
        """
        query_embedding = self.llm.get_embedding(query_text)
        
        where_clause = {}
        if framework_id:
            where_clause = {"framework_id": framework_id}
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_clause if where_clause else None
        )
        
        formatted_results = []
        if results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results else [0]*len(docs)
            
            for doc, meta, dist in zip(docs, metas, distances):
                formatted_results.append({
                    "text": doc,
                    "metadata": meta,
                    "score": 1 - dist
                })
                
        return formatted_results

    def delete_doc_index(self, doc_id: str) -> None:
        self.collection.delete(where={"doc_id": doc_id})

    def _chunk_text(self, text: str, chunk_size: int = 900, overlap: int = 90) -> List[str]:
        chunks = []
        words = text.split()
        if not words:
            return []
            
        current_chunk = []
        current_len = 0
        
        for word in words:
            current_chunk.append(word)
            current_len += len(word) + 1
            if current_len >= chunk_size:
                chunks.append(" ".join(current_chunk))
                overlap_words = int((overlap / chunk_size) * len(current_chunk))
                current_chunk = current_chunk[-max(1, overlap_words):]
                current_len = sum(len(w) + 1 for w in current_chunk)
                
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks
