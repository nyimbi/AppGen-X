# General Ledger Core PBC

## Purpose

The General Ledger Core PBC owns financial-accounting truth for an AppGen-X
composition. It records balanced journal activity as immutable ledger events,
derives projections from the event stream, supports continuous close, validates
posting policy, exposes audit proofs, and publishes AppGen-X event contracts for
subledger synchronization. Other PBCs integrate through APIs, events, and
read-only projections; they do not share GL tables.

## Owned Datastore Boundary

The PBC owns:

- `gl_core_ledger_event_log`: canonical immutable event log with tenant,
  event identity, valid time, processing time, payload hash, previous hash, and
  signature.
- `gl_core_journal_event`: append-only posting event, tenant, valid time,
  processing time, payload digest, signature, hash chain, and event type.
- `gl_core_journal_entry`: journal header, period, status, source document
  digest, approval state, reversal/accrual linkage, and posting intent.
- `gl_core_journal_line`: debit and credit lines, account, dimensions, amount,
  currency, source document digest, and confidence metadata.
- `gl_core_ledger_account`: chart of accounts, account hierarchy, normal
  balance, account type, consolidation mapping, and statutory reporting tags.
- `gl_core_accounting_period`: fiscal calendar, period state, close controls,
  approval timestamps, and reopen policy.
- `gl_core_ledger_projection`: projection lineage, dimension hash, balance
  hash, source event count, and rebuild proof.
- `gl_core_account_projection`: derived account balances by tenant, entity,
  reporting dimension, period, and currency.
- `gl_core_consensus_replica`: geo-partitioned replication node, term,
  commit index, quorum state, and health signal.
- `gl_core_schema_extension`: schema-on-read extension registry with field
  compatibility, version, and owned-table enforcement.
- `gl_core_tenant_ledger_partition`: tenant residency, key reference,
  retention policy, and compliance boundary.
- `gl_core_probabilistic_posting`: uncertain posting primitives with
  confidence, uncertainty exposure, and statement propagation evidence.
- `gl_core_close_snapshot`: continuous close snapshot, controls, proof hash,
  approval state, and reporting view.
- `gl_core_causal_scenario`: counterfactual driver, impact hash, and replayable
  causal scenario evidence.
- `gl_core_reconciliation_case`: bank, subledger, intercompany, and clearing
  reconciliation suggestions, decisions, and exception state.
- `gl_core_semantic_source_document`: source document digest, semantic account
  derivation, confidence, and human-auditable explanation trail.
- `gl_core_regulatory_rule_version`: compiled accounting-standard rule version,
  effective date, predicate, and impact-analysis hash.
- `gl_core_policy_rule`: posting, approval, close, revaluation, materiality, and
  reconciliation rules.
- `gl_core_predictive_validation_run`: pre-posting simulation decision, risk
  score, model version, and validation trace.
- `gl_core_audit_proof`: disclosure-minimized proof channel, public claims
  hash, proof hash, and regulator/viewer channel.
- `gl_core_policy_decision`: dynamic policy decision, actor context, action,
  decision, and reason codes.
- `gl_core_control_assertion`: continuous control assertion, status,
  evidence hash, and control testing timestamp.
- `gl_core_ledger_federation_link`: external ledger projection name, API
  contract, event contract, and federation trust boundary.
- `gl_core_identity_credential`: decentralized identifier, issuer, subject,
  credential hash, and counterparty verification evidence.
- `gl_core_resilience_drill`: failure scenario, decision, remaining quorum, and
  recovery evidence.
- `gl_core_crypto_key_epoch`: crypto-agile key epoch, signing algorithm,
  attestation, and rotation timestamp.
- `gl_core_carbon_execution_window`: region, carbon intensity, selected
  execution window, and scheduling proof.
- `gl_core_financial_model`: regulated model metadata, feature lineage, drift
  score, and materiality gate.
- `gl_core_outbox`, `gl_core_inbox`, and `gl_core_dead_letter`: AppGen-X event
  contract tables for exactly-once handler semantics, retries, and dead-letter
  triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

