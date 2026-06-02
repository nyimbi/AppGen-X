# Electronic Health Records Core

This package is a self-contained AppGen-X PBC slice for the owned electronic health record. It implements package-local chart intake, duplicate-review controls, encounter documentation controls, clinical order safety checks, critical-result acknowledgement, allergy capture, medication reconciliation, care-note attestation, patient-summary redaction, AppGen-X outbox/inbox/dead-letter behavior, governed rules and parameters, workbench UI metadata, and agent/document-instruction CRUD previews.

## Executable Slice

- `ehr_core_app.py` contains the in-memory one-PBC EHR runtime.
- `runtime.py` publishes runtime, schema, service, API, and release contracts.
- `services.py` exposes a stateful service layer over the executable slice.
- `routes.py` maps package-local HTTP routes to service operations.
- `ui.py` defines the workbench, forms, wizards, and controls for EHR operators.
- `agent.py` provides chatbot/document-instruction planning and governed CRUD previews.
- `config.py`, `permissions.py`, and `seed_data.py` define governance, RBAC, and seed artifacts.

## Core Behavior

- Patient chart creation detects duplicate identity candidates and opens review instead of auto-merging records.
- Encounter intake enforces care-setting-specific documentation completeness.
- Clinical orders surface allergy warnings and block unsafe lifecycle transitions.
- Critical observations open acknowledgement queues until read-back evidence is recorded.
- Medication reconciliation preserves discrepancy evidence and unresolved counts.
- Care notes require the correct signer and keep amendment lineage.
- Patient summaries are generated with profile-specific redaction for clinical, handoff, and patient-portal views.

## Validation

- `python3 -m py_compile src/pyAppGen/pbcs/electronic_health_records_core/ehr_core_app.py src/pyAppGen/pbcs/electronic_health_records_core/runtime.py src/pyAppGen/pbcs/electronic_health_records_core/services.py src/pyAppGen/pbcs/electronic_health_records_core/routes.py src/pyAppGen/pbcs/electronic_health_records_core/ui.py src/pyAppGen/pbcs/electronic_health_records_core/agent.py src/pyAppGen/pbcs/electronic_health_records_core/release_evidence.py`
- `./.venv/bin/pytest -q src/pyAppGen/pbcs/electronic_health_records_core/tests tests/test_pbc_electronic_health_records_core_runtime.py`
- `python3 - <<'PY'` with `pbc_implementation_release_audit(("electronic_health_records_core",))` and `pbc_generation_smoke_audit(("electronic_health_records_core",))`

## Limits

This is an executable reference slice, not a production persistence layer. It models owned tables and workflows in memory so the PBC can function coherently in isolation without touching shared AppGen-X infrastructure.
