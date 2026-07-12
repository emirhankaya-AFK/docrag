import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
import google.generativeai as genai
from ..config import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.prompts = self._load_prompts()
        self.mock_mode = not self.api_key
        
        if not self.mock_mode:
            genai.configure(api_key=self.api_key)
            
    def _load_prompts(self) -> Dict[str, str]:
        prompt_path = Path(__file__).parent.parent / "config" / "prompts.yaml"
        if prompt_path.exists():
            with open(prompt_path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def generate_text(self, prompt_name: str, variables: Dict[str, Any]) -> str:
        prompt_template = self.prompts.get(prompt_name, "")
        if not prompt_template:
            prompt_template = "{text}"
            if "text" not in variables:
                variables["text"] = str(variables)
                
        formatted_prompt = prompt_template.format(**variables)
        
        if self.mock_mode:
            return self._mock_response(prompt_name, variables)
            
        try:
            model = genai.GenerativeModel(settings.DEFAULT_MODEL)
            response = model.generate_content(formatted_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}. Falling back to mock.")
            return self._mock_response(prompt_name, variables)

    def generate_json(self, prompt_name: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        prompt_template = self.prompts.get(prompt_name, "")
        formatted_prompt = prompt_template.format(**variables)
        
        if self.mock_mode:
            return json.loads(self._mock_response(prompt_name, variables, json_format=True))
            
        try:
            model = genai.GenerativeModel(settings.DEFAULT_MODEL)
            response = model.generate_content(
                formatted_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text.strip())
        except Exception as e:
            print(f"Gemini JSON API Error: {e}. Falling back to mock.")
            return json.loads(self._mock_response(prompt_name, variables, json_format=True))

    def get_embedding(self, text: str) -> List[float]:
        if self.mock_mode or not self.api_key:
            import random
            random.seed(hash(text))
            return [random.uniform(-0.1, 0.1) for _ in range(1536)]
            
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding API Error: {e}. Falling back to mock vector.")
            import random
            random.seed(hash(text))
            return [random.uniform(-0.1, 0.1) for _ in range(1536)]

    def _mock_response(self, prompt_name: str, variables: Dict[str, Any], json_format: bool = False) -> str:
        if json_format:
            if prompt_name == "search_context":
                return json.dumps({
                    "name": "fastapi.HTTPException",
                    "parameters": "status_code: int, detail: str = None, headers: dict = None",
                    "description": "An exception class that represents HTTP errors. Raising it will immediately return the status code and detail to the client.",
                    "code_example": "from fastapi import HTTPException\n\nraise HTTPException(status_code=400, detail='Invalid request data')"
                })
            return "{}"
        else:
            if prompt_name == "qa":
                return "To raise HTTP exceptions in FastAPI, use the `HTTPException` class from `fastapi`. Import it and raise it with a `status_code` and optional `detail` string: `raise HTTPException(status_code=404, detail='Not found')`."
            elif prompt_name == "error_explanation":
                return f"""### Root Cause Analysis
The error `{variables.get('error_message')}` is typically raised when attempting to iterate or unpack a function return value that resolves to `None`. 

### Steps to Fix
1. Inspect the function returning this value to ensure it returns a valid iterable (tuple, list) in all execution paths.
2. Add defensive checks: check if the value is not `None` before unpacking.

### Corrected Code
```python
result = fetch_data()
if result is not None:
    x, y = result
else:
    # Handle error
    x, y = default_values()
```
"""
            elif prompt_name == "code_gen":
                return f"""```python
# Generated code example for task
from fastapi import FastAPI, Depends

app = FastAPI()

def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {{"q": q, "skip": skip, "limit": limit}}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```
"""
            elif prompt_name == "best_practice":
                return """# Best Practices for FastAPI Dependency Injection

## Do's
- Use `Depends()` to extract shared logic (database connections, auth scopes).
- Prefer class-based dependencies when carrying states or configuration flags.

## Don'ts
- Don't write nested, circular dependencies that become hard to trace.
- Avoid performing heavy, non-cached queries inside dependency functions.

## Performance Tips
- Use `yield` dependencies to handle resource cleanup (like DB session closes) automatically.
"""
            return f"Mock text response for {prompt_name}"
