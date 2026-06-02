# Medical Device Lifecycle Standalone Implementation Plan

## Goal

Turn `medical_device_lifecycle` into a coherent standalone one-PBC slice that exercises realistic biomedical engineering operations without touching shared AppGen-X generator code. The slice must stay package-local, preserve the owned-table boundary, and make device registration, assignment, calibration, maintenance, recall, usage traceability, regulatory evidence, and governed assistant previews executable.

## Scope

- Limit all edits to `src/pyAppGen/pbcs/medical_device_lifecycle`.
- Keep AppGen-X eventing and owned-table naming intact.
- Add only package-local documents, UI surfaces, tests, and standalone runtime composition.

## Domain Slice

The standalone slice will model the highest-risk medical device control loop:

1. Device registry and qualification
   - Capture unique device identity, model, serial, lot, firmware, risk class, implantable status, current department/location, and qualification status.

2. Assignment and point-of-care readiness
   - Prevent assignment when the device is recalled, quarantined, maintenance-bound, or calibration overdue.
   - Keep patient-linked assignments preview-only and permission-aware in assistant flows.

3. Calibration and maintenance control
   - Record calibration outcomes, next due dates, out-of-tolerance impacts, maintenance completion, and return-to-service gating.

4. Recall containment and regulatory evidence
   - Match recalls by device, model, lot, or firmware.
   - Surface recall hold queues, evidence gaps, and notification/remediation workbench views.

5. Governed assistant and release evidence
   - Infer likely forms, wizards, and route previews from recall letters, maintenance notes, calibration packets, and evidence documents.
   - Prove package-local forms/wizards/controls/standalone coverage in release evidence and tests.

## Work Items

1. Add package-local operational surfaces
   - Create `forms.py`, `wizards.py`, and `controls.py` with biomedical-engineering-specific forms, guided flows, and control assertions.

2. Build a standalone app shell
   - Add `standalone.py` with an in-memory app that supports device registration, assignment, calibration, maintenance, recalls, usage traces, regulatory evidence, policy/runtime updates, workbench rendering, and assistant preview dispatch.

3. Wire package metadata and assistant composition
   - Update `__init__.py`, `agent.py`, `ui.py`, `manifest.py`, and `release_evidence.py` to expose the new standalone surface and package-local artifacts.

4. Strengthen focused verification
   - Add focused tests for assignment gating, recall containment, release evidence completeness, and standalone route/workbench execution.

## Non-Goals

- No edits to central DSL, shared generator, language files, or progress ledgers.
- No cross-PBC schema access or shared-table reads.
- No new third-party dependencies.

## Verification Plan

- Compile modified package modules with `python -m py_compile`.
- Run package-local pytest for `src/pyAppGen/pbcs/medical_device_lifecycle/tests`.
- Run focused smoke/audit snippets for standalone app, UI contract, assistant workspace, and release evidence.
