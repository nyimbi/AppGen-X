# Defense Readiness Logistics PBC

`defense_readiness_logistics` is a standalone AppGen-X Packaged Business Capability for unit readiness, mission assets, maintenance, supply, deployment kits, movement control, and release governance.

When composed by itself, it is expected to produce a working domain application: users can configure the PBC, open a readiness workbench, enter records through forms, follow guided wizards, enforce blocking controls, ask the PBC assistant for help, intake operational documents, and execute database-backed service commands against PBC-owned records.

## Owned Boundary

The PBC owns only `defense_readiness_logistics_*` tables. It covers readiness, assets, supply, maintenance, deployment, inspections, movements, personnel qualifications, ammunition lots, fuel allocations, load plans, theater support, controlled custody, readiness exceptions, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X inbox/outbox/dead-letter events.

Ordinary database backends are limited to PostgreSQL, MySQL, and MariaDB. Eventing uses the AppGen-X event contract; generated users do not choose a stream engine.

## Executable Capabilities

- Assess unit readiness across personnel, certifications, assets, supplies, ammunition, fuel, and inspection evidence.
- Register mission assets with serviceability, serial or lot traceability, controlled-item markers, and availability windows.
- Project maintenance status using fault codes, required parts, available parts, deferred faults, projected return, confidence, and readiness impact.
- Score supply readiness from demand, on-hand stock, in-transit stock, approved substitutes, ammunition restrictions, and fuel availability.
- Validate deployment kit completeness, critical missing items, and expiration blockers.
- Plan logistics movement by mode, including convoy route review, airlift weight checks, sealift dangerous-goods documents, hazardous load segregation, controlled-item custody, fuel plan gaps, and asset double-booking.
- Release deployment plans only when readiness, kit, movement, and blocking exceptions are clear.
- Build commander, maintenance, supply, movement, classified review, and exception queues.

## UI and Assistant

The PBC exposes forms for readiness assessment, mission assets, maintenance projections, supply readiness, deployment kits, movement orders, deployment release, and controlled custody.

It exposes wizards for readiness validation, mission capability rollup, deployment release, maintenance recovery, movement order approval, and first-run single-PBC launch.

The assistant contributes PBC-scoped skills to the composed single agent. It can route movement orders, maintenance narratives, supply shortage memos, asset records, and readiness reports into mutation previews with stable document digests, citations required, AppGen-X event evidence, and human confirmation before datastore changes.

## Release Evidence

Release evidence covers schema, migrations, models, services, APIs, events, handlers, UI, forms, wizards, controls, assistant skills, governance, retry/dead-letter behavior, and the single-PBC app smoke test.

Run package checks with:

```bash
python3 -m py_compile src/pyAppGen/pbcs/defense_readiness_logistics/*.py src/pyAppGen/pbcs/defense_readiness_logistics/tests/*.py
./.venv/bin/pytest -q src/pyAppGen/pbcs/defense_readiness_logistics/tests
```
