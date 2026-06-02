# Release Evidence - Trade Finance Operations

Directory: `pbcs/trade_finance_operations`

Generated checks:
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
- forms_wizards_controls
- standalone_workflows
- release_evidence_pack
- contract_tests

Verification snapshot:
- `python3 -m compileall src/pyAppGen/pbcs/trade_finance_operations` -> success
- `PYTHONPATH=src python3 - <<'PY' ... direct test function runner ... PY` -> 13 focused test functions executed without assertion failures
- `PYTHONPATH=src:src/pyAppGen/pbcs/trade_finance_operations/_audit_vendor python3 - <<'PY' ... focused trade_finance_operations repo audits ... PY` -> source, source-runtime-tests, package-local-assurance, specification, agent, implementation, implemented-capability, and generation all returned `True`
- `git diff --check` -> clean
