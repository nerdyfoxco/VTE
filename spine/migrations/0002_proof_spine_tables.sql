-- Migration 0002: Proof Spine Tables (Append-Only)
-- Depends on: 0001_core_extensions

-- Trigger Function to Prevent Updates/Deletes
CREATE OR REPLACE FUNCTION prevent_update_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'This table is append-only. Modification or deletion is strictly forbidden to preserve audit trails.';
END;
$$ LANGUAGE plpgsql;

-- 1. Evidence Bundles (Immutable data storage)
CREATE TABLE evidence_bundles (
    bundle_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    collected_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    normalization_schema TEXT NOT NULL,
    items_json JSONB NOT NULL, -- Full payload
    bundle_hash TEXT NOT NULL, -- SHA256 of canonicalized bundle
    UNIQUE(bundle_hash)
);

CREATE TRIGGER enforce_append_only_evidence
BEFORE UPDATE OR DELETE ON evidence_bundles
FOR EACH ROW EXECUTE FUNCTION prevent_update_delete();


-- 2. Decision Objects (The Atom of Truth)
CREATE TABLE decision_objects (
    decision_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Actor
    actor_user_id TEXT NOT NULL,
    actor_role role_enum NOT NULL,
    actor_session_id TEXT,

    -- Intent
    intent_action TEXT NOT NULL,
    intent_target TEXT NOT NULL,
    intent_params JSONB NOT NULL DEFAULT '{}',

    -- Evidence Link
    evidence_hash TEXT REFERENCES evidence_bundles(bundle_hash),
    
    -- Outcome
    outcome outcome_enum NOT NULL,
    policy_version TEXT NOT NULL,

    -- Permit Reference (if Approved)
    permit_token_id UUID, -- Forward reference, nullable initially? No, circular. 
                         -- Better to store permit_id here if generated, or link externally. 
                         -- Decision comes BEFORE Permit. So this field is fine, but might be populated by the Permit generation logic?
                         -- Wait, "Immutable". If we create decision, we don't know permit ID yet. 
                         -- UNLESS: Transaction creates both. 
                         -- OR: Permit links TO Decision.
    
    -- Canonical Hash of this entire object
    decision_hash TEXT NOT NULL UNIQUE
);

CREATE TRIGGER enforce_append_only_decisions
BEFORE UPDATE OR DELETE ON decision_objects
FOR EACH ROW EXECUTE FUNCTION prevent_update_delete();


-- 3. Permit Tokens (Authorization for Side-Effects)
CREATE TABLE permit_tokens (
    token_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    decision_id UUID NOT NULL REFERENCES decision_objects(decision_id),
    
    issued_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    scope_json JSONB NOT NULL,
    signature TEXT NOT NULL, -- Cryptographic signature of the token content
    
    UNIQUE(decision_id) -- 1:1 Decision to Permit (if approved)
);

CREATE TRIGGER enforce_append_only_permits
BEFORE UPDATE OR DELETE ON permit_tokens
FOR EACH ROW EXECUTE FUNCTION prevent_update_delete();
