# Insurance Claims Policy Standalone Slice

This package now includes a package-local standalone application for `insurance_claims_policy`.

The slice stays inside `src/pyAppGen/pbcs/insurance_claims_policy` and owns:
- executable policy issuance, coverage, claims, reserve, adjudication, settlement, fraud, and recovery workflows
- package-local schema, models, migration, service contracts, routes, AppGen-X events, handlers, and governance
- role-aware forms, wizards, controls, workbench rendering, and assistant/document-intake plans
- release evidence, package metadata, focused tests, and standalone smoke coverage

Primary entrypoints:
- `standalone.InsuranceClaimsPolicyStandaloneApp` for one-PBC execution
- `services.InsuranceClaimsPolicyService` for route-bound service execution
- `ui.insurance_claims_policy_standalone_app_contract` and `ui.insurance_claims_policy_render_workbench`
- `release_evidence.build_release_evidence` for auditable readiness checks

The implementation uses only package-owned `insurance_claims_policy_` tables and AppGen-X inbox/outbox/dead-letter tables. Cross-PBC collaboration is represented through declared events, not shared-table mutation.
