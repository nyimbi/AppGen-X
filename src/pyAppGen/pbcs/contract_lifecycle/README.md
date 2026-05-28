# Contract Lifecycle PBC

`contract_lifecycle` is a self-contained AppGen-X packaged business capability for contract lifecycle management. This package owns its datastore schema, executable lifecycle services, routes, AppGen-X event contracts and handlers, workbench UI metadata, RBAC/configuration/rules/parameters, governed agent CRUD planning, release evidence, and focused tests.

## What It Does

- runs contract intake with readiness gating for purpose, counterparty, commercials, owner, and source documents
- supports classification, authoring workspace creation, clause selection, redline triage, approval routing, and signature capture
- activates obligations, records performance evidence, tracks milestones, schedules renewals, executes amendments, and runs compliance checks
- scores contract risk, indexes contract documents, simulates counterparty impact, and surfaces operational queues in a workbench view
- consumes `CustomerUpdated`, `SupplierQualified`, `PolicyChanged`, and `IdentityVerified` through idempotent AppGen-X handlers
- exposes governed assistant support for document-instruction parsing and owned-table CRUD previews with mutation confirmation

## Package Surface

- schema/models: [models.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/models.py), [schema_contract.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/schema_contract.py), [migrations/001_initial.sql](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/migrations/001_initial.sql)
- runtime/services/routes: [application.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/application.py), [services.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/services.py), [routes.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/routes.py), [runtime.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/runtime.py)
- UI and governance: [ui.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/ui.py), [config.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/config.py), [permissions.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/permissions.py)
- events/agent/evidence: [events.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/events.py), [handlers.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/handlers.py), [agent.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/agent.py), [release_evidence.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/contract_lifecycle/release_evidence.py)

## Validation

- package tests: `./.venv/bin/pytest -q src/pyAppGen/pbcs/contract_lifecycle/tests`
- compile check: `./.venv/bin/python -m compileall src/pyAppGen/pbcs/contract_lifecycle`
- package smoke: exported runtime, discovery, release evidence, and smoke entrypoints succeed through package-local execution
