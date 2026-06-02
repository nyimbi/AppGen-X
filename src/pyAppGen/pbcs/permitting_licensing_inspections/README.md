# Permitting Licensing and Inspections

`permitting_licensing_inspections` is now a standalone AppGen-X packaged
business capability for permit and license intake, discipline review, fee
assessment, issuance, inspections, violations, due-process notices, renewals,
and citizen-facing coordination.

## What This Package Provides

- A package-local runtime with governed intake completeness checks, plan-set
  version history, review routing, fee simulation, issuance holds, inspections,
  violations, and renewal decisions.
- A standalone one-PBC app surface in `standalone.py` that bootstraps demo
  state, renders the workbench shell, dispatches package routes, and exposes
  release and agent manifests.
- Explicit `forms.py`, `wizards.py`, and `controls.py` contracts for intake,
  resubmittal, inspections, renewals, and due-process timeline handling.
- Updated package exports in `__init__.py`, `manifest.py`, `ui.py`,
  `agent.py`, and `release_evidence.py` so standalone surfaces are discoverable
  without touching shared generator code.

## Key Entrypoints

- Runtime: `runtime.py`
- Standalone app: `standalone.py`
- UI/workbench: `ui.py`
- Forms/wizards/controls: `forms.py`, `wizards.py`, `controls.py`
- Routes/services: `routes.py`, `services.py`
- Agent planning: `agent.py`
- Release audit: `release_evidence.py`

## Validation

Focused package validation lives in `tests/test_contract.py`,
`tests/test_standalone.py`, `implementation-status.md`, and
`RELEASE_EVIDENCE.md`.
