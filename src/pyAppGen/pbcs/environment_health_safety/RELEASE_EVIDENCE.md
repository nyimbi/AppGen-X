# Release Evidence - Environment Health and Safety

Package directory: `pbcs/environment_health_safety`.

## Included evidence

- Standalone domain engine: `standalone.py` derives contracts, services, handlers, UI, and release checks from one package-local source.
- Schema alignment: owned table metadata, migration DDL, and model contracts describe the same owned boundary.
- Operational evidence: seeded workbench queues demonstrate severity, recordability, notification clocks, hazard promotion, permit issue, and corrective action evidence.
- Governance evidence: policy change, audit sealing, KPI reprioritization, and dead-letter handling are idempotent and package-owned.
- Release docs: `SPECIFICATION.md`, `README.md`, and `implementation-status.md` are part of release readiness.

## Focused verification targets

- Incident closure gate blocks invalid closure.
- Serious notification clocks and acknowledgements are tracked.
- Near-miss cluster promotion creates hazard lineage.
- Permit conflict matrix blocks overlapping conflicting permits.
- Consumed events remain idempotent and domain-specific.
