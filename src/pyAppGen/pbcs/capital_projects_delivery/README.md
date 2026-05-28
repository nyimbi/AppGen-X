# Capital Projects Delivery

`capital_projects_delivery` is a self-contained AppGen PBC for capital project
stage-gate governance inside a single package boundary.

## Implemented Slice

This package now executes a real capital project lifecycle slice:

- create a capital project with a governed default lifecycle stage,
- capture gate checklist evidence through package-local forms,
- approve or reject phase transitions with approver-role controls,
- require a rebaseline reason for backward movement,
- surface gate status in detail and workbench views,
- emit AppGen-X lifecycle events only.

## Single-PBC App Surfaces

The package exposes a one-PBC app contract with:

- database-backed owned tables, migrations, and model contracts,
- forms: intake, gate checklist, gate approval,
- wizards: onboarding and gate approval,
- controls: transition adjacency, exit criteria, rebaseline, approver role,
- services and routes for create, checklist, approval, detail, and workbench,
- UI fragments for workbench, detail, assistant panel, and gate wizard,
- agent help for blocked gates, approvals, rebaselines, and workbench summaries.

## Constraints Kept

- Eventing remains AppGen-X only.
- `stream_engine_picker_visible` remains `False`.
- `shared_table_access` remains `False`.
- All changes stay inside `src/pyAppGen/pbcs/capital_projects_delivery`.

## Validation

Validated with package-local executable tests and smoke checks recorded in
`implementation-status.md`.
