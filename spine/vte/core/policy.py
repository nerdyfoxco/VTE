from typing import Dict, Optional
from pydantic import BaseModel
from vte.api.schema import DecisionDraft, OutcomeEnum, RoleEnum

class PolicyResult(BaseModel):
    allowed: bool
    reason: Optional[str] = None

class PolicyEngine:
    def __init__(self):
        self.rules_version = "1.0-stub"

    def evaluate(self, draft: DecisionDraft, actor_claims: Dict) -> PolicyResult:
        """
        Evaluates the DecisionDraft against hard-coded policy rules.
        """
        
        # 1. Super Admin Override
        # If the actor is a super_admin, they can do anything (for now).
        # In real OPA, this would be a high-priority rule.
        user_role = actor_claims.get("role")
        if user_role == RoleEnum.super_admin:
             return PolicyResult(allowed=True, reason="Super Admin Override")

        # 2. Evidence Requirement for Approvals
        # Rule: You cannot APPROVE a transaction without EVIDENCE.
        if draft.outcome == OutcomeEnum.APPROVED:
            if not draft.evidence_hash or draft.evidence_hash.strip() == "":
                return PolicyResult(
                    allowed=False, 
                    reason="POLICY VIOLATION: Cannot APPROVE without 'evidence_hash'."
                )
            
            # Simple check: Is it a valid-looking hash? (Length check for SHA256)
            if len(draft.evidence_hash) != 64:
                 return PolicyResult(
                    allowed=False, 
                    reason="POLICY VIOLATION: 'evidence_hash' must be a valid SHA256 hex string."
                )

        # 3. Policy Version Check
        # Rule: The draft must cite a supported policy version.
        supported_policies = ["v1.0", "v2.0-beta"]
        if draft.policy_version not in supported_policies:
             return PolicyResult(
                allowed=False, 
                reason=f"POLICY VIOLATION: Unsupported policy_version '{draft.policy_version}'. Supported: {supported_policies}"
            )

        # Default Allow
        return PolicyResult(allowed=True, reason="Policy Checks Passed")
