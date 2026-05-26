# Low-Code Composition Engine PBC

## Purpose

The Low-Code Composition Engine PBC owns the application composition workspace:
selecting PBCs, registering components, composing UI fragments, binding layouts,
publishing experience packages, generating composition DSL, and validating
release readiness. It is the platform package that turns PBC capabilities into
cohesive AppGen-X applications without sharing operational tables.

The PBC integrates with identity, gateway, schema registry, workflow, audit
ledger, and domain PBCs through APIs, AppGen-X events, and read-only
projections.

## Owned Datastore Boundary

The PBC owns:

- `composition_engine_composition_workspace`: tenant, workspace, owner,
  selected PBCs, status, version, and release state.
- `composition_engine_component_registry`: component, owning PBC, fragment key,
  capabilities, permissions, schemas, and compatibility metadata.
- `composition_engine_ui_fragment`: reusable PBC UI fragment registration,
  surface contract, routes, slots, events, and render bindings.
- `composition_engine_layout_binding`: page, slot, fragment, data projection,
  responsive rules, validation state, and publication version.
- `composition_engine_dsl_artifact`: generated composition DSL, checksum,
  package metadata, route map, and smoke-test evidence.
- `composition_engine_release_evidence`: release checks, blockers, approvals,
  package registration plan, and publication proof.
- `composition_engine_outbox`, `composition_engine_inbox`, and
  `composition_engine_dead_letter`: AppGen-X event contract tables for
  exactly-once handlers, retries, and dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

## Standard Table-Stakes Capabilities

The PBC fully implements workspace creation, PBC selection, component registry,
UI fragment registration, layout binding, page composition, route map
generation, permission mapping, schema compatibility checks, generated
composition DSL, package registration plan, publication workflow, release gate
evidence, idempotent handlers, retry/dead-letter evidence, seed workspace data,
configuration schema, executable rules, runtime parameters, workbench views, and
RBAC descriptors for read, compose, publish, approve, configure, and audit.

## Advanced Capabilities

The runtime proves event-sourced composition lifecycle, graph-relational
component topology, multi-tenant workspace isolation, schema-on-read layout
extension, probabilistic release-risk scoring, real-time composition analytics,
counterfactual layout simulation, temporal release-readiness forecasting,
autonomous layout remediation, semantic composition intent parsing, predictive
composition risk scoring, self-healing publication route selection,
zero-knowledge-style publication proofs, immutable composition audit trail,
dynamic composition policy screening, automated release control testing,
universal API and asynchronous composition surfaces, cross-system composition
federation, identity/gateway/schema/workflow/audit integration, decentralized
publisher identity, resilience drills, crypto-agile publication signing,
carbon-aware build scheduling, algebraic layout optimization, mechanism-design
fragment slot allocation, information-theoretic composition anomaly detection,
temporal stochastic release exposure, and governed composition-risk models.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, required fragments,
allowed PBC meshes, route policy, approval requirement, severity, and status.
Parameters include `max_fragments_per_page`, `release_risk_threshold`,
`layout_density_target`, `route_budget`, `preview_batch_limit`, and
`review_sla_hours`.

Configuration includes database backend, event topic, retry limit, default
timezone, allowed target surfaces, allowed layout modes, publication mode, and
workbench limits. Runtime configuration rejects unsupported databases and uses
the AppGen-X event contract for ordinary eventing.

## Public APIs

- `POST /composition-workspaces`
- `POST /composition-workspaces/{id}/pbcs`
- `POST /component-registry`
- `POST /ui-fragments`
- `POST /layout-bindings`
- `POST /composition-dsl`
- `POST /composition-publications`
- `GET /component-registry`
- `GET /composition-workspaces`
- `GET /composition-workbench`

## Events

Emitted events:

- `CompositionWorkspaceCreated`
- `PbcSelectedForComposition`
- `ComponentRegistered`
- `UiFragmentRegistered`
- `LayoutBound`
- `CompositionPublished`
- `PbcDeployed`

Consumed events:

- `SchemaAccepted`
- `RoutePublished`
- `AuditEventSealed`
- `AccessPolicyChanged`
- `WorkflowCompleted`

Handlers are idempotent by `composition_engine:{event_type}:{event_id}`, retry
at least three times, and write failures to `composition_engine_dead_letter`.

## UI and Workbench

The UI exposes a composition workbench, workspace selector, component registry,
PBC selector, fragment catalog, layout canvas, binding inspector, route map,
publication console, release evidence board, rule studio, parameter console,
and configuration panel. Actions are permission-bound and rendered from
package-owned state.

## Release Evidence

Release readiness requires passing runtime smoke, package-local UI contract,
owned tables, API/event/handler surfaces, AppGen-X event contract evidence,
configuration/rule/parameter execution, generated DSL and route-map proof,
package metadata, workbench rendering, and focused unit tests.
