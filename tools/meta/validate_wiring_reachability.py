import json
import os
import sys

# Contract paths
REACHABILITY_INDEX = "contracts/meta/reachability_index_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def validate_wiring():
    print("[INFO] Validating Wiring Reachability...")
    index = load_json(REACHABILITY_INDEX)
    
    # Mocking a scan of the codebase to find "available handlers"
    # In reality, this would use AST parsing or reflection.
    available_handlers = {
        "vte.delinquency.handler.submit",
        "vte.delinquency.consumer.process",
        "vte.unused.handler" # Orphan!
    }
    
    print(f"[INFO] Scanned {len(available_handlers)} implementation handlers.")
    
    bound_handlers = set()
    ports_without_handlers = []
    
    # 1. Check Forward Binding (Port -> Handler)
    for port in index['ports']:
        ref = port['handler_ref']
        if ref not in available_handlers:
            ports_without_handlers.append(port['port_id'])
            print(f"[ERROR] Port {port['port_id']} binds to missing handler: {ref}")
        else:
            bound_handlers.add(ref)
            
    if ports_without_handlers:
        return False, f"Broken Bindings: {ports_without_handlers}"
        
    # 2. Check Reachability (Handler <- Port) detection of Orphans
    # The rule 'no_orphan_handlers' says we should warn or error if a handler is unused.
    orphans = available_handlers - bound_handlers
    if orphans:
        print(f"[WARN] Detected Orphan Handlers (Unreachable): {orphans}")
        # Depending on strictness, we might fail here.
        # Let's say we enforce strictness for this tool
        if index['wiring_rules'].get("no_orphan_handlers"):
             return False, f"Orphan Handlers Detected: {orphans}"

    return True, "Wiring Clean"

if __name__ == "__main__":
    valid, msg = validate_wiring()
    if not valid:
        print(f"[FAIL] {msg}")
        sys.exit(1)
    print(f"[SUCCESS] {msg}")
