import json
import os
import sys

# Contract paths
GRAPH_PATH = "contracts/meta/readiness_graph_v1.json"
LIFECYCLE_POLICY = "contracts/meta/contract_lifecycle_policy.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def emit_index():
    print(f"[INFO] generating enforcement index from {GRAPH_PATH}...")
    graph = load_json(GRAPH_PATH)
    lifecycle = load_json(LIFECYCLE_POLICY)
    
    index = {
        "enforcement_map": {}, # path -> enforcement_action
        "dependency_map": {}   # id -> [dependency_ids]
    }
    
    # 1. Build Dependency Map
    for edge in graph['edges']:
        src = edge['source']
        tgt = edge['target']
        if src not in index['dependency_map']:
            index['dependency_map'][src] = []
        index['dependency_map'][src].append(tgt)
        
    # 2. Build Enforcement Map
    enforcement_rules = lifecycle['enforcement']
    
    for node in graph['nodes']:
        if node['type'] == 'CONTRACT':
            path = node['metadata'].get('path')
            status = node['metadata'].get('status')
            
            if path and status:
                action = enforcement_rules.get(status, "UNKNOWN_ACTION")
                index['enforcement_map'][path] = action
                
    return index

if __name__ == "__main__":
    idx = emit_index()
    print(json.dumps(idx, indent=2))
