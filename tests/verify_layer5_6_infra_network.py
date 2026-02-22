import json
import os
import sys

def verify_infra_network():
    print("Verifying Layer 5 & 6: Infrastructure & Network...")
    
    # Paths
    tf_dir = os.path.join("infrastructure", "terraform")
    ecr_path = os.path.join(tf_dir, "ecr.tf")
    oidc_path = os.path.join(tf_dir, "oidc.tf")
    
    docker_path = "docker-compose.yml"
    egress_path = os.path.join("contracts", "network", "egress_policy_v1.json")
    routing_path = os.path.join("contracts", "routing", "department_routing_rules_v1.json")
    
    # 1. Verify Infrastructure (Layer 5)
    if not os.path.exists(ecr_path):
        print(f"FAIL: ECR Terraform config not found at {ecr_path}")
        sys.exit(1)
        
    if not os.path.exists(oidc_path):
        print(f"FAIL: OIDC Terraform config not found at {oidc_path}")
        sys.exit(1)
        
    if not os.path.exists(docker_path):
        print(f"FAIL: Docker Compose not found at {docker_path}")
        sys.exit(1)
        
    print("PASS: Infrastructure Layer (Physical) verified.")
    
    # 2. Verify Network & Edge (Layer 6)
    if not os.path.exists(egress_path):
        print(f"FAIL: Egress Policy not found at {egress_path}")
        sys.exit(1)
        
    try:
        with open(egress_path, 'r') as f:
            policy = json.load(f)
            print("PASS: Egress Policy is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Egress Policy invalid JSON: {e}")
        sys.exit(1)
        
    if not os.path.exists(routing_path):
        print(f"FAIL: Routing Rules not found at {routing_path}")
        sys.exit(1)

    try:
        with open(routing_path, 'r') as f:
            routing = json.load(f)
            print("PASS: Routing Rules valid JSON.")
    except json.JSONDecodeError as e:
        print(f"FAIL: Routing Rules invalid JSON: {e}")
        sys.exit(1)
        
    print("LAYER 5 & 6 VERIFIED.")

if __name__ == "__main__":
    verify_infra_network()
