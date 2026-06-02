# Professional Services Automation Release Evidence

The package directory `pbcs/professional_services_automation` contains the executable PBC implementation, manifest, schema, migrations, models, services, API routes, AppGen-X events, idempotent handlers, UI workbench fragments, standalone app shell, forms, wizards, controls, permissions, configuration, rules, parameters, seed data, agent skills, and focused tests.

## Evidence

- Owned tables stay under the `professional_services_automation_` prefix and foreign datastore mutation is rejected.
- Runtime and domain-depth contracts remain AppGen-X-only with no shared-table mutation.
- Standalone workbench metadata exposes engagement, staffing, delivery, billing, and release surfaces.
- Forms, wizards, and controls are package-local and release-gated through `release_evidence.py`.
- Documentation artifacts `README.md`, `implementation-plan.md`, `implementation-status.md`, and `RELEASE_EVIDENCE.md` are required by release readiness validation.
- Focused package tests cover standalone validation, UI wiring, control evidence, and release evidence completeness.
