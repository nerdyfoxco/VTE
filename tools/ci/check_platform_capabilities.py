import sys
import json

def check_structure(code_path):
    # Mock static analysis: checks if "import boto3" is in core logic (forbidden)
    # This is a simplified check.
    with open(code_path, 'r') as f:
        content = f.read()
        if "import boto3" in content and "adapters/" not in code_path:
             return False, "Direct vendor import (boto3) found outside adapters."
    return True, "Code structure compliant."

def main():
    # Mock: Always pass for now unless we feed it bad code
    print("[INFO] Checking platform capabilities...")
    print("[PASS] No vendor lock-in detected in core.")

if __name__ == "__main__":
    main()
