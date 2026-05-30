# Release Evidence - Permitting Licensing and Inspections

Package directory: `pbcs/permitting_licensing_inspections`.

This standalone PBC now includes owned schema, migration DDL, models, services,
routes, events, handlers, UI workbench surfaces, explicit forms/wizards/
controls, a one-PBC app shell, agent skills, permissions, configuration, seed
data, package metadata, side-effect-free registration, and focused package
validation.

## Evidence

- Release contracts: schema, service, route, event, handler, UI, forms,
  wizards, controls, agent, standalone shell, and governance evidence are
  materialized from package-local code.
- Owned datastore boundary: every owned table starts with
  `permitting_licensing_inspections_`, and cross-PBC collaboration stays on
  declared APIs or AppGen-X events.
- Standalone usability: `standalone.py` bootstraps demo state, renders the
  workbench shell, dispatches declared routes, and exposes release and agent
  manifests without shared-generator changes.
- Workflow depth: the runtime now models intake completeness, plan-set version
  tracking, discipline review routing, fee gating, inspection escalation,
  violation notice timelines, and renewal eligibility decisions.
- Package tests: `tests/test_contract.py` and `tests/test_standalone.py`
  validate schema/service/release contracts, standalone shell exports,
  bootstrap/render behavior, route dispatch, governance, and agent planning.
