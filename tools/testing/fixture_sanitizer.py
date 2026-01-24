import json
import re

PII_KEYS = ["email", "phone", "ssn", "credit_card", "full_name"]

def sanitize_data(data):
    """
    Recursively traverse JSON-like data and redact PII.
    """
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if k in PII_KEYS:
                new_dict[k] = "[REDACTED]"
            else:
                new_dict[k] = sanitize_data(v)
        return new_dict
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    else:
        return data

def main():
    # Simple CLI for demonstration
    import sys
    if len(sys.argv) > 1:
        # In real usage, this would read a file
        print("Sanitizer CLI mode not fully implemented for this mock.")
    else:
        print("Usage: python fixture_sanitizer.py <input_file>")

if __name__ == "__main__":
    main()
