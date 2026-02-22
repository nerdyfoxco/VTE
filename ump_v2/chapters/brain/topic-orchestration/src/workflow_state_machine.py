from enum import Enum
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class WorkItemState(str, Enum):
    INIT = "INIT"
    IDENTITY_CHECK = "IDENTITY_CHECK"
    LEDGER_PARSE = "LEDGER_PARSE"
    ELIGIBILITY = "ELIGIBILITY"
    DECISION = "DECISION"
    HOLD = "HOLD"
    STOP = "STOP"
    APPROVED = "APPROVED"
    MESSAGE_PREVIEW = "MESSAGE_PREVIEW"
    EXECUTION = "EXECUTION"
    COMPLETE = "COMPLETE"

class WorkflowTransitionError(Exception):
    pass

class WorkflowStateMachine:
    """
    Phase 2 Control Flow: Determines the linear progression of a Work Item.
    Unknown state maps to HOLD. Terminal states are STOP and COMPLETE.
    """
    
    # The deterministic happy path. Any divergence is managed by HOLD/STOP.
    HAPPY_PATH_SEQUENCE = [
        WorkItemState.INIT,
        WorkItemState.IDENTITY_CHECK,
        WorkItemState.LEDGER_PARSE,
        WorkItemState.ELIGIBILITY,
        WorkItemState.DECISION,
        WorkItemState.APPROVED,
        WorkItemState.MESSAGE_PREVIEW,
        WorkItemState.EXECUTION,
        WorkItemState.COMPLETE
    ]
    
    TERMINAL_STATES = {WorkItemState.STOP, WorkItemState.COMPLETE}
    PAUSED_STATES = {WorkItemState.HOLD}
    
    def __init__(self, current_state: str):
        try:
            self.current_state = WorkItemState(current_state)
        except ValueError:
            # Rule: Unknown state -> HOLD
            logger.warning(f"Unknown state '{current_state}' encountered. Bounding to HOLD.")
            self.current_state = WorkItemState.HOLD

    def get_current(self) -> WorkItemState:
        return self.current_state
            
    def transition(self, target_state: str) -> None:
        """
        Attempts to move the workflow to the target state.
        Enforces execution invariants (e.g., cannot leave a terminal state).
        """
        try:
            target = WorkItemState(target_state)
        except ValueError:
            logger.warning(f"Attempted transition to unknown state '{target_state}'. Bounding to HOLD.")
            self.current_state = WorkItemState.HOLD
            return
            
        if self.current_state in self.TERMINAL_STATES:
            raise WorkflowTransitionError(f"Cannot transition out of terminal state: {self.current_state}")
            
        # Exception to sequence: We can ALWAYS move to STOP or HOLD from any non-terminal state
        if target in (WorkItemState.STOP, WorkItemState.HOLD):
            self.current_state = target
            return
            
        # For sequence progression, ensure it's a valid forward move
        if self.current_state not in self.PAUSED_STATES:
            try:
                curr_idx = self.HAPPY_PATH_SEQUENCE.index(self.current_state)
                target_idx = self.HAPPY_PATH_SEQUENCE.index(target)
                if target_idx <= curr_idx:
                    raise WorkflowTransitionError(f"Cannot move backwards in happy path: {self.current_state} -> {target}")
            except ValueError:
                # If either state isn't in happy path (which shouldn't happen given the above checks), default to HOLD
                self.current_state = WorkItemState.HOLD
                return
                
        # If all checks pass, transition
        self.current_state = target
