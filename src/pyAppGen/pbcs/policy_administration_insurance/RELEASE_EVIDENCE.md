# Release Evidence - Insurance Policy Administration

Package directory: `pbcs/policy_administration_insurance`.

This package now includes the original runtime/schema/service/event surface plus a package-local standalone one-PBC application harness, explicit UI forms/wizards/controls, assistant workspace planning, and package-local documentation evidence.

## Evidence

- Runtime evidence: schema, service, route, event, handler, UI, agent, and governance contracts are materialized.
- Standalone evidence: `standalone.py` composes runtime, UI, agent, and release readiness into a package-local standalone app surface.
- UI evidence: issuance, coverage, endorsement, renewal, cancellation, billing, document, and AppGen-X inbox forms are paired with insurance workflow wizards and operator controls.
- Documentation evidence: `README.md`, `implementation-plan.md`, `implementation-status.md`, `SPECIFICATION.md`, and this file are validated by release evidence helpers.
- Test evidence: `tests/test_contract.py` and `tests/test_standalone.py` cover contract integrity and standalone execution.
