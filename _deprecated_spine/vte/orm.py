from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.types import Uuid as UUID
# from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
from sqlalchemy.sql import func
from vte.db import Base
import uuid

# Define Enums (must match DB types)
RoleEnum = Enum('super_admin', 'admin', 'user', 'auditor', 'system_bot', name='role_enum')
OutcomeEnum = Enum('PROPOSED', 'APPROVED', 'MESSAGE_PREVIEW', 'EXECUTION_READY', 'DENIED', 'NEEDS_MORE_EVIDENCE', name='outcome_enum')
CriticalityEnum = Enum('HIGH', 'MEDIUM', 'LOW', name='criticality_enum')

class EvidenceBundle(Base):
    __tablename__ = "evidence_bundles"
    
    bundle_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    collected_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    normalization_schema = Column(String, nullable=False)
    items_json = Column(JSON, nullable=False)
    bundle_hash = Column(String, nullable=False, unique=True)

    @property
    def items(self):
        return self.items_json

class DecisionObject(Base):
    __tablename__ = "decision_objects"

    decision_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    # Actor
    actor_user_id = Column(String, nullable=False)
    actor_role = Column(RoleEnum, nullable=False)
    actor_session_id = Column(String, nullable=True)

    # Intent
    intent_action = Column(String, nullable=False)
    intent_target = Column(String, nullable=False)
    intent_params = Column(JSON, nullable=False, default={})

    # Evidence Link
    evidence_hash = Column(String, ForeignKey("evidence_bundles.bundle_hash"), nullable=True)
    
    # Outcome
    outcome = Column(OutcomeEnum, nullable=False)
    policy_version = Column(String, nullable=False)

    # Permit Reference (This is circular if we wanted a FK to permits, 
    # but the schema definition had `permit_token_id`. 
    # In Migration 0002 line 37: `permit_token_id UUID`.
    # It does NOT have a foreign key constraint in the SQL migration to permit_tokens (likely to avoid cycle).
    permit_token_id = Column(UUID(as_uuid=True), nullable=True)

    # Chain
    decision_hash = Column(String, nullable=False, unique=True)
    previous_hash = Column(String, nullable=True) # Managed by DB Trigger

    @property
    def actor(self):
        # Return object compatible with Actor model
        class ActorProxy:
            def __init__(self, u, r, s):
                self.user_id = u
                self.role = r
                self.session_id = s
        return ActorProxy(self.actor_user_id, self.actor_role, self.actor_session_id)

    @property
    def intent(self):
        class IntentProxy:
            def __init__(self, a, t, p):
                self.action = a
                self.target_resource = t
                self.parameters = p
        return IntentProxy(self.intent_action, self.intent_target, self.intent_params)

class PermitToken(Base):
    __tablename__ = "permit_tokens"
    
    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id = Column(UUID(as_uuid=True), ForeignKey("decision_objects.decision_id"), nullable=False, unique=True)
    
    issued_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    
    scope_json = Column(JSON, nullable=False)
    signature = Column(String, nullable=False)

# --- Inventory Projections (Read Model) ---
class Property(Base):
    __tablename__ = "properties"
    
    property_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    external_ref_id = Column(String, nullable=True, unique=True, index=True) # e.g. AppFolio ID
    
    # Audit Link
    created_at_decision_hash = Column(String, ForeignKey("decision_objects.decision_hash"), nullable=False)
    updated_at_decision_hash = Column(String, ForeignKey("decision_objects.decision_hash"), nullable=False)

    # Relationships
    units = relationship("Unit", back_populates="property")

class Unit(Base):
    __tablename__ = "units"
    
    unit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.property_id"), nullable=False)
    
    name = Column(String, nullable=False) # "101", "Apt B"
    status = Column(String, nullable=False, default="VACANT") # VACANT, OCCUPIED, MAINTENANCE
    tenant_info = Column(JSON, nullable=True) # Snapshot of current tenant
    external_ref_id = Column(String, nullable=True, unique=True, index=True)
    
    # Audit Link
    created_at_decision_hash = Column(String, ForeignKey("decision_objects.decision_hash"), nullable=False)
    updated_at_decision_hash = Column(String, ForeignKey("decision_objects.decision_hash"), nullable=False)

    property = relationship("Property", back_populates="units")

# --- Security & Identity ---

class TOTPDevice(Base):
    __tablename__ = "totp_devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True) # Linking to external/string User ID
    name = Column(String, nullable=False) # e.g. "Kevin's iPhone"
    secret = Column(String, nullable=False) # Encrypted or raw secret
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    last_used_at = Column(TIMESTAMP(timezone=True), nullable=True)
    confirmed = Column(String, default="false") # "true" after first verification

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False) # e.g. "decision:create"
    description = Column(String, nullable=True)

class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    role = Column(RoleEnum, primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"), primary_key=True)

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    token_jti = Column(String, unique=True, nullable=False) # JWT ID
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    revoked = Column(String, default="false")

