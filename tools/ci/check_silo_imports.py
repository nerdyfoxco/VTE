import os
import re
import sys
from pathlib import Path

# Define silos and their forbidden dependencies
# Format: "Silo": ["Forbidden1", "Forbidden2"]
SILO_RULES = {
    "spine": ["web", "mobile"],
    "web": ["spine", "mobile"],  # Web should access spine via API, not code import
    "mobile": ["spine", "web"],  # Mobile should access spine via API, not code import
}

def check_imports(file_path, silo_name, forbidden_silos):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            return [] # Skip binary files

    errors = []
    for i, line in enumerate(lines):
        line = line.strip()
        # Regex to catch: import x, from x import y
        # Very basic, but sufficient for top-level package enforcement
        for forbidden in forbidden_silos:
            # Matches "import forbidden" or "import forbidden.foo"
            if re.match(r'^import\s+' + re.escape(forbidden) + r'(\.|\s|$)', line):
                errors.append(f"Line {i+1}: Forbidden import '{forbidden}' in {silo_name}")
            # Matches "from forbidden"
            if re.match(r'^from\s+' + re.escape(forbidden) + r'(\.|\s)', line):
                errors.append(f"Line {i+1}: Forbidden from-import '{forbidden}' in {silo_name}")
    return errors

def main():
    root_dir = Path(os.getcwd())
    if not (root_dir / "spine").exists():
        print("Error: Must run from monorepo root (C:\\Bintloop\\VTE)")
        sys.exit(1)

    fail = False
    for silo, forbidden in SILO_RULES.items():
        silo_path = root_dir / silo
        if not silo_path.exists():
            continue
        
        print(f"Scanning {silo} for forbidden imports: {forbidden}...")
        
        for root, dirs, files in os.walk(silo_path):
            for file in files:
                if file.endswith(".py") or file.endswith(".js") or file.endswith(".ts") or file.endswith(".dart"):
                    # Basic check for all text files, though syntax varies given language
                    # For JS/Dart, 'import' syntax is similar enough for 'import x' or 'import "package:x"'
                    # We might need language specific regex if false positives occur, but for now strict strictness.
                    
                    full_path = Path(root) / file
                    errors = check_imports(full_path, silo, forbidden)
                    if errors:
                        fail = True
                        for e in errors:
                            print(f"  [VIOLATION] {full_path}: {e}")

    if fail:
        print("\nFAILURE: Silo boundaries violated.")
        sys.exit(1)
    else:
        print("\nSUCCESS: No silo violations found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
