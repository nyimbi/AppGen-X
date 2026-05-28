# Audit Ledger

This PBC owns append-only audit evidence, signature-chain verification,
retention policy governance, forensic export preparation, release evidence,
and AppGen-X inbox/outbox/dead-letter handling for the `audit_ledger`
business boundary. It stays within owned tables and ordinary relational
backends: PostgreSQL, MySQL, and MariaDB.

## Implemented executable slice

The current slice adds real sealing and proof behavior on top of the generated
package scaffolding:

- evidence-envelope admissibility checks for sealed audit events
- canonical payload normalization and deterministic digest generation
- immutable correction linkage without rewriting prior events
- per-tenant sequence integrity proofs for signature-chain verification
- forensic export disclosure minimization with verifier instructions
- release notarization bundles built from owned state only

## Key module entry points

- `ledger_proofs.py`
  Pure package-local logic for canonicalization, envelope validation,
  correction planning, chain proofs, disclosure plans, and notarization.
- `runtime.py`
  Runtime commands and queries wired to the new proof logic for event sealing,
  chain verification, export preparation, control testing, and release
  evidence.
- `services.py`
  Service-layer previews for audit-event sealing and forensic-export
  minimization.
- `agent.py`
  Agent-facing previews for governed audit mutations and minimized disclosure.
- `ui.py`
  Workbench proof widgets and rendered proof summaries.
- `release_evidence.py`
  Package release readiness with proof-slice evidence and notarization output.

## Validation commands

```bash
python3 -m compileall src/pyAppGen/pbcs/audit_ledger
./.venv/bin/pytest tests/test_pbc_audit_ledger_implementation.py tests/test_pbc_audit_ledger_runtime.py src/pyAppGen/pbcs/audit_ledger/tests/test_contract.py src/pyAppGen/pbcs/audit_ledger/tests/test_runtime_capabilities.py -q
```

## Scope notes

- Eventing remains AppGen-X only.
- No stream-engine picker or non-AppGen-X transport was introduced.
- No shared or foreign-table reads/writes were added.
- The slice is intentionally limited to sealing, proof, disclosure, and
  release-evidence behavior; broader backlog items remain open for later
  slices.
