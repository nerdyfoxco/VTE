import logging
import re
import uuid
from vte.adapters.gmail.poller import GmailPoller
from vte.orm import DecisionObject, Unit
from vte.api.schema import DecisionDraft, RoleEnum, OutcomeEnum
from sqlalchemy.orm import Session
from datetime import datetime

logger = logging.getLogger("vte.agent.ingestion")

class IngestionAgent:
    """
    Intelligent Agent that converts Raw Events (Emails) into Structured Decisions.
    """
    def __init__(self, db: Session):
        self.db = db
        self.poller = GmailPoller()

    def run_cycle(self):
        """
        1. Poll
        2. Analyze
        3. Draft Decision
        4. (Auto) Approve
        """
        logger.info("Starting Ingestion Cycle...")
        emails = self.poller.poll_leases()
        
        for email in emails:
            decision_draft = self.analyze_email(email)
            if decision_draft:
                self.submit_decision(decision_draft, email.get("source_id"))

    def analyze_email(self, email: dict) -> dict:
        """
        Heuristic Analysis of Email.
        Returns a Decision Payload or None.
        """
        subject = email.get("subject", "")
        snippet = email.get("snippet", "")
        content = f"{subject} {snippet}"
        
        # Heuristic 1: "New Lease for Unit X"
        # Regex to find "Unit <Number>"
        unit_match = re.search(r"Unit\s+(\d+|[A-Z])", content, re.IGNORECASE)
        
        if "Lease" in subject and unit_match:
            unit_name = unit_match.group(1)
            # Find tenant name (naive: assume generic or extract from 'from')
            tenant_name = email.get("sender", "Unknown Tenant")
            
            logger.info(f"MATCH: Found Lease for Unit {unit_name} from {tenant_name}")
            
            return {
                "intent_action": "UPDATE_UNIT_TENANT",
                "unit_name": unit_name, # We need to resolve this to UUID later
                "tenant_name": tenant_name,
                "evidence_summary": f"Email from {tenant_name}: {subject}"
            }
            
        return None

    def submit_decision(self, analysis: dict, source_id: str):
        """
        Persist the decision to the Ledger.
        """
        raw_name = analysis["unit_name"]
        
        # 1. Resolve Unit Name to UUID
        # Try exact match first, then "Unit " + name
        unit = self.db.query(Unit).filter(Unit.name == raw_name).first()
        if not unit:
            unit = self.db.query(Unit).filter(Unit.name == f"Unit {raw_name}").first()
            
        if not unit:
            print(f"DEBUG: Unit resolution failed for '{raw_name}'. Tried 'Unit {raw_name}' too.")
            logger.warning(f"Skipping: Unit '{raw_name}' not found in DB.")
            return

        if not unit:
            logger.warning(f"Skipping: Unit '{raw_name}' not found in DB.")
            return

        # 2. Persist Evidence (Email)
        # We must create an EvidenceBundle so the Decision can link to it.
        from vte.orm import EvidenceBundle
        evidence_hash = f"email_{source_id}"
        
        # Check if exists (Idempotency)
        existing_evidence = self.db.query(EvidenceBundle).filter(EvidenceBundle.bundle_hash == evidence_hash).first()
        if not existing_evidence:
            evidence = EvidenceBundle(
                bundle_hash=evidence_hash,
                normalization_schema="email_ingest_v1",
                items_json=analysis,
                collected_at=datetime.utcnow()
            )
            self.db.add(evidence)
            # Commit evidence first to satisfy FK
            self.db.commit()

        # 3. Submit Decision
        decision_id = uuid.uuid4()
        decision_hash = f"hash_{decision_id}" 
        
        decision = DecisionObject(
            decision_id=decision_id,
            timestamp=datetime.utcnow(),
            actor_user_id="agent_ingestion",
            actor_role=RoleEnum.system_bot,
            intent_action="UPDATE_UNIT_TENANT",
            intent_target=str(unit.unit_id),
            intent_params={
                "tenant_name": analysis["tenant_name"],
                "lease_source": source_id
            },
            evidence_hash=evidence_hash, 
            outcome=OutcomeEnum.APPROVED, # Auto-approve for demo
            policy_version="1.0",
            decision_hash=decision_hash,
            previous_hash="chain"
        )
        
        self.db.add(decision)
        try:
            self.db.commit()
            logger.info(f"Decision SUBMITTED: {decision_id}. Unit {unit.name} -> Occupied.")
            
            # Trigger Projection Immediately (or let background worker do it)
            from vte.tasks import handle_inventory_projection
            handle_inventory_projection(decision, self.db)
            
        except Exception as e:
            logger.error(f"Failed to submit decision: {e}")
            self.db.rollback()
