# Subscription Billing implementation status

Last updated: 2026-05-30

## improve1 executable coverage

- Scope: all 50 features in `improve1.md` for `subscription_billing`.
- Traceability: every feature row in `IMPROVE1_TRACEABILITY.md` maps to code/model artifacts, UI surfaces, service/API artifacts, tests, and release evidence.
- Domain behavior evidence: `tests/test_domain_behavior.py` exercises plan catalog, trial start, subscription activation, addons, usage metering, invoice generation, credit memos, payment application, renewal, plan change orders, entitlement handoff, revenue recognition, billing exceptions, dunning, event idempotency, retry/dead-letter handling, owned-boundary checks, release evidence, AppGen-X-only eventing, backend allowlist enforcement, UI/workbench rendering, forms, wizards, controls, standalone app, repository read model, and AI agent document/CRUD planning.
- Runtime rules and configuration: tests assert runtime configuration, parameter bounds, rule registration, schema extension, AppGen-X event topic enforcement, and rejection of unsupported datastore/event intake.
- Advanced capabilities: tests assert revenue exposure scoring, proration simulation, control tests, UI binding evidence, service/API/schema/release contracts, dunning retry policy, AppGen-X outbox/inbox/dead-letter contracts, and cross-PBC dependencies through events/projections rather than shared tables.

## Current evidence commands

- Passed: `/Volumes/Media/src/pjs/appgen/.venv/bin/pytest src/pyAppGen/pbcs/subscription_billing/tests` - 22 passed.
- Passed: improve1 sweep over 441 package-local improve1 test files - 877 passed.
- Passed: `git diff --check -- src/pyAppGen/pbcs` - no whitespace errors.
