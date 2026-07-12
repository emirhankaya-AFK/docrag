from pydantic import BaseModel
from typing import List

class CodeExample(BaseModel):
    id: str
    framework: str
    language: str
    task_description: str
    code_block: str
    tags: List[str] = []
