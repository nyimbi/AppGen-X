# Release Evidence - Nonprofit Program Impact

Package directory: `pbcs/nonprofit_program_impact`.

This standalone PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, forms, wizards, controls, assistant skills, permissions, configuration, package metadata, and focused package tests.

## Evidence

- Release evidence contracts materialize schema, service, API, permissions, UI, forms, wizards, controls, assistant, and standalone app sections.
- Owned datastore boundary: every owned table starts with `nonprofit_program_impact_` and cross-PBC collaboration stays on AppGen-X events or declared APIs.
- Standalone app surface: `standalone.py` exercises theory-of-change setup, beneficiary enrollment, service capture, outcomes, evidence packs, donor reports, workbench rendering, and control-center execution.
- Assistant guardrails: mutation previews stay preview-only, require confirmation, and reject foreign-table access.
- Package tests: `tests/test_contract.py` and `tests/test_standalone.py` validate schema/service/release evidence, package metadata, workbench surfaces, and standalone smoke behavior.
