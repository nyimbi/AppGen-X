# Permitting Licensing and Inspections Implementation Status

## Status

Implemented package-local convergence toward a standalone one-PBC permitting,
licensing, and inspections app.

## Completed

- Replaced shallow runtime placeholders with domain-shaped application,
  plan-set, review, fee, issuance, inspection, violation, and renewal flows.
- Added package-local forms, wizards, and controls for intake completeness,
  resubmittals, inspections, renewals, and due-process timelines.
- Added standalone orchestration in `standalone.py` and standalone shell
  metadata/rendering in `ui.py`.
- Updated agent, manifest, package exports, release evidence, routes, services,
  permissions, config, and seed data to reflect the standalone surface.
- Added focused tests for contracts plus standalone bootstrap/render/dispatch
  behavior.
- Added package-local README and implementation notes for future maintainers.

## Remaining Risks

- Validation is package-local smoke coverage; this slice still uses in-memory
  state rather than a live database or HTTP server.
- Route coverage stays intentionally bounded to the declared public APIs even
  though the standalone app exposes deeper runtime actions directly.

## Repo Gates

- `pbc_source_artifact_contract`: covered by package metadata/discovery and
  standalone export assertions.
- `pbc_implementation_release_audit`: covered by release evidence validation and
  runtime/UI/agent/standalone checks.
- `pbc_generation_smoke_audit`: covered by runtime smoke and standalone render
  plus route-dispatch tests.
