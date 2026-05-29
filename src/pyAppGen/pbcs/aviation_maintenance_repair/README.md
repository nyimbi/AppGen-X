# Aviation Maintenance and Repair PBC

`aviation_maintenance_repair` now exposes a standalone one-PBC maintenance
release-planning slice for AppGen-X. The package stays inside its owned
boundary and executes a full release-to-service workflow using package-local
records, workflow contracts, UI metadata, assistant planning, and release
readiness evidence.

## Standalone Slice

The executable slice covers:

- aircraft intake with tail, type, and subtype release context;
- serialized component eligibility with life limits, release certificate,
  quarantine, and effectivity checks;
- work-card closeout with required signoffs, duplicate inspection,
  authorization, tooling, and consumable checks;
- deferred-defect and AD gating before release;
- document-instruction planning that previews owned-table CRUD mutations;
- human-certifier-only release authorization;
- package-local workbench forms, wizards, controls, and release queues.

## Main Entry Points

- `runtime.py`: package-local state, record intake, document planning, release
  assessment, workbench queries, and release evidence.
- `models.py`: domain-specific model and table contracts for the standalone
  slice.
- `workflows.py`: `release_to_service` and
  `document_instruction_planning` workflow definitions.
- `services.py` and `routes.py`: standalone service and API contracts for the
  slice.
- `ui.py`: workbench fragments, forms, wizards, and controls.
- `agent.py`: governed assistant planning, CRUD previews, and release
  guardrails.
- `release_evidence.py`: executable release-readiness gates and validation.

## Guardrails

All writes and projections stay inside `aviation_maintenance_repair_*` owned
structures. Cross-PBC behavior is limited to declared AppGen-X events only.
The assistant can preview mutations and explain release blockers, but it cannot
certify return-to-service. A human certifier with release authorization is
required for approval.

## Verification

The standalone slice is validated with package-local compile, `unittest`, and
smoke/audit commands from this directory.
