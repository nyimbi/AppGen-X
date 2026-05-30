# Privacy Consent Governance Release Evidence

The package directory `pbcs/privacy_consent_governance` contains the standalone one-PBC application surface, owned schema and migration, package-local services and routes, AppGen-X eventing, UI/workbench wiring, AI planning surfaces, seed bundle, and focused tests.

## Evidence

- Owned tables are all under the `privacy_consent_governance_` prefix and foreign datastore mutation is rejected.
- The standalone app exposes forms, wizards, controls, and package-local workbench routes for consent, rights, policy, and release flows.
- Services expose command/query contracts with owned datastore plus outbox transaction boundaries only.
- Events use the AppGen-X outbox, inbox, retry, idempotency, and dead-letter contract.
- Agent skills support document intake, instruction planning, and governed CRUD previews scoped to owned tables only.
- Release readiness is executable through `pbc_spec_smoke_audit()`, `pbc_source_artifact_contract()`, `pbc_implementation_release_audit()`, and `pbc_generation_smoke_audit()`.