The executable `gl_core_build_schema_contract()` returns one model and one
migration descriptor per owned table, plus owned-only relationships for journal
headers, lines, accounts, periods, projections, close snapshots, and
reconciliation cases. Cross-PBC references are represented only as declared
APIs, consumed AppGen-X events, or package-local projections.

## Standard Table-Stakes Capabilities

The PBC fully implements chart of accounts, journal entry capture, journal-line
balancing, posting periods, trial balance, ledger projection, account
reconciliation, financial statement projection, period close, audit trail,
approval policy, reporting dimensions, multi-entity isolation, currency and
revaluation support, intercompany support, subledger integration, budget
control, source document evidence, configuration schema, executable rules,
runtime parameters, seed data, permissions, and workbench views.

The standard accounting surface also includes chart versioning, recurring
journals, reversal entries, accruals and deferrals, allocation processing,
currency translation, retained-earnings rollforward, consolidation support,
financial-statement mapping, segment reporting, statutory reporting, electronic
audit-file evidence, tenant-level residency, and source-document attachment
lineage. `gl_core_build_service_contract()` proves command methods for these
surfaces and binds every mutation to the GL-owned datastore plus AppGen-X
outbox transaction boundary.

## Advanced Capabilities

The runtime proves event-sourced ledger lifecycle, deterministic consensus
simulation, schema-on-read extensibility, tenant isolation, real-time
transactional and analytical projections, probabilistic postings, continuous
close, causal scenarios, autonomous reconciliation, semantic account derivation,
compiled regulatory rules, predictive posting validation, disclosure-minimized
audit proofs, dynamic policy enforcement, immutable trail verification,
automated controls, universal API and event contracts, ledger federation,
event-driven subledger synchronization, decentralized identity verification,
resilience drills, crypto-agile signing, carbon-aware execution, temporal
accounting queries, privacy-preserving consolidation evidence, reconciliation
game resolution, information-theoretic auditability, formal invariants,
distributed runtime evidence, cryptographic engineering, and regulated
financial-model governance.

Advanced capability implementation is executable, not merely catalog metadata:

- event sourcing appends immutable journal events, signs them, links them by
  hash, and rebuilds account projections from the event log;
- quorum replication simulates consensus commit, failure recovery, and
  remaining-quorum evidence;
- schema-on-read extensions are accepted only for GL-owned tables with safe
  field names and compatibility metadata;
- tenant partitions expose independent key references, residency, and retention
  boundaries;
- probabilistic postings propagate confidence and uncertainty exposure into
  statement evidence;
- continuous close snapshots combine projections, controls, approval state, and
  proof hashes without waiting for batch period-end processing;
- causal scenarios replay counterfactual account balances from the current
  projection;
- semantic source-document handling derives account candidates with confidence
  and audit trail;
- regulatory rules compile into versioned predicates and can be impact-audited;
- predictive posting validation simulates approval, policy, and balance risks
  before a journal is posted;
- disclosure-minimized audit proofs expose public claims without disclosing
  journal-line payloads;
- dynamic policy decisions evaluate actor, tenant, action, amount, and reason
  codes at command time;
- control assertions continuously test balance, hash-chain, sequence, and
  append-only invariants;
- federation links expose read-only virtual ledger views through declared APIs
  and projections rather than table sharing;
- identity credentials verify counterparty claims through DID/credential hashes;
- resilience drills replay node failure and partition scenarios;
- crypto epochs support algorithm agility and rotation attestation;
- carbon-aware scheduling selects lower-intensity execution windows for
  non-urgent ledger workloads;
- private consolidation emits commitments and proofs without exposing clear
  balances;
- reconciliation games compute confidence-weighted settlement candidates;
- information-auditability metrics measure event-pattern entropy and anomaly
  signals;
- regulated model governance records feature lineage, drift score, and
  materiality gates for financial automation.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, status, and
