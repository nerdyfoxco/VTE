import sys
import os
import json

# Add project root to path
# Add project root to path (assuming script is in tests/)
sys.path.append(os.getcwd())

try:
    from tools.testing.fixture_sanitizer import sanitize_data
except ImportError:
    # Fallback if running from root
    sys.path.append(os.path.join(os.getcwd(), 'VTE'))
    from tools.testing.fixture_sanitizer import sanitize_data

def test_sanitization():
    print("[INFO] Starting Fixture Sanitization Verification...")

    original_fixture = {
        "user_id": "u_123",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "metadata": {
            "last_login": "2023-01-01",
            "phone": "555-0199"
        },
        "orders": [
            {"id": "o_1", "amount": 100},
            {"id": "o_2", "amount": 250, "note": "Gift for mom"} # 'note' is not explicitly PII but could be sensitive. Policy usually defines strict keys.
        ]
    }

    print("  > Sanitizing fixture...")
    sanitized = sanitize_data(original_fixture)
    print(f"    Result: {json.dumps(sanitized, indent=2)}")

    # Verification Logic
    failures = []
    
    # Check Redaction
    if sanitized["full_name"] != "[REDACTED]":
        failures.append("full_name was not redacted")
    if sanitized["email"] != "[REDACTED]":
        failures.append("email was not redacted")
    if sanitized["metadata"]["phone"] != "[REDACTED]":
        failures.append("nested phone was not redacted")

    # Check Preservation
    if sanitized["user_id"] != "u_123":
        failures.append("user_id was lost/changed")
    if sanitized["orders"][0]["amount"] != 100:
        failures.append("order amount was lost/changed")

    if failures:
        print(f"    [FAIL] Failures detected: {failures}")
        sys.exit(1)
    else:
        print("    [PASS] PII redacted, structural data preserved.")

    print("\n[SUCCESS] Fixture Sanitization Proven.")

if __name__ == "__main__":
    test_sanitization()
