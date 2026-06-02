# Agri Supply Chain Traceability

`agri_supply_chain_traceability` is now an executable standalone AppGen-X PBC slice.
This package owns its schema and model contracts, runtime state transitions,
stateful service layer, API routes, workbench UI metadata, forms, wizards,
controls, event/handler surfaces, permissions, governed agent planning, release
artifacts, and focused tests without depending on shared generator changes.

## Standalone Slice

The implemented slice is a one-PBC traceability app focused on release-readiness
for agricultural shipments. It can bootstrap package-local state, record the
core evidence needed for traceability, render a standalone workbench, and issue
an explainable release verdict.

### Covered package-local records

- `farm_lot`
- `input_batch`
- `certification`
- `storage_event`
- `transport_leg`
- `recall_link`
- `provenance_proof`

### Covered workflows

- farm lot intake
- input application capture
- certification scope review
- storage and cold-chain review
- transport and seal review
- provenance proof capture
- release-readiness assessment
- document-led intake planning
- recall investigation planning

## Main Entrypoints

- Runtime: `runtime.py`
- Services: `services.py`
- Routes: `routes.py`
- UI/workbench: `ui.py`
- Standalone app: `standalone.py`
- Agent planning: `agent.py`
- Release audit: `release_evidence.py`
- Focused tests: `tests/test_contract.py`, `tests/test_standalone.py`

## What the standalone app exposes

- A stateful service over package-local runtime state.
- Route dispatch for runtime configuration, evidence recording, workbench reads,
  service-contract reads, release-evidence reads, and release-gate execution.
- Workbench shell metadata with navigation, forms, wizards, and reusable
  controls for intake, compliance, release review, and document planning.
- Governed CRUD and document-instruction planning that stay inside owned agri
  traceability tables.
- Release evidence that checks source artifacts, implementation audit coverage,
  and standalone generation smoke for this package.

## Validation

Focused package-local validation is captured in:

- `tests/test_contract.py`
- `tests/test_standalone.py`
- `implementation-status.md`
- `RELEASE_EVIDENCE.md`
