# Release Evidence - Airline Operations Control

Package directory: `src/pyAppGen/pbcs/airline_operations_control`.

## Delivered Standalone Slice

This package now targets a standalone one-PBC OCC workbench with package-local runtime, services, routes, UI, assistant planning, permissions, and release evidence. The slice stays within AppGen-X eventing, only uses `airline_operations_control_` owned tables, and keeps all executable behavior inside the package.

## Evidence Categories

- Schema and models: owned-table-only schema contract and model metadata for all business and event tables.
- Services and routes: package-local stateful service facade plus dispatchable standalone API routes.
- UI and workflows: role-aware workbench, forms, wizards, controls, attention queue, turn watchlist, and recovery workflow scaffolding.
- Assistant planning: document-instruction parsing, candidate-table selection, and governed CRUD previews.
- Permissions and governance: action-permission mapping, role bundles, configuration defaults, bounded parameters, and rule compilation.
- Events and handlers: AppGen-X emitted/consumed event contracts, idempotent handler behavior, and dead-letter evidence.

## Scenario Packs

- `on_time_rotation`: proves canonical leg timeline plus stable tail continuity.
- `late_inbound_broken_turn`: proves minimum-turn watchlist and prioritized attention queue.
- `diversion_and_return_to_gate`: proves branch-aware timeline handling under disruption.
- `ferry_recovery_leg`: proves recovery-oriented leg variants remain coherent in the tail graph.

## Validation Sources

Release readiness is backed by:

- package-local contract tests under `src/pyAppGen/pbcs/airline_operations_control/tests`
- runtime/service/route/release smoke checks in package code
- focused compile and compileall checks for the package
- package-local audit calls for capability assurance, route contract validation, release evidence validation, and standalone smoke

## Boundary Evidence

- Every owned table starts with `airline_operations_control_`.
- Shared-table mutation is forbidden.
- Cross-PBC collaboration is represented only through declared AppGen-X events or explicit API contracts.
- Assistant CRUD planning rejects foreign tables before mutation planning proceeds.
