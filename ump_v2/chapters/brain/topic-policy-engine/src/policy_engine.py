from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class PolicyDecisionType(str, Enum):
    CONTACT = "CONTACT"
    HOLD = "HOLD"
    STOP = "STOP"

class ProposedDecision(BaseModel):
    model_config = ConfigDict(extra='forbid')
    decision: PolicyDecisionType
    reason_code: str
    source_component: str = Field(description="The topic or rule that generated this decision.")

class FinalDecision(BaseModel):
    decision: PolicyDecisionType
    primary_reason: str
    contributing_reasons: List[str]

class PolicyEngine:
    """
    Phase 1 System Core: Enforces output precedence.
    Rule: STOP overrides HOLD overrides CONTACT.
    """
    
    # Precedence lookup for simple comparison. Higher integer wins.
    # Any unknown state must be mapped to HOLD by the caller, but here we strictly rely on the Enum.
    PRECEDENCE_MAP = {
        PolicyDecisionType.CONTACT: 1,
        PolicyDecisionType.HOLD: 2,
        PolicyDecisionType.STOP: 3
    }
    
    def evaluate(self, proposals: List[ProposedDecision]) -> FinalDecision:
        """
        Takes a list of proposed decisions from various rules/tables and reduces them
        to a single authoritative FinalDecision based on the precedence map.
        """
        if not proposals:
            # Deterministic default: If no decisions were made, we default to HOLD to fail safely.
            return FinalDecision(
                decision=PolicyDecisionType.HOLD,
                primary_reason="NO_PROPOSALS",
                contributing_reasons=[]
            )
            
        winning_proposal = proposals[0]
        contributing_reasons = []
        
        for p in proposals:
            if self.PRECEDENCE_MAP[p.decision] > self.PRECEDENCE_MAP[winning_proposal.decision]:
                winning_proposal = p
            
            # Record all holding/stopping reasons for the trace
            if p.decision in (PolicyDecisionType.HOLD, PolicyDecisionType.STOP):
                contributing_reasons.append(f"[{p.source_component}] {p.reason_code}")
                
        # Deduplicate reasons
        contributing_reasons = list(set(contributing_reasons))
                
        return FinalDecision(
            decision=winning_proposal.decision,
            primary_reason=winning_proposal.reason_code,
            contributing_reasons=contributing_reasons
        )
