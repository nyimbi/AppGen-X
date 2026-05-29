# Actuarial Pricing and Reserving PBC

`actuarial_pricing_reserving` is a standalone AppGen-X Packaged Business Capability for actuarial pricing, reserving, capital scenario analysis, model validation, actuarial controls, release evidence, and agent-assisted actuarial operations.

## Owned Boundary

The PBC owns these datastore concepts: rating models, actuarial assumptions, experience studies, reserve estimates, loss triangles, capital scenarios, model validations, governed policy rules, runtime parameters, schema extensions, control assertions, governed model registry entries, and AppGen-X inbox/outbox/dead-letter event tables.

It does not own policy administration, claims administration, reinsurance administration, finance close, general ledger, filing submission, or audit source-of-truth tables. Those dependencies are represented through declared AppGen-X events, APIs, and projections.

## Standalone Application Surface

A one-PBC app can use the package-local contracts in `standalone.py`:

- `single_pbc_app_contract()` exposes schema, service, API, runtime, UI, forms, wizards, controls, routes, agent skills, DSL metadata, release simulation, and declared dependencies.
- `actuarial_forms_contract()` surfaces pricing, assumption, experience study, reserve, capital, validation, filing, memo, and release forms.
- `actuarial_wizards_contract()` surfaces rate indication, assumption change, reserve close, capital/reinsurance, validation, and agent document CRUD wizards.
- `actuarial_controls_contract()` surfaces owned-boundary, eventing, model activation, assumption materiality, reserve close, data freshness, agent mutation, and proof-chain gates.
- `full_actuarial_release_simulation()` validates an end-to-end actuarial story from data freshness through premium trace, reserve selection, capital and validation checks, memo evidence, proof chain, finance handoff event, and agent preview.

## Actuarial Capabilities

The package implements table-stakes actuarial functionality: model version governance, rating factors, premium trace reconstruction, assumption registry, impact analysis, experience study validation, data quality gates, credibility blending, loss triangle validation, development factor calculation, chain ladder and expected loss reserve methods, rollforward reconciliation, reserve uncertainty, expenses/profit/dislocation support, regulatory evidence, capital stress, solvency thresholds, catastrophe/reinsurance projections, validation/backtesting/drift monitoring, control assertions, close locking, dependency freshness, large-loss/on-level/trend/fairness support, reproducible run packages, cryptographic proof chains, management signoff, and release simulations.

## Agent and UI

The PBC contributes `actuarial_pricing_reserving_skills` to the composed application agent. Agent plans require citations, record identity where needed, preview evidence, human confirmation, and permission checks before any create/update/delete action. UI contracts expose role-aware forms, wizards, controls, workbench fragments, table browsers, advanced panels, and edge-case queues without exposing stream-engine choices.

## Events

Eventing uses the AppGen-X contract only. The package emits actuarial created, updated, approved, and exception events. It consumes declared policy, audit, and operational KPI events plus projection dependencies for claims, reinsurance, finance handoff, filings, and actuarial release evidence.

## Verification

Run focused verification from the repository root or this worktree:

```bash
PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/actuarial_pricing_reserving
PYTHONPATH=src python3 -m pytest -q src/pyAppGen/pbcs/actuarial_pricing_reserving/tests
PYTHONPATH=src python3 -c "from pyAppGen.pbc import pbc_generation_smoke_audit, pbc_implementation_release_audit; print(pbc_implementation_release_audit(('actuarial_pricing_reserving',))['ok']); print(pbc_generation_smoke_audit(('actuarial_pricing_reserving',))['ok'])"
```
