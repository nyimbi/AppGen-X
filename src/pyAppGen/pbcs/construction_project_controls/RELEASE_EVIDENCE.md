# Release Evidence - Construction Project Controls

Package directory: `src/pyAppGen/pbcs/construction_project_controls`

## Implemented Slice

This release evidence covers the package-local slice built around:

- WBS hierarchy and rollup integrity
- active frozen baseline revisions
- quantity-based progress acceptance with evidence gates
- EV and forecast rollups
- float-threshold exception handling
- governed assistant document-to-draft previews
- release-readiness scorecard and seeded demo scenarios

## Artifact Coverage

- Schema, model, and migration contract: `runtime.py`, `models.py`, `migrations/001_initial.sql`
- Services and route dispatch: `services.py`, `routes.py`
- UI and one-PBC workbench surfaces: `ui.py`, `forms.py`, `wizards.py`, `controls.py`
- Eventing and idempotent handlers: `events.py`, `handlers.py`
- RBAC, rules, and parameters: `permissions.py`, `config.py`
- Assistant preview and CRUD guardrails: `agent.py`
- Seed scenarios and release readiness: `seed_data.py`, `release_evidence.py`

## Evidence Checks

- `schema_models_migrations`: owned construction tables, model contracts, and migration DDL exist and remain package-local.
- `service_api_events_handlers`: service contracts, route contracts, AppGen-X event contracts, and retry/dead-letter behavior are executable.
- `forms_wizards_controls`: one-PBC app surfaces are declared and exposed through the UI contract.
- `wbs_progress_earned_value_slice`: WBS hierarchy, progress acceptance, EV rollups, and float escalation are covered by focused tests.
- `assistant_document_instruction_governance`: document instructions become governed draft previews with confirmation requirements.
- `go_live_scorecard`: readiness categories are computed without cross-PBC coupling.

## Seed Scenarios

- `SEED-ONTRACK`: baseline-frozen project with healthy float and steady progress.
- `SEED-DELAY`: negative-float project that surfaces a critical exception.
- `SEED-CHANGE`: pending commercial exposure affecting forecast.
- `SEED-OVER`: contractor overstatement held in the progress review queue.

## Verification Sources

- `tests/test_contract.py`
- `tests/test_app_slice.py`
- package smoke entrypoints exposed through `__init__.py`, `services.py`, `routes.py`, and `ui.py`

## Known Limitations

- The package executes as in-memory, side-effect-free facades rather than a mounted web application.
- `SPECIFICATION.md` was not fully narrowed to the slice, so it may describe broader ambition than the implemented behavior.
