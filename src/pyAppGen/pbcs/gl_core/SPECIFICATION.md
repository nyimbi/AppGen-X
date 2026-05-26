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

- `gl_core_journal_event`: append-only posting event, tenant, valid time,
  processing time, payload digest, signature, hash chain, and event type.
- `gl_core_journal_line`: debit and credit lines, account, dimensions, amount,
  currency, source document digest, and confidence metadata.
- `gl_core_account_projection`: derived account balances by tenant, entity,
  reporting dimension, period, and currency.
- `gl_core_close_snapshot`: continuous close snapshot, controls, proof hash,
  approval state, and reporting view.
- `gl_core_reconciliation_case`: bank, subledger, intercompany, and clearing
  reconciliation suggestions, decisions, and exception state.
- `gl_core_policy_rule`: posting, approval, close, revaluation, materiality, and
  reconciliation rules.
- `gl_core_outbox`, `gl_core_inbox`, and `gl_core_dead_letter`: AppGen-X event
  contract tables for exactly-once handler semantics, retries, and dead-letter
  triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

## Standard Table-Stakes Capabilities

The PBC fully implements chart of accounts, journal entry capture, journal-line
balancing, posting periods, trial balance, ledger projection, account
reconciliation, financial statement projection, period close, audit trail,
approval policy, reporting dimensions, multi-entity isolation, currency and
revaluation support, intercompany support, subledger integration, budget
control, source document evidence, configuration schema, executable rules,
runtime parameters, seed data, permissions, and workbench views.

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

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, status, and
scope-specific predicates such as balance requirements, approval thresholds, and
close constraints. Parameters include `approval_threshold`,
`materiality_threshold`, `close_tolerance`, `revaluation_threshold`,
`retention_days`, and `workbench_limit`.

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

## Release Evidence

Release readiness requires a passing runtime smoke, package-local UI contract,
owned-table evidence, AppGen-X event contract evidence, balanced journal tests,
configuration/rule/parameter execution, generated DSL compatibility, package
metadata, workbench rendering, and focused unit tests.
