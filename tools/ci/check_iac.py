import os
import sys

# Defines prohibited patterns in IaC/Container configs
PROHIBITED_PATTERNS = [
    # Docker
    (r"EXPOSE 22", "SSH Port Exposure"),
    (r"USER root", "Root User Execution"),
    (r":latest", "Unpinned Image Tag"),
    # Terraform (Stub regex)
    (r"ingress\s*{\s*from_port\s*=\s*0\s*to_port\s*=\s*65535", "Open Ingress"),
    (r"egress\s*{\s*cidr_blocks\s*=\s*\[\"0.0.0.0/0\"\]", "Unrestricted Egress") 
]

def check_iac(root_dir):
    print(f"Scanning IaC/Container configs in {root_dir}...")
    violations = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith("Dockerfile") or file.endswith(".tf"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        import re
                        for pattern, name in PROHIBITED_PATTERNS:
                            if re.search(pattern, content):
                                violations.append(f"{path}: {name}")
                except Exception:
                    pass

    if violations:
        print("\n[FAIL] IaC Policy Violations:")
        for v in violations:
            print(f"  - {v}")
        return False

    print("[PASS] IaC Compliant.")
    return True

if __name__ == "__main__":
    if check_iac("C:/Bintloop/VTE"):
        sys.exit(0)
    else:
        sys.exit(1)
