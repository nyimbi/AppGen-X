# Wealth Portfolio Management Implementation Plan

## Goal

Turn `src/pyAppGen/pbcs/wealth_portfolio_management` into a complete package-local wealth portfolio management slice with a real standalone execution path, while preserving the source-package contracts and leaving shared generator code untouched.

## Constraints

- Stay entirely inside `src/pyAppGen/pbcs/wealth_portfolio_management`.
- Preserve the deployment-facing PBC contract on PostgreSQL, MySQL, and MariaDB.
- Keep AppGen-X as the only eventing contract and keep all stream-engine picker controls hidden.
- Use sqlite only as a package-local standalone execution harness for focused tests and smoke evidence.
- Do not modify shared docs, generators, language packs, or the repo progress ledger.

## Workstreams

1. Wealth-specific domain depth
   Replace generic placeholder operations with wealth portfolio operations for household onboarding, IPS, suitability, drift, tax-aware rebalancing, fees, documents, advisor review, and compliance surveillance.

2. Package-local standalone data layer
   Add a sqlite-backed store for portfolio bundles, mandates, suitability, fee schedules, document packages, trade proposals, performance snapshots, advisor reviews, compliance alerts, and AppGen-X inbox/outbox/dead-letter evidence.

3. Executable services and routes
   Expose a one-PBC service and route surface for onboarding, investment policy capture, suitability, fee schedules, document intake, tax-aware rebalance proposals, performance, advisor review, surveillance, and workbench/detail queries.

4. UI/workbench depth
   Materialize a workbench blueprint with explicit forms, wizards, and controls for advisor operations instead of only fragment names.

5. Governed AI assistance
   Enrich the agent contract so chatbot planning, document intake, and CRUD previews route into the standalone surface and keep confirmation gates on all mutation-oriented skills.

6. Release and assurance evidence
   Hand-craft README, implementation status, specification, release evidence, and focused tests so source/package/spec/agent/implementation/capability/generation audits can pass for this PBC in isolation.

## Validation Plan

- `python3 -m py_compile` for modified package modules
- focused `pytest` for `src/pyAppGen/pbcs/wealth_portfolio_management/tests`
- `git diff --check`
- focused repo audit helpers for source, package-local assurance, specification, agent capability, implementation release, implemented capability, and generation smoke
