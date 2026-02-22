import sys
import unittest
from pathlib import Path

# The current dir is chapters/brain/topic-policy-engine/tests
# The src dir is chapters/brain/topic-policy-engine/src
current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"

# Add the specific src directory to path to bypass python hyphen-import restrictions
sys.path.insert(0, str(src_dir))

from policy_engine import PolicyEngine, ProposedDecision, PolicyDecisionType

class TestPolicyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PolicyEngine()

    def test_contact_only_proposals(self):
        proposals = [
            ProposedDecision(decision=PolicyDecisionType.CONTACT, reason_code="LOW_RISK", source_component="rule_1"),
            ProposedDecision(decision=PolicyDecisionType.CONTACT, reason_code="NO_DELINQUENCY", source_component="rule_2")
        ]
        result = self.engine.evaluate(proposals)
        self.assertEqual(result.decision, PolicyDecisionType.CONTACT)
        
    def test_hold_overrides_contact(self):
        proposals = [
            ProposedDecision(decision=PolicyDecisionType.CONTACT, reason_code="LOW_RISK", source_component="rule_1"),
            ProposedDecision(decision=PolicyDecisionType.HOLD, reason_code="AWAITING_FUNDS", source_component="rule_2")
        ]
        result = self.engine.evaluate(proposals)
        self.assertEqual(result.decision, PolicyDecisionType.HOLD)
        self.assertEqual(result.primary_reason, "AWAITING_FUNDS")
        self.assertIn("[rule_2] AWAITING_FUNDS", result.contributing_reasons)

    def test_stop_overrides_all(self):
        proposals = [
            ProposedDecision(decision=PolicyDecisionType.CONTACT, reason_code="LOW_RISK", source_component="rule_1"),
            ProposedDecision(decision=PolicyDecisionType.HOLD, reason_code="AWAITING_FUNDS", source_component="rule_2"),
            ProposedDecision(decision=PolicyDecisionType.STOP, reason_code="LEGAL_REP_REGISTERED", source_component="compliance_rule")
        ]
        result = self.engine.evaluate(proposals)
        self.assertEqual(result.decision, PolicyDecisionType.STOP)
        self.assertEqual(result.primary_reason, "LEGAL_REP_REGISTERED")
        
    def test_empty_proposals_defaults_to_hold(self):
        result = self.engine.evaluate([])
        self.assertEqual(result.decision, PolicyDecisionType.HOLD)
        self.assertEqual(result.primary_reason, "NO_PROPOSALS")

if __name__ == '__main__':
    unittest.main()
