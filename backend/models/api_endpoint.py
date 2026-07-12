from pydantic import BaseModel
from typing import List, Optional

class APIEndpoint(BaseModel):
    name: str
    signature: Optional[str] = None
    parameters: Optional[str] = None
    description: Optional[str] = None
    version_added: Optional[str] = None
    is_deprecated: bool = False
    deprecation_reason: Optional[str] = None
