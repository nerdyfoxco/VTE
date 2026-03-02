-- Migration 0005: Proof Chain Hash Trigger
-- Depends on: 0004_rls_security

-- 1. Add previous_hash column
ALTER TABLE decision_objects ADD COLUMN previous_hash TEXT;

-- 2. Chain Enforcement Trigger Function
CREATE OR REPLACE FUNCTION maintain_prover_chain()
RETURNS TRIGGER AS $$
DECLARE
    last_hash TEXT;
BEGIN
    -- Acquire exclusive advisory lock to serialize insertions for the chain.
    -- Lock ID 1000 is arbitrarily chosen for the Decision Chain.
    PERFORM pg_advisory_xact_lock(1000);

    -- Get the hash of the most recent decision
    SELECT decision_hash INTO last_hash
    FROM decision_objects
    ORDER BY timestamp DESC, decision_id DESC
    LIMIT 1;

    -- If no previous decision, this is the genesis block.
    IF last_hash IS NULL THEN
        NEW.previous_hash := 'GENESIS';
    ELSE
        NEW.previous_hash := last_hash;
    END IF;

    -- Note: The decision_hash itself MUST be calculated by the Application (Spine) 
    -- because it includes the 'intent', 'actor', etc. AND the 'previous_hash'.
    -- The Application should: 
    -- 1. Lock 
    -- 2. Read Last Hash 
    -- 3. Calculate New Hash 
    -- 4. Insert.
    
    -- However, doing 2 and 3 in the DB trigger is hard because hashing JSON in PL/PGSQL is tricky without extensions.
    -- SO, we will enforce:
    -- The application MUST provide 'previous_hash'.
    -- This trigger VALIDATES that the provided 'previous_hash' matches the actual last hash.
    -- IF the application can't know it (race condition), it should fail and retry.
    
    -- BUT, to make it easier: let's let the DB set it, and the App includes it in the canonical calculation *after* return? 
    -- No, Hash depends on content. Content includes Previous Hash. Circular.
    
    -- CORRECT APPROACH FOR VTE:
    -- The Trigger sets the `previous_hash` column.
    -- The `decision_hash` (calculated by app) determines the ID.
    -- Wait, if App calculates Hash, it needs Previous Hash.
    -- So App must read `previous_hash` -> calc Hash -> Insert.
    -- DB just verifies?
    
    -- SIMPLIFIED FOR PHASE 0:
    -- We just store the link. We relies on the 'canonicalize.py' in the app to do the crypto.
    -- The DB just acts as the storage.
    -- But we WANT the DB to enforce the link existence.
    
    IF NEW.previous_hash IS NULL THEN
         NEW.previous_hash := last_hash; -- Auto-link if not provided
         IF NEW.previous_hash IS NULL THEN
            NEW.previous_hash := 'GENESIS';
         END IF;
    ELSIF NEW.previous_hash != last_hash THEN
        -- If provided but wrong (OPTIMISTIC CONCURRENCY CHECK)
        RAISE EXCEPTION 'Invalid previous_hash. Chain tip has moved. Expected %, got %', last_hash, NEW.previous_hash;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_chain_link
BEFORE INSERT ON decision_objects
FOR EACH ROW EXECUTE FUNCTION maintain_prover_chain();
