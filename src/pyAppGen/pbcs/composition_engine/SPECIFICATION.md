# Composition Engine PBC

## Purpose

The Composition Engine PBC owns the AppGen-X application composition plane. It
turns selected Packaged Business Capabilities into an application package by
managing workspaces, selected PBCs, component registrations, UI fragments,
layout bindings, generated composition DSL, package registration plans, package
index entries, release evidence, and publication events. The package is a
complete PBC in its own directory and exposes executable runtime functions,
descriptor APIs, RBAC, UI/workbench binding evidence, event contracts, and
release-smoke evidence.

The PBC does not share operational tables with other PBCs. It consumes
AppGen-X events and reads projections from identity, gateway, schema registry,
workflow, audit, and package-registration flows. Cross-PBC integration is
represented through API descriptors, consumed events, and read-only projections.

## Owned Datastore Boundary

The logical owned tables are:

- `composition_workspace`: tenant workspace, owner, target surface, status,
  selected PBCs, version, and publication state.
- `component_registry`: component identity, owning PBC, fragment key,
  permissions, schemas, and compatibility state.
- `ui_fragment`: reusable fragment metadata, routes, slots, emitted or
  consumed event references, and availability state.
- `layout_binding`: page, slot, fragment, projection, responsive rules, and
  validation status.
- `dsl_artifact`: generated composition DSL, route map, dependency boundary,
  checksum, and smoke evidence.
- `composition_plan`: selected PBCs, binding graph, route count, package
  target, and validation status.
- `composition_validation_run`: accepted or blocked validation decisions,
  blockers, missing fragments, selected PBCs, and route counts.
- `package_registration_plan`: side-effect-free registration plan, requested
  principal, package metadata, index entries, and registration steps.
- `package_index_entry`: package-discovery index metadata derived from a
  validated workspace.
- `release_evidence`: publication record, route count, risk score, package
  plan, and release state.
- `composition_rule`, `composition_parameter`, and
  `composition_configuration`: executable rules, tunable parameters, and
  runtime configuration.

Runtime event tables are
`composition_engine_appgen_outbox_event`,
`composition_engine_appgen_inbox_event`, and
`composition_engine_dead_letter_event`. Supported backing stores are exactly
PostgreSQL, MySQL, and MariaDB. Runtime configuration rejects any user-facing
stream-engine or event-transport picker and requires the fixed
`appgen.composition.events` AppGen-X topic.

## Standard Capabilities

The package implements standard composition table stakes:

- Workspace creation and tenant-scoped workspace isolation.
- PBC selection with reason and mesh capture.
- Component registration for PBC-owned fragments.
- UI fragment registration with route, slot, and event metadata.
- Layout binding with page, slot, fragment, and projection references.
- Composition plan validation with blockers for missing selections, missing
  bindings, missing required fragments, and route-budget violations.
- Generated composition DSL with selected PBCs, pages, projection references,
  AppGen-X event contract metadata, owned-table evidence, and dependency
  boundaries that declare no shared tables.
- Side-effect-free package registration planning. Planning returns the proposed
  package metadata, index entries, and steps without mutating the caller state.
- Publication that records release evidence, package-registration plans,
  package-index metadata, and AppGen-X outbox events.
- Idempotent inbox handling for consumed AppGen-X events.
- Retry and dead-letter evidence for unsupported or failed events.
- Rule, parameter, and configuration execution.
- Descriptor API contract with command/query routes, owned tables, required
  permissions, idempotency keys, emitted events, and consumed events.
- Action-level permissions for read, compose, approve, publish, event,
  configure, and audit operations.
- UI and workbench contracts for composition operators.

## Advanced Capabilities

The executable runtime proves advanced composition behavior through
`composition_engine_runtime_smoke()`:

- Event-sourced composition lifecycle with hash-chained mutation events.
- Graph-relational component topology from workspaces, components, fragments,
  and bindings.
- Multi-tenant workspace isolation.
- Schema-on-read layout extension restricted to owned composition tables.
- Probabilistic release-risk scoring.
- Real-time composition analytics in the workbench view.
- Counterfactual layout simulation.
- Temporal release-readiness forecasting.
- Autonomous layout remediation recommendations.
- Semantic composition-intent parsing.
- Predictive composition risk scoring.
- Self-healing publication route selection.
- Zero-knowledge-style publication proofs.
- Immutable composition audit trail validation.
- Dynamic policy screening.
- Automated composition control testing.
- Universal API and asynchronous event surface.
- Cross-system composition federation through projections.
- Identity, gateway, schema, workflow, and audit integration without table
  sharing.
