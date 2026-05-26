# Schema Registry and Contract Validation PBC

## Purpose

The Schema Registry and Contract Validation PBC owns the lifecycle of API,
event, projection, and integration contracts across an AppGen-X composition. It
is the authoritative package for schema subjects, versioned schema artifacts,
compatibility rules, contract validation, consumer compatibility evidence,
breaking-change prevention, contract projections, and release gates.

The PBC composes with the gateway, identity, audit ledger, workflow,
composition, and every domain PBC through declared API calls, event contracts,
and read-only projections. It never shares tables with another PBC.

## Owned Datastore Boundary

The PBC owns these table families:

- `schema_registry_schema_subject`: subject identity, tenant, domain, owner PBC,
  channel, namespace, lifecycle status, and tags.
- `schema_registry_schema_version`: immutable version payload, semantic version,
  fingerprint, compatibility status, governance classification, and lineage.
- `schema_registry_compatibility_rule`: tenant- and subject-scoped rules for
  backward, forward, transitive, additive-only, semantic, and policy-aware checks.
- `schema_registry_contract_violation`: blocked change, payload validation,
  producer and consumer impact, severity, remediation, and release-blocking state.
- `schema_registry_consumer_binding`: API, handler, projection, and package
  consumers bound to contract versions.
- `schema_registry_validation_run`: synchronous and asynchronous validation
  evidence for payloads, schema changes, package registration, and release gates.
- `schema_registry_contract_projection`: generated read models for gateway,
  audit, composition, and domain package discovery.
- `schema_registry_outbox`, `schema_registry_inbox`, and
  `schema_registry_dead_letter`: AppGen-X event contract tables for exactly-once
  handler semantics, retries, and dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

## Standard Table-Stakes Capabilities

The PBC fully implements these ordinary capabilities:

- Subject catalog for API, event, projection, document, and package contracts.
- Versioned schema registration with immutable fingerprints.
- Compatibility policies at global, tenant, subject, channel, and consumer scope.
- Backward, forward, full, transitive, additive-only, semantic, and policy-aware
  compatibility checks.
- JSON, Avro-like, document, event, command, query, and projection schema shapes.
- Required-field, type, enum, range, semantic tag, and PII classification checks.
- Contract validation for incoming payloads and generated PBC packages.
- Producer and consumer binding with impact analysis.
- Breaking-change blocking with remediation plans.
- Contract violation lifecycle, assignment, severity, SLA, and release gate state.
- Idempotent event handlers and contract event outbox.
- Retry and dead-letter evidence for failed validations.
- Schema evolution proposal workflow with approval-ready evidence.
- Generated API contracts for registration, compatibility checks, subjects,
  versions, consumers, violations, and projections.
- Workbench views for registry operations, compatibility triage, validation
  traces, consumer impact, and release readiness.
- RBAC descriptors for read, register, validate, approve, publish, configure,
  and audit actions.
- Configuration schema, rules, parameters, seed subjects, and package metadata.

## Advanced Capabilities

The advanced runtime proves:

- Event-sourced schema lifecycle with immutable hash chaining.
- Graph-relational subject and consumer topology.
- Multi-tenant contract isolation.
- Schema-on-read extension without downtime.
- Probabilistic breaking-change, payload, and consumer-impact risk scoring.
- Real-time contract analytics for change velocity and validation health.
- Counterfactual schema-evolution simulation.
- Temporal compatibility-health forecasting.
- Autonomous remediation recommendations.
- Semantic schema intent parsing from natural-language registration requests.
- Predictive contract risk scoring.
- Self-healing contract route selection for validation failover.
- Zero-knowledge-style schema acceptance proof generation.
- Immutable audit trails and automated control tests.
- Universal API plus asynchronous contract surfaces.
- Cross-system schema federation through read-only projections.
- Gateway, identity, audit, workflow, and composition integration contracts.
- Decentralized producer and consumer identity verification.
- Resilience drills for validation, projection, and package-registration failure.
- Crypto-agile schema signing and fingerprint rotation.
- Carbon-aware validation scheduling for large compatibility sweeps.
- Algebraic schema-diff minimization.
- Mechanism-design consumer impact allocation.
- Information-theoretic validation anomaly detection.
- Temporal stochastic contract-exposure modeling.
- Governed probabilistic models for contract risk and drift.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, mode,
classification, severity, status, and optional consumer/channel filters.
Parameters are runtime-tunable, audited values such as
`compatibility_threshold`, `max_schema_fields`, `semantic_similarity_floor`,
`violation_risk_threshold`, `review_sla_hours`, and `retention_days`.

Configuration includes database backend, event topic, retry limits, allowed
schema formats, default compatibility mode, namespace policy, timezone, and
workbench limits. Runtime configuration rejects unsupported databases and
exposes the AppGen-X event contract as the only ordinary eventing surface.

## Public APIs

- `POST /schemas/subjects`
- `POST /schemas/versions`
- `POST /schemas/compatibility-checks`
- `POST /schemas/payload-validations`
- `POST /schemas/consumer-bindings`
- `POST /schemas/violations`
- `POST /schemas/projections`
- `GET /schemas/subjects`
- `GET /schemas/subjects/{subject_id}/versions`
- `GET /schemas/workbench`

## Events

Emitted events:

- `SchemaSubjectRegistered`
- `SchemaAccepted`
- `BreakingSchemaBlocked`
- `PayloadValidated`
- `ContractViolationRecorded`
- `ContractProjectionPublished`
- `CompatibilityRuleChanged`

Consumed events:

- `PbcDeployed`
- `EventContractProposed`
- `RoutePublished`
- `AccessPolicyChanged`
- `WorkflowDefinitionPublished`
- `PackageRegistrationRequested`

Handlers are idempotent by `schema_registry:{event_type}:{event_id}`, retry at
least three times, and write failures to `schema_registry_dead_letter`.

## UI and Workbench

The UI contract exposes a registry workbench, subject catalog, schema editor,
compatibility studio, consumer impact map, payload validation console, violation
triage board, projection publisher, governance rule studio, parameter console,
configuration panel, and audit evidence view. Actions are permission-bound and
the workbench renders from package-owned state.

## Release Evidence

Release readiness requires a passing runtime smoke, package-local UI contract,
AppGen-X event contract evidence, owned-table checks, no shared-table
dependencies, generated DSL compatibility, package registration metadata,
configuration/rule/parameter execution, and focused unit tests.
