# Cybersecurity Operations Center

Package-local standalone PBC for SOC workflows inside `src/pyAppGen/pbcs/cybersecurity_operations_center`.

## What This Package Owns

- owned schema and migration DDL for alerts, incidents, threat intel, playbooks, containment, evidence, policy/rule/parameter state, governed models, and AppGen-X event tables
- executable runtime commands and queries for alert lifecycle, incident promotion, evidence custody, containment approvals, playbook stages, workbench projections, case detail graphs, and handoff packets
- service and route contracts for command/query access
- UI/workbench metadata including forms, wizards, controls, supervisor lane, evidence-review lane, and assistant panel
- governed agent/document planning and owned-table-only CRUD previews
- focused tests and release evidence

## Core Flows

1. Ingest a detection-aware alert with deduplication and lineage.
2. Enrich and triage the alert through the supported lifecycle.
3. Promote a cluster into an incident with explainable scoring.
4. Record evidence with chain-of-custody state and sealing readiness.
5. Create containment actions with approval boundaries.
6. Simulate staged playbook runs with human breakpoints.
7. Render workbench lanes, case detail graph, and shift handoff output.

## Primary Modules

- `models.py` — typed owned models, lifecycle rules, table metadata, SQL definitions
- `runtime.py` — executable state machine and release/runtime smoke
- `services.py` — package-local service façade
- `routes.py` — HTTP-style route contract and dispatch
- `ui.py` — workbench/detail/forms/wizards/controls contracts
- `events.py` / `handlers.py` — AppGen-X event envelopes and consumed-event handling
- `agent.py` — governed assistant and CRUD/document planning
- `standalone.py` — executable one-PBC app manifest, bootstrap, and demo workspace
- `tests/` — focused contract, workflow, and standalone tests

## Local Validation

Use package-local validation from this directory:

```bash
python3 -m compileall .
PYTHONPATH=/Volumes/Media/src/pjs/appgen/src python3 -m unittest tests.test_contract tests.test_workflows tests.test_standalone
```

## Requested Gate Coverage

- `pbc_source_artifact_contract`
- `pbc_implementation_release_audit`
- `pbc_generation_smoke_audit`

See [implementation-plan.md](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/cybersecurity_operations_center/implementation-plan.md) and [RELEASE_EVIDENCE.md](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/cybersecurity_operations_center/RELEASE_EVIDENCE.md) for the exact mapping.
