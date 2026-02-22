from enum import Enum
import sys
from pathlib import Path

# Fix relative imports
current_dir = Path(__file__).resolve().parent
policy_src = current_dir.parent.parent / "topic-policy-engine" / "src"
sys.path.insert(0, str(policy_src))
sys.path.insert(0, str(current_dir))

from policy_engine import FinalDecision, PolicyDecisionType
from workflow_state_machine import WorkflowStateMachine, WorkItemState

class ExecutionAction(str, Enum):
    PROCEED = "PROCEED"
    SUSPEND = "SUSPEND"
    TERMINATE = "TERMINATE"

class HoldStopEngine:
    """
    Phase 2 Control Flow: Wrapper that transcribes PolicyEngine outcomes into 
    concrete WorkflowStateMachine transitions.
    """
    
    @staticmethod
    def enforce(decision: FinalDecision, state_machine: WorkflowStateMachine) -> ExecutionAction:
        """
        Interprets a FinalDecision and mutates the state machine if required.
        Returns the action the executor thread should take.
        """
        
        if decision.decision == PolicyDecisionType.STOP:
            # Fatal policy violation. Mutate state machine to STOP and kill execution thread.
            state_machine.transition(WorkItemState.STOP.value)
            return ExecutionAction.TERMINATE
            
        elif decision.decision == PolicyDecisionType.HOLD:
            # Suspended policy. Mutate state machine to HOLD and pause execution thread.
            state_machine.transition(WorkItemState.HOLD.value)
            return ExecutionAction.SUSPEND
            
        elif decision.decision == PolicyDecisionType.CONTACT:
            # Proceeding. State machine transitions proceed on the normal happy path elsewhere.
            return ExecutionAction.PROCEED
            
        # Deterministic fallback: ANY unknown decision type causes a SUSPEND.
        state_machine.transition(WorkItemState.HOLD.value)
        return ExecutionAction.SUSPEND
