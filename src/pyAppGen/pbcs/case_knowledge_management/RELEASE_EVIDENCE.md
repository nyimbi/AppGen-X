# Case and Knowledge Management Release Evidence

## Evidence Scope

This PBC now contains a package-local executable one-slice app for support case and knowledge operations at `src/pyAppGen/pbcs/case_knowledge_management`. The evidence below is tied to the owned package implementation only.

## Proven Areas

- Owned schema covers support, queueing, SLA, escalation, knowledge, article quality, freshness, governed models, and AppGen-X event tables.
- `application.py` executes a full case-to-knowledge lifecycle using only package-local state.
- Services, routes, handlers, UI contracts, configuration, RBAC, and agent helpers all wrap the same runtime.
- Governed CRUD rejects foreign tables and requires confirmation for mutations.
- Event handling records inbox/dead-letter evidence and supports idempotent replay handling.
- Focused tests cover contract integrity, runtime workflow behavior, route/service dispatch, and governance boundaries.

## Key Runtime Scenarios

- Create, classify, route, assign, and resolve a support case.
- Publish and version a knowledge article.
- Capture feedback and score article quality.
- Generate next-best-resolution recommendations with citations.
- Handle supported incoming AppGen-X events and dead-letter unsupported ones.

## Validation Entry Points

- `release_evidence.py`
- `tests/test_contract.py`
- `tests/test_app_slice.py`
