# Construction Contracts and Commercials Implementation Plan

## Scope

Implement this PBC as a package-local, executable construction contracts and commercials slice without touching shared generator code, central DSL surfaces, or other PBCs.

## Outcome Targets

1. Replace scaffold-style placeholder behavior with domain-specific contract-commercial logic for:
   - contract lifecycle and schedule-of-values validation
   - pay application intake, certification, retainage, waivers, and payment certificate traces
   - variation orders, notice timeliness, and commercial claims
   - subcontract commercial compliance, workbench queues, and final account blockers
2. Keep existing package entrypoints stable while making the slice executable through package-local runtime, services, routes, UI, RBAC, config, events, handlers, and agent helpers.
3. Add package-owned release evidence, scenario seeds, README documentation, and focused tests that prove the slice works end to end.

## File-Level Plan

- `core.py`
  - Add the package-local executable domain core, schema contracts, route metadata, UI/forms/wizards/controls, RBAC, rules, parameters, event helpers, release simulation, and smoke checks.
- `runtime.py`
  - Re-export the executable core through the existing runtime entrypoints expected by the package.
- `services.py`, `routes.py`, `ui.py`, `agent.py`, `config.py`, `permissions.py`, `events.py`, `handlers.py`, `seed_data.py`, `domain_depth.py`
  - Convert wrappers to domain-specific behavior backed by the shared package-local core.
- `manifest.py`, `migrations/001_initial.sql`, `README.md`, `RELEASE_EVIDENCE.md`, `implementation-status.md`
  - Update package metadata and documentation to match the implemented slice.
- `tests/test_contract.py`
  - Replace shallow scaffold assertions with focused lifecycle, controls, workbench, agent, event, and release tests.

## Verification Plan

1. Run the package-local pytest module for `construction_contracts_commercials`.
2. Run a package-local smoke command that exercises runtime, service, route, and release evidence entrypoints.
3. Run a syntax-level compilation check across the package.

## Constraints

- Edit only `src/pyAppGen/pbcs/construction_contracts_commercials`.
- Preserve package entrypoints used by the wider repo.
- Do not add external dependencies.
- Keep all datastore references inside the PBC-owned table boundary.
