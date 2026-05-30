# Waste and Recycling Operations Implementation Plan

## Source Reviewed

- `improve1.md` waste and recycling backlog.
- Existing manifest, runtime, services, routes, UI, agent, release evidence, and tests.

## Implementation Intent

Make `waste_recycling_operations` usable as a one-PBC application for municipal and commercial waste operations. The package must execute route release, bin lifecycle, material stream rules, pickup proof, missed pickup recovery, contamination education/escalation, hazardous material exception handling, disposal ticket reconciliation, recycling yield and diversion reporting, and governed AI task previews while keeping external fleet, workforce, customer, billing, and facility systems as projections/events rather than shared tables.

## Delivery Steps

1. Preserve AppGen-X-only eventing and PostgreSQL/MySQL/MariaDB backend policy.
2. Add PBC-local forms, wizards, controls, and standalone app methods.
3. Wire standalone smoke into package and release evidence.
4. Add tests proving successful and blocked operational paths.
5. Re-run compile, tests, diff check, and focused source/package/spec/agent/implementation/capability/generation audits.
