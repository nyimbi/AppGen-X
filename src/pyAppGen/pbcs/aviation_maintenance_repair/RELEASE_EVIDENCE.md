# Release Evidence - Aviation Maintenance and Repair

Package directory: `pbcs/aviation_maintenance_repair`.

This standalone slice now proves one executable maintenance release workflow
inside the PBC boundary.

## Executable Evidence

- Schema and models: domain-specific model contracts exist for aircraft,
  components, work cards, deferred defects, airworthiness directives,
  compliance releases, and package governance records.
- Workflows: `release_to_service` and `document_instruction_planning` are
  executable package-local workflows with named wizard steps.
- Services and routes: standalone service operations and API route contracts are
  aligned to aircraft intake, component/work-card updates, document planning,
  release planning, and workbench queries.
- UI surface: workbench metadata exposes forms, wizards, controls, queues, and
  release panels for the standalone slice.
- Assistant guardrails: document-intake planning previews owned-table CRUD
  mutations and explicitly blocks assistant self-certification.
- Eventing and handlers: AppGen-X event envelopes, outbox/inbox/dead-letter
  tables, and idempotent consumed-event handlers are package-local and
  executable.
- Release governance: component airworthiness, work-card closeout, deferred
  defects, AD compliance, and human-certifier gates produce deterministic
  blocker evidence.

## Validation

- `python3 -m compileall .`
- `python3 -m unittest discover .../aviation_maintenance_repair/tests -p 'test_*.py'`
- package/runtime/release/capability smoke functions all returned `True`

## Boundary Proof

All owned tables begin with `aviation_maintenance_repair_`. Cross-PBC behavior
is limited to declared AppGen-X events. No shared generator, DSL, or external
progress-ledger files were modified for this slice.
