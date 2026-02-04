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

    # TODO: Add emit() to post to API or DB directly?
    # For now, Agents might return data tasks, or we inject a repository.
    # Decoupling: Agents return 'EvidenceBundleDraft', Task runner saves it.
