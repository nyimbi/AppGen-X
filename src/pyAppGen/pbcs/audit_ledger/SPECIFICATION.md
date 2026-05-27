# Audit Ledger PBC

## Purpose

The Audit Ledger PBC is the immutable evidence and assurance package for
AppGen-X compositions. It owns the evidence trail for domain mutations, access
decisions, routing changes, workflow outcomes, package registration actions,
configuration changes, release controls, forensic exports, and disclosure
proofs. The package is intentionally composable: it never reaches into another
PBC's operational tables. It consumes declared AppGen-X events, accepts explicit
API commands, stores only audit-owned records, and publishes read-only
projections for identity, gateway, schema, workflow, composition, and release
governance consumers.

The package-local implementation is executable. Runtime functions configure the
PBC, enforce allowed database backends, reject user-selectable stream-engine
fields, record sealed audit events, maintain a per-tenant signature chain,
capture access evidence, define retention policy, prepare forensic exports,
assert controls, process idempotent inbox events, produce retry and dead-letter
evidence, render workbench state, describe APIs and permissions, and verify
that table references stay inside the owned datastore boundary.

## Owned Datastore Boundary

Audit Ledger owns these tables:

- `audit_ledger_audit_event`: immutable tenant-scoped evidence envelope with
  source PBC, aggregate, actor, action, classification, payload digest,
  sequence, previous hash, event hash, signature, and seal status.
- `audit_ledger_signature_chain`: per-tenant hash-chain link with sequence,
  previous hash, event hash, signature, verification flag, and tamper evidence.
- `audit_ledger_retention_policy`: classification policy, minimum retention,
  legal hold flag, disposal action, export policy, and policy status.
- `audit_ledger_forensic_export`: export request, requested disclosure fields,
  checksum, proof bundle reference, event count, approval metadata, and status.
- `audit_ledger_access_evidence`: principal, resource, action, decision,
  context digest, policy source, and tenant.
- `audit_ledger_control_assertion`: continuous control assertion with severity,
  status, evidence references, release-blocking flag, and remediation reason.
- `audit_ledger_rule`: executable rule records for mutation, access,
  retention, export, control, and release-gate behavior.
- `audit_ledger_parameter`: tunable runtime parameters such as retention days,
  export limits, tamper thresholds, disclosure limits, and review service
  levels.
- `audit_ledger_configuration`: backend, event topic, retry policy, signature
  algorithm, timezone, classification list, export modes, and workbench limit.
- `audit_ledger_projection_link`: handoff record for read-only projections
  pushed to identity, gateway, schema, workflow, composition, and release
  governance consumers.
- `audit_ledger_schema_extension`: validated schema-on-read field registration
  for owned Audit Ledger tables only.
- `audit_ledger_disclosure_proof`: proof hash, disclosed fields, and issuance
  metadata for minimized evidence bundles.
- `audit_ledger_anomaly_signal`: entropy-style anomaly observations for audit
  trails and disclosure surfaces.
- `audit_ledger_identity_credential`: decentralized actor identity verification
  evidence scoped to Audit Ledger review flows.
- `audit_ledger_resilience_drill`: degraded replay and dead-letter readiness
  evidence for chaos and recovery drills.
- `audit_ledger_crypto_key_epoch`: signature-policy epoch history for
  crypto-agile and quantum-resistant audit signing.
- `audit_ledger_carbon_processing_window`: carbon-aware processing windows used
  to schedule low-intensity export and analytics work.
- `audit_ledger_governed_model`: approved audit-risk model metadata, drift
  score, and governance state.

Runtime support tables are also owned:
`audit_ledger_appgen_outbox_event`, `audit_ledger_appgen_inbox_event`, and
`audit_ledger_dead_letter_event`.
Ordinary backing stores are limited to PostgreSQL, MySQL, and MariaDB.
Cross-PBC dependencies are represented only as API calls, consumed events, and
read-only projections. Shared operational tables are not allowed.

## Configuration and Event Contract

The required event topic is `appgen.audit.events`, and the event contract is
AppGen-X. The runtime rejects unsupported eventing fields such as stream-engine
or event-transport selectors because ordinary PBC users should not choose an
eventing implementation. Configuration records include:

