# Implementation Plan

## Selected Slice

Implement executable maintenance release governance for
`aviation_maintenance_repair`, using the backlog areas around work-card
signoff, component life/traceability, tooling and consumables, deferred
defects, technician authorization, and release-to-service packs.

## Code Plan

- Add a pure `maintenance_release.py` module that evaluates:
  - component installation eligibility from remaining life, release documents,
    quarantine state, and effectivity;
  - work-card closeout from required signatures, duplicate inspection,
    technician authorizations, tooling calibration, consumable shelf life, and
    open non-routine links;
  - release-to-service pack readiness from closed work cards, deferred defect
    expiry, airworthiness directive compliance, component eligibility, and
    human certifier evidence.
- Wire the release pack into `runtime.py` with package-local state,
  `aviation_maintenance_repair_assess_release_to_service`, workbench
  projections, service contract exposure, runtime smoke, and release evidence.
- Expose the release pack in `services.py`, `ui.py`, and `agent.py` without
  introducing shared-table access or stream-engine selection.
- Add focused tests proving accepted and blocked release packs, component
  lockout, work-card signoff governance, UI/service/agent exposure, and release
  evidence.

## Review Criteria

- All new functions are deterministic and side-effect-free except runtime state
  returned by command functions.
- All records remain inside `aviation_maintenance_repair_*` owned tables.
- Release events use the declared AppGen-X event contract only.
- AI assistance can preview and explain evidence but cannot certify release
  without human certifier input.

