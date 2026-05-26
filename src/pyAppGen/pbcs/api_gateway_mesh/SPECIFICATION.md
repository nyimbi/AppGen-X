# API Gateway Mesh

Package-local implementation contract for the API Gateway Mesh PBC. The package owns service registration, endpoint catalog, route publication, route versions, traffic policy, rate limits, mTLS identity, route health, traffic telemetry, AppGen-X event evidence, rules, parameters, configuration, UI fragments, and release validation for platform ingress and service-to-service routing.

## Stable Identity

- PBC key: `api_gateway_mesh`.
- Mesh: platform fabric.
- Implementation directory: `src/pyAppGen/pbcs/api_gateway_mesh`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_api_gateway_mesh_runtime.py`.
- Source registration entrypoint: `implementation_contract()`.
- Event topic: `appgen.gateway.events`.
- Event contract: AppGen-X.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- User-facing stream-engine selection is not exposed.

## Owned Boundary

Owned tables and generated model artifacts:

- `service_registration`
- `endpoint_catalog`
- `service_route`
- `route_version`
- `rate_limit_policy`
- `mtls_identity`
- `traffic_policy`
- `retry_budget`
- `circuit_breaker`
- `fallback_route`
- `service_health`
- `traffic_sample`
- `gateway_rule`
- `gateway_parameter`
- `gateway_configuration`
- `gateway_service_map_projection`
- `gateway_route_contract_projection`
- `gateway_policy_screening`
- `gateway_route_publication_proof`
- `gateway_federation_projection`
- `gateway_resilience_drill`
- `gateway_crypto_epoch`
- `gateway_carbon_routing_window`
- `gateway_route_optimization`
- `gateway_traffic_allocation`
- `gateway_anomaly_signal`
- `gateway_stochastic_exposure`
- `gateway_parsed_request`
- `gateway_control_assertion`
- `gateway_governed_model`
- `gateway_retry_evidence`
- `gateway_health_forecast`
- `gateway_exception_resolution`
- `gateway_route_risk_score`
- `gateway_route_selection`
- `api_gateway_mesh_appgen_outbox_event`
- `api_gateway_mesh_appgen_inbox_event`
- `api_gateway_mesh_dead_letter_event`

The PBC does not share identity, schema, audit, composition, tenant, service, or business-domain tables. Cross-PBC integration is represented only by declared APIs, events, or projections:

- Consumed events: `PbcDeployed`, `AccessPolicyChanged`, `SchemaAccepted`, `AuditEventSealed`, and `TenantProvisioned`.
- API dependencies: `GET /identity/policies`, `GET /schemas/routes`, `POST /audit/route-events`, and `POST /composition/services`.
- Projections and handoffs: `identity_policy_projection`, `schema_contract_projection`, `audit_route_projection`, `composition_service_projection`, `pbc_deployment_projection`, and `tenant_gateway_projection`.
- Emitted events: `ServiceRegistered`, `RoutePublished`, `RateLimitApplied`, `ServiceHealthChanged`, `MeshPolicyChanged`, and `TrafficSampleRecorded`.

## Standard Capabilities

- Service registration with PBC ownership, service name, version, region, upstream list, endpoint catalog, and registered/blocked status.
- Route definition and publication with host, path, method, protocol, version, route hash, canary policy, and blocked-path enforcement.
- Host/path/method/protocol matching descriptors and route versioning.
- mTLS workload identity with service binding, issuer validation, active status, and service identity evidence.
- Rate limits, quotas, burst controls, tenant/principal scoping, retry budgets, and fair-use policy evidence.
- Traffic policies for canary, upstream selection, fallback routes, backpressure, circuit breakers, and resilience controls.
- Service health capture with latency SLO, error-rate threshold, healthy/degraded status, and health-change events.
- Traffic sampling with requests, p95 latency, error rate, saturation, risk scoring, and telemetry events.
- Service map generation with service-route topology edges.
- AppGen-X outbox/inbox idempotency, retry evidence, and dead-letter evidence.
- Package-local schema, service, and release-evidence contracts for generated gateway packages.
- Projections for PBC deployment, access policies, accepted schemas, sealed audit events, and tenant provisioning.
- Multi-tenant gateway isolation through tenant-scoped services, routes, policies, telemetry, rules, parameters, configuration, and workbench views.
- RBAC descriptors for service, route, policy, identity, event, configuration, read, and audit actions.
- Package-local workbench UI for services, routes, rate limits, mTLS identities, traffic policies, service map, telemetry, health, resilience, rules, parameters, configuration, and event evidence.

## Advanced Capabilities

- Event-sourced gateway lifecycle with immutable hash-chain route and policy history.
- Graph-relational service topology across services, routes, versions, tenants, upstreams, identities, traffic policies, samples, and health.
- Multi-tenant gateway isolation and owned-table schema evolution.
- Probabilistic latency, saturation, abuse, and failure-risk scoring.
- Real-time mesh analytics over service map, route health, latency, error rate, rate limits, and SLO burn.
- Counterfactual traffic-policy simulation for canary and failover decisions.
- Temporal route health, latency, error, and saturation forecasting.
- Autonomous gateway exception resolution for latency breaches, mTLS failures, and quota exhaustion.
- Semantic route request parsing for service onboarding and operations workflows.
- Predictive route risk scoring and self-healing route selection.
- Zero-knowledge route-publication proof generation.
- Dynamic gateway policy screening by restricted path and route state.
- Automated controls for configuration, rules, parameters, published routes, and hash-chain integrity.
- Universal descriptor API and AppGen-X event contracts.
- Cross-system gateway federation through identity, schema, audit, and composition projections.
- Decentralized service identity verification through DID-like evidence.
- Chaos-engineered gateway tolerance for upstream timeouts and mTLS identity failures.
- Quantum-resistant route authorization simulation through crypto-agile epoch rotation.
- Carbon-aware gateway routing windows.
- Algebraic route optimization and mechanism-design traffic allocation.
- Information-theoretic traffic anomaly detection.
- Temporal traffic exposure stochastic modeling.
- Governed route-risk model registration with feature lineage, drift, and explainability controls.

## Runtime Services

- `configure_runtime` validates backend, exact AppGen-X event topic, retry limit, allowed methods, allowed protocols, regions, timezone, workbench limit, and stream-picker absence.
- `set_parameter` accepts only supported gateway parameters.
- `register_rule` validates rule identity, tenant, status, and routing scope, then stores deterministic compiled evidence.
- `register_schema_extension` accepts only owned-table schema extensions.
- `receive_event` idempotently handles PBC deployment, access policy, schema, audit, and tenant events; records inbox evidence; schedules retries; and dead-letters exhausted failures.
- `register_service` owns service registration state and service topology evidence.
- `register_mtls_identity` owns workload identity state and verified service-identity evidence.
- `publish_route` owns route publication, route hash, routing policy, and downstream projection handoffs.
- `apply_rate_limit` owns rate-limit policy state.
- `record_health` owns service-health state and health-change events.
- `record_traffic_sample` owns traffic telemetry and risk scoring.
- `build_service_map` exposes service-route topology.
- `build_api_contract` emits descriptor-level route, permission, idempotency, event, dependency, and owned-table evidence.
- `build_schema_contract` emits generation-ready owned-table, relationship, migration, and model evidence for all gateway-owned artifacts.
- `build_service_contract` declares the gateway command/query surface and the owned transaction boundary.
- `build_release_evidence` proves schema depth, migration coverage, service depth, AppGen-X-only eventing, permission coverage, backend allowlist compliance, and absence of shared-table access.
- `permissions_contract` maps runtime commands to RBAC permissions.
- `verify_owned_table_boundary` accepts owned tables and declared API/event/projection dependencies, then reports direct foreign-table violations.
- `build_workbench_view` exposes operational and release evidence.

## API Contract

- `POST /services` maps to `register_service`.
- `POST /routes` maps to `publish_route`.
- `POST /rate-limits` maps to `apply_rate_limit`.
- `POST /mtls-identities` maps to `register_mtls_identity`.
- `POST /service-health` maps to `record_health`.
- `POST /traffic-samples` maps to `record_traffic_sample`.
- `POST /gateway/events/inbox` maps to `receive_event`.
- `POST /gateway-rules` maps to `register_rule`.
- `POST /gateway-parameters` maps to `set_parameter`.
- `POST /gateway-configuration` maps to `configure_runtime`.
- `GET /service-map` maps to `build_service_map`.
- `GET /gateway/contracts/schema` maps to `build_schema_contract`.
- `GET /gateway/contracts/service` maps to `build_service_contract`.
- `GET /gateway/release-evidence` maps to `build_release_evidence`.
- `GET /gateway-workbench` maps to `build_workbench_view`.

Every route descriptor includes owned tables, command or query binding, idempotency key where applicable, required permission, emitted events, consumed events, fixed AppGen-X eventing evidence, and dependency evidence.

## Events And Handlers

Emitted events:

- `ServiceRegistered`
- `RoutePublished`
- `RateLimitApplied`
- `ServiceHealthChanged`
- `MeshPolicyChanged`
- `TrafficSampleRecorded`

Consumed events:

- `PbcDeployed`
- `AccessPolicyChanged`
- `SchemaAccepted`
- `AuditEventSealed`
- `TenantProvisioned`

Handlers are idempotent by idempotency key or event type and event id. Duplicate processed events do not create duplicate state changes. Failed events record retry evidence until the configured retry limit and then produce dead-letter records.

## Rules, Parameters, And Configuration

Rules cover routing, rate limit, identity, traffic, resilience, telemetry, allowed methods, allowed protocols, required identity, blocked paths, retry budget, fallback behavior, and status.

Parameters include:

- `default_rate_limit_per_minute`
- `latency_slo_ms`
- `error_rate_threshold`
- `canary_percent`
- `retry_budget`
- `retention_days`
- `circuit_breaker_error_threshold`
- `fallback_latency_budget_ms`
- `traffic_sample_percent`
- `workbench_limit`

Configuration includes database backend, event topic, retry limit, allowed methods, allowed protocols, allowed regions, default timezone, and workbench limit. Runtime configuration records `event_contract: AppGen-X`, allowed relational backends, hidden stream-engine picker evidence, non-selectable event-contract evidence, and owned tables.

## Schema, Service, And Release Contracts

`api_gateway_mesh_build_schema_contract()` emits the package-owned schema plan for service registration, routing, policy, resilience, proofs, projections, retry evidence, governed models, and AppGen-X inbox/outbox/dead-letter tables. Every owned table has a package-local migration path under `pbcs/api_gateway_mesh/migrations/` and a package-local generated model descriptor.

`api_gateway_mesh_build_service_contract()` declares the gateway command/query surface used by generated applications: runtime configuration, parameters, rules, schema extension, AppGen-X inbox handling, service registration, mTLS identity, route publication, rate limiting, health, telemetry, control testing, governed-model registration, service maps, contract evidence, resilience, crypto rotation, carbon-aware routing, optimization, allocation, anomaly detection, stochastic exposure, and owned-boundary verification.

`api_gateway_mesh_build_release_evidence()` is the package-local release gate. It proves owned-schema depth, one migration descriptor per owned table, service command depth, AppGen-X-only API/eventing, permission coverage for key commands, backend allowlist compliance, and no shared-table access.

## UI And Workbench

UI fragments:

- `GatewayMeshWorkbench`
- `ServiceRegistry`
- `RouteDesigner`
- `RateLimitPolicyBoard`
- `MtlsIdentityConsole`
- `TrafficPolicyConsole`
- `ServiceMapView`
- `RouteTelemetryDashboard`
- `ServiceHealthPanel`
- `ResilienceControlPanel`
- `GatewayRuleStudio`
- `GatewayParameterConsole`
- `GatewayConfigurationPanel`

The workbench exposes service, route, published-route, rate-limit, mTLS identity, traffic-sample, request, inbox, outbox, retry, dead-letter, release-blocking, configuration, rule, parameter, and owned-boundary evidence. Visible actions are RBAC-filtered by service, route, policy, identity, event, configuration, read, and audit permissions.

## Release Evidence

The focused test suite proves:

- Runtime smoke covers every declared standard and advanced capability key.
- The package declares owned tables, allowed relational backends, fixed AppGen-X eventing, descriptor APIs, schema/service/release contracts, and action-level RBAC.
- Configuration, parameters, rules, schema extensions, event handling, service registration, mTLS identity, route publication, rate limits, service health, traffic samples, service map, UI, and workbench evidence execute.
- Boundary validation accepts owned tables and declared API/event/projection dependencies, then rejects direct foreign-table references.
- Invalid backend, stream-picker configuration, unsupported parameters, non-owned schema extensions, idempotent duplicates, retries, and dead letters are verified.

## Seed And Release Evidence

Release evidence includes package-local seed data for default gateway policies,
safe HTTP methods, supported protocols, rate-limit bands, retry budgets, and
health-state thresholds. Generated packages must validate those seed descriptors
with the schema, migration, model, service, route, event, handler, UI, RBAC,
configuration, and release evidence contracts.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `api_gateway_mesh`
- Mesh: `platform`
- Datastore backend: `None`

### Owned Tables

- `service_route`
- `rate_limit_policy`
- `mtls_identity`
- `traffic_sample`

### API Routes

- `POST /routes`
- `POST /rate-limits`
- `GET /service-map`

### Emitted Events

- `RoutePublished`
- `ServiceHealthChanged`

### Consumed Events

- `PbcDeployed`
- `AccessPolicyChanged`

### UI Fragments

- None declared

### Permissions

- None declared

### Configuration Keys

- None declared

### Standard Features

- None declared

### Advanced Capabilities

- None declared

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->
