# Capital Projects Delivery Implementation Plan

## Selected Improvement Slice

Implement backlog item 1 from `improve1.md`: a governed stage-gate lifecycle for
`capital_project` with executable transition rules, gate approvals, blocked exit
criteria, and lifecycle-aware workbench/detail outputs.

## Why This Slice

- It introduces real domain behavior instead of expanding static contracts.
- It fits the current package boundary without shared-table access.
- It uses existing AppGen-X event types, especially
  `CapitalProjectsDeliveryApproved`, while keeping stream-engine selection hidden.
- It is small enough to complete, verify, and document inside this package.

## Planned Code Changes

- Add pure lifecycle helpers for canonical capital project phases, gate criteria,
  approver-role validation, and transition decisions.
- Extend the runtime state and command/query functions to:
  - create lifecycle-aware capital projects,
  - record gate checklist evidence,
  - approve valid phase transitions,
  - reject invalid or blocked transitions,
  - emit lifecycle-rich AppGen-X approval events,
  - expose lifecycle summaries in workbench/detail outputs.
- Update service/runtime contracts to advertise the new executable slice.
- Add package-local tests for:
  - default lifecycle creation,
  - blocked transition rejection,
  - successful gate approval with event context,
  - backward transition rebaseline enforcement,
  - workbench/detail lifecycle evidence.

## Constraints

- Work only inside `src/pyAppGen/pbcs/capital_projects_delivery`.
- Keep eventing AppGen-X only.
- Keep `stream_engine_picker_visible` false.
- Keep `shared_table_access` false.
- Do not stage, commit, or push.

## Validation Plan

- Run focused package tests under `capital_projects_delivery/tests`.
- Run a package-local compile pass to catch syntax/import regressions.
- Review the diff for contract consistency and remove any review findings before
  writing `README.md` and `implementation-status.md`.
