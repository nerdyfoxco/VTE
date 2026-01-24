import json
import os
import sys

# Contract paths
ONTOLOGY_PATH = "contracts/ontology/vte_ontology_v1.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def validate_ontology():
    print("[INFO] Validating Ontology...")
    ontology = load_json(ONTOLOGY_PATH)
    
    types = ontology['types']
    relationships = ontology['relationships']
    
    print(f"[INFO] Found {len(types)} Types: {list(types.keys())}")
    
    # 1. Check Typos in Relationships
    for rel_name, rel_def in relationships.items():
        src = rel_def['source']
        tgt = rel_def['target']
        
        if src not in types:
            return False, f"Relationship {rel_name} references unknown source: {src}"
        if tgt not in types:
            return False, f"Relationship {rel_name} references unknown target: {tgt}"
            
    # 2. Check Cycles (Simple DFS)
    # Graph: Type -> [Target Types]
    adj = {t: [] for t in types}
    for rel_def in relationships.values():
        adj[rel_def['source']].append(rel_def['target'])
        
    visited = set()
    stack = set()
    
    def visit(node):
        visited.add(node)
        stack.add(node)
        
        for neighbor in adj[node]:
            if neighbor not in visited:
                if visit(neighbor):
                    return True
            elif neighbor in stack:
                return True # Cycle
        
        stack.remove(node)
        return False
        
    for t in types:
        if t not in visited:
            if visit(t):
                return False, f"Cycle detected involving type: {t}"

    return True, "Ontology Acyclic & Complete"

if __name__ == "__main__":
    valid, msg = validate_ontology()
    if not valid:
        print(f"[FAIL] {msg}")
        sys.exit(1)
    print(f"[SUCCESS] {msg}")