- `database_backend`: one of `postgresql`, `mysql`, or `mariadb`.
- `event_topic`: exactly `appgen.audit.events`.
- `retry_limit`: inbox retry limit before dead-letter evidence is written.
- `signature_algorithm`: crypto-agile signature policy identifier.
- `allowed_classifications`: accepted classification values for evidence.
- `export_modes`: supported export surfaces such as proof bundle or archive.
- `default_timezone`: timestamp interpretation boundary.
- `workbench_limit`: bounded workbench result size.

The configuration is exposed to UI/workbench binding evidence with
`stream_engine_picker_visible` set to false and
`user_selectable_event_contract` set to false.

## Standard Capabilities

The package implements the normal audit table stakes expected in enterprise
systems:

- Append-only event capture with tenant-local sequence numbers.
- Immutable hash chaining with a genesis link per tenant.
- Payload digesting and signature metadata for each sealed event.
- Tamper checks that compare audit event hashes with signature-chain links.
- Source PBC, aggregate, actor, action, and classification indexing.
- Access-decision evidence capture with context hashing.
- Retention, disposal, and legal-hold policy management.
- Forensic export preparation with event filtering, disclosure set, checksum,
  and proof-bundle reference.
- Continuous control assertions with release-blocking evidence.
- Event outbox and inbox records under the AppGen-X contract.
- Idempotent handlers keyed by event type and event id.
- Retry evidence and dead-letter records for failed or unsupported consumed
  events.
- Projection stores for identity access, gateway routes, schema contracts,
  workflow completions, composition releases, and deployed PBCs.
- API descriptors for command/query routes with required permissions,
  idempotency keys, emitted events, consumed events, and owned-table usage.
- Permission descriptors for read, seal, verify, export, publish, event,
  configure, and audit actions.
- Rule and parameter engines for runtime policy behavior.
- UI fragments for event search, chain verification, forensic exports,
  retention, access evidence, controls, proof disclosure, anomalies, rules,
  parameters, and configuration.
- Package-local release evidence through smoke checks, focused tests, and
  implementation contract output.

## Advanced Capabilities

Audit Ledger also proves advanced behavior beyond the table-stakes surface:

- Event-sourced audit lifecycle: immutable events are the primary evidence
  stream; queryable workbench views are derived from owned state.
- Graph-relational evidence topology: source PBC, aggregate, actor, control,
  access, export, and projection relationships remain navigable without foreign
  table access.
- Multi-tenant isolation: sequencing, chain verification, workbench views, and
  retention policies are tenant-scoped.
- Schema-on-read evidence envelopes: package-owned tables can receive validated
  extension fields while foreign tables are rejected.
- Probabilistic risk scoring: tamper, control, retention, and export factors
  produce bounded risk estimates.
- Real-time assurance analytics: workbench counters and control results are
  derived from current state without batch export.
- Counterfactual disclosure simulation: proposed retention and disclosure sets
  can be scored before export.
- Evidence-health forecasting: historical health points can be projected over a
  future horizon.
- Autonomous control remediation: known failure reasons map to remediation
  actions such as rebuilding a chain from verified events or opening a release
  blocker.
- Semantic audit query parsing: simple natural-language search text extracts
  audit id, actor, and action filters.
- Self-healing ingestion route selection: available routes are selected by
  latency, and failover use is recorded.
- Disclosure proof generation: minimized disclosure payloads produce
  proof-style hashes without exposing full event content.
- Dynamic policy screening: active rules and classifications determine whether
  an audit event is clear or requires review.
- Automated control testing: configuration, database, rules, outbox, dead
  letter, hash chain, and signature checks are release-audit inputs.
- Cross-system federation: projections expose read-only evidence to declared
  consumers.
- Decentralized actor identity verification: AppGen-X actor identifiers can be
  checked against trusted registry metadata.
- Resilience drills, crypto epoch rotation, carbon-aware processing windows,
  algebraic evidence minimization, export reviewer allocation, anomaly
  detection, stochastic exposure modeling, and governed audit-risk model
  registration.

## APIs

The public API contract is descriptor based:

