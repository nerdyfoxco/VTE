# VTE Phase 0: Sealed Definition of Done

**Version:** 1.0
**Status:** SEALED

## 1. Immutable Truth Schemas (Contracts)
- [x] **Decision Object (v1)**: Defined, includes `decision_hash` and `previous_hash` (logical).
- [x] **Evidence Bundle (v1)**: Defined, immutable contents with `normalization_schema`.
- [x] **Permit Token (v1)**: Defined, signed authorization for side-effects.
- [x] **RBAC Policy (v1)**: Defined, roles `super_admin`, `admin`, `user`, `auditor`, `system_bot`.

## 2. Infrastructure & Persistence
- [x] **PostgreSQL 16**: Containerized (`vte-spine-db`) and running.
- [x] **Migrations Applied**:
    - `0001`: Core Extensions (UUID, Enums).
    - `0002`: Proof Spine Tables w/ Append-Only Triggers.
    - `0003`: Idempotency Locks.
    - `0004`: Row-Level Security (RLS).
    - `0005`: Proof Chain Linking (Previous Hash).
    - `0006`: Operational Kill Switch.

## 3. Enforcement Logic (Runtime)
- [x] **Canonicalization**: RFC 8785 strict JSON generator implemented (`canonicalize.py`).
- [x] **Golden Vectors**: Cross-language test vectors generated.
- [x] **ProofVerifier**: `verify_decision_integrity` and `verify_evidence_link` implemented in Python.

## 4. Governance & Safety
- [x] **Silo Enforcement**: CI script (`check_silo_imports.py`) active.
- [x] **Repo Governance**: `CODEOWNERS` file creates review gates for `/contracts` and `/spine`.
- [x] **Surface Map**: Allowed I/O strictly defined in `surface_map_v1.json`.
- [x] **Run-Mode Truth**: Environment strictness defined in `run_mode_truth_table_v1.json`.

## 5. Next Steps (Phase 1 Execution)
- Implement API Endpoints (FastAPI) to expose these contracts.
- Connect `spine` to `web` and `mobile`.
- Implement actual side-effect drivers (Email, S3).
