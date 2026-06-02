# Environment Health and Safety Standalone Slice

This package now contains a package-local standalone implementation for the `environment_health_safety` PBC. It does not depend on shared generators for domain behavior.

## What is included

- Owned schema, migration, and model metadata for incidents, hazards, inspections, permits, corrective actions, training, audits, rules, parameters, schema extensions, control assertions, governed models, and AppGen-X event tables.
- Executable in-memory services for serious-incident lifecycle gates, notification clocks, near-miss hazard promotion, corrective action effectiveness, inspection sync, permit conflict checks, policy re-evaluation, audit sealing, KPI reprioritization, and continuous control testing.
- Route, event, handler, UI, form, wizard, control, workflow, and agent contracts derived from the same local metadata.
- Seeded release evidence and focused package tests.

## Standalone focus

The current slice goes deep on the operational loop around incident response, hazard prevention, permit coordination, inspection capture, corrective actions, and governance evidence. It intentionally avoids shared generator files and keeps all mutations inside `environment_health_safety_*` tables.
