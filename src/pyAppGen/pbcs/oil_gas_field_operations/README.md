# Oil and Gas Field Operations PBC

`oil_gas_field_operations` is now a standalone one-PBC AppGen-X slice for route-based field surveillance. It centers daily production capture, field tickets, workover readiness, HSE boundary events, and a morning production review assistant inside this package only.

## What This Package Owns

- Oil-and-gas-owned schema, migrations, models, services, routes, handlers, permissions, and release evidence.
- Package-local app surfaces for field operations: [forms.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/forms.py), [wizards.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/wizards.py), [controls.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/controls.py), and [standalone.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/standalone.py).
- Governed assistant previews for morning review, workover readiness, and bounded CRUD planning.

## Domain Shape

This standalone surface is aimed at lease operators, production engineers, and field supervisors who need to:

- register wells with field, pad, lease, interval, lift, and integrity context,
- capture daily production with phase/disposition detail and production-test state,
- triage downtime, integrity, metering, and haul-off field tickets,
- assemble workover readiness packs with recent decline and barrier evidence,
- monitor HSE boundary events alongside route operations,
- generate a read-only morning production brief before taking action.

## Key Entry Points

- Runtime: [runtime.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/runtime.py)
- Services: [services.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/services.py)
- Routes: [routes.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/routes.py)
- Workbench UI: [ui.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/ui.py)
- Forms: [forms.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/forms.py)
- Wizards: [wizards.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/wizards.py)
- Controls: [controls.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/controls.py)
- Assistant support: [agent.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/agent.py)
- Standalone app: [standalone.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/standalone.py)
- Release evidence: [release_evidence.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/release_evidence.py)

## One-PBC App Surface

The package now exposes:

- forms for well hierarchy intake, daily production capture, field ticket triage, workover readiness, HSE event logging, and morning review requests,
- guided wizards for pad startup, morning review, workover readiness, HSE response, and release readiness,
- a control center for release readiness, production balance, integrity follow-up, assistant guardrails, and ticket reconciliation,
- a standalone app class that runs the end-to-end field-operations slice without touching shared generators or other PBCs.

## Verification

Primary verification lives in package-local tests under [tests](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/tests) and in the executable standalone smoke path inside [standalone.py](/private/tmp/appgen-pbc-oil-gas-field-operations-standalone/src/pyAppGen/pbcs/oil_gas_field_operations/standalone.py).
