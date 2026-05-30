# Release Evidence - Sports Venue Event Operations

Package directory: `pbcs/sports_venue_event_operations`.

This standalone slice includes owned schema contracts, runtime and standalone services, route dispatch, workbench UI surfaces, agent previews, package-local audits, and focused tests.

## Evidence

- Standalone app: venue setup, calendar, ingress or egress, staffing, concessions, ticketing, credentialing, crowd, incidents, weather, broadcast, sponsor, turnover, accessibility, lost or found, emergency, and analytics flows execute in package-local smoke tests.
- UI and workbench: forms, wizards, controls, supervisor workbench, and rendered summary cards are exposed without any stream engine picker.
- Agent: document intake and CRUD preview planning stay inside owned tables and always require confirmation for mutations.
- Boundaries: owned datastore references stay inside `sports_venue_event_operations_` tables and only use the AppGen-X outbox, inbox, and dead-letter tables for eventing.
- Backends: runtime and standalone manifests allow only PostgreSQL, MySQL, and MariaDB.
- Audits: source, package, spec, agent, implementation, capability, and generation audits run from `audit.py`.
