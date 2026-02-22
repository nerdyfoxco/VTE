import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request

# --- Path Injection for Windows Bug Workaround (Strangler Fig Roots) ---
base_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(base_dir / "foundation" / "src"))
sys.path.insert(0, str(base_dir / "chapters" / "kidneys" / "topic-compliance" / "src"))
sys.path.insert(0, str(base_dir / "chapters" / "heart" / "topic-idempotency" / "src"))
sys.path.insert(0, str(base_dir / "chapters" / "lungs" / "src"))
sys.path.insert(0, str(base_dir / "chapters" / "brain" / "topic-policy-engine" / "src"))
sys.path.insert(0, str(base_dir / "chapters" / "brain" / "topic-orchestration" / "src"))
sys.path.insert(0, str(base_dir / "chapters" / "eyes" / "src"))
sys.path.insert(0, str(base_dir / "chapters" / "hands" / "src"))
sys.path.insert(0, str(base_dir / "spine" / "src"))
# --- Import Sealed Components ---
from security.correlation_guard import validate_envelope, PipeEnvelopeRejectError
from security.redaction_engine import RedactionEngine
from consent_registry import ConsentRegistry, ConsentViolationError
from idempotency_middleware import IdempotencyMiddleware, DuplicateExecutionError
from backpressure_manager import BackpressureManager, BackpressureError
from decision_table_compiler import DecisionTableCompiler
from policy_engine import PolicyEngine
from hold_stop_engine import HoldStopEngine, ExecutionAction
from workflow_state_machine import WorkflowStateMachine
from approval_guard import ApprovalGuard, ApprovalRecord

class SubscriptionError(Exception):
    pass

# Live Integration Additions
from gmail_adapter import GmailIngestionAdapter
from gmail_sender import GmailSenderWorker, ExecutionNotApprovedError

# Database Connectors
from db.database import get_db, AsyncSessionLocal, engine, Base
from db.models import DecisionTraceModel, WorkflowStateModel, ConsentRecordModel, TenantModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends

# Disable synchronous initialization for async engine.
# In a real setup, we use Alembic for async schema generation, 
# but for local dev we'll let a lifespan event or startup script handle this.

app = FastAPI(title="VTE 2.0 Spine & Organs E2E", version="E2E-Integration")

from getattr(sys, "modules", {"fastapi.middleware.cors": __import__("fastapi.middleware.cors", fromlist=["CORSMiddleware"])})["fastapi.middleware.cors"] import CORSMiddleware
# Production CORS Locking
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:5173"], # Fallback for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bind Phase 2 AppFolio Integrations
from api.routes.appfolio import router as appfolio_router
app.include_router(appfolio_router)

# Bind Phase 5 Production AppFolio Integration (The "Last Mile" GTM Webhook)
from api.routes.production_sync import router as production_sync_router
app.include_router(production_sync_router)

# Bind Stripe Billing API
from api.routes.billing import router as billing_router
app.include_router(billing_router)

# --- Initialize Singletons on Boot ---
redaction_engine = RedactionEngine(str(base_dir / "foundation" / "src" / "security" / "redaction_rules.json"))
# We keep the JSON fallback for jurisdiction, but will wire real DB constraint checking live
consent_registry = ConsentRegistry(str(base_dir / "chapters" / "kidneys" / "topic-compliance" / "src" / "jurisdiction_rules.json"))
idempotency = IdempotencyMiddleware(default_ttl_seconds=60)
backpressure = BackpressureManager(max_capacity=100)

rules = [
    {"rule_id": "r1", "key": "balance_owed", "expected_value": 0, "decision": "HOLD", "reason": "ZERO_BALANCE"},
    {"rule_id": "r2", "key": "status", "expected_value": "delinquent", "decision": "CONTACT", "reason": "DELINQUENT_STATUS"},
    {"rule_id": "r3", "key": "has_legal", "expected_value": True, "decision": "STOP", "reason": "LEGAL_REPRESENTATION"},
    # AppFolio Specific Rules
    {"rule_id": "r4", "key": "is_only_new_water", "expected_value": True, "decision": "HOLD", "reason": "WATER_BILL_GRACE_PERIOD"},
    {"rule_id": "r5", "key": "dnc_active", "expected_value": True, "decision": "HOLD", "reason": "DO_NOT_CONTACT_OVERRIDE"},
    {"rule_id": "r6", "key": "death_sickness", "expected_value": True, "decision": "HOLD", "reason": "SENSITIVE_HUMAN_STATE_PAUSE"}
]
compiler = DecisionTableCompiler(rules)
policy_engine = PolicyEngine()

