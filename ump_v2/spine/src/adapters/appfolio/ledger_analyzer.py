from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone

class LedgerEntry(BaseModel):
    id: str
    description: str
    amount: float
    date_posted: datetime
    balance_running: float
    category: Optional[str] = None

class LedgerAnalyzer:
    """
    VTE 2.0 (Kevin Closure) Adapter:
    Parses unstructured AppFolio ledger arrays into deterministic categories
    to power strict State Machine Engine policies.
    """
    
    WATER_KEYWORDS = ["utility", "water", "sewer", "trash"]
    LEGAL_KEYWORDS = ["legal", "eviction", "court", "attorney"]
    RENT_KEYWORDS = ["rent", "lease", "monthly"]

    def __init__(self, raw_ledger_data: List[dict]):
        self.raw_data = raw_ledger_data
        self.entries: List[LedgerEntry] = []
        self._parse()

    def _parse(self):
        """Maps unstructured dicts to strict Pydantic entries and categorizes."""
        for raw in self.raw_data:
            entry = LedgerEntry(**raw)
            desc_lower = entry.description.lower()
            
            if any(k in desc_lower for k in self.LEGAL_KEYWORDS):
                entry.category = "LEGAL"
            elif any(k in desc_lower for k in self.WATER_KEYWORDS):
                entry.category = "WATER"
            elif any(k in desc_lower for k in self.RENT_KEYWORDS):
                entry.category = "RENT"
            else:
                entry.category = "OTHER"
                
            self.entries.append(entry)

    def assess_hold_conditions(self) -> Dict[str, bool]:
        """
        Calculates deterministic "HOLD" variables for the VTE Brain.
        Example: If the ONLY remaining balance is Water < 5 days late, DO NOTCONTACT.
        """
        current_balance = sum(e.amount for e in self.entries)
        
        # Determine if the remaining balance strictly consists of recent utilities
        recent_utilities = [
            e for e in self.entries 
            if e.category == "WATER" and 
            (datetime.now(timezone.utc) - e.date_posted).days <= 5 and
            e.amount > 0 # Represents a charge
        ]
        
        total_recent_water = sum(u.amount for u in recent_utilities)
        
        # The core "Kevin" business logic check
        is_only_new_water = (total_recent_water >= current_balance) and (current_balance > 0)
        
        has_legal_action = any(e.category == "LEGAL" for e in self.entries)
        
        return {
            "is_only_new_water": is_only_new_water,
            "has_legal_action": has_legal_action,
            "balance_owed": current_balance
        }
