from typing import Dict, Any, List
from ..services.doc_parser import DocParserService
from ..services.code_extractor import CodeExtractorService

class DocParsingAgent:
    @staticmethod
    def parse_documentation(file_path: str, file_format: str, framework_name: str) -> Dict[str, Any]:
        """
        Coordinates document reading, header segmentation, and code snippets extraction.
        """
        parsed_data = DocParserService.parse_file(file_path, file_format)
        
        # Extract code blocks
        code_examples = CodeExtractorService.extract_and_tag_code(parsed_data, framework_name)
        
        return {
            "full_text": parsed_data["full_text"],
            "headings": parsed_data["headings"],
            "code_examples": code_examples
        }
