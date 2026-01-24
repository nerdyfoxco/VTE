-- Migration 0006: Operational Kill Switch
-- Depends on: 0005_proof_chain_link

-- Config Table
CREATE TABLE system_config (
    key TEXT PRIMARY KEY,
    value JSONB NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_by TEXT
);

-- Initial Config
INSERT INTO system_config (key, value, updated_by)
VALUES ('global_kill_switch', '{"active": false, "reason": null}', 'system_init');

-- Function to check Kill Switch
CREATE OR REPLACE FUNCTION check_kill_switch()
RETURNS TRIGGER AS $$
DECLARE
    ks JSONB;
BEGIN
    SELECT value INTO ks FROM system_config WHERE key = 'global_kill_switch';
    
    IF (ks->>'active')::boolean IS TRUE THEN
        RAISE EXCEPTION 'VTE GLOBAL KILL SWITCH ACTIVE: Transaction Rejected. Reason: %', ks->>'reason';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to Permit Tokens (The point of side-effect authorization)
CREATE TRIGGER enforce_kill_switch
BEFORE INSERT ON permit_tokens
FOR EACH ROW EXECUTE FUNCTION check_kill_switch();
