# Release Evidence - Wealth Portfolio Management

Package directory: `pbcs/wealth_portfolio_management`.

This package now includes:

- source-owned schema, migration DDL, model contracts, service contracts, API routes, AppGen-X events, handlers, permissions, configuration, seed hooks, and package metadata
- a standalone one-PBC sqlite execution harness for household onboarding, IPS, suitability, rebalancing, performance, advisor review, document readiness, and compliance surveillance
- governed assistant planning with confirmation-gated mutation skills and `governed_datastore_crud`
- hand-crafted package-local `README.md`, `implementation-plan.md`, `implementation-status.md`, and `SPECIFICATION.md`

## Evidence

- Source package boundary: all deployment-facing owned tables stay under the `wealth_portfolio_management_` prefix and no foreign table writes are introduced.
- Datastore policy: deployment-facing contracts remain on PostgreSQL, MySQL, and MariaDB; sqlite is used only as a package-local standalone harness.
- Event policy: AppGen-X is the only event contract, with inbox, outbox, dead-letter, idempotency, and retry evidence.
- Standalone workbench: executable service, route, UI, and agent surfaces cover portfolio onboarding, investment policy capture, suitability, fee projection, document intake, tax-aware trade proposals, performance snapshots, advisor review, and compliance surveillance.
- Documentation: package-local implementation plan, implementation status, specification, and README are materialized for audit traceability.
- Focused tests: contract tests and standalone workflow tests exercise the source package evidence and the standalone wealth flow.
