-- Migration 0004: Row-Level Security (RLS) & DB Roles
-- Depends on: 0003_idempotency_locks

-- Enable RLS on core tables
ALTER TABLE decision_objects ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_bundles ENABLE ROW LEVEL SECURITY;
ALTER TABLE permit_tokens ENABLE ROW LEVEL SECURITY;

-- Create Roles (if they don't exist)
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'vte_auditor') THEN
    CREATE ROLE vte_auditor;
  END IF;
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'vte_worker') THEN
    CREATE ROLE vte_worker;
  END IF;
END
$$;

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO vte_worker, vte_auditor;

-- WORKER POLICIES
-- Workers can insert decisions/evidence/permits but CANNOT delete ever.
-- They can read what they need.
GRANT INSERT, SELECT ON decision_objects TO vte_worker;
GRANT INSERT, SELECT ON evidence_bundles TO vte_worker;
GRANT INSERT, SELECT ON permit_tokens TO vte_worker;
GRANT ALL ON idempotency_locks TO vte_worker; -- Needs delete/update for locks

-- AUDITOR POLICIES
-- Auditors can ONLY SELECT.
GRANT SELECT ON ALL TABLES IN SCHEMA public TO vte_auditor;

-- RLS POLICIES

-- Policy: Auditors see everything
CREATE POLICY auditor_read_all ON decision_objects
    FOR SELECT TO vte_auditor USING (true);

CREATE POLICY auditor_read_all_evidence ON evidence_bundles
    FOR SELECT TO vte_auditor USING (true);

CREATE POLICY auditor_read_all_permits ON permit_tokens
    FOR SELECT TO vte_auditor USING (true);

-- Policy: Workers see everything (for now, simpler than partitioning by tenant at this stage)
-- In a multi-tenant system, we would restrict this.
CREATE POLICY worker_read_all ON decision_objects
    FOR SELECT TO vte_worker USING (true);

CREATE POLICY worker_insert_decisions ON decision_objects
    FOR INSERT TO vte_worker WITH CHECK (true);

-- Note: The spine_app user (superuser effectively in container, or owner) bypasses RLS unless FORCE is used.
-- We keep RLS as a defense-in-depth for separate roles we might introduce later.
