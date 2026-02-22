import json
from pathlib import Path
from typing import Dict, Any, Optional

class ConsentViolationError(Exception):
    """Raised when an operation is attempted without explicit user consent."""
    pass

class ConsentRegistry:
    """
    Phase 6 Kidneys (Compliance): Mechanically checks outbound intent against 
    a mock user consent database and jurisdiction rules.
    Fails closed if the action is not authorized.
    """
    def __init__(self, rules_path: Optional[str] = None):
        if rules_path is None:
            rules_path = Path(__file__).resolve().parent / "jurisdiction_rules.json"
        
        self.rules_path = Path(rules_path)
        self.jurisdiction_rules = self._load_rules()
        
        # Mock database of user preferences
        self._user_db = {
            "user_1": {"region": "US", "consent_granted": True},
            "user_2": {"region": "EU", "consent_granted": False},
            "user_3": {"region": "NK", "consent_granted": True} # Blocked region bypass attempt
        }

    def _load_rules(self) -> Dict[str, Any]:
        if not self.rules_path.exists():
            # Fail closed explicitly if compliance rules are missing.
            raise FileNotFoundError("Critical Error: jurisdiction_rules.json missing from Compliance module.")
        with open(self.rules_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def verify_action(self, user_id: str, action_type: str) -> None:
        """
        Validates if the user can be engaged based on Region and Consent.
        Throws ConsentViolationError if the check fails.
        """
        user_data = self._user_db.get(user_id)
        if not user_data:
            raise ConsentViolationError(f"Compliance Blocked: User '{user_id}' not found. Defaulting to ZERO consent.")
            
        region = user_data["region"]
        
        if region in self.jurisdiction_rules.get("blocked_regions", []):
            raise ConsentViolationError(f"Compliance Blocked: Trade embargo. Cannot execute '{action_type}' for user in blocked region: {region}")
            
        if not user_data["consent_granted"]:
            raise ConsentViolationError(f"Compliance Blocked: Explicit consent revoked or not granted by '{user_id}'. Cannot execute '{action_type}'.")
            
        # Consent is valid and region is allowed.
        pass
