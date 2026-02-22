from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from datetime import datetime, timezone
import sys
from pathlib import Path

# Fix relative import when running as a module directly
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from database import Base

class WorkflowStateModel(Base):
    __tablename__ = "workflow_states"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(String, index=True)
    work_item_id = Column(String, index=True, unique=True)
    current_state = Column(String)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DecisionTraceModel(Base):
    __tablename__ = "decision_traces"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(String, index=True)
    work_item_id = Column(String, index=True)
    intent_hash = Column(String, unique=True, index=True)
    final_decision = Column(String)
    action = Column(String)
    trace_log = Column(JSON) # To securely store array of contributing reasons
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ConsentRecordModel(Base):
    __tablename__ = "consent_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    region = Column(String)
    consent_granted = Column(Boolean)

class IdempotencyKeyModel(Base):
    __tablename__ = "idempotency_keys"
    id = Column(Integer, primary_key=True, index=True)
    intent_hash = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)

# --- VTE 3.0 Identity Plane Models ---

class TenantModel(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, unique=True, index=True)
    name = Column(String)
    stripe_customer_id = Column(String, unique=True, index=True, nullable=True)
    subscription_status = Column(String, default="inactive") # "active", "past_due", "canceled"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class UserModel(Base):
    """
    Physical Representation of the VTE 3.0 Identity.
    Enforces the 'SignUp' Schema Invariants at the data layer.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    tenant_id = Column(String, index=True)
    totp_secret = Column(String)
    mfa_enrolled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RoleModel(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    role_name = Column(String) # e.g., "admin", "agent", "auditor"
