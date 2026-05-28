## Audit Ledger Implementation Plan

### Goal
Implement a real executable audit-ledger slice that improves the sealing,
proof, and disclosure domain behavior without broadening scope beyond the
owned `audit_ledger` package and its owned tables.

### Chosen backlog slice
- `1. Evidence envelope completeness gate`
- `2. Per-tenant sequence integrity proof`
- `4. Canonical payload digest strategy`
- `8. Disclosure minimization planner`
- `26. Release evidence notarization bundle`
- `36. Immutable audit correction pattern`

### Why this slice
- The existing package already exposes runtime commands for event sealing,
  signature verification, forensic export, workbench rendering, service
  planning, agent guidance, and release evidence.
- Those surfaces are present but shallow; sealing and proof quality are the
  clearest place to add real executable domain behavior without changing the
  overall package contract.
- The chosen backlog items reinforce each other:
  canonicalization drives deterministic payload digests, complete envelopes
  drive admissible sealing, chain proofs validate the sealed sequence, export
  planning uses those proofs for minimized disclosures, and release evidence
  can publish a notarization-style summary of the owned ledger state.

### Package-local scope
- Add one package-local audit proof module with pure functions for:
  envelope validation, canonical payload normalization, digest calculation,
  chain proofing, disclosure planning, correction planning, and release
  notarization summaries.
- Extend `runtime.py` to use that executable logic for:
  `record_audit_event`, `verify_signature_chain`,
  `prepare_forensic_export`, `build_workbench_view`,
  `run_control_tests`, and `build_release_evidence`.
- Surface previews through `services.py` and `agent.py`.
- Add UI metadata and rendered workbench evidence for the new proof slice in
  `ui.py`.
- Attach the new executable proof evidence to `release_evidence.py`.
- Add focused tests in `tests/test_pbc_audit_ledger_implementation.py`.
- Write `README.md` and `implementation-status.md` after verification.

### Behavior to implement
1. Validate an audit-event envelope and derive admissible defaults only where
   the evidence is still defensible.
2. Canonicalize payloads deterministically so equivalent payloads hash the
   same even when object key order differs.
3. Seal audit events with explicit envelope metadata, payload digest,
   canonicalization version, timestamp basis, and causality evidence.
4. Support immutable correction metadata so a new event can correct a prior
   sealed event without rewriting history.
5. Produce per-tenant sequence integrity proofs that detect sequence gaps,
   duplicate sequence numbers, previous-hash mismatches, inadmissible
   envelopes, payload-digest drift, and non-monotonic timestamps.
6. Plan forensic export disclosure with selected fields, withheld fields,
   proof coverage, approval requirement flags, and verifier instructions.
7. Build release notarization evidence from owned tables only and preserve the
   AppGen-X event contract.

### Verification plan
- Run targeted tests:
  - `tests/test_pbc_audit_ledger_implementation.py`
  - `tests/test_pbc_audit_ledger_runtime.py`
  - `src/pyAppGen/pbcs/audit_ledger/tests/test_contract.py`
  - `src/pyAppGen/pbcs/audit_ledger/tests/test_runtime_capabilities.py`
- Run compile checks for the owned package:
  - `python3 -m compileall src/pyAppGen/pbcs/audit_ledger`

### Non-goals for this slice
- No new datastore backend beyond PostgreSQL, MySQL, and MariaDB.
- No non-AppGen-X event transport or stream-engine picker.
- No writes outside the `audit_ledger` owned tables and runtime-owned inbox,
  outbox, and dead-letter tables.
- No changes to unrelated PBCs, top-level package catalogs, staging, commit,
  or push operations.
