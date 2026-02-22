from typing import List, Dict, Any, Callable
import sys
from pathlib import Path

# Add policy engine src map to path so compiler can resolve it.
# Architecture rule: topic-orchestration can consume topic-policy-engine
current_dir = Path(__file__).resolve().parent
policy_src_dir = current_dir.parent.parent / "topic-policy-engine" / "src"
sys.path.insert(0, str(policy_src_dir))

from policy_engine import ProposedDecision, PolicyDecisionType

class DecisionRule:
    """A deterministic rule targeting a single feature/field."""
    def __init__(self, key: str, expected_value: Any, decision: PolicyDecisionType, reason: str, rule_id: str):
        self.key = key
        self.expected_value = expected_value
        self.decision = decision
        self.reason = reason
        self.rule_id = rule_id
        
    def evaluate(self, context: Dict[str, Any]) -> ProposedDecision | None:
        if self.key in context:
            if context[self.key] == self.expected_value:
                return ProposedDecision(
                    decision=self.decision,
                    reason_code=self.reason,
                    source_component=self.rule_id
                )
        return None

class DecisionTableCompiler:
    """
    Phase 2 Brain Runtime: Compiles rule dictionaries into an executable evaluation graph.
    Returns a proposal list suitable for the PolicyEngine Core.
    """
    def __init__(self, raw_rules: List[Dict[str, Any]]):
        self.compiled_rules: List[DecisionRule] = []
        self._compile(raw_rules)
        
    def _compile(self, raw_rules: List[Dict[str, Any]]):
        for idx, rule in enumerate(raw_rules):
            try:
                self.compiled_rules.append(
                    DecisionRule(
                        key=rule["key"],
                        expected_value=rule["expected_value"],
                        decision=PolicyDecisionType(rule["decision"]),
                        reason=rule["reason"],
                        rule_id=rule.get("rule_id", f"compiled_rule_{idx}")
                    )
                )
            except (KeyError, ValueError) as e:
                # Compile-time failure if rules are malformed. Ensures deterministic guarantee.
                raise ValueError(f"Failed to compile rule index {idx}: {e}")
                
    def evaluate(self, context: Dict[str, Any]) -> List[ProposedDecision]:
        """
        Executes the compiled rules against an evidence context.
        If ambiguity exists (e.g., no rules match), yields a HOLD proposal by default.
        """
        proposals = []
        for rule in self.compiled_rules:
            result = rule.evaluate(context)
            if result:
                proposals.append(result)
                
        # Deterministic Safety: If no rules match the given context, propose HOLD due to ambiguity.
        if not proposals:
            proposals.append(
                ProposedDecision(
                    decision=PolicyDecisionType.HOLD,
                    reason_code="AMBIGUOUS_EVIDENCE_NO_RULE_MATCH",
                    source_component="decision_compiler"
                )
            )
            
        return proposals
