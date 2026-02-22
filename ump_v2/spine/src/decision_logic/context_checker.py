from typing import List

class ContextChecker:
    """
    VTE 2.0 (Kevin Closure) Engine Plugin:
    Analyzes unstructured text (e.g., AppFolio Ledger Notes or maintenance requests)
    to detect highly sensitive human states that require a mandatory HOLD.
    """
    
    DEATH_KEYWORDS = ["passed away", "deceased", "died", "funeral", "estate of"]
    SICKNESS_KEYWORDS = ["hospital", "surgery", "cancer", "icu", "medical emergency"]
    
    @classmethod
    def analyze_notes(cls, notes: List[str]) -> dict:
        """
        Scans a list of text notes and returns boolean flags for the state machine.
        Returns True if ANY note triggers a keyword.
        """
        has_death_context = False
        has_sickness_context = False
        
        for note in notes:
            note_lower = note.lower()
            if any(k in note_lower for k in cls.DEATH_KEYWORDS):
                has_death_context = True
            
            if any(k in note_lower for k in cls.SICKNESS_KEYWORDS):
                has_sickness_context = True
                
        return {
            "death_context_detected": has_death_context,
            "sickness_context_detected": has_sickness_context
        }
