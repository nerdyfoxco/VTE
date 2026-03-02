import json
import logging
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from vte.orm import DecisionObject, PermitToken, Property, Unit
from vte.core.integrity_verifier import IntegrityVerifier
from vte.core.permits import PermitIssuer
from vte.api.schema import OutcomeEnum

logger = logging.getLogger("vte.core.engine")

CONTRACTS_DIR = Path("C:/Bintloop/VTE/contracts/features")

class WorkflowEngine:
    def __init__(self, db: Session):
        self.db = db
        self.verifier = IntegrityVerifier()
        self.permit_issuer = PermitIssuer(db)
        self.contracts = self._load_contracts()

    def _load_contracts(self) -> Dict[str, Any]:
        """
        Loads all feature contracts into memory.
        """
        contracts = {}
        # Recursive glob or specific bundle list
        # MVP: Load vte_inventory_v1 explicitly or via glob
        for schema_path in CONTRACTS_DIR.glob("*/*.json"):
            if "scope_contract" in schema_path.name:
                try:
                    with open(schema_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        feature_id = data.get("feature_id")
                        if feature_id:
                            contracts[feature_id] = data
                            logger.info(f"Loaded Contract: {feature_id}")
                except Exception as e:
                    logger.error(f"Failed to load contract {schema_path}: {e}")
        return contracts

    def find_contract_for_trigger(self, trigger: str) -> Optional[Dict[str, Any]]:
        """
        Finds the contract that handles this trigger.
        """
        for contract in self.contracts.values():
            for transition in contract.get("transitions", []):
                if transition.get("trigger") == trigger:
                    return contract
        return None

    def execute_decision(self, decision_id: uuid.UUID) -> Dict[str, Any]:
        """
        Main Enty Point:
        1. Verify Integrity.
        2. Identify Contract.
        3. Validate State Transition.
        4. Issue Permit.
        5. Execute Side Effects.
        """
        decision = self.db.query(DecisionObject).filter(DecisionObject.decision_id == decision_id).first()
        if not decision:
            raise ValueError(f"Decision {decision_id} not found")

        # 0. Idempotency Guard (VTE PRD Compliance)
        # Prevent double-fire execution (e.g., sending two eviction notices concurrently).
        # We enforce this by checking if a permit was already issued for this exact UUID.
        existing_permit = self.db.query(PermitToken).filter(PermitToken.decision_id == decision_id).first()
        if existing_permit:
            logger.info(f"[IDEMPOTENCY LOCK] Decision {decision_id} already executed. Returning cached success.")
            return {"status": "skipped", "reason": "idempotent_duplicate_catch", "permit_id": str(existing_permit.token_id)}

        # 1. Integrity Check (Kernel)
        # We assume Evidence was verified at ingestion, but we verify Decision Integrity here
        try:
            self.verifier.verify_decision_integrity(decision)
        except Exception as e:
            logger.error(f"[INTEGRITY FAULT] Decision {decision_id} failed cryptographic verification: {e}")
            raise

        # 2. Identify Contract
        action = decision.intent_action
        contract = self.find_contract_for_trigger(action)
        if not contract:
            logger.warning(f"No contract found for action {action}. execution skipped (or legacy fallback).")
            return {"status": "skipped", "reason": "no_contract"}

        # 3. Validate Transition (State Machine)
        transition = self._validate_transition(decision, contract)
        
        # 4. Issue Permit (Kernel)
        permit = self.permit_issuer.issue_permit(decision)
        
        # 5. Execute Side Effects
        result = self._execute_side_effects(decision, transition, contract)
        
        return {"status": "success", "permit_id": str(permit.token_id), "side_effects": result}

    def _validate_transition(self, decision: DecisionObject, contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks if the transition is allowed given the current state of the target entity.
        Returns the transition definition.
        """
        action = decision.intent_action
        target_id = decision.intent_target
        
        # Find transition definition
        transition_def = None
        for t in contract["transitions"]:
            if t["trigger"] == action:
                transition_def = t
                break
        
        if not transition_def:
            raise ValueError(f"Action {action} is not a valid transition in {contract['feature_id']}")

        # Resolve Current State of Target
        current_state = self._get_current_state(target_id, transition_def["target_type"])
        
        # Check 'from' state
        allowed_from = transition_def["from"]
        if allowed_from != "*" and current_state != allowed_from:
             raise ValueError(f"Invalid Transition. Current State: {current_state}, Action requires: {allowed_from}")
             
        # Check Logic/Invariants (Stub)
        
        return transition_def

    def _get_current_state(self, target_id: str, target_type: str) -> str:
        """
        Resolves current state from DB based on type.
        """
        if not target_id: 
            return "VOID" # or PROPOSED?
            
        if target_type == "property":
            # For REGISTER, target might not exist yet.
            try:
                # Ensure UUID compatibility
                pid = uuid.UUID(target_id)
                prop = self.db.query(Property).filter(Property.property_id == pid).first()
            except ValueError:
                return "VOID" # Invalid UUID
                
            return "ACTIVE" if prop else "VOID"

        elif target_type == "unit":
            try:
                # Ensure UUID compatibility
                uid = uuid.UUID(target_id)
                unit = self.db.query(Unit).filter(Unit.unit_id == uid).first()
            except ValueError:
                return "VOID"
                
            return unit.status if unit else "VOID"
            
        return "UNKNOWN"

    def _execute_side_effects(self, decision: DecisionObject, transition: Dict[str, Any], contract: Dict[str, Any]) -> List[str]:
        """
        Executes the side effects defined in the contract.
        """
        results = []
        action = decision.intent_action
        defined_effects = contract.get("side_effects", {}).get(action, [])
        
        for effect in defined_effects:
            logger.info(f"Executing Side Effect: {effect}")
            
            if effect == "db_projection_property":
                 self._project_property(decision)
                 results.append("db_projection_property")
            elif effect == "db_projection_unit":
                 self._project_unit(decision)
                 results.append("db_projection_unit")
            elif effect == "db_projection_unit_status":
                 self._project_unit_status(decision, transition["to"])
                 results.append("db_projection_unit_status")
            elif effect == "appfolio_sync":
                 self._execute_appfolio_sync(decision)
                 results.append("appfolio_sync")
            elif effect == "db_update_tenant_info":
                 self._project_unit_tenant_info(decision)
                 results.append("db_update_tenant_info")
            elif effect == "email_notification_welcome":
                 pass
            else:
                logger.warning(f"Unknown side effect: {effect}")
                
        return results

    def _execute_appfolio_sync(self, decision: DecisionObject):
        """
        Executes 'write_note' or other AppFolio actions.
        """
        from vte.adapters.appfolio.client import AppFolioClient
        
        action = decision.intent_action
        target = decision.intent_target
        params = decision.intent_params or {}
        
        # We map generic intent to AppFolio actions
        # In this specific case, the 'action' might be 'WRITE_NOTE' if the contract says so,
        # or the contract says trigger 'WRITE_NOTE' -> side_effect 'appfolio_sync'.
        # The Decision Intent matches the Trigger.
        
        # Legacy/Contract Mapping:
        # If action is WRITE_NOTE (from contract) or write_note (legacy)
        
        logger.info("Executing AppFolio Sync...")
        client = AppFolioClient() 
        try:
            client.start()
            if not client.navigate_to_tenant(target):
                 logger.error("AppFolio Navigation Failed")
                 return
            
            # Helper to determine content based on action
            content = params.get("content", "")
            if action == "REGISTER_UNIT": # Example: Create Unit in AppFolio?
                # Stub
                pass
            elif action == "WRITE_NOTE" or action == "write_note":
                if client.write_note(content, dry_run=params.get("dry_run", False)):
                    logger.info(f"AppFolio Note Written: {content}")
                else:
                    logger.error("AppFolio Write Failed")
            
        except Exception as e:
            logger.error(f"AppFolio Error: {e}")
        finally:
            client.close()

    # --- Projections (Moved from Tasks.py) ---
    def _project_property(self, decision: DecisionObject):
        # ... logic from handle_inventory_projection ...
        import uuid
        params = decision.intent_params or {}
        prop = Property(
            property_id=uuid.UUID(decision.intent_target) if decision.intent_target else uuid.uuid4(),
            name=params.get("name"),
            address=params.get("address"),
            external_ref_id=params.get("external_ref_id"),
            created_at_decision_hash=decision.decision_hash,
            updated_at_decision_hash=decision.decision_hash
        )
        self.db.add(prop)
        self.db.commit()

    def _project_unit(self, decision: DecisionObject):
        import uuid
        params = decision.intent_params or {}
        unit = Unit(
            unit_id=uuid.UUID(decision.intent_target) if decision.intent_target else uuid.uuid4(),
            property_id=uuid.UUID(params.get("property_id")),
            name=params.get("name"),
            status=params.get("status", "VACANT"),
            created_at_decision_hash=decision.decision_hash,
            updated_at_decision_hash=decision.decision_hash
        )
        self.db.add(unit)
        self.db.commit()

    def _project_unit_status(self, decision: DecisionObject, new_status: str):
        import uuid
        try:
             unit_id = uuid.UUID(decision.intent_target)
             unit = self.db.query(Unit).filter(Unit.unit_id == unit_id).first()
             if unit:
                unit.status = new_status
                unit.updated_at_decision_hash = decision.decision_hash
                self.db.add(unit)
                self.db.commit()
        except ValueError:
             logger.error(f"Invalid UUID for unit target: {decision.intent_target}")

    def _project_unit_tenant_info(self, decision: DecisionObject):
        import uuid
        try:
             unit_id = uuid.UUID(decision.intent_target)
             unit = self.db.query(Unit).filter(Unit.unit_id == unit_id).first()
             if unit:
                params = decision.intent_params or {}
                # Update status if needed, but primary is tenant_info
                # Logic: Update tenant info blobs
                # Assume params has tenant details
                current_info = unit.tenant_info or {}
                # Merge?
                current_info.update(params)
                unit.tenant_info = current_info
                
                # Also implied OCCUPIED? Or separate transition?
                # Contract says transition to OCCUPIED. 
                # If transition handled status, this handles data.
                
                unit.updated_at_decision_hash = decision.decision_hash
                self.db.add(unit)
                self.db.commit()
        except ValueError:
             logger.error(f"Invalid UUID for unit target: {decision.intent_target}")
