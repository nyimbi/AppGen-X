# Accounts Receivable and Credit Release Evidence

Directory: `pbcs/ar_credit`

Current release surface covers:
- Owned AR runtime schema, service, API, permissions, and workflow slice.
- AppGen-X event contract, inbox/outbox/dead-letter evidence, and idempotent
  handlers.
- Standalone app shell, SQLite repository, and package-local workbench render.
- Domain forms, guided wizards, operational controls, and assistant previews.
- Seeded demo workspace used by smoke validation and release evidence checks.
- Package-local contract tests for repository, standalone UI surface, and
  release readiness.

Primary dynamic checks are produced by `release_evidence.py` and include:
- `owned_schema_depth`
- `migration_per_owned_table`
- `service_command_depth`
- `api_event_contract`
- `permissions_cover_commands`
- `backend_allowlist`
- `no_shared_table_access`
- `workflow_slice_execution`
- `service_workflow_surface`
- `ui_workflow_surface`
- `agent_preview_surface`
- `forms_present`
- `wizards_present`
- `controls_present`
- `standalone_surface`
- `repository_surface`
- `control_center_surface`
