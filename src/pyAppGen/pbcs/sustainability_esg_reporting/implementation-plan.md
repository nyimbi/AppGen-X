# Sustainability ESG Reporting Implementation Plan

## Source Reviewed

- `improve1.md` sustainability and ESG backlog.
- Existing specification, blueprint, manifest, runtime, models, services, routes, UI, agent, slice app, release evidence, and tests.

## Implementation Intent

Make `sustainability_esg_reporting` executable as a one-PBC ESG reporting application. The package must support double materiality, facility/activity data, Scope 1/2/3 calculations, emissions factors, renewable instruments, water and waste metrics, social/governance metrics, supplier ESG inputs, assurance controls/evidence/exceptions, restatements, targets/progress, climate scenarios, disclosure packets, board packs, regulator filings, and governed AI previews.

## Delivery Steps

1. Preserve AppGen-X-only eventing and PostgreSQL/MySQL/MariaDB backend policy.
2. Keep all mutations inside `sustainability_esg_reporting_*` owned tables and package-local event tables.
3. Expose executable runtime, schema, service, route, UI, agent, and slice-app surfaces for standalone ESG reporting.
4. Prove domain flows through compile, tests, diff hygiene, and focused release audits.
5. Record code review and verification evidence in `implementation-status.md`.

## Acceptance Gates

- PBC-local tests pass.
- Source/package/spec/agent/implementation/capability/generation audits pass.
- README, plan, and status artifacts explain how a one-PBC ESG app runs and is verified.
