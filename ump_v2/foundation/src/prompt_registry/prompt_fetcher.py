import json
from pathlib import Path

class PromptNotFoundError(Exception):
    pass

class PromptFetcher:
    """
    Phase 1 Control Plane: Authoritative prompt dictionary.
    Ensures that prompts cannot drift dynamically by forcing code to request
    a specific verisoned string ID.
    """
    
    def __init__(self, registry_path: str = None):
        if registry_path is None:
            # Default to the adjacent prompts.json
            current_dir = Path(__file__).resolve().parent
            registry_path = current_dir / "prompts.json"
            
        self.registry_path = Path(registry_path)
        self._prompts = self._load()
        
    def _load(self) -> dict:
        if not self.registry_path.exists():
            return {}
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def get_prompt(self, prompt_id: str) -> str:
        """
        Retrieves a versioned prompt string.
        Fails closed explicitly if the requested version is missing.
        """
        if prompt_id not in self._prompts:
            raise PromptNotFoundError(
                f"Determinism Error: Prompt ID '{prompt_id}' was not found in the registry. "
                "AI prompts must be explicitly pinned and cannot be dynamically generated."
            )
        return self._prompts[prompt_id]
