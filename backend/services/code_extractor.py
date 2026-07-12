from typing import List, Dict, Any
import re

class CodeExtractorService:
    @staticmethod
    def extract_and_tag_code(parsed_data: Dict[str, Any], framework_name: str) -> List[Dict[str, Any]]:
        """
        Takes parsed text/code blocks and formats them as ready-to-use CodeExample entries.
        """
        examples = []
        raw_blocks = parsed_data.get("code_blocks", [])
        
        # If no code blocks were parsed but text has backticks, run a regex backup
        if not raw_blocks:
            text = parsed_data.get("full_text", "")
            for match in re.finditer(r"```(\w*)\n([\s\S]*?)```", text):
                raw_blocks.append({
                    "language": match.group(1).strip() or "python",
                    "code": match.group(2).strip()
                })
                
        for idx, block in enumerate(raw_blocks):
            code = block["code"]
            lang = block["language"] or "python"
            
            # Simple heuristic to guess task description from surrounding lines
            task = f"Usage example in {framework_name}"
            tags = [framework_name.lower(), lang.lower()]
            
            # Look for keywords in code to add tags
            lower_code = code.lower()
            if "auth" in lower_code or "login" in lower_code or "jwt" in lower_code:
                tags.append("authentication")
                task = f"Authentication flow in {framework_name}"
            elif "router" in lower_code or "get(" in lower_code or "post(" in lower_code:
                tags.append("routing")
                task = f"API routing setups in {framework_name}"
            elif "db" in lower_code or "session" in lower_code or "select" in lower_code:
                tags.append("database")
                task = f"Database connectivity pattern in {framework_name}"
                
            examples.append({
                "id": f"code_{idx}_{hash(code) % 10000}",
                "framework": framework_name,
                "language": lang,
                "task_description": task,
                "code_block": code,
                "tags": list(set(tags))
            })
            
        return examples
