from pydantic import BaseModel
from typing import Optional, Dict, Any

class GoogleEmail(BaseModel):
    source_id: str
    thread_id: str
    subject: str
    sender: str
    date_raw: str
    snippet: str

    def to_evidence_data(self) -> Dict[str, Any]:
        return self.model_dump()
