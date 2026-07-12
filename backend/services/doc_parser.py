import fitz
from bs4 import BeautifulSoup
import re
from typing import Dict, Any, List

class DocParserService:
    @staticmethod
    def parse_file(file_path: str, file_format: str) -> Dict[str, Any]:
        """
        Parses HTML, Markdown, or PDF documentation files to retrieve structure and text.
        """
        file_format = file_format.lower()
        if file_format == "html":
            return DocParserService.parse_html(file_path)
        elif file_format == "md" or file_format == "markdown":
            return DocParserService.parse_markdown(file_path)
        elif file_format == "pdf":
            return DocParserService.parse_pdf(file_path)
        else:
            # Fallback plain text read
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return {"full_text": content, "headings": [], "code_blocks": []}

    @staticmethod
    def parse_html(file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            
        # Extract headings
        headings = []
        for tag in soup.find_all(re.compile(r"^h[1-6]$")):
            headings.append({
                "level": int(tag.name[1]),
                "text": tag.get_text().strip()
            })
            
        # Extract code blocks
        code_blocks = []
        for tag in soup.find_all(["pre", "code"]):
            text = tag.get_text().strip()
            if text:
                # Guess language
                cls = tag.get("class", [])
                lang = "python"
                for c in cls:
                    if "js" in c or "javascript" in c:
                        lang = "javascript"
                        break
                    elif "bash" in c or "sh" in c:
                        lang = "bash"
                        break
                code_blocks.append({
                    "language": lang,
                    "code": text
                })
                
        # Clean text
        full_text = soup.get_text(separator="\n")
        
        return {
            "full_text": full_text,
            "headings": headings,
            "code_blocks": code_blocks
        }

    @staticmethod
    def parse_markdown(file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract headings (regex matching lines starting with #)
        headings = []
        for match in re.finditer(r"^(#{1,6})\s+(.*)$", content, re.MULTILINE):
            headings.append({
                "level": len(match.group(1)),
                "text": match.group(2).strip()
            })
            
        # Extract code blocks (regex matching triple backticks)
        code_blocks = []
        for match in re.finditer(r"```(\w*)\n([\s\S]*?)```", content):
            code_blocks.append({
                "language": match.group(1).strip() or "python",
                "code": match.group(2).strip()
            })
            
        return {
            "full_text": content,
            "headings": headings,
            "code_blocks": code_blocks
        }

    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        doc = fitz.open(file_path)
        full_text = []
        
        for page in doc:
            full_text.append(page.get_text())
            
        complete_text = "\n\n".join(full_text)
        
        # Simple heading detection (e.g. short, capitalized lines)
        headings = []
        for line in complete_text.split("\n"):
            line = line.strip()
            if len(line) < 60 and line.isupper() and len(line) > 3:
                headings.append({"level": 2, "text": line})
                
        return {
            "full_text": complete_text,
            "headings": headings,
            "code_blocks": []  # Harder to extract cleanly from PDF, fall back to LLM processing
        }
