# Actuarial Pricing and Reserving Implementation Plan

## Objective

Make `actuarial_pricing_reserving` usable as a standalone one-PBC application for actuarial pricing, reserving, capital scenarios, validation, controls, release evidence, and agent-assisted actuarial work without owning policy, claims, reinsurance, finance, filing, or ledger source-of-truth tables.

## Implementation Shape

1. Preserve the existing package boundary under `src/pyAppGen/pbcs/actuarial_pricing_reserving`.
2. Add a package-local `standalone.py` contract that joins the existing actuarial engine, runtime, schema, services, routes, events, handlers, UI, permissions, and release evidence.
3. Surface the full improve1 backlog through explicit forms, wizards, controls, route contracts, DSL exposure, seed data, and a full release simulation.
4. Keep all external policy, claims, reinsurance, finance, filing, audit, and KPI inputs as declared AppGen-X event/API projections.
5. Require human confirmation, citations, record identity, and permission checks for agent-driven CRUD previews.
6. Prove runtime safety with focused tests and PBC release/generation audits.

## Capability Coverage

The standalone surface covers rating model governance, factor libraries, premium traces, assumption registries, impact analysis, experience studies, data quality, credibility, triangles, development factors, reserve methods, rollforwards, uncertainty, discounting/inflation, expenses/profit, adequacy diagnostics, dislocation, filing support, capital scenarios, solvency metrics, catastrophe accumulation, reinsurance projection, model validation, backtesting, assumption calendars, controls, pricing and reserve workbenches, finance handoff events, dependency freshness, large loss handling, on-leveling, trends, fairness, scenarios, memo assembly, agent analysis, governed agent CRUD, model registry, drift, currency/jurisdiction controls, reproducible run packages, cryptographic proof chains, management signoff, full release simulation, overlap guardrails, and composition DSL/agent exposure.

## Verification Plan

- Compile the package.
- Run package-local tests, including the new standalone app tests.
- Run focused PBC source, package-local, specification, agent capability, implementation, implemented capability, and generation smoke audits for `actuarial_pricing_reserving`.
- Review diff scope and whitespace.
