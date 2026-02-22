import sys
import unittest
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

# Add policy engine path to fix sub-imports
policy_src_dir = current_dir.parent.parent / "topic-policy-engine" / "src"
sys.path.insert(0, str(policy_src_dir))

from decision_table_compiler import DecisionTableCompiler
from policy_engine import PolicyDecisionType

class TestDecisionTableCompiler(unittest.TestCase):
    
    def setUp(self):
        self.raw_rules = [
            {
                "rule_id": "rule_legal",
                "key": "has_legal_representation",
                "expected_value": True,
                "decision": "STOP",
                "reason": "LEGAL_REPRESENTATION"
            },
            {
                "rule_id": "rule_balance",
                "key": "balance_owed",
                "expected_value": 0,
                "decision": "HOLD",
                "reason": "ZERO_BALANCE"
            },
            {
                "rule_id": "rule_delinquent",
                "key": "status",
                "expected_value": "delinquent",
                "decision": "CONTACT",
                "reason": "DELINQUENT_STATUS"
            }
        ]
        self.compiler = DecisionTableCompiler(self.raw_rules)

    def test_compilation_success(self):
        self.assertEqual(len(self.compiler.compiled_rules), 3)
        
    def test_malformed_rule_throws_compile_error(self):
        bad_rules = [{"key": "missing_fields"}]
        with self.assertRaises(ValueError):
            DecisionTableCompiler(bad_rules)

    def test_evaluation_stop_matching(self):
        context = {"has_legal_representation": True, "status": "active"}
        proposals = self.compiler.evaluate(context)
        
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0].decision, PolicyDecisionType.STOP)
        self.assertEqual(proposals[0].reason_code, "LEGAL_REPRESENTATION")

    def test_evaluation_ambiguity_yields_hold(self):
        # Context that matches NO rules
        context = {"unknown_field": True}
        proposals = self.compiler.evaluate(context)
        
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0].decision, PolicyDecisionType.HOLD)
        self.assertEqual(proposals[0].reason_code, "AMBIGUOUS_EVIDENCE_NO_RULE_MATCH")

    def test_evaluation_multiple_matches(self):
        # Context matching both a STOP and a CONTACT
        context = {
            "has_legal_representation": True,
            "status": "delinquent"
        }
        proposals = self.compiler.evaluate(context)
        
        self.assertEqual(len(proposals), 2)
        decisions = [p.decision for p in proposals]
        self.assertIn(PolicyDecisionType.STOP, decisions)
        self.assertIn(PolicyDecisionType.CONTACT, decisions)
        # Note: Merging precedence is the job of the PolicyEngine (UMP-0101)

if __name__ == '__main__':
    unittest.main()