scope-specific predicates such as balance requirements, approval thresholds, and
close constraints. Parameters include `approval_threshold`,
`materiality_threshold`, `close_tolerance`, `revaluation_threshold`,
`retention_days`, and `workbench_limit`.

Configuration and parameter behavior is part of the runtime contract:

- unsupported database backends are rejected;
- the event topic must be `appgen.gl.events`;
- event-engine picker fields are rejected before configuration is accepted;
- every accepted configuration records the PostgreSQL/MySQL/MariaDB allowlist,
  fixed AppGen-X event contract, owned tables, and non-selectable event surface;
- schema extensions must target owned GL tables and must use safe field names;
- invalid parameters and incomplete rules fail fast with explicit errors.

Configuration includes database backend, event topic, retry limit, default
currency, default timezone, allowed account types, and workbench limits. Runtime
configuration rejects unsupported databases and exposes the AppGen-X event
contract as the ordinary eventing surface.

## Public APIs

- `POST /gl/journal-events`
- `POST /gl/journals/validate`
- `GET /gl/projections`
- `GET /gl/trial-balance`
- `POST /gl/close-snapshots`
- `POST /gl/reconciliations`
- `POST /gl/policy-rules`
- `GET /gl/audit-proof`
- `GET /gl/workbench`

The executable API contract also exposes command/query ownership evidence for
journal posting, validation, projections, trial balance, close snapshots,
reconciliation, policy rules, event inbox handling, audit proofs, and the GL
workbench. Every route declares its owned-table set, permission, idempotency
key, and emitted or consumed event type. The API contract explicitly sets
`shared_table_access` to false and hides any stream-engine picker.

## Events

Emitted events:

- `JournalPosted`
- `CloseSnapshotCreated`
- `ReconciliationSuggested`
- `PostingPolicyChanged`
- `LedgerProjectionBuilt`

Consumed events:

- `InvoiceApproved`
- `PaymentCaptured`
- `PayrollPosted`
- `AssetDepreciated`
- `TaxCalculated`

Handlers are idempotent by `gl_core:{event_type}:{event_id}`, retry at least
three times, and write failures to `gl_core_dead_letter`.

## UI and Workbench

The UI exposes a GL workbench, journal entry console, trial-balance view,
account projection explorer, close command center, reconciliation queue, policy
rule studio, parameter console, configuration panel, audit-proof viewer, and
controls dashboard. Actions are permission-bound and rendered from package-owned
state.

Workbench binding evidence includes owned tables, AppGen-X outbox/inbox/dead
letter tables, event topic, configuration state, retry/dead-letter counts, rule
counts, parameter counts, control status, close-readiness status, and visible or
locked actions per principal permission set.

## Release Evidence

Release readiness requires:

- `gl_core_runtime_smoke()` returning `ok: True` with every advanced capability
  check passing;
- `gl_core_build_schema_contract()` returning at least 30 owned tables, one
  migration descriptor per table, owned relationships, model descriptors, and
  no shared-table access;
- `gl_core_build_service_contract()` returning at least 20 command methods,
  owned-datastore transaction boundaries, declared API/event/projection
  dependencies, and no shared tables;
- `gl_core_build_release_evidence()` returning `ok: True` for schema depth,
  migration coverage, service command depth, API/event contract evidence,
  permission coverage, backend allowlist, and shared-table rejection;
- package `implementation_contract()` exposing the same owned tables,
  schema/service/release contracts, UI, API, permissions, backend allowlist,
  emitted/consumed event types, and fixed event topic;
- focused tests proving balanced and rejected journals, configuration,
  parameters, rules, schema extension validation, idempotent inbox handling,
  retry/dead-letter behavior, projection building, workbench rendering,
  permission-bound actions, and owned-table boundary rejection;
- `pbc_implementation_release_audit(("gl_core",))`,
  `pbc_implemented_capability_audit(("gl_core",))`, full generation/capability
  audits, and `pbc_release_audit()` returning `ok: True`;
- restricted-name scans over the changed GL package/test/spec files returning
  clean and no stream-engine or non-AppGen-X event picker exposed to ordinary
  users.
