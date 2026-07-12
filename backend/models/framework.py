from pydantic import BaseModel
from typing import Optional

class Framework(BaseModel):
    id: str
    name: str
    current_version: str
    doc_format: str  # HTML, MD, PDF
    language: str