- Decentralized publisher identity verification.
- Resilience drills and degraded publication modes.
- Crypto-agile publication signing.
- Carbon-aware build scheduling.
- Algebraic layout optimization.
- Mechanism-design fragment-slot allocation.
- Information-theoretic anomaly detection.
- Temporal stochastic release-exposure modeling.
- Governed composition-risk model registration.

## Configuration, Parameters, and Rules

Configuration requires `database_backend`, `event_topic`, `retry_limit`,
`allowed_targets`, `allowed_layout_modes`, `publication_mode`,
`default_timezone`, and `workbench_limit`. The backend must be one of
`postgresql`, `mysql`, or `mariadb`; the event topic must be
`appgen.composition.events`; the event contract is always `AppGen-X`;
`stream_engine_picker_visible` and `user_selectable_event_contract` are false.

Supported parameters include `max_fragments_per_page`,
`release_risk_threshold`, `layout_density_target`, `route_budget`,
`preview_batch_limit`, and `review_sla_hours`. Unsupported parameter keys are
rejected so package behavior remains explicit.

Rules are executable records with `rule_id`, tenant, scope, required fragments,
allowed meshes, route policy, approval requirement, severity, and status. Rules
compile to a stable hash and are used by plan validation and policy screening.

## Events and Handlers

Emitted events are:

- `CompositionWorkspaceCreated`
- `PbcSelectedForComposition`
- `ComponentRegistered`
- `UiFragmentRegistered`
- `LayoutBound`
- `CompositionPlanValidated`
- `PackageRegistrationPlanned`
- `CompositionPublished`
- `PbcDeployed`

Consumed events are:

- `SchemaAccepted`
- `RoutePublished`
- `AuditEventSealed`
- `AccessPolicyChanged`
- `WorkflowCompleted`
- `PackageRegistrationRequested`

Handlers are idempotent by explicit event idempotency key or by
`{event_type}:{event_id}`. A duplicate processed event returns the previous
handler and does not mutate state. Failed or unsupported events append inbox,
retry evidence, and after the configured retry limit a dead-letter entry. The
handler stores projections in package-local dictionaries for schema, route,
audit, access-policy, workflow, and package-registration events.

## Public API Contract

The runtime exposes descriptor routes for:

- `POST /composition-workspaces`
- `POST /composition-workspaces/{id}/pbcs`
- `POST /component-registry`
- `POST /ui-fragments`
- `POST /layout-bindings`
- `POST /composition-plans/validate`
- `POST /package-registration-plans`
- `POST /composition-dsl`
- `POST /composition-publications`
- `POST /composition/events/inbox`
- `GET /composition-workbench`

Every descriptor declares command or query handler, owned tables, emitted or
consumed events, required permission, and idempotency key. The contract also
publishes allowed database backends, owned tables, emitted and consumed events,
configuration variables, and `shared_table_access: false`.

## UI and Workbench

The UI contract includes the composition workbench, workspace selector, PBC
selector, component registry, fragment catalog, layout canvas, binding
inspector, route-map view, publication console, release-evidence board, rule
studio, parameter console, and configuration panel. UI actions are derived from
the package permissions contract. The configuration editor shows the required
AppGen-X topic and backend allowlist while keeping stream-engine selection
hidden.

Workbench rendering reads only package-owned state. It exposes cards for
workspaces, published packages, components, fragments, and bindings. It also
reports configuration, rule, parameter, outbox, inbox, and dead-letter binding
evidence, including the package-owned outbox, inbox, and dead-letter tables.

## Boundary Verification

`composition_engine_verify_owned_table_boundary()` accepts references to owned
tables, runtime event tables, consumed event types, declared API dependencies,
and declared projections. It rejects undeclared table references, proving that
the PBC does not couple itself to another PBC's datastore. Declared dependency
APIs are identity policy lookup, gateway route lookup, schema contract lookup,
workflow approval command, and audit event command. Declared projections are
identity, gateway, schema, workflow, audit, PBC deployment, and package
registration projections.

## Release Evidence

Package release evidence is executable:

- `composition_engine_runtime_capabilities()` exposes capability and operation
  metadata.
- `composition_engine_runtime_smoke()` runs the standard and advanced behavior
  path.
- `composition_engine_build_api_contract()` proves API, event, permission,
  table, backend, and configuration descriptors.
- `composition_engine_permissions_contract()` proves action-level RBAC.
- `composition_engine_ui_contract()` and
  `composition_engine_render_workbench()` prove UI fragments and workbench
  binding.
- Focused tests in `tests/test_pbc_composition_engine_runtime.py` verify
  configuration rejection, event handling, side-effect-free package planning,
  schema extension ownership, boundary validation, API descriptors, RBAC, UI
  evidence, runtime smoke, and release audit behavior.
