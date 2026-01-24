import json
import subprocess
from datetime import datetime

# In a real implementation, this would call 'syft' or 'trivy' or 'pip freeze' + 'npm list'.
# For Phase 0.5, we output a valid dummy SPDX to verify the structure.

def generate_sbom():
    sbom = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "VTE-Spine-SBOM",
        "documentNamespace": "http://spdx.org/spdxdocs/vte-spine-1.0",
        "creationInfo": {
            "created": datetime.utcnow().isoformat() + "Z",
            "creators": ["Tool: vte-sbom-gen-0.1"]
        },
        "packages": [
            {
                "name": "fastapi",
                "version": "0.109.0",
                "SPDXID": "SPDXRef-Package-fastapi"
            },
            {
                "name": "sqlalchemy",
                "version": "2.0.25",
                "SPDXID": "SPDXRef-Package-sqlalchemy"
            }
        ]
    }
    return json.dumps(sbom, indent=2)

if __name__ == "__main__":
    print(generate_sbom())
