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
- focused contract and workflow tests
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
