import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class ErrorDatabaseService:
    def __init__(self):
        self.mappings = self._load_mappings()

    def _load_mappings(self) -> Dict[str, Any]:
        path = Path(__file__).parent.parent / "config" / "error_mappings.yaml"
        if path.exists():
            with open(path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def lookup_error(self, error_message: str) -> Optional[Dict[str, Any]]:
        """
        Scans error mappings to find matching patterns.
        """
        for err_type, data in self.mappings.items():
            if err_type.lower() in error_message.lower():
                return {
                    "error_type": err_type,
                    "explanation": data["explanation"],
                    "solution": data["solution"]
                }
        return None
