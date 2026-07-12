import pytest
from pathlib import Path
from .generate_test_docs import create_sample_docs
from backend.services.doc_parser import DocParserService
from backend.services.code_extractor import CodeExtractorService
from backend.services.llm_service import LLMService
from backend.services.rag_service import RAGService
from backend.agents.search_agent import SearchAgent

@pytest.fixture(scope="module")
def sample_md():
    md_path = Path(__file__).parent / "temp_test_doc.md"
    create_sample_docs(str(md_path))
    yield str(md_path)
    if md_path.exists():
        md_path.unlink()

def test_markdown_parsing(sample_md):
    parsed = DocParserService.parse_file(sample_md, "md")
    assert "Dependency Injection" in parsed["full_text"]
    assert len(parsed["headings"]) > 0
    assert parsed["headings"][0]["text"] == "FastAPI Dependency Injection"
    assert len(parsed["code_blocks"]) > 0
    assert parsed["code_blocks"][0]["language"] == "python"

def test_code_extraction(sample_md):
    parsed = DocParserService.parse_file(sample_md, "md")
    examples = CodeExtractorService.extract_and_tag_code(parsed, "FastAPI")
    assert len(examples) > 0
    assert examples[0]["framework"] == "FastAPI"
    assert "routing" in examples[0]["tags"]

def test_semantic_search(sample_md):
    parsed = DocParserService.parse_file(sample_md, "md")
    llm = LLMService()
    rag = RAGService(llm)
    
    doc_id = "test_doc_search_id"
    meta = {"file_name": "fastapi_di.md"}
    
    # Index
    rag.index_doc_file(doc_id, "fastapi", parsed["full_text"], meta)
    
    # Query
    results = rag.query_docs("Depends", "fastapi")
    assert len(results) > 0
    
    # Clean
    rag.delete_doc_index(doc_id)
