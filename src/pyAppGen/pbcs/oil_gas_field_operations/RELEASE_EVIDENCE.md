# Release Evidence - Oil and Gas Field Operations

Package directory: `pbcs/oil_gas_field_operations`.

This standalone PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, forms, wizards, controls, agent skills, standalone app composition, permissions, configuration, package metadata, side-effect-free registration, and focused package tests.

## Evidence

- Release evidence is executable through [release_evidence.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/release_evidence.py) and includes forms, wizards, controls, assistant preview, standalone contract, standalone smoke, and docs presence.
- Owned datastore boundary remains package-local: every owned table starts with `oil_gas_field_operations_` and cross-PBC collaboration still uses AppGen-X events or declared APIs.
- The standalone app in [standalone.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/standalone.py) exercises well registration, daily production capture, field ticket triage, workover readiness, HSE logging, and morning review.
- Package tests under `tests/test_contract.py`, `tests/test_app_surface.py`, and `tests/test_standalone_app.py` cover release evidence, routes, services, assistant guardrails, and the standalone app journey.
