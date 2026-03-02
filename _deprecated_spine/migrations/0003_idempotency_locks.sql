-- Migration 0003: Idempotency Locks
-- Depends on: 0002_proof_spine_tables

-- Idempotency Lock Table
-- Used to prevent duplicate processing of the same business event.
-- Keys should be deterministically derived from the event (e.g. "claim_submission:<hash>").
CREATE TABLE idempotency_locks (
    lock_key TEXT PRIMARY KEY,
    locked_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    worker_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACQUIRED'
);

-- Index for cleanup of expired locks
CREATE INDEX idx_idempotency_expires ON idempotency_locks(expires_at);

-- View for Auditors to see recent lock activity without full table access
CREATE VIEW view_recent_locks AS
SELECT lock_key, locked_at, worker_id, status
FROM idempotency_locks
WHERE locked_at > NOW() - INTERVAL '1 day';
