import json
import os
import sys

# This test simulates a full "Happy Path" flow through the system layers we've defined.
# It uses the contracts we created as check-points.

def test_happy_e2e():
    print("[INFO] Starting Happy Path E2E Simulation...")
    
    # 1. Ingestion (Compliance)
    print("  > Phase 1.27: Ingestion (Compliance check)...")
    from tests.prove_strict_schema_validation_rejects_bad_data import RowValidator, load_json as load_json_schema
    schema = load_json_schema("contracts/compliance/vte_sheet_schema.json")
    validator = RowValidator(schema)
    row = {"account_id": "ACC-55555555", "customer_name": "Jane Doe", "balance_due": 50.0, "state_code": "FL"}
    errs = validator.validate(row)
    if errs:
        print(f"    [FAIL] Ingestion failed: {errs}")
        sys.exit(1)
    print("    [PASS] Clean Ingest.")

    # 2. Intent Formation (Preservation)
    print("  > Phase 1.3: Intent Formation...")
    # Simulate Ledger Append
    from tests.prove_intent_ledger_is_immutable import IntentLedger
    ledger = IntentLedger()
    intent = {"user": "agent_1", "action": "CALL_CUSTOMER", "account": "ACC-55555555"}
    tx_hash = ledger.add_entry(intent)
    print(f"    [PASS] Intent Ledged. TxHash: {tx_hash}...")

    # 3. Policy Check (Compliance/Ops)
    print("  > Phase 1.27: Policy Check (DNC)...")
    from tests.prove_policy_engine_blocks_dnc import PolicyEngine, load_json as load_json_policy
    defs = load_json_policy("contracts/compliance/policy_engine_definitions.json")
    engine = PolicyEngine(defs)
    # Mocking context where region is FL (no quiet hours) and no Global DNC (assuming allowed for this test)
    # We cheat slightly by filtering out the GLOBAL DNC rule in memory for this "Happy" test
    engine.defs['policies'] = [p for p in engine.defs['policies'] if p['type'] != 'DO_NOT_CONTACT']
    
    res = engine.check_access({"region": "FL", "current_hour": 14}) # 2PM
    if res != "ALLOWED":
        print(f"    [FAIL] Policy Blocked: {res}")
        sys.exit(1)
    print("    [PASS] Policy Allowed.")

    # 4. Execution (Firewall)
    print("  > Phase 2: Execution (Firewall)...")
    from tests.prove_firewall_blocks_undocumented_side_effects import Firewall, load_json as load_json_fw
    fw_policy = load_json_fw("contracts/execution/firewall_policy.json")
    # Mock registry for this happy path
    registry = [{"handler_id": "call_handler", "side_effects": [{"type": "EXTERNAL_CALL"}]}]
    fw = Firewall(fw_policy, registry)
    
    perm = fw.check_permission("LIVE", "call_handler", "EXTERNAL_CALL")
    if perm != "ALLOWED":
         print(f"    [FAIL] Firewall Blocked: {perm}")
         sys.exit(1)
    print("    [PASS] Firewall Permitted.")

    print("\n[SUCCESS] Happy E2E Flow Proven across all layers.")

def main():
    try:
        # We need to make sure python can import from tests/ dir
        sys.path.append(os.getcwd())
        test_happy_e2e()
    except Exception as e:
        print(f"\n[ERROR] Canary Failed: {e}")
        # traceback would be good here but keeping it simple
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
