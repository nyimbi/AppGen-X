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
3. Add a standalone one-PBC app surface with local store, services, route dispatch, workbench rendering, agent workspace coverage, release evidence, and focused tests.
4. Add package-owned release evidence, scenario seeds, README documentation, and focused tests that prove the slice works end to end.

## File-Level Plan

- `core.py`
  - Preserve the package-local executable domain core, schema contracts, route metadata, UI/forms/wizards/controls, RBAC, rules, parameters, event helpers, release simulation, and smoke checks.
- `models.py`, `services.py`, `routes.py`, `ui.py`, `agent.py`, `standalone.py`
  - Add a real standalone package-local bundle backed by the existing commercial-controls core.
- `runtime.py`, `events.py`, `handlers.py`, `config.py`, `permissions.py`, `seed_data.py`, `domain_depth.py`
  - Keep wrappers aligned with the executable package-local core and standalone evidence.
- `manifest.py`, `README.md`, `RELEASE_EVIDENCE.md`, `implementation-status.md`
  - Update package metadata and documentation to match the standalone-capable slice.
- `tests/test_contract.py`, `tests/test_standalone.py`
  - Keep focused lifecycle tests and add standalone app/store/service/route/UI/agent coverage.

## Verification Plan

1. Run the package-local pytest modules for `construction_contracts_commercials`.
2. Run a package-local smoke command that exercises runtime, service, route, standalone app, and release evidence entrypoints.
3. Run a syntax-level compilation check across the package.
4. Run focused package audits such as capability assurance and release-evidence validation when available.

## Constraints

- Edit only `src/pyAppGen/pbcs/construction_contracts_commercials`.
- Preserve package entrypoints used by the wider repo.
- Do not add external dependencies.
- Keep all datastore references inside the PBC-owned table boundary.
