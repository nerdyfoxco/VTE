import json
import datetime
import sys
import uuid

# Mock Event Data Source
MOCK_EVENTS = [
    {"timestamp": "2023-10-27T10:00:00Z", "type": "ALERT_FIRED", "data": {"alert_name": "HighLatency"}},
    {"timestamp": "2023-10-27T10:05:00Z", "type": "PAGE_ACKNOWLEDGED", "data": {"user": "sre_oncall"}},
    {"timestamp": "2023-10-27T10:10:00Z", "type": "MITIGATION_ACTION", "data": {"action": "Rollback", "component": "API"}}
]

def emit_timeline(incident_id):
    # In a real tool, this would query PagerDuty, Slack, datadog, etc.
    # Here we construct a valid timeline based on the contract.
    
    timeline = {
        "incident_id": incident_id,
        "severity": "SEV-1",
        "start_time_utc": "2023-10-27T10:00:00Z",
        "end_time_utc": "2023-10-27T10:30:00Z",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "events": MOCK_EVENTS
    }
    
    # Simulate partial PII scrubbing (mock)
    # The tool is responsible for ensuring the output is clean.
    
    return timeline

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default for demo
        inc_id = f"inc_{uuid.uuid4().hex[:6]}"
    else:
        inc_id = sys.argv[1]
        
    timeline = emit_timeline(inc_id)
    print(json.dumps(timeline, indent=2))
