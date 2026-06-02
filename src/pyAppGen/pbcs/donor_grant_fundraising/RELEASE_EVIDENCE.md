# Release Evidence - Donor Grant and Fundraising

Package directory: `pbcs/donor_grant_fundraising`.

This PBC includes owned schema, contract-aligned migration DDL, models, services, routes, events, handlers, UI workbench surfaces, a package-local standalone shell, agent skills, permissions, configuration, seed data, side-effect-free registration, and focused package tests.

## Evidence

- Release evidence materializes schema, service, route, event, handler, UI, standalone-shell, agent, and governance contracts.
- The migration DDL creates every owned `donor_grant_fundraising_*` table declared by the runtime schema contract.
- The route surface now covers donor, campaign, pledge, gift, restriction, grant-application, stewardship-touchpoint, and workbench operations.
- Eventing uses the AppGen-X outbox/inbox contract with retry and dead-letter evidence.
- The standalone shell boots defaults, seeds demo data, executes package-local operating flows, and renders workbench queues without touching shared generator code.
- Package tests validate schema/service/release evidence, event contracts, side-effect-free registration, route dispatch, governance hooks, domain workflows, standalone shell behavior, and idempotent handlers.
