import json
import hashlib
import time
import subprocess
import sys
import os

# VTE Release Dossier Emitter
# Aggregates results from all safety checks into a single signed artifact.

VERSION = "0.99.1-RC1"
OUTPUT_FILE = "vte_release_dossier.json"

def run_check(name, command):
    print(f"Running Control: {name}...")
    start = time.time()
    try:
        # Running in shell for demo purposes; real system would use import
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        duration = time.time() - start
        
        status = "PASS" if result.returncode == 0 else "FAIL"
        print(f"  Result: {status} ({duration:.2f}s)")
        return {
            "control": name,
            "status": status,
            "output_snippet": result.stdout[:200] if status == "FAIL" else "OK",
            "timestamp": time.time()
        }
    except Exception as e:
        return {"control": name, "status": "ERROR", "error": str(e)}

def emit_dossier():
    print(f"Generating VTE Release Dossier v{VERSION}...")
    
    checks = [
        ("Secret Scan", "python tools/ci/check_secrets.py"),
        ("Enforcement Index", "python tools/ci/check_contract_enforcement_index_complete.py"),
        ("Chaos Game", "python tests/chaos/chaos_game_simulation.py"),
        ("Tenant Canary", "python tests/prove_cross_tenant_read_write_denied.py"),
        ("State Canary", "python tests/prove_no_unregistered_transition_possible.py")
    ]
    
    results = []
    all_pass = True
    
    for name, cmd in checks:
        # Adjust path for execution context
        cmd = cmd.replace("tools/", "C:/Bintloop/VTE/tools/")
        cmd = cmd.replace("tests/", "C:/Bintloop/VTE/tests/")
        
        res = run_check(name, cmd)
        results.append(res)
        if res["status"] != "PASS":
            all_pass = False

    dossier = {
        "meta": {
            "version": VERSION,
            "generated_at": time.time(),
            "environment": "BUILD_AGENT"
        },
        "verdict": "GO" if all_pass else "NO_GO",
        "evidence": results
    }
    
    # Sign (Stub)
    payload_str = json.dumps(dossier, sort_keys=True)
    dossier["signature"] = hashlib.sha256(payload_str.encode()).hexdigest()
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(dossier, f, indent=2)
        
    print(f"\n[Release Verdict]: {dossier['verdict']}")
    print(f"Dossier emitted to {OUTPUT_FILE}")
    
    return all_pass

if __name__ == "__main__":
    if emit_dossier():
        sys.exit(0)
    else:
        sys.exit(1)
