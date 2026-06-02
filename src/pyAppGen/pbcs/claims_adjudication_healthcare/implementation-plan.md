# Healthcare Claims Adjudication Implementation Plan

## Objective

Make `claims_adjudication_healthcare` usable as a standalone one-PBC payer adjudication app covering claim intake, line adjudication, eligibility/provider projection boundaries, benefit rules, medical necessity, prior authorization, coding validation, COB, cost share, pricing, denials, appeals, payment integrity, attachment evidence, corrections, recoveries, controls, UI, and governed assistant planning.

## Plan

1. Preserve the existing executable runtime and add a package-local standalone app surface rather than replacing working adjudication code.
2. Map all 50 `improve1.md` backlog items to concrete forms, wizards, controls, route contracts, DSL exposure, declared dependencies, and release simulation evidence.
3. Keep member enrollment, provider master, prior authorization, accumulator, fee schedule, and audit inputs as declared AppGen-X projections; reject shared table references.
4. Add executable helpers for canonicalization, mixed line outcomes, duplicate scoring, overlap guardrails, scenario library, and full claims adjudication simulation.
5. Wire standalone evidence through package exports, UI, routes, agent contribution, and release evidence.
6. Add focused tests and run compile, tests, diff checks, and available PBC audits.
