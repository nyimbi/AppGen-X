# Implementation Status

## Complete In This Slice

- owned-model contract layer with typed records and explicit SQL definitions
- executable runtime for:
  - alert intake with first-class detection context
  - deduplication and correlation lineage
  - alert enrichment, triage, suppression, and lifecycle transitions
  - incident promotion preview and creation
  - asset exposure review
  - threat intel approval with recommendation preview
  - staged playbook execution with breakpoints
  - containment approval boundaries
  - response evidence chain-of-custody capture
  - AppGen-X inbox/outbox/dead-letter handling
  - workbench, case detail graph, handoff packet, and backlog risk assessment
- service contracts and route dispatch for the package-local app surface
- UI/workbench contracts with forms, wizards, controls, supervisor lane, and evidence-review lane
- governed agent/document planning and owned-table-only CRUD preview
- standalone one-PBC app manifest, bootstrap, demo workspace, and render helpers
- focused contract, workflow, and standalone tests
- package-local docs:
  - `README.md`
  - `implementation-plan.md`
  - `RELEASE_EVIDENCE.md`
  - `SPECIFICATION.md`

## Intentionally Deferred

- external SIEM/SOAR integrations
- background scheduling for intel expiry or retention purges
- true persistent datastore adapters beyond owned schema/migration contracts and executable in-package runtime state
- richer anomaly-detection models beyond current explainable risk heuristics
- full evidence-request sub-entity modeling

## Remaining Risks

- Runtime persistence is modeled in package-local state rather than a live database adapter.
- The package proves route/service/runtime behavior through focused tests, not through a running HTTP server.
- Release evidence depends on package-local smoke/tests; repo-global audit wrappers were not modified because scope was explicitly limited to this package.

## 2026-05-30 improve1 SOC-Control Execution Slice

- Added `soc_control.py` as the side-effect-free executable proof layer for all 50 SOC improve1 backlog items.
- Bound each feature to owned SOC tables, AppGen-X event lineage, UI fragment, service/API route, permission, agent skill, configuration guardrails, retry/dead-letter evidence, and release evidence.
- Wired SOC controls into runtime capabilities, runtime smoke, release evidence, UI contracts, traceability artifacts, and focused package tests.
