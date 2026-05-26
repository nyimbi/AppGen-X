# Personnel Directory and Identity PBC Specification

`personnel_identity` is the AppGen-X packaged business capability for workforce
identity: departments, workers, employment facts, organization structure,
position and manager relationships, role assignments, identity attributes,
access context, lifecycle status, and employee events used by HCM, time, payroll,
onboarding, finance, and operations packages. The implementation is owned under
`src/pyAppGen/pbcs/personnel_identity/`.

## Owned Boundary

- **PBC key:** `personnel_identity`
- **Mesh:** `hcm`
- **Owned tables:** `personnel_department`, `personnel_employee`,
  `personnel_employment_lifecycle`, `personnel_manager_relationship`,
  `personnel_role_assignment`, `personnel_role_review`,
  `personnel_identity_attribute`, `personnel_identity_assurance`,
  `personnel_policy_rule`, `personnel_parameter`, `personnel_configuration`,
  `personnel_provisioning_event`, `personnel_access_exception`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only
- **Required event topic:** `appgen.people.events`
- **Emits:** `DepartmentRegistered`, `EmployeeCreated`,
  `EmployeeStatusChanged`, `RoleChanged`, `IdentityAttributeChanged`
- **Consumes:** `EmployeeProvisioned`, `AccessPolicyChanged`,
  `OrgUnitChanged`, `RoleReviewRequested`
- **Primary APIs:** `POST /personnel/departments`,
  `POST /personnel/employees`, `POST /personnel/employees/{id}/status`,
  `POST /personnel/employees/{id}/roles`,
  `POST /personnel/employees/{id}/attributes`,
  `POST /personnel/events/inbox`, `GET /personnel/org-chart`,
  `GET /personnel/workbench`
- **UI artifacts:** people directory, org chart, identity attribute console,
  role assignment workbench, access context review, lifecycle exception queue,
  policy editor

The package owns personnel identity records. Payroll, time, onboarding,
federated identity, CRM, finance, and operations packages receive personnel
facts through APIs, events, and projections rather than shared people tables.
Runtime dependencies are explicitly declared as consumed AppGen-X events,
package APIs, or package-local projections such as
`employee_provisioning_projection`, `access_policy_projection`,
`org_unit_projection`, and `role_review_projection`. No external PBC receives
permission to read or mutate the owned personnel tables directly.

## Rules, Parameters, and Configuration

The runtime must execute personnel identity rules, parameters, and
configuration:

- **Rules:** employee identifier uniqueness, worker type eligibility, department
  membership, manager relationship, role assignment, segregation-of-duties,
  sensitive attribute protection, lifecycle status transitions, identity
  provisioning gate, regional residency, and access-review policy.
- **Parameters:** maximum roles per worker, access risk threshold, manager span
  limit, identity assurance threshold, stale attribute age, review cadence,
  lifecycle grace period, provisioning retry limit, and org-depth limit.
- **Configuration:** datastore backend, event topic, retry limit, default
  country, allowed worker types, allowed employment statuses, attribute
  retention, privacy region, default identity assurance level, and workbench
  limits.

The runtime exposes operations to configure the package, set parameters,
register rules, and apply them during department registration, employee
creation, role assignment, identity attribute updates, org-chart generation, and
access-risk review.

Configuration is executable, not documentary. `configure_runtime` rejects any
backend outside PostgreSQL, MySQL, or MariaDB, rejects every event topic except
`appgen.people.events`, marks `event_contract` as `AppGen-X`, and records that
the stream-engine picker is not visible or user selectable. Unsupported
parameters such as stream-engine selectors are rejected by the parameter layer.
Rules compile to stable hashes so later audit trails can prove which personnel
policy controlled a worker, role, lifecycle transition, or identity attribute
decision.

Schema extension is restricted to owned personnel tables. Regional identity
payloads, clearance metadata, local workforce attributes, or privacy tags may be
registered against owned tables, but attempts to extend payroll, time, finance,
access, or commerce tables fail. Field names must be lowercase snake case, and
new extension fields merge with existing table-local extension definitions.

## Event Handling and Resilience

The runtime uses the AppGen-X event contract only. Outbound events are appended
to the package outbox with stable idempotency keys of the form
`personnel_identity:<event_type>:<event_id>`. Inbound events enter
`personnel_identity_appgen_inbox_event`, are keyed by event type and event id,
and are stored in `handled_events` so duplicate delivery is side effect free.
`EmployeeProvisioned` updates employee provisioning projections,
`AccessPolicyChanged` updates policy projections, `OrgUnitChanged` updates org
unit projections, and `RoleReviewRequested` updates role review projections.
Unsupported or failed inbound events create retry evidence until the configured
retry limit is reached; after that they move to
`personnel_identity_dead_letter_event` with the reason
`unsupported_or_failed_personnel_event`.

The package therefore proves the usual distributed-system requirements for a
composable PBC: idempotent handlers, explicit retry accounting, visible
dead-letter evidence, no user-selectable event transport, no shared tables, and
declared dependency projections for data owned elsewhere.

