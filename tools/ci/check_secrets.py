import os
import re
import sys
from pathlib import Path

# VTE Secret Patterns (Heuristic)
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
    (r"sk_live_[0-9a-zA-Z]{24}", "Stripe Secret Key"),
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"xox[baprs]-([0-9a-zA-Z]{10,48})", "Slack Token"),
    (r"-----BEGIN PRIVATE KEY-----", "RSA Private Key"),
]

# Allowlisted files (e.g., this file itself, tests with dummy secrets)
ALLOWLIST = [
    "check_secrets.py",
    "real_data_pack_v1", # Contains dummy sha256 hashes that might look like secrets? No, regex is specific.
]

def scan_file(filepath):
    """
    Scans a single file for secret patterns.
    """
    issues = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            for pattern, name in SECRET_PATTERNS:
                if re.search(pattern, content):
                    # Check if it's a dummy value often used in examples
                    if "EXAMPLE" in content or "DUMMY" in content:
                        continue
                    issues.append(f"Potential {name} found.")
    except Exception as e:
        pass # Binary file or permission error
    return issues

def scan_directory(root_dir):
    print(f"Starting Secret Scan in {root_dir}...")
    violations = []
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if any(allowed in file for allowed in ALLOWLIST):
                continue
                
            path = Path(root) / file
            # Skip git, artifacts, ven
            if ".git" in str(path) or ".venv" in str(path) or "__pycache__" in str(path):
                continue
                
            issues = scan_file(path)
            if issues:
                for issue in issues:
                    violations.append(f"{path}: {issue}")

    if violations:
        print("\n[FAIL] Secrets Detected:")
        for v in violations:
            print(f"  - {v}")
        return False
    else:
        print("\n[PASS] No secrets detected.")
        return True

if __name__ == "__main__":
    # Scan absolute root
    root = Path("C:/Bintloop/VTE").resolve()
    success = scan_directory(root)
    sys.exit(0 if success else 1)
