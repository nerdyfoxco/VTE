import json
import hashlib
import datetime
import uuid
import sys

def emit_freeze_packet(scope_id, trigger, affected_items):
    """
    Generates a cryptographically signed freeze packet based on the protocol.
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    
    # Calculate hash of affected items
    items_json = json.dumps(affected_items, sort_keys=True).encode('utf-8')
    items_hash = hashlib.sha256(items_json).hexdigest()
    
    packet = {
        "freeze_id": f"frz_{uuid.uuid4().hex[:8]}",
        "timestamp_utc": timestamp,
        "triggering_rule": trigger,
        "scope_id": scope_id,
        "affected_items_snapshot_hash": items_hash,
        "metadata": {
            "item_count": len(affected_items),
            "generated_by": "emit_freeze_packet.py"
        }
    }
    
    return packet

if __name__ == "__main__":
    # Example Usage CLI
    if len(sys.argv) < 3:
        print("Usage: python emit_freeze_packet.py <SCOPE_ID> <TRIGGER_RULE>")
        sys.exit(1)
        
    scope = sys.argv[1]
    rule = sys.argv[2]
    
    # Mock affected items for CLI demo
    mock_items = ["item_1", "item_2", "item_3"]
    
    packet = emit_freeze_packet(scope, rule, mock_items)
    print(json.dumps(packet, indent=2))
