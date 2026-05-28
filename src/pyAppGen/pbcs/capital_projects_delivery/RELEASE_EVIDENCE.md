# Release Evidence - Capital Projects Delivery

Package directory: `pbcs/capital_projects_delivery`.

## Scope Proven

This package now proves a usable single-PBC capital project delivery app slice
with:

- owned database-backed tables, migrations, and model contracts,
- AppGen-X-only outbox/inbox/dead-letter eventing,
- executable lifecycle gate creation, checklist, approval, and rollback logic,
- forms, wizards, controls, workbench views, services, routes, and agent help,
- release checks for lifecycle controls and single-PBC usability.

## Evidence Summary

- Lifecycle gates: invalid forward transitions raise
  `CapitalProjectsDeliveryExceptionOpened`; valid approvals emit
  `CapitalProjectsDeliveryApproved` with gate context.
- Boundary safety: all writes remain inside `capital_projects_delivery_*` owned
  tables; `shared_table_access` is `False`.
- App shell usability: the package exposes database, forms, wizards, controls,
  workbench, services, and agent-help contracts through
  `capital_projects_delivery_build_single_pbc_app_contract()`.
- Validation: package-local executable tests and smoke checks passed; exact
  commands and results are recorded in `implementation-status.md`.
