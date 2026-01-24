from pydantic import BaseModel, Field, UUID4, Json
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum

# Enums
class RoleEnum(str, Enum):
    super_admin = "super_admin"
    admin = "admin"
    user = "user"
    auditor = "auditor"
    system_bot = "system_bot"

class OutcomeEnum(str, Enum):
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    NEEDS_MORE_EVIDENCE = "NEEDS_MORE_EVIDENCE"

# Shared Models
class Actor(BaseModel):
    user_id: str
    role: RoleEnum
    session_id: Optional[str] = None

class Intent(BaseModel):
    action: str
    target_resource: str
    parameters: Dict[str, Any] = {}

# --- Evidence ---
class EvidenceItem(BaseModel):
    source: str
    type: str
    data: Dict[str, Any] # or Json
    sha256: str

class EvidenceBundleDraft(BaseModel):
    normalization_schema: str
    items: List[EvidenceItem]

class EvidenceBundleRead(EvidenceBundleDraft):
    bundle_id: UUID4
    collected_at: datetime
    bundle_hash: str

    class Config:
        from_attributes = True

# --- Decision ---
class DecisionDraft(BaseModel):
    actor: Actor
    intent: Intent
    evidence_hash: Optional[str]
    outcome: OutcomeEnum
    policy_version: str
    permit_token_id: Optional[UUID4] = None

class DecisionRead(BaseModel):
    decision_id: UUID4
    timestamp: datetime
    
    actor_user_id: str
    actor_role: RoleEnum
    actor_session_id: Optional[str]
    
    intent_action: str
    intent_target: str
    intent_params: Dict[str, Any]

    evidence_hash: Optional[str]
    outcome: OutcomeEnum
    policy_version: str
    permit_token_id: Optional[UUID4]

    decision_hash: str
    previous_hash: Optional[str]

    class Config:
        from_attributes = True
