# GL Core Implementation Plan

## Objective

Upgrade `src/pyAppGen/pbcs/gl_core` into a coherent standalone one-PBC general
ledger app package without touching any other PBC or global file.

## Package-Local Workstreams

1. Runtime truth alignment
   - Keep `runtime.py` as the behavioral source of truth for owned tables,
     journal posting, close controls, policy evaluation, AppGen-X eventing,
     and release gates.
   - Align `manifest.py`, `events.py`, `handlers.py`, `config.py`, and
     `permissions.py` to the runtime’s real event topic, permissions, and
     consumed/emitted event types.

2. Standalone repository and app surface
   - Add `repository.py` to provide package-local database write plans and
     stateful persistence helpers for accounts, periods, journal drafts,
     source documents, close snapshots, and reconciliation cases.
   - Add `standalone.py` to bootstrap one-tenant GL state, seed data, consume
     inbound events, prepare journal drafts, post journals, and render the
     workbench shell entirely inside `gl_core`.

3. Stateful service and route execution
   - Upgrade `services.py` and `routes.py` from pure planning metadata to a
     stateful executable facade over the existing runtime functions.
   - Preserve contract evidence, idempotency keys, and the AppGen-X event
     boundary while making routes usable by the standalone app.

4. UI/operator depth
   - Extend `ui.py` with forms, wizards, controls, and standalone navigation
     for chart governance, journal posting, close, reconciliation, and audit
     proof review.
   - Keep workbench rendering deterministic and side-effect-free.

5. Agent/governance/release convergence
   - Strengthen `agent.py` so finance instruction intake resolves to owned
     tables, forms, wizards, routes, permissions, and event expectations.
   - Refresh release evidence and package docs to include standalone and
     repository proof plus the repo-gate proxies:
     `pbc_source_artifact_contract`,
     `pbc_implementation_release_audit`, and
     `pbc_generation_smoke_audit`.

6. Focused verification
   - Add focused package tests for contracts, repository smoke, standalone app
     execution, and repo-gate proxy evidence.
   - Validate by compiling the package, running focused `gl_core` tests, and
     executing relevant `pyAppGen.pbc` contract audits for `gl_core`.