# Live Actors
gmail_adapter = GmailIngestionAdapter(tenant_id="ws_123")
gmail_sender = GmailSenderWorker(tenant_id="ws_123")


async def internal_process_envelope(raw_json: dict, db: AsyncSession) -> dict:
    """Core deterministic pipeline reused across all endpoints. Now requires DB Session."""
    await backpressure.register_ingestion()
    try:
        # 2. Pipe Envelope Validation
        envelope = validate_envelope(raw_json)
        
        # 2b. SaaS Gating: Enforce Subscription Status
        tenant_res = await db.execute(select(TenantModel).filter(TenantModel.tenant_id == envelope.workspace_id))
        tenant = tenant_res.scalars().first()
        if not tenant or tenant.subscription_status != "active":
             raise SubscriptionError(f"Tenant {envelope.workspace_id} has an inactive Stripe subscription. Operations Suspended.")
        
        # 3. PII Redaction
        redacted_payload = redaction_engine.redact(envelope.payload)
        # 4. Idempotency Check
        intent_hash = idempotency.check_and_record(envelope.workspace_id, "EVALUATE", redacted_payload)
        
        # 5. Compliance Check (Kidneys - DB Driven)
        user_id = redacted_payload.get("user_id", "user_1")
        
        # Async Query true DB state
        result = await db.execute(select(ConsentRecordModel).filter(ConsentRecordModel.user_id == user_id))
        db_user = result.scalars().first()
        
        if db_user:
             # Override mock registry with real database state
             consent_registry._user_db[user_id] = {"region": db_user.region, "consent_granted": db_user.consent_granted}
        consent_registry.verify_action(user_id, "EVALUATE")
        
        # 6. Brain Workflow Execution
        machine = WorkflowStateMachine("DECISION")
        proposals = compiler.evaluate(redacted_payload)
        final_decision = policy_engine.evaluate(proposals)
        action = HoldStopEngine.enforce(final_decision, machine)
        
        # --> PERSISTENCE: Save Trace to Database
        db_trace = DecisionTraceModel(
            workspace_id=envelope.workspace_id,
            work_item_id=envelope.work_item_id,
            intent_hash=intent_hash,
            final_decision=final_decision.decision.value,
            action=action.value,
            trace_log={"reasons": final_decision.contributing_reasons, "primary": final_decision.primary_reason}
        )
        db.add(db_trace)
        await db.commit()

        # 7. Approval Guard
        if action == ExecutionAction.PROCEED:
             approval = ApprovalRecord(is_required=False)
             ApprovalGuard.enforce(approval)
             
        await backpressure.release_capacity()
        return {
            "status": "success",
            "action": action.value,
            "decision": final_decision.decision.value,
            "reason": final_decision.primary_reason,
            "state_machine_status": machine.get_current().value,
            "intent_hash": intent_hash,
            "envelope": envelope.model_dump() # Return the parsed envelope so Hands can use it
        }
    except Exception as e:
        if not isinstance(e, (PipeEnvelopeRejectError, SubscriptionError)): 
            await backpressure.release_capacity()
        raise e


