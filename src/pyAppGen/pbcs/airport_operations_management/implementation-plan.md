# Airport Operations Management Implementation Plan

## Objective

Make `airport_operations_management` usable as a standalone one-PBC airport operations center covering gates, stands, slots, runway/taxiway constraints, turnarounds, baggage, passenger flows, deicing, safety controls, disruptions, command-board views, and governed assistant support.

## Plan

1. Preserve the package boundary under `src/pyAppGen/pbcs/airport_operations_management` and keep all external AODB, ATC, weather, baggage-system, common-use, airline, and audit inputs as AppGen-X event/API projections.
2. Add a package-local standalone app contract with explicit forms, wizards, controls, route contracts, DSL exposure, seeded operating scenarios, and a go-live drill simulation.
3. Implement executable domain primitives for turnaround milestone graphs, remote-stand bussing, deicing queues, A-CDM slot reconciliation, baggage contingency, passenger-flow capacity forecasting, disruption playbooks, gate-change impact previews, assistant planning, boundary guardrails, and drill scorecards.
4. Connect the standalone surface into package `__init__`, UI, routes, agent, and release evidence so generated apps can discover it.
5. Add focused tests proving the forms/wizards/controls cover all 50 improve1 backlog items, the operating primitives execute, boundaries reject foreign tables, the assistant is citation/confirmation gated, and package smoke/release evidence include the standalone app.

## Verification

Run package compile, package tests, focused PBC audits, and diff hygiene checks before commit. Live database execution remains out of scope for this slice; database support is represented by migrations/contracts for PostgreSQL, MySQL, and MariaDB.
