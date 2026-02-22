from typing import List

class TagScanner:
    """
    VTE 2.0 (Kevin Closure) Adapter:
    Scans AppFolio tenant profiles for strict control tags.
    Ensures 'Fail-Closed' behavior if Do-Not-Contact tags exist.
    """
    
    DNC_TAGS = ["dnc", "do not contact", "attorney representation", "bankruptcy"]
    JBA_TAGS = ["jba", "city of seattle", "jba restrictions"]

    def __init__(self, tenant_tags: List[str]):
        self.tags = [tag.lower().strip() for tag in tenant_tags]

    def has_dnc(self) -> bool:
        """Returns True if any DNC tags are present."""
        return any(any(dnc in tag for dnc in self.DNC_TAGS) for tag in self.tags)
        
    def has_jurisdiction_restrictions(self) -> bool:
        """Returns True if jurisdiction imposes unique contact limits (JBA)."""
        return any(any(jba in tag for jba in self.JBA_TAGS) for tag in self.tags)
        
    def extract_context(self) -> dict:
        """Generates the determinisitic tag context for the PolicyEngine."""
        return {
            "dnc_active": self.has_dnc(),
            "jba_active": self.has_jurisdiction_restrictions(),
            "raw_tags_count": len(self.tags)
        }
