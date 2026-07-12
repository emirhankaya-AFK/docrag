import pytest
from pathlib import Path
from .generate_test_docs import create_sample_docs
from backend.services.doc_parser import DocParserService
from backend.services.llm_service import LLMService
from backend.services.rag_service import RAGService
from backend.agents.qa_agent import QAAgent

@pytest.fixture(scope="module")
def sample_md():
    md_path = Path(__file__).parent / "temp_test_doc_qa.md"
    create_sample_docs(str(md_path))
    yield str(md_path)
    if md_path.exists():
        md_path.unlink()

def test_docs_qa(sample_md):
    parsed = DocParserService.parse_file(sample_md, "md")
    llm = LLMService()
    rag = RAGService(llm)
    
    doc_id = "test_doc_qa_id"
    meta = {"file_name": "fastapi_di.md"}
    
    rag.index_doc_file(doc_id, "fastapi", parsed["full_text"], meta)
    
    qa_agent = QAAgent(llm, rag)
    ans = qa_agent.answer_question("How do I use Depends in FastAPI?", "fastapi")
    
    assert ans["answer"] != ""
    assert len(ans["sources"]) > 0
    
    rag.delete_doc_index(doc_id)
