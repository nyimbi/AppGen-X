# Schema Registry and Contract Validation Release Evidence

Directory: `pbcs/schema_registry`

## Implemented Standalone Evidence

- `repository.py` provides an owned-state repository that persists only inside `schema_registry` tables and runtime state.
- `services.py` and `routes.py` expose a standalone command/query surface for runtime configuration, subject onboarding, compatibility checks, payload validation, violation triage, projections, and workbench queries.
- `forms.py` and `wizards.py` define database-backed forms and guided workflows for onboarding, breaking-change review, and release readiness.
- `ui.py` now includes standalone app metadata, controls, forms, wizards, and renderable workbench state.
- `agent.py` contributes an assistant workspace with scoped skills, confirmation requirements, and wizard routing.
- `standalone.py` bootstraps the one-PBC app and loads a demo workspace end-to-end.
- `tests/test_standalone.py` proves the standalone app, repository, forms, and wizard contracts execute together.

## Generated Checks

- stable_manifest
- source_package_directory
- owned_schema_only
- migration_artifact
- model_artifact
- domain_capability_depth
- workflow_coverage
- policy_control_coverage
- automation_loop_coverage
- analytics_coverage
- advanced_domain_not_required
- service_commands
- api_routes
- event_outbox_inbox
- typed_emitted_events
- typed_consumed_events
- idempotent_handlers
- retry_dead_letter_policy
- ui_fragments
- permissions
- configuration_schema
- seed_data
- self_registration_metadata
- contract_tests
