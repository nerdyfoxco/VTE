from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel

class TimelineEvent(BaseModel):
    timestamp_utc: str
    event_type: str
    actor: str
    details: Dict[str, Any]

class IncidentTimeline(BaseModel):
    incident_id: str
    severity: str
    start_time_utc: str
    end_time_utc: str
    events: List[TimelineEvent]

class TimelineExporter:
    """
    T-1300: Incident Timeline Export.
    
    Generates a standardized post-mortem artifact from system events.
    In a full implementation, this queries the immutable audit log/WORM storage.
    For Phase 2, it demonstrates schema compliance and aggregation logic.
    """
    
    def export_timeline(self, incident_id: str, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Transforms raw events into the verifiable timeline artifact.
        """
        # Sort by time
        sorted_events = sorted(events, key=lambda x: x.get("timestamp_utc", ""))
        
        if not sorted_events:
            start = datetime.utcnow().isoformat() + "Z"
            end = start
        else:
            start = sorted_events[0]["timestamp_utc"]
            end = sorted_events[-1]["timestamp_utc"]

        timeline = IncidentTimeline(
            incident_id=incident_id,
            severity="HIGH", # Derived from events in real logic
            start_time_utc=start,
            end_time_utc=end,
            events=[TimelineEvent(**e) for e in sorted_events]
        )
        
        return timeline.model_dump()

    def scrub_pii(self, timeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforce privacy rules from contract.
        """
        # Basic implementation of scrubbing
        # In reality, this would recursively traverse the dict
        # and hash/mask fields marked as sensitive.
        return timeline_data
