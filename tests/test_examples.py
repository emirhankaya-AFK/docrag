import pytest
from backend.services.version_manager import VersionManagerService
from backend.services.llm_service import LLMService
from backend.services.rag_service import RAGService
from backend.agents.example_agent import ExampleAgent

def test_semver_manager():
    # Compare 0.111.0 vs 0.95.0 -> 1 (v1 is higher)
    res = VersionManagerService.compare_versions("0.111.0", "0.95.0")
    assert res == 1
    
    # Compare 1.2.0 vs 1.2.0 -> 0 (equal)
    res2 = VersionManagerService.compare_versions("v1.2.0", "1.2")
    assert res2 == 0
    
    # Check deprecation
    status = VersionManagerService.is_method_deprecated(
        method_added_ver="0.90.0",
        current_ver="0.98.0",
        deprecation_ver="0.95.0"
    )
    assert status["is_deprecated"] is True
    assert "deprecated" in status["warning"]

def test_example_generation():
    llm = LLMService()
    rag = RAGService(llm)
    agent = ExampleAgent(llm, rag)
    
    code = agent.generate_example("Create FastAPI depends dependency", "fastapi")
    assert "def " in code or "class " in code or "import " in code
