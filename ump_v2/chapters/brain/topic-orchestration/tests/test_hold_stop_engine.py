import sys
import unittest
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

policy_src = current_dir.parent.parent / "topic-policy-engine" / "src"
sys.path.insert(0, str(policy_src))

from hold_stop_engine import HoldStopEngine, ExecutionAction
from policy_engine import FinalDecision, PolicyDecisionType
from workflow_state_machine import WorkflowStateMachine, WorkItemState

class TestHoldStopEngine(unittest.TestCase):
    
    def setUp(self):
        # Fresh state machine starting perfectly fine on happy path
        self.state_machine = WorkflowStateMachine("DECISION")

    def test_stop_decision_terminates(self):
        decision = FinalDecision(
            decision=PolicyDecisionType.STOP,
            primary_reason="FRAUD_DETECTED",
            contributing_reasons=[]
        )
        action = HoldStopEngine.enforce(decision, self.state_machine)
        
        self.assertEqual(action, ExecutionAction.TERMINATE)
        self.assertEqual(self.state_machine.get_current(), WorkItemState.STOP)

    def test_hold_decision_suspends(self):
        decision = FinalDecision(
            decision=PolicyDecisionType.HOLD,
            primary_reason="AWAITING_DOCS",
            contributing_reasons=[]
        )
        action = HoldStopEngine.enforce(decision, self.state_machine)
        
        self.assertEqual(action, ExecutionAction.SUSPEND)
        self.assertEqual(self.state_machine.get_current(), WorkItemState.HOLD)
        
    def test_contact_decision_proceeds(self):
        decision = FinalDecision(
            decision=PolicyDecisionType.CONTACT,
            primary_reason="ALL_CLEAR",
            contributing_reasons=[]
        )
        # Should NOT mutate the state machine—leaves it where it was
        action = HoldStopEngine.enforce(decision, self.state_machine)
        
        self.assertEqual(action, ExecutionAction.PROCEED)
        self.assertEqual(self.state_machine.get_current(), WorkItemState.DECISION)

if __name__ == '__main__':
    unittest.main()