- `POST /audit-events` records and seals an audit event.
- `POST /audit-events/access-evidence` captures access evidence.
- `POST /audit-events/verify-chain` verifies a tenant signature chain.
- `POST /retention-policies` defines a retention policy.
- `POST /forensic-exports` prepares a forensic export.
- `POST /control-assertions` records a continuous control assertion.
- `POST /audit-projections` publishes a read-only audit projection.
- `POST /audit-events/inbox` handles consumed AppGen-X events idempotently.
- `GET /audit-workbench` returns a tenant-scoped workbench view.

Each route states whether it is a command or query, the owned tables it uses,
emitted or consumed events, the required permission, and the idempotency key.
The API contract declares `shared_table_access` as false.

## Schema Contract

The package-local schema contract is executable and returns:

- owned table descriptors for every Audit Ledger table, including AppGen-X
  outbox, inbox, and dead-letter tables;
- model descriptors for code generation and workbench binding;
- migration descriptors for every owned table with the relational backend
  allowlist;
- owned-table relationships for signature chains, proofs, anomalies, forensic
  exports, and projection handoffs;
- `shared_table_access: false` evidence.

## Service Contract

The package-local service contract declares the transaction boundary as the
Audit Ledger owned datastore plus the AppGen-X outbox. Command methods cover
runtime configuration, rule/parameter registration, inbox handling, event
sealing, access evidence, retention, control assertions, forensic exports,
projection publication, disclosure proofs, resilience/crypto/carbon operations,
and governed model registration. Query methods cover workbench views, schema
and release evidence descriptors, boundary verification, retention disclosure
simulation, audit query parsing, risk scoring, remediation, route selection,
and stochastic exposure modeling.

## Events and Handlers

Emitted events are `AuditEventSealed`, `SignatureChainVerified`,
`RetentionPolicyChanged`, `ForensicExportPrepared`,
`ControlAssertionFailed`, and `AuditProjectionPublished`.

Consumed events are `AccessPolicyChanged`, `WorkflowCompleted`,
`RoutePublished`, `SchemaAccepted`, `PbcDeployed`, and
`CompositionPublished`. Handlers are idempotent by
`{event_type}:{event_id}` unless a caller supplies an explicit idempotency key.
Handled events record processed, retrying, or dead-letter status with attempt
counts. Failed or unsupported events write retry evidence and, after the
configured limit, a dead-letter record.

## UI and Workbench

The workbench is a real package surface, not documentation. It binds to package
state, exposes owned-table and event-table evidence, reports configuration,
rules, parameters, outbox, inbox, and dead-letter counts, and filters audit
events, access evidence, exports, controls, and retention policies by tenant.
UI actions are permission-gated; missing permissions lock the corresponding
command. The configuration panel shows the fixed AppGen-X topic, allowed
database backends, and hidden stream-engine picker.

## Release Evidence

Release readiness requires package-local runtime smoke success, descriptor API
coverage, permission coverage, UI binding coverage, owned-table boundary
verification, AppGen-X event-contract evidence, rules/parameters/configuration
execution, hash-chain and tamper checks, idempotent inbox and dead-letter
tests, schema contract depth, service contract depth, and focused unit tests.
The release evidence contract also proves that UI/workbench binding evidence
uses the AppGen-X contract, the fixed topic, and the full owned-table list. The
implementation is complete only when these checks pass without requiring
central registry changes for the package-local slice.

## Seed And Release Evidence

Release evidence includes package-local seed data for audit event classes,
retention tiers, control assertion types, proof channels, and review queues.
Generated applications validate those seed descriptors together with owned
schema, migration, model, service, route, event, handler, UI, RBAC,
configuration, and release contracts.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `audit_ledger`
- Mesh: `platform`
- Datastore backend: `postgresql`

### Owned Tables

- `audit_event`
- `signature_chain`
- `retention_policy`
- `forensic_export`
- `access_evidence`
- `control_assertion`
- `rule`
- `parameter`
- `configuration`
- `projection_link`
- `schema_extension`
- `disclosure_proof`
- `anomaly_signal`
- `identity_credential`
- `resilience_drill`
- `crypto_key_epoch`
- `carbon_processing_window`
- `governed_model`
- `appgen_outbox_event`
- `appgen_inbox_event`
- `dead_letter_event`

### API Routes

