from pydantic import BaseModel
from typing import Optional

class ErrorLog(BaseModel):
    error_type: str
    message: str
    stacktrace: Optional[str] = None
    framework: Optional[str] = None

class ErrorTroubleshootResult(BaseModel):
    error_type: str
    root_cause: str
    fix_steps: str
    corrected_code: str
