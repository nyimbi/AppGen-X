# Release Evidence - Agri Supply Chain Traceability

Package directory: `src/pyAppGen/pbcs/agri_supply_chain_traceability`.

## Implemented Slice

This package now provides an executable standalone AppGen-X PBC surface for
agricultural release-readiness. The slice records package-local traceability
facts, renders a one-PBC workbench, plans governed document and CRUD actions,
and evaluates whether a shipment candidate should be approved or blocked.

## Evidence Areas

- Source artifacts: `README.md`, `SPECIFICATION.md`, `implementation-plan.md`,
  `implementation-status.md`, `RELEASE_EVIDENCE.md`, `standalone.py`,
  `migrations/001_initial.sql`, `tests/test_contract.py`, and
  `tests/test_standalone.py`.
- Runtime and service execution: owned-table state transitions, idempotent
  event intake, release-gate execution, service contracts, and workbench
  queries.
- Route surface: package-local API routes for configuration, parameters, rules,
  events, evidence capture, release gating, workbench reads, service-contract
  reads, and release-evidence reads.
- UI surface: standalone shell metadata, navigation, forms, wizards, controls,
  workbench rendering, and release-gate panel output.
- Agent surface: document-instruction planning, governed CRUD previews,
  release-gate hints, and recall investigation planning.
- Repo-gate style audits: source artifact contract, implementation release
  audit, and generation smoke audit.

## Expected Validation Commands

```bash
python3 -m py_compile \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/runtime.py \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/services.py \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/routes.py \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/ui.py \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/agent.py \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/models.py \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/release_evidence.py \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/standalone.py \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/__init__.py

python3 -m pytest -q \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/tests/test_contract.py \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/tests/test_standalone.py
```

## Gate Intent

- `pbc_source_artifact_contract`: prove the standalone slice ships with the
  required package-local artifacts.
- `pbc_implementation_release_audit`: prove schema, services, routes, events,
  permissions, UI, agent, and release evidence agree.
- `pbc_generation_smoke_audit`: prove runtime smoke and standalone smoke both
  execute successfully in package scope.
