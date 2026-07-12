from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Documentation(BaseModel):
    id: str
    framework_id: str
    file_name: str
    file_path: str
    file_format: str  # HTML, MD, PDF
    uploaded_at: datetime = datetime.now()