## API, RBAC, and UI Contract

`build_api_contract` returns descriptor routes rather than opaque strings. Every
route names its command or query and the owned table it uses. The contract also
declares owned tables, allowed database backends, emitted and consumed events,
the fixed AppGen-X topic, hidden stream-engine picker state, and
`shared_table_access: false`. `permissions_contract` defines action-level RBAC
for department creation, employee creation, lifecycle transition, role
assignment, identity attributes, reviews, inbound event handling, configuration,
schema extension, control testing, and workbench access.

The UI contract exposes the personnel workbench, department console, employee
master console, lifecycle board, manager hierarchy, org chart, role console,
role review queue, identity attribute console, segregation-of-duties panel,
assurance panel, provisioning monitor, employee event timeline, privacy panel,
directory search, approval queue, rule studio, parameter console, and
configuration panel. UI binding evidence includes the owned tables, outbox,
inbox, dead-letter tables, RBAC mapping, required event topic, allowed database
backends, AppGen-X event contract, and hidden stream-engine picker.

## Standard Table-Stakes Capabilities

1. Department and organization-unit registration with parent relationships,
   legal entity, cost center, and manager assignment.
2. Employee/person record creation with worker type, employment status, hire
   date, job, department, manager, country, and identity handle.
3. Employee lifecycle transitions for provisioned, active, leave, suspended,
   terminated, and alumni states.
4. Manager hierarchy and org-chart generation.
5. Role assignment, role change, removal, expiry, and access-context evidence.
6. Identity attributes for email, directory id, badge, region, clearance,
   employment profile, payroll profile, and time profile.
7. Segregation-of-duties and sensitive-role screening.
8. Identity assurance, proof, and access-risk scoring.
9. Employee provisioning consumed-event handling with idempotency evidence.
10. Employee and role event emission for downstream time, payroll, onboarding,
    access, finance, and service packages.
11. Multi-tenant and multi-entity personnel isolation.
12. Privacy, residency, retention, and attribute minimization controls.
13. Directory search, identity attribute lookup, and org projection APIs.
14. Approval and review workflow for sensitive changes.
15. Retry, dead-letter, and idempotency evidence for role and provisioning
    handlers.
16. Permissions and ABAC descriptors for create, update, role, attribute,
    review, configure, and audit operations.
17. Configuration schema and seed data for worker types, statuses, role groups,
    countries, and default parameters.
18. Workbench views for active workers, role risk, provisioning gaps, org
    exceptions, stale attributes, and review queues.
19. Release-audit evidence for package ownership, manifests, schema, migrations,
    models, services, routes, events, handlers, UI, permissions, configuration,
    tests, registration metadata, and generation smoke.

## Advanced Capabilities

1. Event-sourced workforce identity lifecycle.
2. Graph-relational org and identity topology across department, employee,
   manager, role, attribute, policy, and provisioning nodes.
3. Multi-tenant workforce identity isolation.
4. Schema-on-read identity extensibility for regional, role, and workforce
   attributes.
5. Probabilistic identity assurance and access risk.
6. Real-time directory, org, and access analytics convergence.
7. Counterfactual org and access-policy simulation.
8. Temporal workforce movement and access-risk forecasting.
9. Autonomous role and access exception recommendations.
10. Semantic personnel document and provisioning event parsing.
11. Predictive attrition, access, and compliance-risk scoring.
12. Self-healing provisioning route selection.
13. Zero-knowledge personnel eligibility proof.
14. Immutable workforce identity audit trail.
15. Dynamic personnel policy screening.
16. Automated identity control testing.
17. Universal API and async event contracts.
18. Cross-system people federation with onboarding, time, payroll, access,
    finance, and service packages.
19. Identity provider and directory integration evidence.
20. Decentralized employee identity verification.
21. Chaos-engineered provisioning tolerance.
22. Crypto-agile identity authorization.
23. Carbon-aware batch identity processing.
24. Algebraic role and access optimization.
25. Mechanism-design manager and role allocation.
26. Information-theoretic identity anomaly detection.
27. Stochastic workforce-risk exposure modeling.
28. Distributed systems engineering for idempotent handlers.
29. Probabilistic ML workforce-risk governance.
30. Cryptographic engineering for proofs and hash chains.
31. Mathematical optimization for org, role, and access decisions.
32. People MLOps governance with feature lineage, drift, and explainability.

## Runtime Completeness Contract

The runtime must prove that rules, parameters, and configuration execute and
influence employee and role decisions; that personnel identity state stays
inside the package boundary; that AppGen-X outbox events are idempotent; that
backend configuration rejects anything outside PostgreSQL, MySQL, or MariaDB;
that eventing remains bound to the AppGen-X event contract without user-facing
stream-engine selection; that package-local UI fragments expose department,
employee, lifecycle, manager hierarchy, org chart, role, identity attribute,
segregation-of-duties, assurance, provisioning, privacy, directory search,
approval, rule, parameter, and configuration workbench surfaces; and that all
standard and advanced capability claims have testable release evidence.
