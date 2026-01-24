from datetime import datetime
from typing import Dict, Any, List

class StateMachineEngine:
    def __init__(self, schema: Dict[str, Any]):
        self.states = set(schema["states"])
        self.transitions = schema["transitions"]
        self.side_effects = schema.get("side_effects", {})
        
    def validate_transition(self, current_state: str, trigger: str) -> str:
        """
        Determines the next state based on current state and trigger.
        Returns next_state if valid, else raises InvalidTransitionError.
        """
        for t in self.transitions:
            if t["from"] == current_state and t["trigger"] == trigger:
                return t["to"]
        
        raise ValueError(f"Invalid transition from {current_state} via {trigger}")

    def get_side_effects(self, next_state: str) -> List[str]:
        """Returns the list of side-effect keys to execute upon entering next_state."""
        return self.side_effects.get(next_state, [])

# Stub for Phase 0.97 verification
if __name__ == "__main__":
    schema = {
        "states": ["A", "B"],
        "transitions": [{"from": "A", "to": "B", "trigger": "go"}],
        "side_effects": {"B": ["send_email"]}
    }
    engine = StateMachineEngine(schema)
    next_s = engine.validate_transition("A", "go")
    print(f"Transition A -> {next_s} OK. Side-effects: {engine.get_side_effects(next_s)}")
