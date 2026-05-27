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

Package-local schema descriptors enumerate every owned table, the three runtime
event tables, relationships, generated migration paths under
`pbcs/composition_engine/migrations/{sequence}_{table}.sql`, and model
descriptors under `pbcs/composition_engine/models/{table}.py`. Schema metadata
proves `shared_table_access: false`, the relational backend allowlist, the
fixed AppGen-X topic, and hidden event-contract selection.

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
runtime event tables, configuration variables, the fixed AppGen-X topic,
hidden event-contract selectors, and `shared_table_access: false`.

Package-local service descriptors enumerate runtime commands and read models:
configuration, parameter, rule, schema-extension, inbox intake, workspace
creation, PBC selection, component registration, fragment registration, layout
binding, plan validation, side-effect-free package planning, DSL generation,
publication, control tests, and boundary verification. The service contract
also declares idempotent handlers, side-effect-free commands, retry/dead-letter
evidence, external API and projection dependencies, and AppGen-X-only eventing.

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
- `composition_engine_build_schema_contract()` proves owned schema depth,
  runtime event tables, migration descriptors, model descriptors, backend
  allowlist compliance, and no shared table access.
- `composition_engine_build_service_contract()` proves command/query depth,
  AppGen-X-only eventing, side-effect-free package planning, retry/dead-letter
  evidence, and declared dependency boundaries.
- `composition_engine_build_release_evidence()` is the package-local release
  gate. It proves schema, service, API, permission, UI, workbench, backend, and
  owned-boundary evidence without relying on shared modules.
- `composition_engine_permissions_contract()` proves action-level RBAC.
- `composition_engine_ui_contract()` and
  `composition_engine_render_workbench()` prove UI fragments and workbench
  binding.
- Focused tests in `tests/test_pbc_composition_engine_runtime.py` verify
  configuration rejection, event handling, side-effect-free package planning,
  schema extension ownership, generated DSL validity, boundary validation, API
  descriptors, schema/service/release contracts, RBAC, UI/workbench evidence,
  runtime smoke, and release audit behavior.

## Seed And Release Evidence

Release evidence includes package-local seed data for starter composition
templates, package states, validation severities, deployment plan statuses, and
view-slot policies. The package validates those seeds with schema, migration,
model, service, route, event, handler, UI, RBAC, configuration, and release
contracts before composition plans are approved.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `composition_engine`
- Mesh: `platform`
- Datastore backend: `postgresql`

### Owned Tables

- `composition_workspace`
- `component_registry`
- `ui_fragment`
- `layout_binding`
- `dsl_artifact`
- `composition_plan`
- `composition_validation_run`
- `package_registration_plan`
- `package_index_entry`
- `release_evidence`
- `composition_rule`
- `composition_parameter`
- `composition_configuration`

### API Routes

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
- `GET /composition/schema-contract`
- `GET /composition/service-contract`
- `GET /composition/release-evidence`

### Emitted Events

- `CompositionWorkspaceCreated`
- `PbcSelectedForComposition`
- `ComponentRegistered`
- `UiFragmentRegistered`
- `LayoutBound`
- `CompositionPlanValidated`
- `PackageRegistrationPlanned`
- `CompositionPublished`
- `PbcDeployed`

### Consumed Events

- `SchemaAccepted`
- `RoutePublished`
- `AuditEventSealed`
- `AccessPolicyChanged`
- `WorkflowCompleted`
- `PackageRegistrationRequested`

### UI Fragments

- `CompositionEngineWorkbench`
- `CompositionWorkspaceBoard`
- `ComponentRegistryConsole`
- `UiFragmentCatalog`
- `LayoutBindingDesigner`
- `CompositionPublicationConsole`
- `CompositionReleaseEvidencePanel`
- `CompositionRuleStudio`
- `CompositionParameterConsole`
- `CompositionConfigurationPanel`

### Permissions

- `composition_engine.read`
- `composition_engine.compose`
- `composition_engine.approve`
- `composition_engine.publish`
- `composition_engine.event`
- `composition_engine.configure`
- `composition_engine.audit`

### Configuration Keys

- `COMPOSITION_ENGINE_DATABASE_URL`
- `COMPOSITION_ENGINE_EVENT_TOPIC`
- `COMPOSITION_ENGINE_RETRY_LIMIT`
- `COMPOSITION_ENGINE_ALLOWED_TARGETS`
- `COMPOSITION_ENGINE_ALLOWED_LAYOUT_MODES`
- `COMPOSITION_ENGINE_PUBLICATION_MODE`
- `COMPOSITION_ENGINE_DEFAULT_TIMEZONE`

### Standard Features

- `workspace_management`
- `pbc_selection`
- `component_registry`
- `ui_fragment_registry`
- `layout_binding`
- `page_composition`
- `route_map_generation`
- `permission_mapping`
- `schema_compatibility_check`
- `composition_dsl_generation`
- `package_registration_plan`
- `publication_workflow`
- `release_gate_evidence`
- `preview_rendering`
- `responsive_layout_rules`
- `fragment_slotting`
- `idempotent_handlers`
- `retry_dead_letter`
- `permissions`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `seed_data`
- `workbench`
- `audit_evidence`
- `release_gate`
- `package_registration_validation`
- `appgen_event_contract`

### Advanced Capabilities

- `event_sourced_composition_lifecycle`
- `graph_relational_component_topology`
- `multi_tenant_workspace_isolation`
- `schema_on_read_layout_extension`
- `probabilistic_release_risk_scoring`
- `real_time_composition_analytics`
- `counterfactual_layout_simulation`
- `temporal_release_readiness_forecasting`
- `autonomous_layout_remediation`
- `semantic_composition_intent_parsing`
- `predictive_composition_risk_scoring`
- `self_healing_publication_route_selection`
- `zero_knowledge_publication_proof`
- `immutable_composition_audit_trail`
- `dynamic_composition_policy_screening`
- `automated_composition_control_testing`
- `universal_api_async_composition_surface`
- `cross_system_composition_federation`
- `identity_gateway_schema_workflow_audit_integration`
- `decentralized_publisher_identity`
- `chaos_engineered_composition_tolerance`
- `quantum_resistant_publication_signing`
- `carbon_aware_composition_build`
- `algebraic_layout_optimization`
- `mechanism_design_fragment_slot_allocation`
- `information_theoretic_composition_anomaly_detection`
- `temporal_release_exposure_stochastic_modeling`
- `distributed_systems_engineering`
- `probabilistic_ml_composition_risk`
- `cryptographic_engineering`
- `mathematical_optimization`
- `composition_mlops_governance`

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->

## Agent, Chatbot Skills, And Self-Registration Contract

The `composition_engine` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `composition_engine_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Low-Code Composition Engine` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `composition_engine_composition_workspace`, `composition_engine_component_registry`, `composition_engine_ui_fragment`, `composition_engine_layout_binding`, `composition_engine_dsl_artifact`, `composition_engine_composition_plan`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as , uses AppGen-X event expectations such as `CompositionWorkspaceCreated`, `PbcSelectedForComposition`, `ComponentRegistered`, `UiFragmentRegistered`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `composition_engine`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `composition_engine_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

