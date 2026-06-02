# Insurance Claims and Policy Release Evidence

The package directory `pbcs/insurance_claims_policy` now contains a coherent standalone PBC slice rather than disconnected scaffolding.

## Evidence

- Owned schema, models, and migration are aligned to the package-local insurance policy, claims, reserve, settlement, fraud, recovery, governance, and AppGen-X event tables.
- `standalone.py` provides executable package-local workflows for policy issuance, FNOL, coverage determination, reserve management, adjudication, settlement, communication, fraud review, and recovery.
- `services.py` and `routes.py` expose route-bound service operations without leaving the package-owned datastore boundary.
- `events.py` and `handlers.py` preserve AppGen-X outbox, inbox, idempotency, retry, and dead-letter behavior.
- `ui.py` exposes forms, wizards, controls, and a command-center workbench for the standalone app surface.
- `agent.py` provides document-intake, coverage reasoning, settlement planning, and governed CRUD previews.
- `release_evidence.py` verifies docs, schema/service/route/event/UI/agent/governance contracts, and standalone smoke readiness.
