# API Gateway Mesh Implementation Plan

## Scope

- Keep changes inside `src/pyAppGen/pbcs/api_gateway_mesh` and `tests/test_pbc_api_gateway_mesh_implementation.py`.
- Preserve AppGen-X-only eventing and owned-table-only boundaries.
- Strengthen executable behavior instead of adding docs-only surface.

## Backlog Items Selected

1. Route publication safety case
2. Host, path, and method collision analysis
3. Agent-assisted incident triage

## Planned Code Changes

- Extend `runtime.py` with deterministic route collision analysis and a route publication safety case used by `publish_route`.
- Upgrade `services.py` and `routes.py` so the service/route layer can execute runtime functions when explicit state is supplied, while preserving side-effect-free planning mode.
- Align `permissions.py`, `events.py`, and `handlers.py` with the runtime AppGen-X contract and owned dead-letter/inbox/outbox tables.
- Expose safety-case and incident-triage surfaces through `ui.py`, `agent.py`, and `release_evidence.py`.
- Add focused implementation tests for runtime execution, collision blocking, safety-case evidence, route dispatch, handler execution, and release readiness.

## Verification Plan

- Run targeted Python import/execution checks with `PYTHONPATH=src`.
- Run the package-local runtime/contract tests and the new implementation test with `uv run pytest`.
- Re-check changed files for boundary, eventing, and contract mismatches.
