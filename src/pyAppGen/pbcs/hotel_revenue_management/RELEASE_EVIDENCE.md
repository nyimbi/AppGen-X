# Release Evidence - Hotel Revenue Management

Package directory: `pbcs/hotel_revenue_management`.

This standalone slice includes owned schema, aligned migration DDL, model and
service contracts, route dispatch, AppGen-X event contracts, idempotent
handlers, workbench UI metadata, assistant skills, package-local bootstrap
workflows, dynamic release evidence, and focused tests.

## Evidence Highlights

- Owned datastore boundary stays inside `hotel_revenue_management_` tables and
  package-local AppGen-X runtime tables.
- Sellable inventory, BAR/inheritance pricing, channel parity, segmented demand,
  overbooking limits, yield explanations, and revenue snapshots are executable
  in package-local runtime smoke.
- Release readiness reads local docs, tests, UI, agent, route, handler, and
  domain-depth contracts via `release_evidence.py`.
- Standalone app composition exposes the package as a one-PBC workbench and
  assistant surface without touching shared generator or language assets.

## Expected Validation

- Compile package Python sources.
- Run focused contract and standalone tests.
- Confirm runtime and standalone smoke functions remain green.
