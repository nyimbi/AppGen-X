# Release Evidence - Capital Projects Delivery

Package directory: `pbcs/capital_projects_delivery`.

## Scope Proven

This package now proves a usable standalone one-PBC capital project delivery app slice with:

- owned database-backed tables, migrations, and model contracts,
- AppGen-X-only outbox/inbox/dead-letter eventing,
- executable lifecycle gate creation, checklist, approval, rollback, and workbench logic,
- forms, wizards, controls, workflows, services, routes, assistant planning, and standalone shell rendering,
- release checks that explicitly name the package-level source artifact, implementation release, and generation smoke audits.

## Evidence Summary

- Lifecycle controls: invalid forward transitions emit `CapitalProjectsDeliveryExceptionOpened`; valid approvals emit `CapitalProjectsDeliveryApproved` with stage, approver-role, and rebaseline context.
- Standalone app shell: `capital_projects_delivery.standalone.CapitalProjectsDeliveryStandaloneApp` bootstraps the slice, loads a demo tenant, dispatches package routes, renders the workbench shell, and exposes a release snapshot.
- Boundary safety: all writes remain inside `capital_projects_delivery_*` owned tables; `shared_table_access` remains `False`; stream-engine choice stays hidden.
- Workflow and assistant planning: gate-approval workflows, document instruction intake, and CRUD planning resolve to package-local routes, permissions, idempotency keys, and AppGen-X event expectations.
- Validation: focused compile, package-local executable tests, and the selected PBC audits are recorded in `implementation-status.md`.