- `POST /audit-events`
- `POST /audit-events/access-evidence`
- `POST /audit-events/verify-chain`
- `POST /retention-policies`
- `POST /forensic-exports`
- `POST /control-assertions`
- `POST /audit-projections`
- `POST /audit-events/inbox`
- `GET /audit-workbench`

### Emitted Events

- `AuditEventSealed`
- `SignatureChainVerified`
- `RetentionPolicyChanged`
- `ForensicExportPrepared`
- `ControlAssertionFailed`
- `AuditProjectionPublished`

### Consumed Events

- `AccessPolicyChanged`
- `WorkflowCompleted`
- `RoutePublished`
- `SchemaAccepted`
- `PbcDeployed`
- `CompositionPublished`

### UI Fragments

- `AuditLedgerWorkbench`
- `AuditEventSearch`
- `SignatureChainVerifier`
- `ForensicExportConsole`
- `AuditRetryEvidenceConsole`
- `AuditReleaseEvidencePanel`
- `RetentionPolicyBoard`
- `AccessEvidenceView`
- `ControlAssertionBoard`
- `ProofDisclosureDesigner`
- `AuditAnomalyDashboard`
- `AuditRuleStudio`
- `AuditParameterConsole`
- `AuditConfigurationPanel`

### Permissions

- `audit_ledger.read`
- `audit_ledger.seal`
- `audit_ledger.verify`
- `audit_ledger.export`
- `audit_ledger.publish`
- `audit_ledger.event`
- `audit_ledger.configure`
- `audit_ledger.audit`

### Configuration Keys

- `AUDIT_LEDGER_DATABASE_URL`
- `AUDIT_LEDGER_EVENT_TOPIC`
- `AUDIT_LEDGER_RETRY_LIMIT`
- `AUDIT_LEDGER_SIGNATURE_ALGORITHM`
- `AUDIT_LEDGER_DEFAULT_TIMEZONE`
- `AUDIT_LEDGER_ALLOWED_CLASSIFICATIONS`

### Standard Features

- `append_only_audit_events`
- `tenant_sequence`
- `hash_chain`
- `signature_metadata`
- `event_sealing`
- `chain_verification`
- `tamper_detection`
- `source_pbc_indexing`
- `actor_action_indexing`
- `access_evidence`
- `retention_policy`
- `legal_hold`
- `forensic_export`
- `proof_bundle`
- `control_assertion`
- `release_blocking_controls`
- `payload_digest`
- `disclosure_minimization`
- `idempotent_handlers`
- `retry_dead_letter`
- `permissions`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `schema_contract`
- `service_contract`
- `release_evidence_contract`
- `projection_handoffs`
- `disclosure_proof_registry`
- `anomaly_signal_registry`
- `identity_credential_registry`
- `crypto_epoch_registry`
- `carbon_window_registry`
- `governed_model_registry`
- `seed_data`
- `workbench`
- `release_gate`
- `appgen_event_contract`

### Advanced Capabilities

- `event_sourced_audit_lifecycle`
- `graph_relational_evidence_topology`
- `multi_tenant_audit_isolation`
- `schema_on_read_evidence_envelope`
- `probabilistic_tamper_control_risk_scoring`
- `real_time_audit_analytics`
- `counterfactual_retention_disclosure_simulation`
- `temporal_evidence_health_forecasting`
- `autonomous_control_remediation`
- `semantic_audit_query_parsing`
- `predictive_audit_risk_scoring`
- `self_healing_audit_ingestion_route_selection`
- `zero_knowledge_event_disclosure_proof`
- `immutable_regulatory_trail`
- `dynamic_audit_policy_screening`
- `automated_audit_control_testing`
- `universal_api_async_audit_surface`
- `cross_system_audit_federation`
- `identity_gateway_schema_workflow_composition_integration`
- `decentralized_actor_identity`
- `chaos_engineered_audit_tolerance`
- `quantum_resistant_audit_signing`
- `carbon_aware_audit_processing`
- `algebraic_evidence_minimization`
- `mechanism_design_export_reviewer_allocation`
- `information_theoretic_audit_anomaly_detection`
- `temporal_evidence_exposure_stochastic_modeling`
- `distributed_systems_engineering`
- `probabilistic_ml_audit_risk`
- `cryptographic_engineering`
- `mathematical_optimization`
- `audit_mlops_governance`

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->
