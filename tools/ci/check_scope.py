import json
import os
import sys
import fnmatch

# Contract paths
PRODUCT_MAP_PATH = "contracts/product/product_boundary_map.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def check_scope(file_path):
    boundary_map = load_json(PRODUCT_MAP_PATH)
    boundaries = boundary_map['boundaries']
    
    # Simple check: does the file belong to ANY boundary?
    # Or more strictly: does it violate cross-boundary rules?
    # For this version, let's just trace which boundary it belongs to.
    
    matched_areas = []
    
    # Normalize path (simple)
    file_path = file_path.replace("\\", "/")
    
    for area, patterns in boundaries.items():
        for pattern in patterns:
            # Simple glob matching
            if fnmatch.fnmatch(file_path, pattern):
                matched_areas.append(area)
                break
                
    if not matched_areas:
        return "UNKNOWN_SCOPE"
        
    if len(matched_areas) > 1:
        return f"AMBIGUOUS_SCOPE: {matched_areas}"
        
    return matched_areas[0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_scope.py <FILE_PATH>")
        sys.exit(1)
        
    scope = check_scope(sys.argv[1])
    print(f"Scope: {scope}")
    
    if "AMBIGUOUS" in scope:
        sys.exit(1)
