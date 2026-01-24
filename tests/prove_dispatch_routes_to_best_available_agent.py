import json
import os
import sys

# Contract paths
ASSIGNMENT_POLICY = "contracts/hitl/hitl_assignment_policy.json"

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r') as f:
        return json.load(f)

class Dispatcher:
    def __init__(self, policy):
        self.policy = policy
        
    def find_best_agent(self, task_skills, agents):
        candidates = []
        
        # 1. Filter by Skills & Capacity
        for agent in agents:
            # Check skills (simplified strict match)
            if not all(s in agent['skills'] for s in task_skills):
                continue
                
            # Check capacity
            if agent['active_items'] >= self.policy['constraints']['max_concurrent_items_per_agent']:
                continue
                
            candidates.append(agent)
            
        if not candidates:
            return None
            
        # 2. Sort by Strategy: Low Active Count, then Longest Idle (simplified)
        # We want FEWEST active items first.
        candidates.sort(key=lambda x: x['active_items'])
        
        return candidates[0]['id']

def test_dispatch_logic():
    print("[INFO] Loading Assignment Policy...")
    policy = load_json(ASSIGNMENT_POLICY)
    dispatcher = Dispatcher(policy)
    
    agents = [
        {"id": "A1", "skills": ["fraud"], "active_items": 5}, # Full
        {"id": "A2", "skills": ["fraud"], "active_items": 2}, # Best Match
        {"id": "A3", "skills": ["compliance"], "active_items": 0}, # Wrong Skill
        {"id": "A4", "skills": ["fraud"], "active_items": 4}  # Busy but available
    ]
    
    task_skills = ["fraud"]
    
    print(f"  > Dispatching task req: {task_skills}...")
    selected = dispatcher.find_best_agent(task_skills, agents)
    
    if selected != "A2":
        print(f"[FAIL] Expected A2 (Least Busy Qualified), got {selected}")
        sys.exit(1)
        
    print(f"  > Selected Agent: {selected}")
    print("[PASS] Dispatcher selected most qualified, least busy agent.")
    
    # Test Capacity Block
    print("  > Testing saturated capacity...")
    full_agents = [{"id": "F1", "skills": ["fraud"], "active_items": 5}]
    selected_full = dispatcher.find_best_agent(task_skills, full_agents)
    if selected_full is not None:
         print(f"[FAIL] Should have returned None for full capacity. Got {selected_full}")
         sys.exit(1)
    print("[PASS] Dispatcher respects max capacity.")

def main():
    try:
        test_dispatch_logic()
        print("\n[SUCCESS] Dispatch Logic Proven.")
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
