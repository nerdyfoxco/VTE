from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import os
import sys
from pathlib import Path

# Fix module imports
base_dir = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(base_dir / "spine" / "src"))
sys.path.insert(0, str(base_dir / "spine" / "db"))
sys.path.insert(0, str(base_dir / "foundation" / "src"))

from database import get_db
from adapters.appfolio.ledger_analyzer import LedgerAnalyzer
from adapters.appfolio.tag_scanner import TagScanner
from adapters.appfolio.session_proxy import AppFolioSessionProxy
from decision_logic.context_checker import ContextChecker
from hands.kevin_sender import GmailSenderWorker

router = APIRouter(prefix="/api/appfolio", tags=["AppFolio Automation"])

# Initialize the state-aware sender component
kevin_sender = GmailSenderWorker(tenant_id="ws_123")

@router.post("/sync-ledger")
async def sync_ledger(request: Request, db: Session = Depends(get_db)):
    """
    VTE 2.0 Phase 2: autonomous ingestion of an AppFolio Tenant Ledger.
    """
    try:
        raw_payload = await request.json()
        tenant_id = raw_payload.get("tenant_id", "af_tnt_123")
        work_item_id = raw_payload.get("work_item_id", "untracked_item")
        
        from main import internal_process_envelope, PipeEnvelopeRejectError, BackpressureError, DuplicateExecutionError, ConsentViolationError
        
        # 1. Establish Secure Proxy Session
        proxy = AppFolioSessionProxy(tenant_id=tenant_id)
        proxy.connect()
        
        # 2. Extract Data via Adapters
        ledger = LedgerAnalyzer(raw_payload.get("ledger_entries", []))
        tags = TagScanner(raw_payload.get("tenant_tags", []))
        
        # 3. Assess Brain Contexts
        hold_conditions = ledger.assess_hold_conditions()
        tag_context = tags.extract_context()
        human_state_context = ContextChecker.analyze_notes(raw_payload.get("notes", []))
        
        import uuid
        from datetime import datetime
        
        # 4. Synthesize the deterministic VTE Envelope Payload
        envelope_payload = {
            "workspace_id": tenant_id,
            "work_item_id": work_item_id,
            "correlation_id": str(uuid.uuid4()),
            "organ_source": "appfolio_ingestion_proxy",
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "balance_owed": hold_conditions["balance_owed"],
                "is_only_new_water": hold_conditions["is_only_new_water"],
                "has_legal": tag_context["jba_active"] or hold_conditions["has_legal_action"],
                "dnc_active": tag_context["dnc_active"],
                "death_sickness": human_state_context["death_context_detected"] or human_state_context["sickness_context_detected"],
                "status": raw_payload.get("status", "delinquent"),
                "tenant_name": raw_payload.get("tenant_name", "Unknown Resident")
            }
        }
        
        # 5. Route through the VTE Spine 
        # (This triggers Redaction, Compliance, Engine Evaluation, and DB Tracing)
        engine_result = await internal_process_envelope(envelope_payload, db)
        
        # 6. Physical Execution Guard
        action_decision = engine_result.get("action")
        kevin_dispatch_status = "Skipped (Action != PROCEED)"
        
        if action_decision == "PROCEED":
             # Build the physical context required by the template
             physical_context = {
                 "tenant_name": envelope_payload["payload"]["tenant_name"],
                 "balance_owed": str(envelope_payload["payload"]["balance_owed"]),
                 "work_item_id": work_item_id
             }
             kevin_dispatch_status = kevin_sender.execute(action_decision, physical_context)
             
        return {
            "vte_sync_status": "OK",
            "ingestion_source": "AppFolio Proxy",
            "brain_engine_result": {
                "decision": engine_result.get("decision"),
                "reason": engine_result.get("reason"),
                "action": action_decision
            },
            "hands_execution_result": kevin_dispatch_status
        }
        
    except Exception as e:
        # Check if it was one of our rejected safety guards lazily
        error_str = str(e)
        if any(x in str(type(e).__name__) for x in ["PipeEnvelopeRejectError", "BackpressureError", "DuplicateExecutionError", "ConsentViolationError"]):
            raise HTTPException(status_code=400, detail=f"Safety Guard Tripped: {error_str}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {error_str}")
