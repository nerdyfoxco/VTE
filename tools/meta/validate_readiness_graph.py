import json
import os
import sys

# Contract paths
SCHEMA_PATH = "contracts/meta/readiness_graph_schema.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def validate_graph(graph_path):
    print(f"[INFO] Validating Graph: {graph_path}")
    graph = load_json(graph_path)
    schema = load_json(SCHEMA_PATH)
    
    node_ids = set()
    
    # 1. Validate Nodes
    for node in graph['nodes']:
        node_id = node['id']
        node_type = node['type']
        
        if node_id in node_ids:
            return False, f"Duplicate Node ID: {node_id}"
        node_ids.add(node_id)
        
        if node_type not in schema['node_types']:
            return False, f"Unknown Node Type: {node_type}"
            
        # Check required metadata
        required_meta = schema['node_types'][node_type]['required_metadata']
        for field in required_meta:
            if field not in node['metadata']:
                return False, f"Node {node_id} missing metadata '{field}'"

    # 2. Validate Edges
    for edge in graph['edges']:
        src = edge['source']
        tgt = edge['target']
        edge_type = edge['type']
        
        if src not in node_ids:
             return False, f"Edge source not found: {src}"
        if tgt not in node_ids:
             return False, f"Edge target not found: {tgt}"
             
        if edge_type not in schema['edge_types']:
             return False, f"Unknown Edge Type: {edge_type}"
             
    return True, "Valid"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_readiness_graph.py <GRAPH_PATH>")
        sys.exit(1)
        
    path = sys.argv[1]
    valid, msg = validate_graph(path)
    if not valid:
        print(f"[FAIL] {msg}")
        sys.exit(1)
    else:
        print("[SUCCESS] Graph is valid.")
