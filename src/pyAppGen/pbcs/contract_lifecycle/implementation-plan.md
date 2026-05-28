# Contract Lifecycle PBC Implementation Plan

## Scope

Implement the `contract_lifecycle` package as a self-contained AppGen-X PBC slice that can execute a realistic contract lifecycle flow using package-local code only. All changes remain under `src/pyAppGen/pbcs/contract_lifecycle`.

## Goals

1. Replace static placeholder descriptors with one package-local source of truth for:
   - owned schema/model metadata
   - contract lifecycle operations
   - AppGen-X emitted/consumed event contracts
   - forms, wizards, controls, and workbench UI
   - RBAC roles, permissions, rules, parameters, and configuration
   - agent/chatbot document-instruction and governed CRUD planning
2. Make the package executable in tests and smoke checks as a one-PBC CLM application.
3. Produce focused release evidence and package-local documentation of what is implemented and what remains intentionally out of scope.

## Design

### 1. Single package-local domain source of truth

Create a package-local domain module that defines:

- owned tables and field definitions
- lifecycle states and allowed transitions
- domain operations and their target tables/events
- rule and parameter catalogs
- forms, wizard steps, controls, workbench sections
- RBAC roles and permission-to-role mappings
- deterministic sample data and release-ready smoke scenarios

This module will also expose an in-memory application state plus executable commands for:

- intake, classification, authoring workspace, clause selection
- negotiation/redlines, approval routing, signature capture
- obligation activation/performance, milestones, renewals
- amendments, compliance checks, risk scoring, search indexing
- exception resolution, policy compilation, counterparty simulation

### 2. Thin exported modules over the shared domain

Refit the existing package files so they read from the shared domain model instead of duplicating stale tuples:

- `models.py` and `schema_contract.py`
- `services.py` and `service_contract.py`
- `routes.py`
- `events.py` and `handlers.py`
- `ui.py`
- `config.py` and `permissions.py`
- `agent.py`
- `release_evidence.py`
- `runtime.py`
- `seed_data.py`

### 3. Focused contract-lifecycle behavior

Bias the executable flow toward realistic CLM concerns:

- intake readiness and classification gates
- party authority and clause governance evidence
- approval route compilation driven by risk/value
- signature gating on approvals and signer authority
- obligation activation from approved/signed contracts
- renewal and amendment tracking
- AppGen-X boundary proof and idempotent external event handling

### 4. Verification

Add focused tests for:

- end-to-end happy path through major lifecycle steps
- invalid lifecycle transitions and approval/signature guards
- governed CRUD/document instruction planning
- route, UI, rules, parameters, and release evidence coverage
- event idempotency and dead-letter behavior

Run package-local tests and lightweight smoke/compile checks.

## Deliverables

- executable package-local implementation
- `README.md`
- `implementation-status.md`
- refreshed release evidence
- focused tests and validation evidence
