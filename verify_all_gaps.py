import subprocess
import os
import sys

# List of Verification Scripts corresponding to Gaps
SCRIPTS = [
    { "gap": "21", "name": "OIDC Discovery", "script": "verify_oidc.py" },
    { "gap": "34", "name": "Auth Wiring", "script": "verify_auth.py" },
    { "gap": "35a", "name": "Pagination", "script": "verify_pagination.py" },
    { "gap": "35b", "name": "Sorting", "script": "verify_sorting.py" },
    { "gap": "36", "name": "Filtering", "script": "verify_filtering.py" },
    { "gap": "37", "name": "Search", "script": "verify_search.py" },
    { "gap": "38", "name": "Empty States", "script": "verify_empty_state_playwright.py" },
    { "gap": "39", "name": "Loading States", "script": "verify_loading.py" },
    { "gap": "40", "name": "Error States", "script": "verify_error_state.py" },
    { "gap": "41", "name": "Breadcrumbs", "script": "verify_breadcrumbs.py" },
    { "gap": "42", "name": "Mobile Layout", "script": "verify_mobile.py" }
]

def run_script(script_info):
    name = script_info["name"]
    script = script_info["script"]
    print(f"--------------------------------------------------")
    print(f"Running Gap {script_info['gap']}: {name} ({script})...")
    
    try:
        # Run script and capture output
        # We assume scripts rely on printed stdout for SUCCESS/FAILURE or exit code.
        # Most of my scripts print "SUCCESS" or "FAILURE".
        result = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=60)
        
        output = result.stdout
        error = result.stderr
        
        if result.returncode == 0 and "SUCCESS" in output:
             print(f"[PASS] {name}")
             # Extract screenshot path if mentioned? 
             # For now, just trust the script saved it.
             return True, output
        else:
             print(f"[FAIL] {name}")
             print("OUTPUT:", output)
             print("ERROR:", error)
             return False, output + "\n" + error
             
    except subprocess.TimeoutExpired:
        print(f"[FAIL] {name} (Timeout)")
        return False, "Timeout"
    except Exception as e:
        print(f"[FAIL] {name} (Exception: {e})")
        return False, str(e)

def main():
    print("Starting VTE Phase 4 Full Regression Suite...")
    print(f"Total Tests: {len(SCRIPTS)}")
    
    results = []
    failed_count = 0
    
    for item in SCRIPTS:
        success, logs = run_script(item)
        results.append({ "item": item, "success": success, "logs": logs })
        if not success:
            failed_count += 1
            
    print("\n==================================================")
    print("REGRESSION SUMMARY")
    print("==================================================")
    for res in results:
        status = "PASS" if res["success"] else "FAIL"
        print(f"Gap {res['item']['gap']}: {res['item']['name']} -> {status}")
        
    if failed_count == 0:
        print("\nALL SYSTEM TESTS PASSED.")
        sys.exit(0)
    else:
        print(f"\n{failed_count} TESTS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
