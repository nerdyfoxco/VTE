from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from spine.db.engine import Base

class DBQueueItem(Base):
    """
    Real World persistence for Unified Queue.
    Replaces the list[] in queue.py
    """
    __tablename__ = "queue_items"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    priority = Column(Integer)
    status = Column(String, default="PENDING")
    assigned_to = Column(String, nullable=True)
    sla_deadline = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    tenant_id = Column(String, index=True) # Multi-tenancy enforcement

class DBAuditLog(Base):
    """
    Start of the Evidence Store.
    """
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    actor = Column(String)
    action = Column(String)
    target = Column(String)
    timestamp = Column(DateTime, default=func.now())
    tenant_id = Column(String, index=True)

class DBUser(Base):
    __tablename__ = "users"
    
    username = Column(String, primary_key=True)
    password_hash = Column(String)
    role = Column(String, default="user")
    tenant_id = Column(String)
    
    # Gap 13: Lifecycle
    email_verified = Column(Boolean, default=False)
    tos_accepted_at = Column(DateTime, nullable=True)
    
    # Gap 1: MFA
    mfa_secret = Column(String, nullable=True) # TOTP Secret
    mfa_enabled = Column(Boolean, default=False)
    
    # Gap 6: Lockout
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    
    # Gap 3: Rotation
    password_changed_at = Column(DateTime, default=func.now())

    # Gap 11: Self-Service Reset
    reset_token = Column(String, nullable=True, index=True)
    reset_token_expires_at = Column(DateTime, nullable=True)

    # Gap 12: Invitation Flow
    invitation_token = Column(String, nullable=True, index=True)
    invitation_expires_at = Column(DateTime, nullable=True)
    invited_by = Column(String, nullable=True)

    # Gap 13: Email Verification
    verification_token = Column(String, nullable=True, index=True)
