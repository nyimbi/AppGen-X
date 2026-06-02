# Telecom Subscription Lifecycle Implementation Plan

## Source Reviewed

- `improve1.md` telecom subscription lifecycle backlog.
- Existing manifest, runtime, services, routes, UI, agent, release evidence, and tests.

## Implementation Intent

Make `telecom_subscription_lifecycle` usable as a one-PBC application for subscription operations: subscriber aggregate, plan versioning, SIM/eSIM lifecycle, activation, provisioning readiness, portability, usage thresholds, roaming spend controls, churn/retention, suspension/barring controls, and governed AI previews while keeping billing, customer master, network adapters, fulfillment, and partner systems as external events/projections.

## Delivery Steps

1. Preserve AppGen-X-only eventing and PostgreSQL/MySQL/MariaDB backend policy.
2. Add PBC-local forms, wizards, controls, standalone app methods, and tests.
3. Wire standalone smoke into package and release evidence.
4. Re-run compile, tests, diff check, and focused source/package/spec/agent/implementation/capability/generation audits.
