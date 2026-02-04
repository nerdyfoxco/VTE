from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, desc
from vte.db import get_db
from typing import List, Optional
from vte.api.schema import DecisionDraft, DecisionRead, EvidenceBundleDraft, EvidenceBundleRead, OutcomeEnum
from vte.orm import DecisionObject, EvidenceBundle
from vte.core.verifier import ProofVerifier
from vte.core.canonicalize import canonical_json_dumps
import hashlib
import hashlib
import json
import datetime

router = APIRouter()
verifier = ProofVerifier()

@router.post("/evidence", response_model=EvidenceBundleRead, status_code=status.HTTP_201_CREATED)
def create_evidence(draft: EvidenceBundleDraft, db: Session = Depends(get_db)):
    """
    Ingests an Evidence Bundle, canonicalizes it, and persists it.
    """
    # 1. Canonicalize & Hash
    # The draft Pydantic model can be dumped to dict
    payload = draft.model_dump() # items are list of dicts
    
    # We must be careful about hash stability. 
    # The 'normalization_schema' + 'items' are the core identity.
    # Collected At is metadata of THIS instance of collection, but if we collect identical evidence twice, 
    # should it have the same hash? 
    # Migration 0002 has unique(bundle_hash).
    # If we include 'collected_at' in hash, every collection is unique.
    # If we exclude it, we dedupe identical evidence collections.
    # VTE philosophy: Evidence is historical fact. 
    # 'Collected At' is part of the fact "I saw this at time T".
    # So we should include it.
    
    # from datetime import datetime
    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    
    # Payload for hashing
    hash_payload = payload.copy()
    hash_payload["collected_at"] = now_iso
    
    try:
        canonical_bytes = canonical_json_dumps(hash_payload)
        bundle_hash = hashlib.sha256(canonical_bytes).hexdigest()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Canonicalization failed: {str(e)}")

    # Create Bundle
    # For SQLite compatibility, pass datetime object, not ISO string.
    # SA will handle conversion.
    db_obj = EvidenceBundle(
        collected_at=datetime.datetime.now(datetime.timezone.utc),
        normalization_schema=draft.normalization_schema,
        items_json=json.loads(json.dumps(draft.model_dump()["items"], default=str)), # Ensure valid JSON
        bundle_hash=bundle_hash
    )
    
    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        db.rollback()
        # Handle duplicate hash collision if desired, but here we likely want to error or return existing.
        # For Phase 0 strictness, error is fine (client should handle).
        raise HTTPException(status_code=500, detail=f"Persistence failed (Collision?): {str(e)}")

    return db_obj

from vte.api.deps import get_current_user_claims
from vte.core.policy import PolicyEngine

policy_engine = PolicyEngine()

@router.post("/decisions", response_model=DecisionRead, status_code=status.HTTP_201_CREATED)
def create_decision(draft: DecisionDraft, claims: dict = Depends(get_current_user_claims), db: Session = Depends(get_db)):
    """
    Ingests a Decision Draft. Requires JWT Auth.
    Ensures 'actor' in draft matches the authenticated user token.
    Enforces Policy Rules via PolicyEngine.
    """
    # 0. Security Enforcement: Overwrite Actor with Trusted Token Claims
    draft.actor.user_id = claims["user_id"]
    
    # 0.5 Policy Enforcement
    policy_result = policy_engine.evaluate(draft, claims)
    if not policy_result.allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=policy_result.reason
        )
    
    # 1. Get Previous Hash...
    # In a real app we'd use select ... for update or advisory lock here.
    # We rely on the DB trigger to optimistic check, but we need the value to calc hash.
    
    last_decision = db.query(DecisionObject).order_by(desc(DecisionObject.timestamp), desc(DecisionObject.decision_id)).first()
    previous_hash = last_decision.decision_hash if last_decision else "GENESIS"

    # 2. Construct Canonical Payload (Nested)
    # We must match the JSON structure expected by the 'decision_object_v1' schema AND the chaining logic.
    # Note: verifier.py expects 'decision_hash' to be calculated from the payload.
    # If we include 'previous_hash' in the payload effectively, we cryptographically bind the chain.
    
    payload = {
        "timestamp": "PENDING", # We need a timestamp. Usually DB sets it, but for hashing we need to set it NOW.
        "actor": {
            "user_id": draft.actor.user_id,
            "role": draft.actor.role.value,
            "session_id": draft.actor.session_id
        },
        "intent": {
            "action": draft.intent.action,
            "target_resource": draft.intent.target_resource,
            "parameters": draft.intent.parameters
        },
        "evidence_hash": draft.evidence_hash,
        "outcome": draft.outcome.value,
        "policy_version": draft.policy_version,
        "permit_token_id": str(draft.permit_token_id) if draft.permit_token_id else None,
        "previous_hash": previous_hash
    }
    
    # Add timestamp
    now_iso = datetime.datetime.utcnow().isoformat() + "Z" 
    payload["timestamp"] = now_iso
    
    # 3. Canonicalize & Hash
    try:
        canonical_bytes = canonical_json_dumps(payload)
        decision_hash = hashlib.sha256(canonical_bytes).hexdigest()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Canonicalization failed: {str(e)}")

    # 4. Map to ORM (Flattened)
    db_obj = DecisionObject(
        timestamp=now_iso, # sqlalchemy might try to cast string to TIMESTAMP, should work
        actor_user_id=draft.actor.user_id,
        actor_role=draft.actor.role, # Enum
        actor_session_id=draft.actor.session_id,
        intent_action=draft.intent.action,
        intent_target=draft.intent.target_resource,
        intent_params=draft.intent.parameters,
        evidence_hash=draft.evidence_hash,
        outcome=draft.outcome, # Enum
        policy_version=draft.policy_version,
        permit_token_id=draft.permit_token_id,
        decision_hash=decision_hash,
        previous_hash=previous_hash # Provided explicitly so Trigger doesn't fail
    )
    
    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Persistence failed: {str(e)}")

    # 5. Trigger Execution (Side Effect)
    # If the decision is APPROVED, we must execute the intent.
    # We do this asynchronously via Celery.
    if db_obj.outcome == OutcomeEnum.APPROVED:
        try:
            from vte.tasks import execute_decision
            # We use delay() to send to Redis queue
            execute_decision.delay(decision_id=str(db_obj.decision_id))
        except Exception as e:
            # We do NOT rollback the decision - it is committed.
            # But we log the failure to enqueue.
            # In a real system, we might need a reliable outbox pattern here.
            # For VTE Phase 17, logging is sufficient.
            print(f"CRITICAL: Failed to enqueue execution task: {e}")

    return db_obj

@router.get("/decisions/{decision_id}", response_model=DecisionRead)
def get_decision(decision_id: str, db: Session = Depends(get_db)):
    obj = db.query(DecisionObject).filter(DecisionObject.decision_id == decision_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Decision not found")
    return obj

@router.get("/decisions", response_model=List[DecisionRead])
def get_decisions(status: Optional[OutcomeEnum] = None, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get list of decisions, optionally filtered by status (e.g., PROPOSED).
    Returns most recent first.
    """
    query = db.query(DecisionObject)
    
    if status:
        query = query.filter(DecisionObject.outcome == status)
        
    query = query.order_by(desc(DecisionObject.timestamp))
    return query.limit(limit).all()
