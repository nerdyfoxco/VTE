import sys
import uuid
import logging
# Foundation Imports
from foundation.runtime.config import config
from foundation.runtime.vte_logger import configure_logger

# Legacy Import (The "Engine")
# We need to make sure 'spine' is in path, usually it is if cwd is root.
try:
    from spine.vte.core.llm import LLMClient as LegacyLLMClient
except ImportError:
    # Fallback for dev/test environments where spine might not be importable directly 
    # if paths aren't set up perfectly. 
    # But for now we assume it exists as per "Legacy Strategy".
    LegacyLLMClient = None

class BrainClient:
    """
    Governance Wrapper for the LLM.
    Enforces:
    1. Trace IDs (Audit)
    2. Config usage (No hardcoded keys)
    3. Exception Safety
    """
    def __init__(self, trace_id: str = None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.logger = configure_logger("BRAIN_CLIENT")
        
        # Initialize Legacy Client using VTE_CONFIG
        # We explicitly pass keys from config to ensure we are using the governed source.
        api_key = config.openai_key or config.google_key
        
        if LegacyLLMClient:
            self._engine = LegacyLLMClient(api_key=api_key)
            self.logger.info("Brain Engine Initialized (Spine)", extra={"trace_id": self.trace_id})
        else:
            self._engine = None
            self.logger.warning("Brain Engine (Spine) NOT FOUND. Running in MOCK mode.", extra={"trace_id": self.trace_id})

    def analyze(self, ledger_data: str, email_content: str) -> str:
        """
        Public Interface for Delinquency Analysis.
        Logs the request and response with trace_id.
        """
        self.logger.info("Brain Analysis Requested", extra={"trace_id": self.trace_id})
        
        if not self._engine:
            return "MOCK: Brain Engine missing."
            
        try:
            # Delegate to Engine
            result = self._engine.analyze_discrepancy(ledger_data, email_content)
            
            self.logger.info("Brain Analysis Complete", extra={"trace_id": self.trace_id})
            return result
        except Exception as e:
            self.logger.error(f"Brain Analysis Failed: {e}", extra={"trace_id": self.trace_id})
            raise e

    def think(self, prompt: str) -> str:
        """
        Agentic Interface: Ask the Brain to think about a prompt.
        """
        self.logger.info("Brain Thought Requested", extra={"trace_id": self.trace_id})
        if not self._engine:
            return '{"action": "ABORT", "reason": "No Brain Engine"}'
            
        try:
            return self._engine.generate(prompt)
        except Exception as e:
            self.logger.error(f"Brain Think Failed: {e}", extra={"trace_id": self.trace_id})
            return '{"action": "ABORT", "reason": "Brain Error"}'

if __name__ == "__main__":
    # Canary Run
    client = BrainClient()
    print("Brain Client Initialized")
    
    # Mock Data
    res = client.analyze("Ledger: $100 owed", "Email: I paid $100")
    print(f"Result: {res}")
    print("Brain Analysis Complete")
