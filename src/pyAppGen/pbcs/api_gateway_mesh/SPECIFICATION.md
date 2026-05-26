# Dynamic API Gateway and Service Mesh PBC Specification

## Scope

`api_gateway_mesh` owns platform ingress, service discovery, route publication,
traffic policy, mTLS identity, rate limiting, resilience, telemetry, policy
enforcement, rules, parameters, configuration, and UI workbench fragments for
AppGen-X composable applications.

The PBC composes with identity, schema registry, audit, workflow, composition,
and all business PBCs through APIs, AppGen-X events, and read-model projections.
It owns gateway and mesh policy records; generated services consume published
routes and mesh decisions through contracts instead of shared tables.

## Owned Boundary

Owned tables:

- `service_registration`
- `service_route`
- `route_version`
- `rate_limit_policy`
- `mtls_identity`
- `traffic_policy`
- `traffic_sample`
- `service_health`
- `circuit_breaker`
- `gateway_rule`
- `gateway_parameter`
- `gateway_configuration`
- `gateway_outbox`
- `gateway_inbox`
- `gateway_dead_letter`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Ordinary eventing
uses the AppGen-X outbox/inbox event contract.

## Standard Capabilities

- Service registration, PBC ownership, endpoint catalog, versioning, health,
  and mesh namespace isolation.
- Route definition, route versioning, host/path/method matching, header
  matching, canary policy, upstream selection, and publication.
- Rate limits, quotas, burst controls, tenant/principal-scoped throttling,
  retry budgets, backpressure, and fair-use enforcement.
- mTLS workload identity, certificate rotation metadata, service identity
  binding, policy-driven access integration, and signed route evidence.
- Circuit breakers, retries, timeout policies, fallback routes, blue/green
  traffic shifting, failover, and dead-letter evidence.
- Traffic sampling, latency/error analytics, SLO health, route telemetry,
  service map, topology projection, policy controls, and audit handoff.
- Rules, parameters, configuration schema, permissions, seed data, idempotent
  handlers, retry/dead-letter evidence, and UI workbench fragments.

## Advanced Capabilities

- Event-sourced gateway lifecycle with immutable hash-chained route and policy
  history.
- Graph-relational service topology spanning services, routes, versions,
  tenants, upstreams, identities, traffic policies, samples, and health.
- Multi-tenant gateway isolation with independently configurable rules,
  parameters, rate limits, mTLS identities, and crypto epochs.
- Schema evolution through governed route and traffic-policy extension
  registration.
- Probabilistic latency, saturation, abuse, and failure-risk scoring.
- Real-time mesh analytics over routes, service map, latency, error rate,
  health, rate-limit usage, and SLO burn.
- Counterfactual traffic simulation for canary, failover, rate-limit, and retry
  policies.
- Temporal latency, error, saturation, and route-health forecasting.
- Autonomous gateway exception recommendation with auditable rationale.
- Semantic route request parsing for service onboarding and operations text.
- Predictive route risk scoring and self-healing mesh route selection.
- Cryptographic route-publication proofs, immutable audit trails, dynamic
  gateway policy screening, and continuous control testing.
- Universal API and AppGen-X event contracts, federation views, decentralized
  service identity, resilience drills, crypto agility, carbon-aware routing,
  mathematical route optimization, traffic allocation, anomaly detection,
  stochastic traffic exposure modeling, and governed gateway models.

## APIs

- `POST /services`
- `POST /routes`
- `POST /routes/{id}/publish`
- `POST /rate-limits`
- `POST /mtls-identities`
- `POST /traffic-policies`
- `POST /traffic-samples`
- `POST /service-health`
- `GET /service-map`
- `GET /route-telemetry`
- `POST /gateway-rules`
- `POST /gateway-parameters`
- `POST /gateway-configuration`

## Events

Emitted:

- `ServiceRegistered`
- `RoutePublished`
- `RateLimitApplied`
- `ServiceHealthChanged`
- `MeshPolicyChanged`

Consumed:

- `PbcDeployed`
- `AccessPolicyChanged`
- `SchemaAccepted`
- `AuditEventSealed`
- `TenantProvisioned`

Handlers are idempotent through `api_gateway_mesh:<EventType>:<event_id>` keys,
retry through the AppGen-X outbox adapter, and route exhausted failures to
`api_gateway_mesh.dead_letter`.

## UI

The package exports a workbench UI contract with fragments for service registry,
route designer, rate-limit policies, mTLS identities, traffic policies, service
map, route telemetry, health, resilience controls, rules, parameters, and
configuration.
