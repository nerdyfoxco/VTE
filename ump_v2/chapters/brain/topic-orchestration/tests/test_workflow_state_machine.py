import sys
import unittest
from pathlib import Path

# The current dir is chapters/brain/topic-orchestration/tests
# The src dir is chapters/brain/topic-orchestration/src
current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"

sys.path.insert(0, str(src_dir))

from workflow_state_machine import WorkflowStateMachine, WorkItemState, WorkflowTransitionError

class TestWorkflowStateMachine(unittest.TestCase):
    def test_initialization_happy_path(self):
        sm = WorkflowStateMachine("INIT")
        self.assertEqual(sm.get_current(), WorkItemState.INIT)

    def test_initialization_unknown_state_bounds_to_hold(self):
        sm = WorkflowStateMachine("GIBBERISH_STATE")
        self.assertEqual(sm.get_current(), WorkItemState.HOLD)

    def test_happy_path_transition(self):
        sm = WorkflowStateMachine("INIT")
        sm.transition("IDENTITY_CHECK")
        self.assertEqual(sm.get_current(), WorkItemState.IDENTITY_CHECK)
        sm.transition("LEDGER_PARSE")
        self.assertEqual(sm.get_current(), WorkItemState.LEDGER_PARSE)

    def test_transition_to_unknown_state_bounds_to_hold(self):
        sm = WorkflowStateMachine("INIT")
        sm.transition("FAKE_STATE")
        self.assertEqual(sm.get_current(), WorkItemState.HOLD)

    def test_backwards_transition_fails(self):
        # We enforce deterministic forward motion on the happy path
        sm = WorkflowStateMachine("DECISION")
        with self.assertRaises(WorkflowTransitionError) as context:
             sm.transition("INIT")
        self.assertIn("Cannot move backwards", str(context.exception))

    def test_terminal_state_lock(self):
        sm = WorkflowStateMachine("STOP")
        with self.assertRaises(WorkflowTransitionError):
            sm.transition("INIT")
            
        sm2 = WorkflowStateMachine("COMPLETE")
        with self.assertRaises(WorkflowTransitionError):
            sm2.transition("HOLD")

    def test_escape_to_stop_or_hold(self):
        sm = WorkflowStateMachine("ELIGIBILITY")
        sm.transition("HOLD")
        self.assertEqual(sm.get_current(), WorkItemState.HOLD)
        
        sm.transition("STOP")
        self.assertEqual(sm.get_current(), WorkItemState.STOP)

if __name__ == '__main__':
    unittest.main()
