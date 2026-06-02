# Gaming and Casino Operations

`gaming_casino_operations` now exposes both the existing source-package contracts and a package-local standalone one-PBC app slice.

## Standalone package-local app

The standalone surface stays entirely inside `src/pyAppGen/pbcs/gaming_casino_operations`.

Key entrypoints:

- `standalone.GamingCasinoOperationsStandaloneApplication` for a mutable one-PBC app shell.
- `services.GamingCasinoOperationsStandaloneService` for executable patron, table, slot, session, payout, responsible-gaming, and compliance flows.
- `routes.dispatch_standalone_route()` for route-level execution.
- `ui.gaming_casino_operations_standalone_workbench_blueprint()` and `ui.gaming_casino_operations_render_standalone_workbench()` for forms, wizards, controls, and the workbench surface.
- `agent.document_instruction_plan()` and `agent.datastore_crud_plan()` for governed assistant intake and mutation previews.
- `release_evidence.build_release_evidence()` and `standalone.gaming_casino_operations_standalone_app_smoke()` for package-local audit evidence.

## Domain coverage

The slice is centered on:

- patron enrollment review with duplicate detection and restriction semantics
- table opening, inventory movement, and shift close controls
- slot configuration governance and fault recovery
- unified wager sessions and player rating capture
- payout approval, hand-pay, and suspicious-activity escalation
- responsible-gaming intervention and compliance case assembly
- AppGen-X inbox/outbox/dead-letter evidence and idempotent consumed-event handling

## Validation targets

Focused validation for this package should include:

- `src/pyAppGen/pbcs/gaming_casino_operations/tests`
- `pbc_source_artifact_contract("gaming_casino_operations")`
- `pbc_implementation_release_audit(("gaming_casino_operations",))`
- `pbc_generation_smoke_audit(("gaming_casino_operations",))`
