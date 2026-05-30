# AP Automation Slice

`ap_automation` is a standalone AppGen-X PBC for accounts payable automation. It owns vendor readiness, invoice intake, matching, approval-aware payment scheduling, payment release, remittance, statement reconciliation, and the supporting AppGen-X event/runtime surfaces.

## Executable surfaces

- `runtime.py`
  Domain workflows for vendor onboarding, bank/tax validation, invoice capture, matching, scheduling, batching, payment execution, remittance, reconciliation, risk, controls, and release evidence.
- `repository.py`
  Owned-table repository bindings for vendor, invoice, payment-release, and statement datasets that back forms, wizards, controls, and the workbench.
- `forms.py`
  Database-backed forms for vendor onboarding, invoice capture, payment batch release, and statement reconciliation.
- `wizards.py`
  Guided vendor onboarding, invoice intake, payment release, and statement-reconciliation flows.
- `controls.py`
  AP control assertions for vendor readiness, duplicate holds, payment-batch integrity, reconciliation visibility, and AppGen-X event contract lock.
- `services.py`, `routes.py`, `events.py`, `handlers.py`
  Executable service/route/event surfaces and handler contracts that stay within `ap_automation_*` owned tables plus AppGen-X inbox/outbox/dead-letter tables.
- `agent.py`
  Assistant contribution for repository lookup, form guidance, wizard planning, control interpretation, and governed CRUD.
- `ui.py`
  Workbench, forms hub, wizard hub, and controls hub contracts.

## How to exercise it

1. Configure a runtime with `ap_automation_configure_runtime(...)`.
2. Load parameters/rules with `ap_automation_set_parameter(...)` and `ap_automation_register_rule(...)`.
3. Use `repository_demo_state()` for a deterministic AP state envelope.
4. Render database-backed forms with `render_form(...)`.
5. Execute guided flows with `execute_wizard(...)`.
6. Validate the owned-scope control stack with `controls.smoke_test()` and `release_evidence.smoke_test()`.

## Scope boundary

- Writes remain inside `ap_automation_*` tables and runtime state.
- Eventing remains locked to AppGen-X on `appgen.ap.events`.
- No shared-table access or cross-PBC rewrites are introduced.