@app.post("/ingest")
async def ingest_event(request: Request, db: AsyncSession = Depends(get_db)):
    """Raw ingestion endpoint (used by Phase 0-6 unittests)."""
    try:
        raw_json = await request.json()
        result = await internal_process_envelope(raw_json, db)
        # We don't trigger hands implicitly here, this is just evaluation ingress
        result.pop("envelope", None)
        return result
    except (PipeEnvelopeRejectError, BackpressureError, DuplicateExecutionError, ConsentViolationError, SubscriptionError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/sync-gmail")
async def sync_gmail(db: AsyncSession = Depends(get_db)):
    """
    Live Integration Endpoint: Triggers the real Eyes adapter to fetch an email,
    passes it through the strict Engine, and invokes the real Hands sender if permitted.
    """
    try:
        # 1. EYES: Fetch unstructured data and map to strict Envelope
        pydantic_envelope = gmail_adapter.fetch_raw_data()
        envelope = gmail_adapter.build_envelope(pydantic_envelope)
        
        # 2. SPINE/BRAIN: Run deterministic core
        engine_result = await internal_process_envelope(envelope, db)
        
        # 3. HANDS: Physical Action Guarded by Engine Results
        action_decision = engine_result.get("action")
        hand_status = "Skipped (Action != PROCEED)"
        
        if action_decision == "PROCEED":
             hand_status = gmail_sender.execute(action_decision, engine_result["envelope"])
             
        return {
            "vte_sync_status": "OK",
            "ingestion_source": "Gmail API",
            "brain_engine_result": {
                "decision": engine_result.get("decision"),
                "reason": engine_result.get("reason"),
                "action": action_decision
            },
            "hands_execution_result": hand_status
        }

    except (PipeEnvelopeRejectError, BackpressureError, DuplicateExecutionError, ConsentViolationError, SubscriptionError) as e:
        raise HTTPException(status_code=400, detail=f"Safety Guard Tripped: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/api/traces")
async def get_traces(db: AsyncSession = Depends(get_db)):
    """API for the Phase 4 Operator UX Trace Viewer."""
    result = await db.execute(select(DecisionTraceModel).order_by(DecisionTraceModel.timestamp.desc()).limit(50))
    traces = result.scalars().all()
    return [{
        "workspace_id": t.workspace_id,
        "work_item_id": t.work_item_id,
        "final_decision": t.final_decision,
        "action": t.action,
        "trace_log": t.trace_log,
        "timestamp": t.timestamp.isoformat() if t.timestamp else None
    } for t in traces]

@app.get("/api/workqueue")
async def get_workqueue(db: AsyncSession = Depends(get_db)):
    """API for the Phase 4 Operator UX Workqueue Dashboard."""
    # Mocking the workqueue pending logic based on DecisionTraces holding items
    result = await db.execute(select(DecisionTraceModel).filter(DecisionTraceModel.action == 'HOLD').order_by(DecisionTraceModel.timestamp.desc()).limit(50))
    held_items = result.scalars().all()
    return [{
        "work_item_id": t.work_item_id,
        "status": "PENDING_APPROVAL",
        "policy_outcome": t.final_decision,
        "timestamp": t.timestamp.isoformat() if t.timestamp else None
    } for t in held_items]

# --- VTE 3.0 Identity API Binding ---
import os
sys.path.insert(0, str(base_dir / "schemas"))
sys.path.insert(0, str(base_dir / "spine" / "src")) # Fix for IAM module resolution
from definitions.identity import SignUp, SignIn, MFAVerify
from iam.auth import IdentityManager

# Intialize the Identity singleton with paths to the built contracts
auth_mgr = IdentityManager(
    mfa_policy_path=str(base_dir / "contracts" / "auth" / "mfa_policy_v1.json"),
    signin_policy_path=str(base_dir / "contracts" / "auth" / "signin_policy_v1.json")
)

@app.post("/api/auth/signup", status_code=201)
async def signup(payload: SignUp):
    """VTE 3.0 Registration: Enforces strict invariant contracts."""
    try:
        # Note: In production, we pass the DB session down to persist to `UserModel`
        result = auth_mgr.register_user(
            email=payload.email, 
            raw_password=payload.password, 
            full_name=payload.full_name, 
            tenant_id=payload.tenant_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/signin")
async def signin(payload: SignIn):
    """VTE 3.0 Login: Always returns an MFA challenge."""
    try:
        challenge = auth_mgr.initiate_signin(payload.email, payload.password)
        return challenge
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
        
@app.post("/api/auth/mfa/verify")
async def verify_mfa(payload: MFAVerify):
    """Outputs the secure session token if TOTP is valid."""
    try:
        session = auth_mgr.verify_mfa(payload.mfa_token_id, payload.totp_code)
        return session
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
