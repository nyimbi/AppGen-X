# Aviation Maintenance and Repair PBC

This PBC owns aircraft maintenance, serialized components, work cards,
maintenance visits, airworthiness directives, deferred defects, compliance
release evidence, workbench surfaces, and governed agent assistance for
maintenance repair operations.

## Implemented Executable Slice

The current implementation adds a release-to-service governance engine in
`maintenance_release.py`. It evaluates whether an aircraft or component can be
released using executable evidence rather than generic status text.

Implemented behavior includes:

- component remaining-life checks for hours and cycles;
- release certificate and shelf-life validation;
- quarantine and effectivity lockout before installation or release;
- work-card closeout validation with required signoff roles;
- duplicate inspection enforcement that blocks self-inspection;
- technician authorization checks by task family and aircraft type;
- controlled tooling return and calibration checks;
- consumable shelf-life and mix-life checks;
- deferred defect countdown and expiry blocking;
- airworthiness directive compliance blocking;
- human certifier requirement for release-to-service;
- AppGen-X outbox events for approved and blocked release packs;
- workbench release queue projection;
- service/UI/agent/release-evidence exposure.

## Runtime Boundary

All state is held inside package-local runtime structures and maps to
`aviation_maintenance_repair_*` owned tables. The PBC does not read or mutate
external inventory, dispatch, audit, or identity tables. Eventing uses the
AppGen-X event contract only.

## Agent Guardrails

The assistant can intake documents, preview release evidence, and explain
blockers, but it cannot certify maintenance release. Final release evidence
requires a human certifier with release authorization.

## Verification

Focused tests cover complete release approval, blocked safety and authorization
gaps, standalone component and work-card evaluators, and service/UI/agent/release
evidence exposure.

