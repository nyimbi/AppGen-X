# Unified Audit Trail and Cryptographic Ledger PBC

## Purpose

The Unified Audit Trail and Cryptographic Ledger PBC owns immutable evidence for
AppGen-X compositions. It records domain mutations, access decisions, route
changes, workflow outcomes, package registration actions, security-relevant
configuration changes, and release evidence as append-only sealed audit events.

The PBC does not own another PBC's operational state. It consumes declared
events, receives explicit API calls, and publishes read-only audit projections,
forensic exports, and verification proofs.

## Owned Datastore Boundary

The PBC owns:

- `audit_ledger_audit_event`: immutable event envelope, tenant, actor, action,
  source PBC, aggregate ID, payload digest, classification, and sequence.
- `audit_ledger_signature_chain`: per-tenant hash-chain link, signature
  algorithm, previous hash, event hash, chain root, and verification state.
- `audit_ledger_retention_policy`: tenant, classification, retention period,
  legal hold, export policy, and disposal eligibility.
- `audit_ledger_forensic_export`: export request, filter, proof bundle,
  disclosure policy, approval state, checksum, and delivery status.
- `audit_ledger_access_evidence`: policy decision, principal, resource, action,
  context digest, and result.
- `audit_ledger_control_assertion`: continuous control assertion, status,
  severity, tested evidence, and release impact.
- `audit_ledger_outbox`, `audit_ledger_inbox`, and `audit_ledger_dead_letter`:
  AppGen-X event contract tables for exactly-once handlers, retries, and
  dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

## Standard Table-Stakes Capabilities

The PBC fully implements:

- Append-only audit event capture.
- Tenant-scoped immutable sequencing.
- Cryptographic hash chaining and signature metadata.
- Source PBC, aggregate, actor, action, and classification indexing.
- Access-decision evidence capture.
- Retention and legal-hold policies.
- Forensic export request, approval, proof, checksum, and delivery metadata.
- Continuous control assertions and release-blocking evidence.
- Payload digesting with disclosure-minimized proof bundles.
- Event ingestion from identity, gateway, schema, workflow, composition, and
  domain PBCs.
- Idempotent handlers, retry policy, and dead-letter evidence.
- Tamper detection, chain verification, and gap detection.
- Workbench views for event search, chain status, forensic exports, retention,
  access evidence, controls, rules, parameters, configuration, and proofs.
- RBAC descriptors for read, seal, verify, export, hold, configure, and audit.
- Configuration schema, executable rules, runtime parameters, seed controls,
  generated APIs, package metadata, generated DSL evidence, and release gates.

## Advanced Capabilities

The runtime proves:

- Event-sourced audit lifecycle with immutable hash chaining.
- Graph-relational evidence topology across PBC sources and actors.
- Multi-tenant audit isolation.
- Schema-on-read evidence envelope extension.
- Probabilistic tamper, retention, and control-risk scoring.
- Real-time audit analytics.
- Counterfactual retention and disclosure simulation.
- Temporal evidence-health forecasting.
- Autonomous control remediation recommendations.
- Semantic audit query parsing.
- Predictive audit risk scoring.
- Self-healing audit ingestion route selection.
- Zero-knowledge-style event disclosure proofs.
- Immutable regulatory trail and automated control testing.
- Universal API and asynchronous audit contract surfaces.
- Cross-system audit federation through read-only projections.
- Identity, gateway, schema, workflow, and composition integration contracts.
- Decentralized actor identity verification.
- Resilience drills for ingestion, chain verification, and export failures.
- Crypto-agile signing and epoch rotation.
- Carbon-aware export and verification scheduling.
- Algebraic evidence minimization.
- Mechanism-design export reviewer allocation.
- Information-theoretic audit anomaly detection.
- Temporal stochastic evidence exposure modeling.
- Governed probabilistic models for audit risk and drift.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, classification,
minimum retention, legal-hold requirement, export approval requirement,
severity, and status. Parameters include `retention_days`, `export_batch_limit`,
`tamper_risk_threshold`, `control_failure_threshold`, `proof_disclosure_limit`,
and `review_sla_hours`.

Configuration includes database backend, event topic, retry limit, signature
algorithm, default timezone, allowed classifications, export delivery modes, and
workbench limits. Runtime configuration rejects unsupported databases and uses
the AppGen-X event contract as the ordinary eventing surface.

## Public APIs

- `POST /audit-events`
- `POST /audit-events/{id}/seal`
- `POST /audit-events/verify-chain`
- `POST /retention-policies`
- `POST /forensic-exports`
- `POST /control-assertions`
- `POST /access-evidence`
- `GET /audit-events`
- `GET /signature-chain`
- `GET /audit-workbench`

## Events

Emitted events:

- `AuditEventSealed`
- `SignatureChainVerified`
- `RetentionPolicyChanged`
- `ForensicExportPrepared`
- `ControlAssertionFailed`
- `AuditProjectionPublished`

Consumed events:

- `AccessPolicyChanged`
- `WorkflowCompleted`
- `RoutePublished`
- `SchemaAccepted`
- `PbcDeployed`
- `CompositionPublished`

Handlers are idempotent by `audit_ledger:{event_type}:{event_id}`, retry at
least three times, and write failures to `audit_ledger_dead_letter`.

## UI and Workbench

The UI exposes an audit workbench, event search, signature-chain verifier,
forensic export console, retention policy board, access evidence view, control
assertion board, proof disclosure designer, audit rule studio, parameter
console, configuration panel, and anomaly dashboard. Actions are permission
bound and rendered from package-owned state.

## Release Evidence

Release readiness requires passing runtime smoke, package-local UI contract,
owned tables, API/event/handler surfaces, AppGen-X event contract evidence,
rule/configuration/parameter execution, generated DSL smoke compatibility,
package metadata, tamper-proof workbench rendering, and focused unit tests.
