# Supply Chain End-to-End Enforcement v1

## Goal
Ensure that ONLY attested, signed, and scanned artifacts are deployed to production.

## Policy
1. All commits MUST be signed (GPG).
2. CI pipeline MUST generate a provenance attestation (SLSA Level 3).
3. Container images MUST be signed with Cosign.
4. Admission Controller MUST reject any pod without a valid signature and attestation.

## Enforcement
- **Build Time**: GitHub Actions blocks unsigned commits.
- **Deploy Time**: OPA Gatekeeper blocks unsigned images.
- **Runtime**: Agents verify integrity periodically.
