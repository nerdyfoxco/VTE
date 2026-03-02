from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging
from vte.api.schema import EvidenceItem, EvidenceBundleDraft

class Agent(ABC):
    """
    Abstract Base Class for all VTE Agents.
    Forces standard logging, error handling, and output formats.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"vte.agent.{agent_id}")
        self.logger.setLevel(logging.INFO)

    @abstractmethod
    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """
        The main execution loop of the agent.
        Must return a summary dict (e.g., {"processed": 5}).
        """
        pass

    def create_evidence(self, source: str, type: str, data: Dict[str, Any], sha256: str) -> EvidenceItem:
        """
        Helper to create valid EvidenceItem.
        """
        return EvidenceItem(
            source=source,
            type=type,
            data=data,
            sha256=sha256
        )

    def emit(self, draft: Any) -> bool:
        """
        Emits a DecisionDraft or EvidenceBundleDraft directly to the VTE API.
        Requires BOT_API_TOKEN environment variable.
        """
        import os
        import requests
        
        api_url = os.getenv("API_URL", "http://localhost:8000/api/v1")
        token = os.getenv("BOT_API_TOKEN", "system-agent-token-1234")
        
        try:
            payload = draft.model_dump() if hasattr(draft, 'model_dump') else draft
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            
            response = requests.post(f"{api_url}/decisions/drafts", json=payload, headers=headers, timeout=5)
            if response.status_code in [200, 201, 202]:
                self.logger.info(f"Successfully emitted draft to API. Status: {response.status_code}")
                return True
            else:
                self.logger.warning(f"Failed to emit draft. API returned {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Error emitting draft to API: {e}")
            return False
