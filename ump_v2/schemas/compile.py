import json
import os
from definitions.identity import SignUp, SignIn, MFAChallenge, MFAVerify

def compile_contracts():
    schema_dir = os.path.dirname(os.path.abspath(__file__))
    contracts_dir = os.path.join(schema_dir, "..", "contracts", "auth")
    os.makedirs(contracts_dir, exist_ok=True)
    
    contracts = {
        "signup_policy_v1.json": SignUp.model_json_schema(),
        "signin_policy_v1.json": SignIn.model_json_schema(),
        "mfa_challenge_v1.json": MFAChallenge.model_json_schema(),
        "mfa_verify_v1.json": MFAVerify.model_json_schema()
    }
    
    for filename, schema in contracts.items():
        filepath = os.path.join(contracts_dir, filename)
        with open(filepath, "w") as f:
            json.dump(schema, f, indent=2)
        print(f"Compiled Contract: {filepath}")

if __name__ == "__main__":
    compile_contracts()
